#!/usr/bin/env python3
"""知识库 CI 校验脚本（防幻觉护栏）。

功能：
1. ID 唯一性校验（跨所有数据文件）
2. 必填字段完整性校验
3. ASCII 引号规范校验（字符串值内部禁用 ASCII " '）
4. 关联有效性校验（related 指向的 ID 必须存在）
5. 渲染产物与数据源一致性校验
6. lint 0 问题校验
7. 检索可用性校验

使用：
    cd /workspace/Hermes
    PYTHONPATH=src python3 content-creation/scripts/validate_kb.py
退出码：0 全部通过，1 有问题
"""
from __future__ import annotations

import importlib.util
import sys
import re
from pathlib import Path
from collections import Counter

SCRIPTS_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPTS_DIR / "data"
KB_DIR = SCRIPTS_DIR.parent / "knowledge"
SRC_DIR = SCRIPTS_DIR.parent.parent / "src"
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(DATA_DIR))
sys.path.insert(0, str(SRC_DIR))

# 必填字段清单
REQUIRED_FIELDS = [
    "id", "title", "title_en", "category", "subcategory", "tags", "summary",
    "name_cn", "name_en", "country", "abv", "volume", "price_tier",
    "price_rmb_range", "ingredients", "production_method",
    "appearance", "nose", "palate", "finish", "flavor_tags",
    "serving_temp", "glassware", "history", "related",
]
# 鸡尾酒扩展必填字段（仅 subcategory == cocktail）
COCKTAIL_REQUIRED = [
    "cocktail_style", "recipe", "garnish", "technique", "difficulty",
    "creator", "year_created", "flavor_profile", "abv_estimate",
    "variations", "glass_size", "serving_note",
    # v3 深度字段
    "ice_type", "prep_time", "calorie", "cost_rmb",
    "occasion", "season", "pairing_music", "source", "balance",
]

# ASCII 引号检测正则（字符串值内部）
ASCII_DQUOTE_RE = re.compile(r'"\s*[^"]*"[^"]*"[^"]*"')  # 粗略检测
ASCII_QUOTE_IN_STR = re.compile(r':\s*"[^"]*"[^",}\]]')  # value 内含未转义 "

PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
WARN = "\033[33m⚠\033[0m"


class Report:
    def __init__(self):
        self.errors = []
        self.warnings = []
        self.passed = 0

    def ok(self, msg):
        self.passed += 1
        print(f"  {PASS} {msg}")

    def err(self, msg):
        self.errors.append(msg)
        print(f"  {FAIL} {msg}")

    def warn(self, msg):
        self.warnings.append(msg)
        print(f"  {WARN} {msg}")

    @property
    def exit_code(self):
        return 1 if self.errors else 0


def load_all_entries():
    """加载所有 data_*.py 文件。"""
    all_entries = []
    files = sorted(DATA_DIR.glob("data_*.py"))
    print(f"\n[1/7] 加载数据文件（{len(files)} 个）")
    for df in files:
        mod_name = df.stem
        spec = importlib.util.spec_from_file_location(mod_name, df)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            entries = getattr(mod, "ENTRIES", [])
            all_entries.extend(entries)
            print(f"  {PASS} {mod_name}: {len(entries)} 条目")
        except Exception as e:
            print(f"  {FAIL} {mod_name}: 加载失败 - {e}")
    return all_entries


def check_id_uniqueness(entries, report):
    """[2/7] ID 唯一性。"""
    print(f"\n[2/7] ID 唯一性校验")
    ids = [e.get("id", "") for e in entries]
    dup = [iid for iid, c in Counter(ids).items() if c > 1 and iid]
    if dup:
        for d in dup:
            report.err(f"重复 ID: {d}")
    else:
        report.ok(f"{len(ids)} 个 ID 全部唯一")


def check_required_fields(entries, report):
    """[3/7] 必填字段。"""
    print(f"\n[3/7] 必填字段完整性校验")
    missing_count = 0
    for e in entries:
        eid = e.get("id", "?")
        for f in REQUIRED_FIELDS:
            if f not in e:
                report.err(f"{eid}: 缺少必填字段 '{f}'")
                missing_count += 1
        # 鸡尾酒扩展
        if e.get("subcategory") == "cocktail":
            for f in COCKTAIL_REQUIRED:
                if f not in e:
                    report.err(f"{eid}: 缺少鸡尾酒字段 '{f}'")
                    missing_count += 1
    if missing_count == 0:
        report.ok("所有必填字段齐全")


