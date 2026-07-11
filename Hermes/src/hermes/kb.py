"""Hermes 知识库核心引擎。

能力：
- 从 Markdown 文件加载知识条目（解析 frontmatter + 正文）
- BM25 全文检索（纯 Python 标准库）
- lint 健康检查
- stats 统计
- search 关键词检索
"""
from __future__ import annotations

import re
import math
import os
from pathlib import Path
from dataclasses import dataclass, field
from collections import Counter, defaultdict
from typing import Optional


# ============================================================
# 数据结构
# ============================================================

@dataclass
class Entry:
    """单个知识条目。"""
    id: str
    title: str
    category: str
    tags: list = field(default_factory=list)
    status: str = "active"
    created: str = ""
    updated: str = ""
    related: list = field(default_factory=list)
    related_typed: dict = field(default_factory=dict)  # 类型化关系 {target_id: rel_type}
    ratings: dict = field(default_factory=dict)
    awards: list = field(default_factory=list)
    data_confidence: str = "simulated"  # simulated/verified/official
    data_source: str = ""  # 数据来源
    source_url: str = ""  # 原始链接
    crawl_date: str = ""  # 抓取时间
    version: int = 1  # 数据版本
    _fm_subcategory: str = ""  # frontmatter 中的规范化子类（优先于 id 推断）
    content: str = ""  # 正文 Markdown
    raw: str = ""  # 原始文件内容
    file_path: Optional[Path] = None

    @property
    def text(self) -> str:
        """用于检索的文本（标题+标签+正文）。"""
        return f"{self.title} {' '.join(self.tags)} {self.content}"

    @property
    def structured_attrs(self) -> dict:
        """从正文提取结构化属性（用于筛选过滤）。

        提取：
        - abv: 酒精度（字符串保留原值，便于显示）
        - abv_num: 酒精度数值（用于范围筛选）
        - price_rmb: 价格区间 [low, high]
        - region: 产地（country/region）
        - subcategory: 子类（从 id 推断）
        - flavor_tags: 风味标签列表
        - flavor_profile: 风味轮廓 dict
        """
        if hasattr(self, "_cached_attrs"):
            return self._cached_attrs
        attrs = {
            "subcategory": self._fm_subcategory or (self.id.split("-")[1] if "-" in self.id else ""),
            "flavor_tags": [],
            "flavor_profile": {},
            "abv_num": None,
            "price_rmb": None,
            "region": "",
            "data_confidence": self.data_confidence,
            "data_source": self.data_source,
        }
        # 从正文提取基础信息
        # 酒精度
        m = re.search(r'\*\*酒精度\*\*：(.+)', self.content)
        if m:
            abv_str = m.group(1).strip()
            # 提取数值
            nums = re.findall(r'(\d+(?:\.\d+)?)', abv_str)
            if nums:
                try:
                    attrs["abv_num"] = float(nums[0])
                except ValueError:
                    pass
        # 价格
        m = re.search(r'\*\*参考价格（RMB）\*\*：¥(\d+)-(\d+)', self.content)
        if m:
            attrs["price_rmb"] = [int(m.group(1)), int(m.group(2))]
        # 产地
        m = re.search(r'\*\*产地\*\*：(.+)', self.content)
        if m:
            attrs["region"] = m.group(1).strip()
        # 风味标签
        m = re.search(r'\*\*风味标签\*\*：(.+)', self.content)
        if m:
            attrs["flavor_tags"] = [t.strip() for t in m.group(1).split(",") if t.strip()]
        # 风味轮廓（从表格提取）
        profile_match = re.search(
            r'## 风味轮廓.*?\| (\d) \|.*?(\d) \|.*?(\d) \|.*?(\d) \|.*?(\d) \|',
            self.content, re.DOTALL,
        )
        if profile_match:
            attrs["flavor_profile"] = {
                "sweet": int(profile_match.group(1)),
                "sour": int(profile_match.group(2)),
                "bitter": int(profile_match.group(3)),
                "strong": int(profile_match.group(4)),
                "aroma": int(profile_match.group(5)),
            }
        self._cached_attrs = attrs
        return attrs


