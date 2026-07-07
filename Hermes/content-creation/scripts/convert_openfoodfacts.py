#!/usr/bin/env python3
"""OpenFoodFacts 原始数据转知识库条目。

把 external/openfoodfacts_raw.json 转换为 data/data_openfoodfacts_supplement.py。
字段对齐 validate_kb.py 的 REQUIRED_FIELDS，并避免字符串内含 ASCII 双引号
（validate_kb.py 的 check_quote_rules 会拒绝）。
"""
import json
import re
from pathlib import Path
from collections import defaultdict


# 子类中文名映射（与 DATA_SPEC.py 一致）
SUBCATEGORY_CN = {
    "whisky": "威士忌",
    "brandy": "白兰地",
    "gin": "金酒",
    "vodka": "伏特加",
    "rum": "朗姆酒",
    "tequila": "龙舌兰",
    "liqueur": "利口酒",
    "wine_red": "红葡萄酒",
    "wine_white": "白葡萄酒",
    "wine_sparkling": "起泡酒",
    "sake": "清酒",
    "beer": "啤酒",
}

# 玻璃杯与适饮温度默认值（按子类）
SERVING_DEFAULTS = {
    "whisky": ("18-20℃", "闻香杯"),
    "brandy": ("18-20℃", "白兰地杯"),
    "gin": ("4-7℃", "烈酒杯"),
    "vodka": ("-5-0℃", "烈酒杯"),
    "rum": ("18-20℃", "烈酒杯"),
    "tequila": ("16-18℃", "龙舌兰杯"),
    "liqueur": ("8-12℃", "利口酒杯"),
    "wine_red": ("16-18℃", "波尔多杯"),
    "wine_white": ("8-12℃", "白葡萄酒杯"),
    "wine_sparkling": ("6-10℃", "笛形香槟杯"),
    "sake": ("5-10℃", " tokuri / 丰杯"),
    "beer": ("4-7℃", "啤酒杯"),
}


def sanitize(s):
    """清洗字符串：去除 ASCII 双引号、控制字符、多余空白。"""
    if not isinstance(s, str):
        s = str(s) if s is not None else ""
    # 去除 ASCII 双引号（避免 validate_kb 的引号规则报错）
    s = s.replace('"', "'")
    # 去除控制字符与换行
    s = re.sub(r"[\r\n\t]+", " ", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def make_slug(name):
    """从名称生成 URL 友好的 slug。"""
    slug = name.lower()
    slug = re.sub(r"[^a-z0-9]+", "-", slug)
    slug = slug.strip("-")
    return slug[:50] or "product"


def make_entry(p, idx):
    """转换单个产品为知识库条目。"""
    subcat = p["subcategory"]
    name = sanitize(p["name"])[:80]
    if not name:
        name = f"OpenFoodFacts Product {idx}"
    brands = sanitize(p.get("brands", ""))
    brand_first = brands.split(",")[0].strip() if brands else ""
    origins = sanitize(p.get("origins", ""))
    country = origins.split(",")[0].strip() if origins else "未知"
    categories = sanitize(p.get("categories", ""))
    abv = sanitize(p.get("abv", "")) or "未知"
    volume = sanitize(p.get("quantity", "")) or "未知"
    image_url = sanitize(p.get("image_url", ""))
    barcode = sanitize(p.get("barcode", ""))
    subcat_cn = SUBCATEGORY_CN.get(subcat, subcat)
    serving_temp, glassware = SERVING_DEFAULTS.get(subcat, ("", ""))

    tags = ["OpenFoodFacts", subcat, subcat_cn]
    if brand_first:
        tags.append(brand_first)

    eid = f"ENT-{subcat}-off-{idx:03d}-{make_slug(name)}"

    summary = f"OpenFoodFacts 真实产品数据：{name}"
    if brand_first:
        summary += f"（{brand_first}）"
    if origins:
        summary += f"，产地 {origins}"
    if abv and abv != "未知":
        summary += f"，酒精度 {abv}"

    return {
        "id": eid,
        "title": name,
        "title_en": name,
        "category": "ENT",
        "subcategory": subcat,
        "tags": tags,
        "summary": summary,
        "name_cn": name,
        "name_en": name,
        "aliases": [brand_first] if brand_first else [],
        "country": country,
        "region": origins,
        "producer": brands,
        "abv": abv,
        "volume": volume,
        "price_tier": "daily",
        "price_rmb_range": [50, 300],
        "ingredients": "",
        "production_method": "",
        "distillation": "",
        "aging": "",
        "vintage": "",
        "appearance": "",
        "nose": "",
        "palate": "",
        "finish": "",
        "flavor_tags": [],
        "serving_temp": serving_temp,
        "glassware": glassware,
        "food_pairing": "",
        "cocktail_use": [],
        "history": "",
        "appellation_law": "",
        "story": "",
        "related": [],
        "availability": "市售",
        "data_source": "OpenFoodFacts",
        "barcode": barcode,
        "image_url": image_url,
        "categories": categories,
    }


def render_value(v):
    """把单个 Python 值渲染为字面量（保证可被 import 且无引号问题）。"""
    if isinstance(v, str):
        # 用 json.dumps 保证转义正确，结果为合法 Python 字符串字面量
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        if not v:
            return "[]"
        inner = ", ".join(render_value(x) for x in v)
        return "[" + inner + "]"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, bool):
        return "True" if v else "False"
    if v is None:
        return "None"
    # 兜底：转字符串
    return json.dumps(str(v), ensure_ascii=False)


def main():
    raw_path = Path("/workspace/Hermes/content-creation/scripts/external/openfoodfacts_raw.json")
    if not raw_path.exists():
        print("原始数据不存在，请先运行 crawl_openfoodfacts.py")
        return
    products = json.loads(raw_path.read_text(encoding="utf-8"))
    print(f"加载 {len(products)} 个产品")

    # 去重（按 name 小写）
    seen = set()
    unique = []
    for p in products:
        name = (p.get("name") or "").strip().lower()
        if not name:
            continue
        if name not in seen:
            seen.add(name)
            unique.append(p)
    print(f"去重后: {len(unique)} 个")

    # 生成条目
    entries = [make_entry(p, i + 1) for i, p in enumerate(unique)]

    # 写入 data_openfoodfacts_supplement.py
    out = Path("/workspace/Hermes/content-creation/scripts/data/data_openfoodfacts_supplement.py")
    lines = [
        '"""OpenFoodFacts 外部数据源补充。',
        "",
        f"共 {len(entries)} 条目，由 convert_openfoodfacts.py 自动生成。",
        '数据来源: OpenFoodFacts (https://world.openfoodfacts.org)',
        '许可证: Open Database License (ODbL)',
        '"""',
        "",
        "ENTRIES = [",
    ]
    for e in entries:
        lines.append("    {")
        for k, v in e.items():
            lines.append(f"        {render_value(k)}: {render_value(v)},")
        lines.append("    },")
    lines.append("]")
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"生成 {len(entries)} 条目 → {out}")

    # 统计
    by_sub = defaultdict(int)
    for e in entries:
        by_sub[e["subcategory"]] += 1
    print(f"子类分布: {dict(by_sub)}")


if __name__ == "__main__":
    main()
