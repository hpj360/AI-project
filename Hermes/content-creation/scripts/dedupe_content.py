#!/usr/bin/env python3
"""Hermes 知识库内容级去重。

按 front matter title 分组，相同 title 的文件保留内容最丰富的版本。
判断"内容丰富度"：
1. 优先有结构化 recipe（鸡尾酒）
2. 优先有 content_body（指导性条目）
3. 优先体长更长的
4. 优先 confidence 更高的（official > verified > simulated）
"""
import re
import sys
from pathlib import Path
from collections import defaultdict

KB_DIR = Path("content-creation/knowledge")


def parse_meta(content):
    """解析 front matter。"""
    if not content.startswith("---"):
        return {}, "", 0
    end = content.find("---", 3)
    if end == -1:
        return {}, "", 0
    fm = content[3:end]
    meta = {}
    title = ""
    for line in fm.split("\n"):
        line = line.rstrip()
        if line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            val = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
        if key == "title":
            title = val
        meta[key] = val
    return meta, title, end + 3


def score_file(content, meta, fm_end):
    """计算文件内容丰富度评分。"""
    score = 0
    body = content[fm_end:].strip() if fm_end else content.strip()
    body_len = len(body)

    # 1. 长度（主要指标）
    score += body_len // 10

    # 2. 有结构化 recipe（鸡尾酒关键）
    has_recipe_table = bool(re.search(r"##\s*配方\s*\n.*?\|", body, re.DOTALL))
    if has_recipe_table:
        score += 500

    # 3. 章节数
    h2_count = len(re.findall(r"^##\s", body, re.MULTILINE))
    score += h2_count * 30

    # 4. 子章节数
    h3_count = len(re.findall(r"^###\s", body, re.MULTILINE))
    score += h3_count * 10

    # 5. 表格数
    table_count = len(re.findall(r"^\|", body, re.MULTILINE))
    score += table_count * 5

    # 6. 置信度加成
    conf = str(meta.get("data_confidence", "")).lower()
    if conf == "official":
        score += 200
    elif conf == "verified":
        score += 100
    elif conf == "simulated":
        score += 10

    # 7. data_source 标注
    if meta.get("data_source"):
        score += 50

    # 8. 有 ratings
    if meta.get("ratings"):
        score += 50

    return score


def main(dry_run=True, min_score_diff=200):
    """min_score_diff: 评分差异超过此值才认为"明显冗余"，避免误删。

    去重 key 使用 (title, subcategory) 而非单 title，
    避免不同子类（威士忌品牌 vs 鸡尾酒）因同名 Chinese title 误删。
    """
    md_files = sorted(KB_DIR.glob("*.md"))
    title_groups = defaultdict(list)
    file_data = {}

    for f in md_files:
        content = f.read_text(encoding="utf-8")
        meta, title, fm_end = parse_meta(content)
        if not title:
            continue
        subcat = str(meta.get("subcategory", "unknown"))
        # 关键修复：用 (title, subcategory) 作为去重 key
        key = (title, subcat)
        sc = score_file(content, meta, fm_end)
        file_data[f.name] = (sc, content, meta, title, subcat, fm_end)
        title_groups[key].append(f.name)

    duplicates = {k: files for k, files in title_groups.items() if len(files) > 1}
    print(f"扫描 {len(md_files)} 个文件")
    print(f"发现 {len(duplicates)} 个重复 (标题+子类) 组（共 {sum(len(v) for v in duplicates.values())} 个文件）")
    print(f"评分差异阈值: {min_score_diff}（超过此值才标记为可删除）\n")

    to_delete = []
    warnings = []
    to_keep = {}

    for key, files in duplicates.items():
        title, subcat = key
        scored = [(f, file_data[f][0]) for f in files]
        scored.sort(key=lambda x: -x[1])
        keep = scored[0][0]
        to_keep[keep] = (title, subcat, scored[0][1])
        for f, sc in scored[1:]:
            diff = scored[0][1] - sc
            if diff >= min_score_diff:
                to_delete.append((f, title, subcat, sc, diff))
            else:
                warnings.append((f, keep, title, subcat, sc, file_data[keep][0], file_data[keep][0] - sc))

    print(f"将删除 {len(to_delete)} 个明显空壳（评分差异>={min_score_diff}）")
    print(f"标记 {len(warnings)} 个差异不明显的重叠版本（需人工审核）\n")

    if to_delete:
        print("=" * 70)
        print("将删除的文件（确认无重要内容）")
        print("=" * 70)
        for f, t, s, sc, diff in to_delete:
            keep = [k for k, (tt, ss, _) in to_keep.items() if tt == t and ss == s][0]
            print(f"  DEL  {f} [{s}] (评分{sc}, 差{diff})")
            print(f"  KEEP {keep} (评分{to_keep[keep][2]})")
            print()

    if warnings:
        print("\n" + "=" * 70)
        print("需要人工审核（评分差异<200，可能含独特信息）")
        print("=" * 70)
        for f, keep, t, s, sc, keep_sc, diff in warnings[:20]:
            print(f"  ⚠ {f} [{s}] (评分{sc}) vs {keep} (评分{keep_sc}, 差{diff})")
        if len(warnings) > 20:
            print(f"  ... 等{len(warnings) - 20}个")

    if dry_run:
        print("\n[DRY RUN] 实际删除请加 --apply")
        return

    for f, t, s, sc, diff in to_delete:
        (KB_DIR / f).unlink()
        print(f"删除: {f}")
    print(f"\n完成，删除 {len(to_delete)} 个文件")


if __name__ == "__main__":
    dry_run = "--apply" not in sys.argv
    main(dry_run=dry_run)