@dataclass
class LintReport:
    """lint 检查报告。"""
    total_files: int = 0
    orphan_files: list = field(default_factory=list)  # 孤立文件
    missing_frontmatter: list = field(default_factory=list)  # 缺 frontmatter
    invalid_status: list = field(default_factory=list)  # 非法 status
    naming_violations: list = field(default_factory=list)  # 命名违规

    @property
    def total_issues(self) -> int:
        return (len(self.orphan_files) + len(self.missing_frontmatter) +
                len(self.invalid_status) + len(self.naming_violations))


# ============================================================
# frontmatter 解析
# ============================================================

FM_PATTERN = re.compile(r'^---\s*\n(.*?)\n---\s*\n(.*)$', re.DOTALL)
VALID_STATUS = {"draft", "active", "deprecated", "archived"}
VALID_CATEGORY = {"ENT", "PRJ", "SOP", "DEC", "ANTI"}


def parse_frontmatter(raw: str) -> tuple[dict, str]:
    """解析 YAML frontmatter（简化版，支持嵌套 ratings/awards）。"""
    m = FM_PATTERN.match(raw)
    if not m:
        return {}, raw
    fm_text = m.group(1)
    body = m.group(2)
    meta = {}
    lines = fm_text.split("\n")
    i = 0
    while i < len(lines):
        line = lines[i].rstrip()
        if not line or line.startswith("#"):
            i += 1
            continue
        # 顶层 key: value
        if not line.startswith(" ") and ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if not val:
                # 可能是嵌套块（ratings: / awards:）
                i += 1
                if key == "ratings":
                    ratings = {}
                    while i < len(lines) and lines[i].startswith("  ") and ":" in lines[i]:
                        sub_line = lines[i].strip()
                        sub_key, _, sub_val = sub_line.partition(":")
                        sub_key = sub_key.strip()
                        sub_val = sub_val.strip()
                        # 解析行内 dict {score: 4.8, votes: 39882}
                        if sub_val.startswith("{") and sub_val.endswith("}"):
                            inner = {}
                            for part in sub_val[1:-1].split(","):
                                if ":" in part:
                                    pk, _, pv = part.partition(":")
                                    inner[pk.strip()] = pv.strip().strip('"\'')
                            ratings[sub_key] = inner
                        else:
                            ratings[sub_key] = sub_val.strip('"\'')
                        i += 1
                    meta[key] = ratings
                    continue
                elif key == "awards":
                    awards = []
                    while i < len(lines) and lines[i].startswith("  -"):
                        sub_line = lines[i].strip("- ").strip()
                        if sub_val.startswith("{") if (sub_val := sub_line.split(":",1)[1].strip() if ":" in sub_line else "") else False:
                            inner = {}
                            if sub_line.startswith("{") and sub_line.endswith("}"):
                                for part in sub_line[1:-1].split(","):
                                    if ":" in part:
                                        pk, _, pv = part.partition(":")
                                        inner[pk.strip()] = pv.strip().strip('"\'')
                            awards.append(inner)
                        else:
                            # 解析 {name: xxx, year: xxx, org: xxx}
                            if "{" in sub_line:
                                dict_part = sub_line[sub_line.index("{"):sub_line.rindex("}")+1]
                                inner = {}
                                for part in dict_part[1:-1].split(","):
                                    if ":" in part:
                                        pk, _, pv = part.partition(":")
                                        inner[pk.strip()] = pv.strip().strip('"\'')
                                awards.append(inner)
                        i += 1
                    meta[key] = awards
                    continue
                else:
                    continue
            # 解析列表 [a, b, c]
            elif val.startswith("[") and val.endswith("]"):
                items = [x.strip().strip('"\'') for x in val[1:-1].split(",") if x.strip()]
                meta[key] = items
            # 解析 dict {a: b, c: d}
            elif val.startswith("{") and val.endswith("}"):
                inner = {}
                for part in val[1:-1].split(","):
                    if ":" in part:
                        pk, _, pv = part.partition(":")
                        inner[pk.strip()] = pv.strip().strip('"\'')
                meta[key] = inner
            else:
                meta[key] = val.strip('"\'')
        i += 1
    return meta, body


