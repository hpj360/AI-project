#!/usr/bin/env python3
"""为知识库条目自动补齐 related 关联关系。

策略：
1. 同子类内：同品牌、同产区、同风味标签的条目建立关联
2. 跨子类：基酒→鸡尾酒（如金酒→马天尼类鸡尾酒）
3. 每个条目最多 5 个关联，避免过度连接
"""
from __future__ import annotations

import sys
from pathlib import Path
from collections import defaultdict
import re

SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "data"))

KB_DIR = Path(__file__).parent.parent / "knowledge"


def load_all_entries():
    """加载所有数据文件的 ENTRIES。"""
    import importlib.util
    data_dir = SCRIPTS_DIR / "data"
    all_entries = []
    for df in sorted(data_dir.glob("data_*.py")):
        mod_name = df.stem
        spec = importlib.util.spec_from_file_location(mod_name, df)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            entries = getattr(mod, "ENTRIES", [])
            all_entries.extend(entries)
        except Exception as e:
            print(f"  {mod_name}: 加载失败 - {e}")
    return all_entries


def find_relations(entries):
    """为每个条目找出关联条目。

    关联策略（按优先级）：
    1. 同品牌（最多 3 个）
    2. 同产区同子类（补到 5）
    3. 跨子类：基酒→鸡尾酒
    4. 跨产区同子类（补到 4）：不同产区同类酒（如不同产区的赤霞珠）
    5. 同子类兜底（补到 5）：相同子类的其他条目随机选
    6. 同风味标签（补到 5）：相同风味标签的条目
    """
    # 建立索引
    by_subcat = defaultdict(list)
    by_brand = defaultdict(list)
    by_region = defaultdict(list)
    by_flavor_tag = defaultdict(list)
    by_subcat_region = defaultdict(list)
    by_country = defaultdict(list)
    for e in entries:
        eid = e.get("id", "")
        sub = e.get("subcategory", "")
        by_subcat[sub].append(e)
        # 品牌从 producer 或 name_en 提取
        producer = (e.get("producer", "") or "").lower()
        if producer:
            by_brand[producer].append(e)
        region = (e.get("region", "") or "").lower()
        if region:
            by_region[region].append(e)
            by_subcat_region[(sub, region)].append(e)
        country = (e.get("country", "") or "").lower()
        if country:
            by_country[(sub, country)].append(e)
        # 风味标签
        for tag in (e.get("flavor_tags") or []):
            by_flavor_tag[tag.lower()].append(e)

    relations = defaultdict(set)
    for e in entries:
        eid = e.get("id", "")
        if not eid:
            continue
        sub = e.get("subcategory", "")
        producer = (e.get("producer", "") or "").lower()
        region = (e.get("region", "") or "").lower()
        country = (e.get("country", "") or "").lower()

        # 1. 同品牌（最多 3 个）
        if producer and len(by_brand[producer]) > 1:
            for other in by_brand[producer]:
                oid = other.get("id", "")
                if oid and oid != eid:
                    relations[eid].add(oid)
                    if len(relations[eid]) >= 3:
                        break

        # 2. 同产区同子类（最多 2 个，补充到 5）
        if region:
            for other in by_region[region]:
                oid = other.get("id", "")
                if oid and oid != eid and other.get("subcategory") == sub:
                    relations[eid].add(oid)
                    if len(relations[eid]) >= 5:
                        break

        # 3. 跨子类：基酒→鸡尾酒
        if sub == "cocktail":
            # 从 recipe 中提取基酒
            recipe = e.get("recipe", [])
            for item in recipe:
                name = (item.get("name", "") or "").lower()
                # 匹配基酒类型
                if "威士忌" in name or "whisky" in name or "bourbon" in name:
                    for other in by_subcat.get("whisky", [])[:3]:
                        relations[eid].add(other.get("id", ""))
                elif "金酒" in name or "gin" in name:
                    for other in by_subcat.get("gin", [])[:3]:
                        relations[eid].add(other.get("id", ""))
                elif "伏特加" in name or "vodka" in name:
                    for other in by_subcat.get("vodka", [])[:3]:
                        relations[eid].add(other.get("id", ""))
                elif "朗姆" in name or "rum" in name:
                    for other in by_subcat.get("rum", [])[:3]:
                        relations[eid].add(other.get("id", ""))
                elif "龙舌兰" in name or "tequila" in name or "梅斯卡尔" in name or "mezcal" in name:
                    for other in by_subcat.get("tequila", [])[:3]:
                        relations[eid].add(other.get("id", ""))
                elif "白兰地" in name or "brandy" in name or "干邑" in name:
                    for other in by_subcat.get("brandy", [])[:3]:
                        relations[eid].add(other.get("id", ""))
                elif "清酒" in name or "sake" in name:
                    for other in by_subcat.get("sake", [])[:3]:
                        relations[eid].add(other.get("id", ""))
                elif "白酒" in name or "baijiu" in name:
                    for other in by_subcat.get("baijiu", [])[:3]:
                        relations[eid].add(other.get("id", ""))

        # 4. 跨产区同子类（补到 4）：不同产区/国家的同类酒
        if len(relations[eid]) < 4 and sub:
            same_sub_diff_region = [
                other for other in by_subcat.get(sub, [])
                if other.get("id", "") != eid
                and (other.get("region", "") or "").lower() != region
            ]
            for other in same_sub_diff_region[:3]:
                oid = other.get("id", "")
                if oid:
                    relations[eid].add(oid)
                    if len(relations[eid]) >= 4:
                        break

        # 5. 同子类兜底（补到 5）：相同子类的其他条目随机选
        if len(relations[eid]) < 5 and sub:
            for other in by_subcat.get(sub, []):
                oid = other.get("id", "")
                if oid and oid != eid and oid not in relations[eid]:
                    relations[eid].add(oid)
                    if len(relations[eid]) >= 5:
                        break

        # 6. 同风味标签（补到 5）
        if len(relations[eid]) < 5:
            for tag in (e.get("flavor_tags") or []):
                for other in by_flavor_tag.get(tag.lower(), []):
                    oid = other.get("id", "")
                    if oid and oid != eid and oid not in relations[eid]:
                        relations[eid].add(oid)
                        if len(relations[eid]) >= 5:
                            break
                if len(relations[eid]) >= 5:
                    break

    # 截断到 5 个
    return {k: list(v)[:5] for k, v in relations.items() if v}


