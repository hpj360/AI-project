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
    ratings: dict = field(default_factory=dict)
    awards: list = field(default_factory=list)
    content: str = ""  # 正文 Markdown
    raw: str = ""  # 原始文件内容
    file_path: Optional[Path] = None

    @property
    def text(self) -> str:
        """用于检索的文本（标题+标签+正文）。"""
        return f"{self.title} {' '.join(self.tags)} {self.content}"


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
    """解析 YAML frontmatter（简化版，不依赖 pyyaml）。"""
    m = FM_PATTERN.match(raw)
    if not m:
        return {}, raw
    fm_text = m.group(1)
    body = m.group(2)
    meta = {}
    for line in fm_text.split("\n"):
        line = line.rstrip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            # 解析列表 [a, b, c]
            if val.startswith("[") and val.endswith("]"):
                items = [x.strip().strip('"\'') for x in val[1:-1].split(",") if x.strip()]
                meta[key] = items
            else:
                meta[key] = val.strip('"\'')
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

    def __init__(self, k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.docs: list[list[str]] = []
        self.doc_ids: list[str] = []
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

    def add(self, doc_id: str, text: str):
        """添加文档。"""
        tokens = self._tokenize(text)
        self.docs.append(tokens)
        self.doc_ids.append(doc_id)
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

    def search(self, query: str, top_k: int = 10) -> list[tuple[str, float]]:
        """检索，返回 [(doc_id, score), ...]。"""
        q_tokens = self._tokenize(query)
        if not q_tokens:
            return []
        scores = []
        for i, doc_tokens in enumerate(self.docs):
            score = 0.0
            dl = self.doc_len[i]
            tf_counter = Counter(doc_tokens)
            for qt in q_tokens:
                if qt not in self.idf:
                    continue
                tf = tf_counter.get(qt, 0)
                if tf == 0:
                    continue
                idf = self.idf[qt]
                # BM25 公式
                norm = 1 - self.b + self.b * (dl / self.avgdl if self.avgdl else 0)
                score += idf * (tf * (self.k1 + 1)) / (tf + self.k1 * norm)
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
        # 构建 BM25 索引
        for eid, e in self.entries.items():
            self.bm25.add(eid, e.text)
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

    def search(self, query: str, top_k: int = 10) -> list[dict]:
        """检索，返回 [{id, title, score, ...}]。"""
        if not self._loaded:
            self.load()
        results = self.bm25.search(query, top_k=top_k)
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
                    "file": str(e.file_path.name) if e.file_path else "",
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
            if not re.match(r'^(ENT|PRJ|SOP|DEC|ANTI)-', eid):
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