def load_entry(path: Path) -> Optional[Entry]:
    """从 Markdown 文件加载单个条目。"""
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception:
        return None
    meta, body = parse_frontmatter(raw)
    eid = meta.get("id", path.stem)
    return Entry(
        id=eid,
        title=meta.get("title", eid),
        category=meta.get("category", eid.split("-")[0] if "-" in eid else ""),
        tags=meta.get("tags", []) if isinstance(meta.get("tags"), list) else [],
        status=meta.get("status", "active"),
        created=meta.get("created", ""),
        updated=meta.get("updated", ""),
        related=meta.get("related", []) if isinstance(meta.get("related"), list) else [],
        related_typed=meta.get("related_typed", {}) if isinstance(meta.get("related_typed"), dict) else {},
        ratings=meta.get("ratings", {}) if isinstance(meta.get("ratings"), dict) else {},
        awards=meta.get("awards", []) if isinstance(meta.get("awards"), list) else [],
        data_confidence=meta.get("data_confidence", "simulated"),
        data_source=meta.get("data_source", ""),
        source_url=meta.get("source_url", ""),
        crawl_date=meta.get("crawl_date", ""),
        _fm_subcategory=meta.get("subcategory", ""),
        version=int(meta.get("version", 1)) if isinstance(meta.get("version", 1), (int, str)) else 1,
        content=body,
        raw=raw,
        file_path=path,
    )


# ============================================================
# BM25 检索
# ============================================================