def update_md_files(relations):
    """更新 .md 文件，注入或替换 related 字段。"""
    updated = 0
    for eid, related in relations.items():
        md_path = KB_DIR / f"{eid}.md"
        if not md_path.exists():
            continue
        content = md_path.read_text(encoding="utf-8")
        related_str = f"related: [{', '.join(related)}]"
        # 如果已有 related 字段，替换它
        if re.search(r'^related:.*$', content, re.MULTILINE):
            content = re.sub(
                r'^related:.*$',
                related_str,
                content,
                count=1,
                flags=re.MULTILINE,
            )
        else:
            # 在 updated: 行后插入 related
            content = re.sub(
                r'(updated: \d{4}-\d{2}-\d{2})',
                r'\1\n' + related_str,
                content,
                count=1,
            )
        md_path.write_text(content, encoding="utf-8")
        updated += 1
    return updated


def main():
    print("=" * 50)
    print("知识库关联关系补齐")
    print("=" * 50)
    entries = load_all_entries()
    print(f"加载 {len(entries)} 条目")
    relations = find_relations(entries)
    print(f"为 {len(relations)} 个条目找到关联")
    total_links = sum(len(v) for v in relations.values())
    print(f"总关联数: {total_links}")
    updated = update_md_files(relations)
    print(f"更新 {updated} 个 .md 文件")
    print("\n✓ 关联关系补齐完成")


if __name__ == "__main__":
    main()
