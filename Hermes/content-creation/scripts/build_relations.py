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
    """为每个条目找出关联条目（带类型）。

    关联类型：
    - same_brand: 同品牌
    - same_region: 同产区同子类
    - base_to_cocktail: 基酒→鸡尾酒
    - cross_region: 跨产区同子类
    - same_subcat: 同子类兜底
    - same_flavor: 同风味标签

    防热点机制：单节点最大入度 ≤30
    """
    MAX_IN_DEGREE = 30
    in_degree = defaultdict(int)

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
        for tag in (e.get("flavor_tags") or []):
            by_flavor_tag[tag.lower()].append(e)

    def try_add(src_id: str, tgt_id: str, rel_type: str,
                rel_dict: dict, rel_set: set) -> bool:
        """尝试添加带类型的关联。"""
        if not tgt_id or tgt_id == src_id or tgt_id in rel_set:
            return False
        if in_degree[tgt_id] >= MAX_IN_DEGREE:
            return False
        rel_dict[tgt_id] = rel_type
        rel_set.add(tgt_id)
        in_degree[tgt_id] += 1
        return True

    # relations[eid] = {target_id: rel_type, ...}
    relations = defaultdict(dict)
    for e in entries:
        eid = e.get("id", "")
        if not eid:
            continue
        sub = e.get("subcategory", "")
        producer = (e.get("producer", "") or "").lower()
        region = (e.get("region", "") or "").lower()
        country = (e.get("country", "") or "").lower()
        rel_dict = relations[eid]
        rel_set = set(rel_dict.keys())

        # 1. 同品牌（最多 3 个）
        if producer and len(by_brand[producer]) > 1:
            for other in by_brand[producer]:
                if try_add(eid, other.get("id", ""), "same_brand", rel_dict, rel_set):
                    if len(rel_dict) >= 3:
                        break

        # 2. 同产区同子类（最多 2 个，补充到 5）
        if region:
            for other in by_region[region]:
                if other.get("subcategory") == sub:
                    if try_add(eid, other.get("id", ""), "same_region", rel_dict, rel_set):
                        if len(rel_dict) >= 5:
                            break

        # 3. 跨子类：基酒→鸡尾酒
        if sub == "cocktail":
            recipe = e.get("recipe", [])
            for item in recipe:
                name = (item.get("name", "") or "").lower()
                if "威士忌" in name or "whisky" in name or "bourbon" in name:
                    for other in by_subcat.get("whisky", [])[:3]:
                        try_add(eid, other.get("id", ""), "base_to_cocktail", rel_dict, rel_set)
                elif "金酒" in name or "gin" in name:
                    for other in by_subcat.get("gin", [])[:3]:
                        try_add(eid, other.get("id", ""), "base_to_cocktail", rel_dict, rel_set)
                elif "伏特加" in name or "vodka" in name:
                    for other in by_subcat.get("vodka", [])[:3]:
                        try_add(eid, other.get("id", ""), "base_to_cocktail", rel_dict, rel_set)
                elif "朗姆" in name or "rum" in name:
                    for other in by_subcat.get("rum", [])[:3]:
                        try_add(eid, other.get("id", ""), "base_to_cocktail", rel_dict, rel_set)
                elif "龙舌兰" in name or "tequila" in name or "梅斯卡尔" in name or "mezcal" in name:
                    for other in by_subcat.get("tequila", [])[:3]:
                        try_add(eid, other.get("id", ""), "base_to_cocktail", rel_dict, rel_set)
                elif "白兰地" in name or "brandy" in name or "干邑" in name:
                    for other in by_subcat.get("brandy", [])[:3]:
                        try_add(eid, other.get("id", ""), "base_to_cocktail", rel_dict, rel_set)
                elif "清酒" in name or "sake" in name:
                    for other in by_subcat.get("sake", [])[:3]:
                        try_add(eid, other.get("id", ""), "base_to_cocktail", rel_dict, rel_set)
                elif "白酒" in name or "baijiu" in name:
                    for other in by_subcat.get("baijiu", [])[:3]:
                        try_add(eid, other.get("id", ""), "base_to_cocktail", rel_dict, rel_set)

        # 4. 跨产区同子类（补到 4）
        if len(rel_dict) < 4 and sub:
            same_sub_diff_region = [
                other for other in by_subcat.get(sub, [])
                if other.get("id", "") != eid
                and (other.get("region", "") or "").lower() != region
            ]
            for other in same_sub_diff_region[:5]:
                if try_add(eid, other.get("id", ""), "cross_region", rel_dict, rel_set):
                    if len(rel_dict) >= 4:
                        break

        # 5. 同子类兜底（补到 5）
        if len(rel_dict) < 5 and sub:
            for other in by_subcat.get(sub, []):
                if try_add(eid, other.get("id", ""), "same_subcat", rel_dict, rel_set):
                    if len(rel_dict) >= 5:
                        break

        # 6. 同风味标签（补到 5）
        if len(rel_dict) < 5:
            for tag in (e.get("flavor_tags") or []):
                for other in by_flavor_tag.get(tag.lower(), []):
                    if try_add(eid, other.get("id", ""), "same_flavor", rel_dict, rel_set):
                        if len(rel_dict) >= 5:
                            break
                if len(rel_dict) >= 5:
                    break

    # 返回 {eid: [(target_id, rel_type), ...]}
    return {k: list(v.items())[:5] for k, v in relations.items() if v}


def update_md_files(relations):
    """更新 .md 文件，注入或替换 related 和 related_typed 字段。

    relations 格式：{eid: [(target_id, rel_type), ...]}
    - related: [id1, id2, ...]（向后兼容）
    - related_typed: {target_id: rel_type, ...}（类型化关系）
    """
    updated = 0
    for eid, related_pairs in relations.items():
        md_path = KB_DIR / f"{eid}.md"
        if not md_path.exists():
            continue
        content = md_path.read_text(encoding="utf-8")
        # 兼容字段：仅 ID 列表
        related_ids = [t for t, _ in related_pairs]
        related_str = f"related: [{', '.join(related_ids)}]"
        # 类型化字段：related_typed: {id: type, ...}
        typed_pairs = [f"{tid}: {rtype}" for tid, rtype in related_pairs]
        related_typed_str = "related_typed: {" + ", ".join(typed_pairs) + "}"

        # 移除已有的 related_typed 字段（避免重复）
        content = re.sub(r'^related_typed:.*$\n?', '', content, flags=re.MULTILINE)
        # 替换或插入 related
        if re.search(r'^related:.*$', content, re.MULTILINE):
            content = re.sub(
                r'^related:.*$',
                related_str + "\n" + related_typed_str,
                content,
                count=1,
                flags=re.MULTILINE,
            )
        else:
            content = re.sub(
                r'(updated: \d{4}-\d{2}-\d{2})',
                r'\1\n' + related_str + "\n" + related_typed_str,
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