class BM25Index:
    """BM25 全文检索（纯 Python 标准库实现）。

    参数：k1=1.5, b=0.75（业界标准值）
    """

    def __init__(self, k1: float = 1.5, b: float = 0.75, title_boost: float = 3.0):
        self.k1 = k1
        self.b = b
        self.title_boost = title_boost  # 标题命中加权倍数
        self.docs: list[list[str]] = []
        self.doc_ids: list[str] = []
        self.titles: list[list[str]] = []  # 标题 tokens（用于加权）
        self.df: Counter = Counter()  # 文档频率
        self.doc_len: list[int] = []
        self.avgdl: float = 0.0
        self.idf: dict[str, float] = {}

    def _tokenize(self, text: str) -> list[str]:
        """分词：中文按字 + 英文按词。"""
        text = text.lower()
        # 英文词
        en_tokens = re.findall(r'[a-z]+', text)
        # 中文字（单字）
        cn_chars = re.findall(r'[\u4e00-\u9fff]', text)
        return en_tokens + cn_chars

    def add(self, doc_id: str, text: str, title: str = "", slug: str = ""):
        """添加文档（支持标题和 slug 加权）。"""
        tokens = self._tokenize(text)
        self.docs.append(tokens)
        self.doc_ids.append(doc_id)
        # 标题 + slug 联合加权字段
        boost_text = f"{title} {title} {slug}" if slug else title
        self.titles.append(self._tokenize(boost_text) if boost_text else [])
        self.doc_len.append(len(tokens))
        for t in set(tokens):
            self.df[t] += 1

    def build(self):
        """构建索引，计算 IDF。"""
        N = len(self.docs)
        self.avgdl = sum(self.doc_len) / N if N else 0
        self.idf = {}
        for term, df in self.df.items():
            # BM25 IDF 公式（加 1 平滑）
            self.idf[term] = math.log((N - df + 0.5) / (df + 0.5) + 1)

    def _extract_cn_phrases(self, query: str) -> list[str]:
        """提取查询中的中文连续片段（>=2 字视为短语）。"""
        return [p for p in re.findall(r'[\u4e00-\u9fff]{2,}', query)]

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """检索，返回 [(doc_id, score), ...]。

        评分包含：
        - BM25 正文分数
        - 标题/slug 命中加权（title_boost=3.0）
        - 中文短语连续匹配奖励（标题中含完整短语额外 +idf*phrase_boost）
        """
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return []
        cn_phrases = self._extract_cn_phrases(query)
        phrase_boost = 5.0
        scores = []
        for i, doc_tokens in enumerate(self.docs):
            score = 0.0
            dl = self.doc_len[i]
            tf_counter = Counter(doc_tokens)
            title_counter = Counter(self.titles[i]) if self.titles else Counter()
            # 原始标题文本（用于短语连续匹配检测）
            # titles[i] 是 boost_text（title+title+slug）的 token 化结果，无法还原原文
            # 因此用 docs/slug/id 推断：标题原文从 doc_id 和 entry title 推断
            for qt in q_tokens:
                if qt not in self.idf:
                    continue
                tf = tf_counter.get(qt, 0)
                title_tf = title_counter.get(qt, 0)
                if tf == 0 and title_tf == 0:
                    continue
                idf = self.idf[qt]
                # BM25 公式
                norm = 1 - self.b + self.b * (dl / self.avgdl if self.avgdl else 0)
                body_score = idf * (tf * (self.k1 + 1)) / (tf + self.k1 * norm) if tf > 0 else 0
                # 标题加权：标题中的词额外 boost
                title_score = idf * title_tf * self.title_boost if title_tf > 0 else 0
                score += body_score + title_score
            # 中文短语连续匹配奖励：boost_text 中连续包含短语字符序列
            if cn_phrases and i < len(self.titles):
                # 用 boost_text 的字符级检测（titles 是 token 化后的，但中文单字 token 顺序保留）
                title_str = "".join(self.titles[i]) if self.titles and i < len(self.titles) else ""
                for phrase in cn_phrases:
                    if phrase in title_str:
                        # 短语中每个字都给 idf 奖励
                        for ch in phrase:
                            if ch in self.idf:
                                score += self.idf[ch] * phrase_boost
            if score > 0:
                scores.append((self.doc_ids[i], score))
        scores.sort(key=lambda x: -x[1])
        return scores[:top_k]


# ============================================================
# 知识库引擎
# ============================================================