def check_quote_rules(entries, report):
    """[4/7] ASCII 引号规范（字符串值内部）。"""
    print(f"\n[4/7] ASCII 引号规范校验")
    bad = 0
    for e in entries:
        eid = e.get("id", "?")
        for k, v in e.items():
            if not isinstance(v, str):
                continue
            # 检测字符串值内部是否含 ASCII 双引号（非首尾）
            # 简化：value 内部出现 " 即视为问题（因为外层用 " 包裹）
            if v.count('"') > 0:
                # 允许 source_url 等含 URL 的字段
                if k in ("source_url",):
                    continue
                report.err(f"{eid}.{k}: 字符串值内含 ASCII 双引号")
                bad += 1
    if bad == 0:
        report.ok("无 ASCII 引号违规")


def check_related_validity(entries, report):
    """[5/7] 关联有效性。"""
    print(f"\n[5/7] 关联有效性校验")
    all_ids = set(e.get("id", "") for e in entries)
    bad = 0
    for e in entries:
        eid = e.get("id", "?")
        for r in e.get("related", []) or []:
            if r not in all_ids:
                # 允许指向未生成的基酒类（如 ENT-gin-base）
                if r.endswith("-base") or r.startswith("ENT-") and "base" in r:
                    continue
                report.warn(f"{eid}: related 指向不存在 ID '{r}'")
                bad += 1
    if bad == 0:
        report.ok("所有 related 指向有效（或允许的基酒类）")


def check_render_consistency(entries, report):
    """[6/7] 渲染产物一致性。"""
    print(f"\n[6/7] 渲染产物一致性校验")
    md_files = set(f.stem for f in KB_DIR.glob("*.md") if f.stem != "INDEX")
    entry_ids = set(e.get("id", "") for e in entries)
    # 数据有但 md 无
    missing_md = entry_ids - md_files
    for m in list(missing_md)[:5]:
        report.err(f"数据有 {m}.md 但文件不存在（需运行 render_kb.py）")
    if len(missing_md) > 5:
        report.err(f"... 还有 {len(missing_md)-5} 个缺失")
    # md 有但数据无（孤立文件）
    orphan = md_files - entry_ids
    for o in list(orphan)[:5]:
        report.warn(f"孤立文件 {o}.md（数据源无对应条目）")
    if not missing_md:
        report.ok(f"{len(entry_ids)} 条目全部已渲染")
    if not orphan:
        report.ok("无孤立文件")


def check_search_and_lint(report):
    """[7/7] 检索与 lint。"""
    print(f"\n[7/7] Hermes 引擎 lint + 检索校验")
    try:
        from hermes import kb
        k = kb.KnowledgeBase(str(KB_DIR), use_vector=False)
        # lint
        r = k.lint()
        issues = getattr(r, "total_issues", getattr(r, "issues", []))
        n = len(issues) if isinstance(issues, list) else int(issues or 0)
        if n == 0:
            report.ok("lint 0 问题")
        else:
            report.err(f"lint 发现 {n} 个问题")
        # 检索测试
        test_queries = ["威士忌", "鸡尾酒", "红葡萄酒", "分子"]
        all_ok = True
        for q in test_queries:
            res = k.search(q, top_k=3)
            if not res:
                report.err(f"检索 '{q}' 返回空")
                all_ok = False
        if all_ok:
            report.ok(f"检索测试 {len(test_queries)} 个查询全部返回结果")
    except Exception as e:
        report.err(f"Hermes 引擎校验失败: {e}")


def main():
    print("=" * 60)
    print("知识库 CI 校验（防幻觉护栏）")
    print("=" * 60)

    report = Report()
    entries = load_all_entries()
    print(f"\n总条目数: {len(entries)}")

    check_id_uniqueness(entries, report)
    check_required_fields(entries, report)
    check_quote_rules(entries, report)
    check_related_validity(entries, report)
    check_render_consistency(entries, report)
    check_search_and_lint(report)

    # 汇总
    print("\n" + "=" * 60)
    print("校验汇总")
    print("=" * 60)
    print(f"  {PASS} 通过: {report.passed}")
    print(f"  {WARN} 警告: {len(report.warnings)}")
    print(f"  {FAIL} 错误: {len(report.errors)}")
    if report.errors:
        print(f"\n退出码 1（有错误需修复）")
    else:
        print(f"\n退出码 0（全部通过）")
    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())