class KnowledgeBase:
    """知识库核心引擎。"""

    def __init__(self, kb_dir: str | Path, use_vector: bool = True):
        self.kb_dir = Path(kb_dir)
        self.entries: dict[str, Entry] = {}
        self.bm25: BM25Index = BM25Index()
        self.use_vector = use_vector
        self._loaded = False

    def load(self):
        """加载所有 .md 文件。"""
        if self._loaded:
            return
        if not self.kb_dir.exists():
            self._loaded = True
            return
        for f in sorted(self.kb_dir.glob("*.md")):
            if f.stem == "INDEX":
                continue
            e = load_entry(f)
            if e and e.id:
                self.entries[e.id] = e
        # 构建 BM25 索引（含标题 + slug 加权）
        for eid, e in self.entries.items():
            self.bm25.add(eid, e.text, title=e.title, slug=eid)
        self.bm25.build()
        self._loaded = True

    def __len__(self) -> int:
        if not self._loaded:
            self.load()
        return len(self.entries)

    def get(self, entry_id: str) -> Optional[Entry]:
        if not self._loaded:
            self.load()
        return self.entries.get(entry_id)

    def search(self, query: str, top_k: int = 10, expand: bool = True) -> list[dict]:
        """检索，返回 [{id, title, score, ...}]。

        参数：
        - expand: 是否启用同义词扩展和拼写纠错（默认 True）
        """
        if not self._loaded:
            self.load()
        # 同义词扩展 + 拼写纠错
        search_query = query
        corrected_info = None
        if expand:
            try:
                from .synonyms import normalize_query
                corrected, applied, expanded = normalize_query(query)
                if applied:
                    corrected_info = applied
                # 用扩展后的词重新组合查询（去重保留顺序）
                if expanded:
                    seen = set()
                    unique = []
                    for w in expanded:
                        if w not in seen:
                            seen.add(w)
                            unique.append(w)
                    search_query = " ".join(unique[:10])  # 限制扩展词数避免过度匹配
            except ImportError:
                pass
        results = self.bm25.search(search_query, top_k=top_k)
        out = []
        for eid, score in results:
            e = self.entries.get(eid)
            if e:
                out.append({
                    "id": e.id,
                    "title": e.title,
                    "category": e.category,
                    "tags": e.tags,
                    "score": round(score, 4),
                    "data_confidence": e.data_confidence,
                    "data_source": e.data_source,
                    "file": str(e.file_path.name) if e.file_path else "",
                })
        return out

    # ============================================================
    # Agent 响应分层模板（P5: 根据数据置信度格式化回答）
    # ============================================================

    # 置信度 → 回答策略映射
    _CONFIDENCE_STRATEGY = {
        "official":  {"label": "权威来源",   "prefix": "",                    "suffix": ""},
        "verified":  {"label": "已验证来源", "prefix": "",                    "suffix": "\n\n> 📖 数据来源：{source}（已验证）"},
        "simulated": {"label": "推测数据",   "prefix": "⚠️ 以下信息为知识库推测，建议进一步核实：\n\n", "suffix": "\n\n> ⚠️ 本条目数据置信度较低（推测生成），实际信息请以品牌官方为准。"},
        "unknown":   {"label": "未标注",     "prefix": "",                    "suffix": "\n\n> ℹ️ 本条目数据来源未标注，请谨慎参考。"},
    }

    def format_response(self, query: str, top_k: int = 5) -> str:
        """根据数据置信度分层格式化 Agent 回答。

        策略：
        - official:  直接引用，标注权威来源（IBA/WSET/官方标准）
        - verified:  标注参考来源（百度百科/Wikipedia/品牌官方）
        - simulated: 降级提示"该信息为推测，建议核实"
        - unknown:   提示"数据来源未标注"

        返回格式化的 Markdown 回答字符串。
        """
        results = self.search(query, top_k=top_k)
        if not results:
            return f"未找到与「{query}」相关的知识条目。"

        # 按置信度分组排序：official > verified > simulated > unknown
        confidence_order = {"official": 0, "verified": 1, "simulated": 2, "unknown": 3}
        results_sorted = sorted(
            results,
            key=lambda r: (confidence_order.get(r.get("data_confidence", "unknown"), 9), -r.get("score", 0)),
        )

        lines = [f"## 关于「{query}」的知识库回答", ""]
        for i, r in enumerate(results_sorted, 1):
            confidence = r.get("data_confidence", "unknown")
            strategy = self._CONFIDENCE_STRATEGY.get(confidence, self._CONFIDENCE_STRATEGY["unknown"])
            source = r.get("data_source", "")
            title = r["title"]
            score = r.get("score", 0)

            # 条目标题行
            lines.append(f"### {i}. {title}")
            lines.append(f"- **置信度**：{strategy['label']}（score: {score}）")
            if source:
                lines.append(f"- **数据来源**：{source}")
            lines.append(f"- **条目 ID**：{r['id']}")

            # 获取条目正文摘要（前 3 行非空内容）
            entry = self.entries.get(r["id"])
            if entry:
                content_lines = [l for l in entry.content.split("\n") if l.strip() and not l.startswith("#")][:3]
                if content_lines:
                    lines.append("")
                    lines.append(strategy["prefix"] + "\n".join(content_lines) + strategy["suffix"].format(source=source))
            lines.append("")

        # 汇总置信度提示
        conf_counts = {}
        for r in results_sorted:
            c = r.get("data_confidence", "unknown")
            conf_counts[c] = conf_counts.get(c, 0) + 1
        summary_parts = [f"{v} 条{self._CONFIDENCE_STRATEGY.get(k, {}).get('label', k)}" for k, v in conf_counts.items()]
        lines += ["---", "", f"**本次回答数据构成**：{', '.join(summary_parts)}", ""]
        return "\n".join(lines)

    def filter(self, *,
               subcategory: str = None,
               abv_min: float = None,
               abv_max: float = None,
               price_max: int = None,
               region: str = None,
               flavor_tag: str = None) -> list[dict]:
        """基于结构化属性筛选条目。

        参数：
        - subcategory: 子类（如 whisky, cocktail, wine_red）
        - abv_min/abv_max: 酒精度范围
        - price_max: 价格上限（取区间下限比较）
        - region: 产地关键词
        - flavor_tag: 风味标签关键词
        """
        if not self._loaded:
            self.load()
        out = []
        for e in self.entries.values():
            attrs = e.structured_attrs
            if subcategory and attrs["subcategory"] != subcategory:
                continue
            if abv_min is not None and (attrs["abv_num"] is None or attrs["abv_num"] < abv_min):
                continue
            if abv_max is not None and (attrs["abv_num"] is None or attrs["abv_num"] > abv_max):
                continue
            if price_max is not None:
                if not attrs["price_rmb"] or attrs["price_rmb"][0] > price_max:
                    continue
            if region and region.lower() not in attrs["region"].lower():
                continue
            if flavor_tag:
                tags_lower = [t.lower() for t in attrs["flavor_tags"]]
                if flavor_tag.lower() not in tags_lower:
                    continue
            out.append({
                "id": e.id,
                "title": e.title,
                "subcategory": attrs["subcategory"],
                "abv_num": attrs["abv_num"],
                "price_rmb": attrs["price_rmb"],
                "region": attrs["region"],
                "flavor_tags": attrs["flavor_tags"],
            })
        return out

    def stats(self) -> dict:
        """统计信息。"""
        if not self._loaded:
            self.load()
        cat_count = Counter(e.category for e in self.entries.values())
        status_count = Counter(e.status for e in self.entries.values())
        # 子分类统计（从 id 推断）
        sub_count = Counter()
        for e in self.entries.values():
            parts = e.id.split("-")
            if len(parts) >= 2:
                sub_count[parts[1]] += 1
        return {
            "total_entries": len(self.entries),
            "categories": dict(cat_count),
            "statuses": dict(status_count),
            "top_subcategories": dict(sub_count.most_common(10)),
        }

    def lint(self) -> LintReport:
        """lint 健康检查。"""
        if not self._loaded:
            self.load()
        report = LintReport(total_files=len(self.entries))
        # 检查 INDEX.md
        index_path = self.kb_dir / "INDEX.md"
        indexed_ids = set()
        if index_path.exists():
            idx_text = index_path.read_text(encoding="utf-8")
            # 提取 [[ID]] 或 ](./ID.md) 格式
            indexed_ids = set(re.findall(r'\(\./([^.]+)\.md\)', idx_text))
            indexed_ids |= set(re.findall(r'\[\[([^\]]+)\]\]', idx_text))
        # 孤立文件：未在 INDEX 中登记
        for eid, e in self.entries.items():
            if indexed_ids and eid not in indexed_ids:
                report.orphan_files.append(eid)
            # 非法 status
            if e.status not in VALID_STATUS:
                report.invalid_status.append(f"{eid}: {e.status}")
            # 命名违规
            if not re.match(r'^(ENT|PRJ|SOP|DEC|ANTI|GRAPE|REGION|PROC|LAW|TREND|SCENE)-', eid):
                report.naming_violations.append(eid)
            # 缺 frontmatter（content 为空且 raw 不含 ---）
            if "---" not in e.raw[:20]:
                report.missing_frontmatter.append(eid)
        return report

    def related_graph(self) -> dict[str, list[str]]:
        """构建关联图谱。"""
        if not self._loaded:
            self.load()
        graph = defaultdict(list)
        for eid, e in self.entries.items():
            for r in e.related:
                graph[eid].append(r)
        return dict(graph)
