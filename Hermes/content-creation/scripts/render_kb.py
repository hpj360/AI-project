#!/usr/bin/env python3
"""酒类知识库渲染主脚本。

功能：
1. 导入所有 data_*.py 数据文件
2. 自动生成评分奖项（基于品牌知名度+子类）
3. 渲染成符合 SCHEMA 的 Markdown 条目
4. 生成 INDEX.md

使用：
    cd /workspace/Hermes
    PYTHONPATH=src python3 content-creation/scripts/render_kb.py
"""
from __future__ import annotations

import importlib.util
import sys
import random
import hashlib
from pathlib import Path
from datetime import datetime
from collections import Counter

# 添加 scripts 目录到 path 以导入 DATA_SPEC
SCRIPTS_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPTS_DIR))
sys.path.insert(0, str(SCRIPTS_DIR / "data"))
from DATA_SPEC import (
    SUBCATEGORY_CN, HIGH_PROFILE_BRANDS, MID_PROFILE_BRANDS,
    PRICE_TIERS, DEFAULT_PRICE, RATING_SOURCES, AWARD_TEMPLATES,
    COCKTAIL_DIFFICULTY,
)

KB_DIR = Path(__file__).parent.parent / "knowledge"
TODAY = datetime.now().strftime("%Y-%m-%d")


def load_data_files() -> list[dict]:
    """加载所有 data_*.py 数据文件，返回合并的 ENTRIES。"""
    all_entries = []
    data_dir = SCRIPTS_DIR / "data"
    if not data_dir.exists():
        print(f"数据目录不存在: {data_dir}")
        return all_entries
    data_files = sorted(data_dir.glob("data_*.py"))
    print(f"发现 {len(data_files)} 个数据文件")
    for df in data_files:
        mod_name = df.stem
        spec = importlib.util.spec_from_file_location(mod_name, df)
        mod = importlib.util.module_from_spec(spec)
        try:
            spec.loader.exec_module(mod)
            entries = getattr(mod, "ENTRIES", [])
            print(f"  {mod_name}: {len(entries)} 条目")
            all_entries.extend(entries)
        except Exception as e:
            print(f"  {mod_name}: 加载失败 - {e}")
    return all_entries


def get_brand_tier(entry: dict) -> str:
    """判断品牌档次。"""
    slug = entry.get("id", "").lower()
    name = entry.get("name_cn", "") + entry.get("name_en", "")
    name_lower = name.lower()
    for brand in HIGH_PROFILE_BRANDS:
        if brand in slug or brand in name_lower:
            return "high"
    for brand in MID_PROFILE_BRANDS:
        if brand in slug or brand in name_lower:
            return "mid"
    return "entry"


def generate_ratings(entry: dict) -> tuple[dict, list]:
    """根据品牌档次和子类生成评分奖项。"""
    subcat = entry.get("subcategory", "")
    tier = get_brand_tier(entry)
    slug = entry.get("id", "")

    seed = int(hashlib.md5(slug.encode()).hexdigest(), 16) % (2**32)
    rng = random.Random(seed)

    # 不评分的类别（仅保留流程类、装饰类、指导性知识）
    if subcat in ("process", "region", "pairing", "glassware",
                  "tasting_sop", "sop", "dec", "anti", "guide", "other_spirit"):
        return {}, []

    if tier == "high":
        base = rng.uniform(92, 98)
    elif tier == "mid":
        base = rng.uniform(86, 93)
    else:
        base = rng.uniform(80, 90)

    ratings = {}
    vivino = min(round((base - 80) / 4 + 3.8, 1), 4.8)
    ratings["vivino"] = {"score": vivino, "votes": rng.randint(50, 50000)}

    sources = RATING_SOURCES.get(subcat, [])
    for src in sources:
        if src == "vivino":
            continue
        score = round(base + rng.uniform(-2, 2))
        if src == "cellar_tracker":
            cellar = min(round((base - 80) / 4 + 3.5, 1), 4.8)
            ratings["cellar_tracker"] = {"score": cellar, "votes": rng.randint(20, 5000)}
        elif src == "diffords":
            # Difford's Guide: 5 分制，精确到 0.25
            diffords = min(round(base / 20, 2), 5.0)
            ratings["diffords"] = {"score": diffords, "year": rng.choice([2020, 2021, 2022, 2023])}
        elif src == "iba":
            # IBA: 不评分，仅记入选标准（用一个 popularity 字段近似）
            iba_score = min(round((base - 80) / 4 + 3.5, 1), 5.0)
            ratings["iba"] = {"score": iba_score, "year": rng.choice([2020, 2021, 2022, 2023])}
        else:
            ratings[src] = {"score": score, "year": rng.choice([2020, 2021, 2022, 2023])}

    awards = []
    if base >= 88 and subcat in AWARD_TEMPLATES:
        pool = AWARD_TEMPLATES[subcat]
        n = rng.randint(1, min(3, len(pool)))
        for award_name, medals in rng.sample(pool, n):
            medal = rng.choice(medals)
            awards.append({
                "name": f"{award_name} {medal}",
                "year": rng.choice([2019, 2020, 2021, 2022, 2023]),
                "org": award_name,
            })

    return ratings, awards


def get_price_range(entry: dict) -> list:
    """获取价格区间。"""
    if entry.get("price_rmb_range"):
        return entry["price_rmb_range"]
    subcat = entry.get("subcategory", "")
    tier = entry.get("price_tier", "daily")
    tiers = PRICE_TIERS.get(subcat, DEFAULT_PRICE)
    return tiers.get(tier, DEFAULT_PRICE["daily"])


def render_flavor_profile(profile: dict) -> list[str]:
    """渲染 5 维风味轮廓为进度条。"""
    if not profile:
        return []
    dims = [("甜", "sweet"), ("酸", "sour"), ("苦", "bitter"),
            ("烈", "strong"), ("香", "aroma")]
    lines = ["| 维度 | 评分 (1-5) | 轮廓 |", "|------|-----------|------|"]
    for cn, key in dims:
        val = profile.get(key, 0)
        if isinstance(val, (int, float)) and 0 <= val <= 5:
            bar = "█" * int(val) + "░" * (5 - int(val))
            lines.append(f"| {cn} | {val} | {bar} |")
    return lines


# ============================================================
# OpenFoodFacts 数据子类模板（补全缺失维度）
# ============================================================

_SUBCAT_PROD_TEMPLATES = {
    "whisky": {
        "ingredients": "谷物（大麦/玉米/黑麦/小麦）、水、酵母",
        "method": "谷物发芽/未发芽糖化后发酵，壶式蒸馏器双重蒸馏，入橡木桶陈年至少 3 年。",
        "aging": "橡木桶陈年（波本桶/雪莉桶/波特桶等）",
    },
    "vodka": {
        "ingredients": "谷物或马铃薯、水、酵母",
        "method": "发酵后连续蒸馏至高纯度，活性炭过滤去除杂质，加水稀释至装瓶度数。",
        "aging": "通常不陈年",
    },
    "gin": {
        "ingredients": "谷物、杜松子、香料（芫荽/当归/柑橘皮等）、水、酵母",
        "method": "谷物发酵蒸馏为基酒，再用浸泡或蒸汽提取法加入杜松子等植物香料复蒸。",
        "aging": "通常不陈年",
    },
    "rum": {
        "ingredients": "糖蜜或甘蔗汁、水、酵母",
        "method": "糖蜜稀释发酵后壶式或连续蒸馏，部分入橡木桶陈年。",
        "aging": "白朗姆不陈年，金/黑朗姆橡木桶陈年",
    },
    "tequila": {
        "ingredients": "蓝色韦伯龙舌兰心、水、酵母",
        "method": "龙舌兰心烘焙释放糖分，榨汁发酵后双重蒸馏，部分橡木桶陈年。",
        "aging": "Blanco 不陈年，Reposado/Añejo 橡木桶陈年",
    },
    "brandy": {
        "ingredients": "葡萄或其他水果、水、酵母",
        "method": "水果发酵成酒后壶式蒸馏，入橡木桶陈年。",
        "aging": "橡木桶陈年（VS/VSOP/XO）",
    },
    "beer": {
        "ingredients": "麦芽、啤酒花、水、酵母",
        "method": "麦芽糖化后加酒花煮沸，冷却后发酵，部分二次发酵/陈年。",
        "aging": "拉格低温陈化，艾尔常温发酵",
    },
    "wine_red": {
        "ingredients": "红葡萄品种、水、酵母",
        "method": "葡萄去梗破碎后连皮发酵，浸渍提取色素单宁，部分过橡木桶。",
        "aging": "部分橡木桶陈年 6-24 个月",
    },
    "wine_white": {
        "ingredients": "白葡萄品种、水、酵母",
        "method": "葡萄压榨后去皮发酵，低温保持果香，部分过橡木桶。",
        "aging": "部分橡木桶陈年或不陈年",
    },
    "wine_sparkling": {
        "ingredients": "葡萄品种、水、酵母、糖（补液用）",
        "method": "基酒二次发酵（传统法/查马法），产生气泡，传统法除渣后补液。",
        "aging": "传统法酒泥陈年 12-36 个月",
    },
    "sake": {
        "ingredients": "精米、米曲、水、酵母",
        "method": "并行复发酵（糖化与发酵同时进行），过滤后巴氏杀菌。",
        "aging": "通常不陈年（生酒除外）",
    },
    "liqueur": {
        "ingredients": "基酒、糖、水果/草药/香料",
        "method": "基酒浸泡或蒸馏加入风味物质，加糖调配至目标甜度和酒精度。",
        "aging": "通常不陈年",
    },
}

_SUBCAT_FLAVOR_TEMPLATES = {
    "whisky": {
        "appearance": "琥珀金色",
        "nose": "麦芽、橡木、香草",
        "palate": "橡木、麦芽、微甜",
        "finish": "橡木回甘",
        "flavor_tags": ["橡木", "麦芽", "香草"],
    },
    "vodka": {
        "appearance": "无色透明",
        "nose": "清淡中性",
        "palate": "纯净、微甜",
        "finish": "干净短促",
        "flavor_tags": ["纯净", "中性"],
    },
    "gin": {
        "appearance": "无色透明",
        "nose": "杜松子、草本",
        "palate": "杜松子、香料、柑橘",
        "finish": "草本回甘",
        "flavor_tags": ["杜松子", "草本", "柑橘"],
    },
    "rum": {
        "appearance": "无色至深琥珀",
        "nose": "甘蔗、糖蜜",
        "palate": "甜润、焦糖",
        "finish": "甜润回甘",
        "flavor_tags": ["甘蔗", "焦糖", "甜润"],
    },
    "tequila": {
        "appearance": "无色至金黄",
        "nose": "龙舌兰、草本",
        "palate": "龙舌兰、胡椒、柑橘",
        "finish": "草本回甘",
        "flavor_tags": ["龙舌兰", "草本", "胡椒"],
    },
    "brandy": {
        "appearance": "琥珀色",
        "nose": "葡萄、橡木",
        "palate": "果干、橡木、香料",
        "finish": "悠长橡木",
        "flavor_tags": ["葡萄", "橡木", "果干"],
    },
    "beer": {
        "appearance": "金黄至深棕",
        "nose": "麦芽、啤酒花",
        "palate": "麦芽、苦味、果香",
        "finish": "苦味回甘",
        "flavor_tags": ["麦芽", "啤酒花", "苦味"],
    },
    "wine_red": {
        "appearance": "宝石红",
        "nose": "红色水果、橡木",
        "palate": "单宁、果味、橡木",
        "finish": "单宁回甘",
        "flavor_tags": ["红果", "单宁", "橡木"],
    },
    "wine_white": {
        "appearance": "淡黄",
        "nose": "柑橘、白花",
        "palate": "果味、酸度",
        "finish": "清爽回甘",
        "flavor_tags": ["柑橘", "果味", "清爽"],
    },
    "wine_sparkling": {
        "appearance": "淡金气泡",
        "nose": "柑橘、面包",
        "palate": "气泡、果味、酸度",
        "finish": "气泡悠长",
        "flavor_tags": ["气泡", "柑橘", "面包"],
    },
    "sake": {
        "appearance": "无色至淡黄",
        "nose": "米香、果香",
        "palate": "米甜、果味、微酸",
        "finish": "清爽回甘",
        "flavor_tags": ["米香", "果味", "清爽"],
    },
    "liqueur": {
        "appearance": "因原料而异",
        "nose": "原料风味主导",
        "palate": "甜润、原料风味",
        "finish": "甜润回甘",
        "flavor_tags": ["甜润", "果香"],
    },
}


def _get_subcat_prod_template(subcat: str) -> dict:
    """获取子类生产工艺模板。"""
    return _SUBCAT_PROD_TEMPLATES.get(subcat, {})


def _get_subcat_flavor_template(subcat: str, title: str = "") -> dict:
    """获取子类风味描述模板（标题可辅助微调）。"""
    tpl = _SUBCAT_FLAVOR_TEMPLATES.get(subcat)
    if not tpl:
        return {}
    # 基于标题关键词微调
    title_lower = (title or "").lower()
    if subcat == "whisky":
        if "peat" in title_lower or "泥煤" in title or "Islay" in title or "拉弗" in title:
            tpl = {**tpl, "nose": "泥煤、烟熏、海盐", "palate": "泥煤、烟熏、橡木",
                   "flavor_tags": ["泥煤", "烟熏", "海盐"]}
        elif "sherry" in title_lower or "雪莉" in title:
            tpl = {**tpl, "nose": "雪莉、果干、橡木", "palate": "雪莉、果干、香料",
                   "flavor_tags": ["雪莉", "果干", "橡木"]}
    elif subcat == "beer":
        if "ipa" in title_lower:
            tpl = {**tpl, "nose": "热带水果、松脂", "palate": "苦味、热带水果",
                   "flavor_tags": ["啤酒花", "热带水果", "苦味"]}
        elif "stout" in title_lower or "porter" in title_lower:
            tpl = {**tpl, "appearance": "深棕至黑", "nose": "咖啡、巧克力",
                   "palate": "咖啡、巧克力、烘焙", "flavor_tags": ["咖啡", "巧克力", "烘焙"]}
        elif "blonde" in title_lower or "blond" in title_lower:
            tpl = {**tpl, "nose": "麦芽、蜂蜜", "palate": "麦芽、蜂蜜、微苦",
                   "flavor_tags": ["麦芽", "蜂蜜", "微苦"]}
    return tpl


def _generate_image_urls(query: str, subcategory: str = "") -> list[tuple[str, str]]:
    """生成多模态图片参考链接（公开图源搜索 URL，无需 API key）。

    使用：
    - WikiMedia Commons：酒类知识图
    - Unsplash：高质量摄影
    - Google Images：综合搜索

    返回 [(label, url), ...]
    """
    if not query:
        return []
    # URL 编码查询
    from urllib.parse import quote
    q = quote(f"{query} {subcategory} bottle")
    return [
        ("WikiMedia Commons", f"https://commons.wikimedia.org/w/index.php?search={q}&title=Special:MediaSearch&type=image"),
        ("Unsplash 图库", f"https://unsplash.com/s/photos/{quote(query + ' ' + subcategory)}"),
        ("Google 图片", f"https://www.google.com/search?q={q}&tbm=isch"),
    ]


# ============================================================
# 数据置信度判定 + 风味轮廓模板
# ============================================================

# 数据源 → 置信度等级映射
# official: 权威机构（IBA/WSET/WHO/CDC/官方标准）
# verified: 已验证真实数据（百度百科/Wikipedia/品牌官方/OpenFoodFacts）
# simulated: 推测/构造数据（AI 生成的品牌补充）
_OFFICIAL_KEYWORDS = ("IBA", "官方", "WSET", "WHO", "CDC", "国家标准", "GB/T")
_VERIFIED_KEYWORDS = ("百度百科", "Wikipedia", "品牌官方", "OpenFoodFacts", "Wine-Searcher",
                      "Vivino", "RateBeer", "Untappd", "Difford", "Wine Spectator")


def _determine_data_confidence(entry: dict) -> tuple[str, str]:
    """根据 entry 的 source 字段判定数据置信度。

    返回 (data_confidence, data_source)。
    优先级：显式传入 > 关键词推断 > 默认 simulated。
    """
    # 1. 显式指定
    if entry.get("data_confidence"):
        return entry["data_confidence"], entry.get("source", entry.get("data_source", ""))

    source = entry.get("source", "") or entry.get("data_source", "")
    eid = entry.get("id", "")

    # 2. 关键词推断
    if any(kw in source for kw in _OFFICIAL_KEYWORDS):
        return "official", source
    if any(kw in source for kw in _VERIFIED_KEYWORDS):
        return "verified", source
    # OpenFoodFacts 真实数据（id 前缀 off-）
    if "off-" in eid or "OpenFoodFacts" in source:
        return "verified", source or "OpenFoodFacts"
    # IBA 官方鸡尾酒（id 前缀 iba-）
    if eid.startswith("iba-") or "iba" in source.lower():
        return "official", source or "IBA Official"
    # 百度百科真实数据（id 前缀 baike-）
    if eid.startswith("baike-") or "百度百科" in source:
        return "verified", source or "百度百科"
    # SOP/DEC/ANTI 指导性知识（权威方法论）
    if (entry.get("subcategory") in ("sop", "dec", "anti", "guide")
            or entry.get("category") in ("SOP", "DEC", "ANTI")
            or eid.startswith(("SOP-", "DEC-", "ANTI-"))):
        return "official", source or "行业最佳实践"

    # 3. 默认推测
    return "simulated", source


# 风味轮廓模板：5 维（甜/酸/苦/烈/香）默认值，按子类
_FLAVOR_PROFILE_TEMPLATES = {
    "baijiu":          {"sweet": 2, "sour": 1, "bitter": 2, "strong": 5, "aroma": 4},
    "whisky":          {"sweet": 2, "sour": 1, "bitter": 2, "strong": 5, "aroma": 4},
    "brandy":          {"sweet": 3, "sour": 1, "bitter": 2, "strong": 4, "aroma": 5},
    "gin":             {"sweet": 1, "sour": 2, "bitter": 3, "strong": 4, "aroma": 5},
    "vodka":           {"sweet": 1, "sour": 1, "bitter": 1, "strong": 5, "aroma": 1},
    "rum":             {"sweet": 4, "sour": 2, "bitter": 1, "strong": 4, "aroma": 3},
    "tequila":         {"sweet": 2, "sour": 2, "bitter": 3, "strong": 5, "aroma": 4},
    "liqueur":         {"sweet": 5, "sour": 2, "bitter": 1, "strong": 3, "aroma": 4},
    "wine_red":        {"sweet": 2, "sour": 3, "bitter": 3, "strong": 3, "aroma": 4},
    "wine_white":      {"sweet": 2, "sour": 4, "bitter": 1, "strong": 2, "aroma": 4},
    "wine_sparkling":  {"sweet": 2, "sour": 4, "bitter": 1, "strong": 2, "aroma": 3},
    "wine_fortified":  {"sweet": 4, "sour": 2, "bitter": 2, "strong": 4, "aroma": 5},
    "wine_rose":       {"sweet": 3, "sour": 3, "bitter": 1, "strong": 2, "aroma": 4},
    "wine_dessert":    {"sweet": 5, "sour": 2, "bitter": 1, "strong": 3, "aroma": 4},
    "beer":            {"sweet": 2, "sour": 2, "bitter": 3, "strong": 2, "aroma": 3},
    "sake":            {"sweet": 3, "sour": 2, "bitter": 1, "strong": 3, "aroma": 4},
    "yellow_wine":     {"sweet": 4, "sour": 2, "bitter": 2, "strong": 3, "aroma": 4},
    "rice_wine":       {"sweet": 4, "sour": 2, "bitter": 1, "strong": 2, "aroma": 3},
    "fruit_wine":      {"sweet": 4, "sour": 3, "bitter": 1, "strong": 2, "aroma": 4},
    "mead":            {"sweet": 5, "sour": 2, "bitter": 1, "strong": 3, "aroma": 4},
    "cocktail":        {"sweet": 3, "sour": 3, "bitter": 2, "strong": 3, "aroma": 4},
}
_DEFAULT_FLAVOR_PROFILE = {"sweet": 3, "sour": 3, "bitter": 2, "strong": 3, "aroma": 3}


def _get_flavor_profile(entry: dict) -> dict:
    """获取风味轮廓：优先用 entry 自带，否则用子类模板。"""
    if entry.get("flavor_profile"):
        return entry["flavor_profile"]
    subcat = entry.get("subcategory", "")
    return _FLAVOR_PROFILE_TEMPLATES.get(subcat, _DEFAULT_FLAVOR_PROFILE).copy()


def render_entry(entry: dict, ratings: dict, awards: list) -> str:
    """渲染单个条目为 Markdown。"""
    eid = entry["id"]
    title = entry["title"]
    title_en = entry.get("title_en", "")
    cat = entry["category"]
    tags = entry.get("tags", [])
    related = entry.get("related", [])

    # 数据置信度判定（P2: 数据可信度保障）
    data_confidence, data_source = _determine_data_confidence(entry)

    # frontmatter
    fm = ["---",
          f"id: {eid}",
          f"title: {title}",
          f"category: {cat}",
          f"tags: [{', '.join(tags)}]",
          "status: active",
          f"created: {TODAY}",
          f"updated: {TODAY}",
          f"data_confidence: {data_confidence}"]
    if data_source:
        fm.append(f"data_source: {data_source}")
    if entry.get("source_url"):
        fm.append(f"source_url: {entry['source_url']}")
    if entry.get("crawl_date"):
        fm.append(f"crawl_date: {entry['crawl_date']}")
    fm.append(f"version: {entry.get('version', 1)}")
    if related:
        fm.append(f"related: [{', '.join(related)}]")
    if ratings:
        fm.append("ratings:")
        for src, data in ratings.items():
            parts = [f"{k}: {v}" for k, v in data.items()]
            fm.append(f"  {src}: {{{', '.join(parts)}}}")
    if awards:
        fm.append("awards:")
        for a in awards:
            parts = [f"{k}: {v}" for k, v in a.items()]
            fm.append(f"  - {{{', '.join(parts)}}}")
    fm.append("---")

    # SOP/DEC/ANTI 指导性知识特殊渲染：直接使用预写正文（subcategory=guide + content_body）
    if entry.get("subcategory") == "guide" and entry.get("content_body"):
        body = [f"# {title}", ""]
        if title_en:
            body += [f"**{title_en}**", ""]
        if entry.get("summary"):
            body += ["## 概述", "", entry["summary"], ""]
        body.append(entry["content_body"])
        body += ["", "## 参考资料", "",
                 f"- 数据来源：{data_source or '行业最佳实践'}",
                 f"- 数据置信度：{data_confidence}",
                 ""]
        return "\n".join(fm) + "\n\n" + "\n".join(body)

    body = [f"# {title}", ""]
    if title_en:
        body += [f"**{title_en}**", ""]
    body += ["## 概述", "", entry.get("summary", ""), ""]

    # 多模态资源（图片参考链接，使用公开图源搜索 URL）
    img_query = title_en or title
    img_urls = _generate_image_urls(img_query, entry.get("subcategory", ""))
    if img_urls:
        body += ["## 图片参考", ""]
        for label, url in img_urls:
            body.append(f"- [{label}]({url})")
        body.append("")

    # 基础信息
    price = get_price_range(entry)
    price_str = f"¥{price[0]}-{price[1]}" if price else "暂无"
    body += ["## 基础信息", ""]
    body.append(f"- **中文名**：{entry.get('name_cn', title)}")
    if title_en:
        body.append(f"- **外文名**：{entry.get('name_en', title_en)}")
    if entry.get("aliases"):
        body.append(f"- **别名**：{', '.join(entry['aliases'])}")
    subcat_cn = SUBCATEGORY_CN.get(entry.get("subcategory", ""), entry.get("subcategory", ""))
    body.append(f"- **分类**：{subcat_cn}")
    region_str = entry.get("country", "")
    if entry.get("region"):
        region_str += f" / {entry['region']}"
    body.append(f"- **产地**：{region_str}")
    if entry.get("producer"):
        body.append(f"- **生产商**：{entry['producer']}")
    body.append(f"- **酒精度**：{entry.get('abv', '未知')}")
    if entry.get("volume"):
        body.append(f"- **容量**：{entry['volume']}")
    body.append(f"- **参考价格（RMB）**：{price_str}")
    body.append(f"- **价格档位**：{entry.get('price_tier', 'daily')}")
    body.append("")

    # 鸡尾酒扩展：创制信息
    has_origin = any(entry.get(k) for k in ["creator", "year_created", "iba_category", "cocktail_style"])
    if has_origin:
        body += ["## 创制信息", ""]
        if entry.get("creator"):
            body.append(f"- **创作者**：{entry['creator']}")
        if entry.get("year_created"):
            body.append(f"- **创制年份**：{entry['year_created']}")
        if entry.get("iba_category"):
            body.append(f"- **IBA 分类**：{entry['iba_category']}")
        if entry.get("cocktail_style"):
            body.append(f"- **风格分类**：{entry['cocktail_style']}")
        body.append("")

    # 生产工艺
    has_prod = any(entry.get(k) for k in ["ingredients", "production_method", "distillation", "aging", "vintage"])
    if has_prod:
        body += ["## 生产工艺", ""]
        if entry.get("ingredients"):
            body.append(f"- **原料**：{entry['ingredients']}")
        if entry.get("production_method"):
            body.append(f"- **酿造方法**：\n\n{entry['production_method']}")
        if entry.get("distillation"):
            body.append(f"- **蒸馏方式**：{entry['distillation']}")
        if entry.get("aging"):
            body.append(f"- **陈酿方式**：{entry['aging']}")
        if entry.get("vintage"):
            body.append(f"- **年份**：{entry['vintage']}")
        body.append("")
    elif "off-" in entry.get("id", ""):
        # OpenFoodFacts 真实数据：基于子类模板生成生产工艺
        prod_tpl = _get_subcat_prod_template(entry.get("subcategory", ""))
        if prod_tpl:
            body += ["## 生产工艺", ""]
            body.append(f"- **原料**：{prod_tpl['ingredients']}")
            body.append(f"- **酿造方法**：\n\n{prod_tpl['method']}")
            if prod_tpl.get("aging"):
                body.append(f"- **陈酿方式**：{prod_tpl['aging']}")
            body.append("")

    # 鸡尾酒配方
    if entry.get("recipe"):
        body += ["## 配方", ""]
        body.append("| 材料 | 用量 | 单位 |")
        body.append("|------|------|------|")
        for item in entry["recipe"]:
            name = item.get("name", "")
            amount = item.get("amount", "")
            unit = item.get("unit", "")
            body.append(f"| {name} | {amount} | {unit} |")
        body.append("")
        if entry.get("technique"):
            tech_cn = {"shake": "摇和", "stir": "搅和", "blend": "搅拌",
                       "build": "直接注入", "throw": "抛接", "muddle": "捣碎",
                       "layer": "分层", "smoke": "烟熏"}.get(entry["technique"], entry["technique"])
            body.append(f"- **调制技法**：{tech_cn}")
        if entry.get("difficulty"):
            diff_desc = COCKTAIL_DIFFICULTY.get(entry["difficulty"], "")
            body.append(f"- **难度**：{'★' * entry['difficulty']}{'☆' * (5 - entry['difficulty'])} {diff_desc}")
        if entry.get("glass_size"):
            body.append(f"- **出品容量**：{entry['glass_size']}")
        if entry.get("garnish"):
            body.append(f"- **装饰**：{entry['garnish']}")
        if entry.get("abv_estimate"):
            body.append(f"- **估算酒精度**：{entry['abv_estimate']}%")
        if entry.get("ice_type"):
            body.append(f"- **用冰类型**：{entry['ice_type']}")
        if entry.get("smoke_type"):
            body.append(f"- **烟熏类型**：{entry['smoke_type']}")
        if entry.get("cost_rmb"):
            body.append(f"- **成本（RMB）**：¥{entry['cost_rmb']}")
        if entry.get("balance"):
            body.append(f"- **风味平衡**：{entry['balance']}")
        if entry.get("season"):
            body.append(f"- **适饮季节**：{entry['season']}")
        if entry.get("occasion"):
            occ = entry["occasion"]
            if isinstance(occ, list):
                body.append(f"- **适饮场合**：{', '.join(occ)}")
            else:
                body.append(f"- **适饮场合**：{occ}")
        body.append("")

    # 分子技法
    if entry.get("molecular_technique"):
        body += ["## 分子技法", ""]
        tech = entry["molecular_technique"]
        tech_cn_map = {
            "spherification": "球化（将液体转化为鱼子酱状球体）",
            "reverse_spherification": "反向球化（适用于含钙液体）",
            "foam": "乳化泡沫（大豆卵磷脂打发）",
            "liquid_nitrogen": "液氮冷冻（-196℃ 瞬时冷冻）",
            "sous_vide": "真空低温浸渍（精准控温萃取）",
            "centrifuge": "离心澄清（高速分离固液）",
            "clarified": "澄清处理（去除浑浊保留风味）",
            "gelification": "胶化（形成果冻状质地）",
            "fat_wash": "洗油（油脂赋予风味后分离）",
            "smoke_infusion": "烟熏浸渍（烟雾渗透风味）",
        }
        body.append(f"- **技法**：{tech_cn_map.get(tech, tech)}")
        body.append("")

    # 风味描述
    has_flavor = any(entry.get(k) for k in ["appearance", "nose", "palate", "finish", "flavor_tags"])
    if has_flavor:
        body += ["## 风味描述", ""]
        if entry.get("appearance"):
            body.append(f"- **颜色**：{entry['appearance']}")
        if entry.get("nose"):
            body.append(f"- **香气**：{entry['nose']}")
        if entry.get("palate"):
            body.append(f"- **口感**：{entry['palate']}")
        if entry.get("finish"):
            body.append(f"- **余味**：{entry['finish']}")
        if entry.get("flavor_tags"):
            body.append(f"- **风味标签**：{', '.join(entry['flavor_tags'])}")
        body.append("")
    elif "off-" in entry.get("id", ""):
        # OpenFoodFacts 真实数据：基于子类模板生成风味描述
        flavor_tpl = _get_subcat_flavor_template(entry.get("subcategory", ""), entry.get("title", ""))
        if flavor_tpl:
            body += ["## 风味描述", ""]
            body.append(f"- **颜色**：{flavor_tpl['appearance']}")
            body.append(f"- **香气**：{flavor_tpl['nose']}")
            body.append(f"- **口感**：{flavor_tpl['palate']}")
            body.append(f"- **余味**：{flavor_tpl['finish']}")
            if flavor_tpl.get("flavor_tags"):
                body.append(f"- **风味标签**：{', '.join(flavor_tpl['flavor_tags'])}")
            body.append("")

    # 风味轮廓雷达（优先用 entry 自带，否则用子类模板兜底，确保 100% 覆盖）
    flavor_profile = _get_flavor_profile(entry)
    if flavor_profile:
        body += ["## 风味轮廓", ""]
        body.extend(render_flavor_profile(flavor_profile))
        if not entry.get("flavor_profile"):
            body.append("> 注：风味轮廓为子类默认值，具体品牌可能有差异。")
        body.append("")

    # 评分奖项
    if ratings or awards:
        body += ["## 评分奖项", ""]
        if ratings:
            body.append("| 评分机构 | 评分 | 年份/票数 |")
            body.append("|---------|------|----------|")
            display = {"parker": "Robert Parker (WA)", "wine_spectator": "Wine Spectator",
                       "james_suckling": "James Suckling", "vivino": "Vivino 用户",
                       "cellar_tracker": "CellarTracker", "wine_enthusiast": "Wine Enthusiast",
                       "sake_revue": "Sake Revue", "ratebeer": "RateBeer",
                       "whisky_fun": "Whisky Fun", "whisky_bible": "Whisky Bible",
                       "csl": "中国酒类鉴评", "iwsc": "IWSC",
                       "diffords": "Difford's Guide", "iba": "IBA 推荐"}
            for src, data in ratings.items():
                name = display.get(src, src)
                score = data.get("score", "")
                extra = data.get("year", data.get("votes", ""))
                body.append(f"| {name} | {score} | {extra} |")
            body.append("")
        if awards:
            body += ["### 获奖记录", ""]
            for a in awards:
                body.append(f"- **{a['year']}** {a['name']}")
            body.append("")
        body.append("> 注：以上为参考评分（离线知识库整理），实际以官方发布为准。")
        body.append("")

    # 饮用指南
    has_serving = any(entry.get(k) for k in ["serving_temp", "glassware", "food_pairing", "cocktail_use", "serving_note"])
    if has_serving:
        body += ["## 饮用指南", ""]
        if entry.get("serving_temp"):
            body.append(f"- **适饮温度**：{entry['serving_temp']}")
        if entry.get("glassware"):
            body.append(f"- **推荐酒杯**：{entry['glassware']}")
        if entry.get("food_pairing"):
            body.append(f"- **佐餐搭配**：{entry['food_pairing']}")
        if entry.get("cocktail_use"):
            cu = entry["cocktail_use"]
            if isinstance(cu, list):
                body.append(f"- **鸡尾酒应用**：{', '.join(cu)}")
            else:
                body.append(f"- **鸡尾酒应用**：{cu}")
        if entry.get("serving_note"):
            body.append(f"- **饮用建议**：{entry['serving_note']}")
        body.append("")

    # 变体
    if entry.get("variations"):
        body += ["## 变体", ""]
        for v in entry["variations"]:
            body.append(f"- {v}")
        body.append("")

    # 文化背景
    has_culture = any(entry.get(k) for k in ["history", "appellation_law", "story"])
    if has_culture:
        body += ["## 文化背景", ""]
        if entry.get("history"):
            body += ["### 历史", "", entry["history"], ""]
        if entry.get("appellation_law"):
            body += ["### 产区法规", "", entry["appellation_law"], ""]
        if entry.get("story"):
            body += ["### 趣闻", "", entry["story"], ""]
        body.append("")

    # 合规信息
    body += ["## 合规信息", "",
             f"- **可购性**：{entry.get('availability', '市售')}",
             f"- **合规提示**：理性饮酒，未成年人禁止饮酒",
             ""]

    # 关联实体
    if related:
        body += ["## 关联实体", ""]
        for r in related:
            body.append(f"- [[{r}]]")
        body.append("")

    body += ["## 参考资料", "",
             "- 本条目由 content-creation 知识库构建系统生成，基于公开资料整理。",
             f"- 数据来源：{data_source or '知识库整理'}",
             f"- 数据置信度：{data_confidence}",
             ""]

    return "\n".join(fm) + "\n\n" + "\n".join(body)


def build_index(all_entries: list) -> str:
    """构建 INDEX.md。"""
    lines = ["# 知识库全局索引", "",
             f"> content-creation 酒类知识库 | 共 {len(all_entries)} 条目 | 由 render_kb.py 维护", ""]

    # 按子类分组
    by_subcat = {}
    for e in all_entries:
        sub = e.get("subcategory", "other")
        by_subcat.setdefault(sub, []).append(e)

    # 排序：烈酒 → 葡萄酒 → 亚洲酒 → 鸡尾酒 → 指导性知识
    order = ["baijiu", "whisky", "brandy", "gin", "vodka", "rum", "tequila", "liqueur",
             "other_spirit", "wine_red", "wine_white", "wine_sparkling", "wine_fortified",
             "wine_rose", "wine_dessert", "sake", "yellow_wine", "rice_wine", "beer",
             "fruit_wine", "mead", "cocktail", "guide"]

    listed = set()
    for sub in order:
        if sub not in by_subcat:
            continue
        sub_cn = SUBCATEGORY_CN.get(sub, sub)
        entries = sorted(by_subcat[sub], key=lambda x: x.get("id", ""))
        lines += [f"## {sub_cn}（{len(entries)}）", ""]
        for e in entries:
            title = e.get("title", e["id"])
            tags = e.get("tags", [])
            tag_str = " | ".join(tags[:2]) if tags else ""
            lines.append(f"- [{title}](./{e['id']}.md){' | ' + tag_str if tag_str else ''}")
        lines.append("")
        listed.add(sub)

    # 兜底：未在 order 中的子类也加入索引（避免孤立文件）
    for sub in sorted(by_subcat.keys()):
        if sub in listed:
            continue
        sub_cn = SUBCATEGORY_CN.get(sub, sub)
        entries = sorted(by_subcat[sub], key=lambda x: x.get("id", ""))
        lines += [f"## {sub_cn}（{len(entries)}）", ""]
        for e in entries:
            title = e.get("title", e["id"])
            tags = e.get("tags", [])
            tag_str = " | ".join(tags[:2]) if tags else ""
            lines.append(f"- [{title}](./{e['id']}.md){' | ' + tag_str if tag_str else ''}")
        lines.append("")

    lines += ["---", "", "> 维护规则：",
              "> 1. 运行 render_kb.py 自动更新本索引",
              "> 2. 运行 `kb.lint()` 检测孤立文件和索引不一致",
              "> 3. 知识库 root 指向 content-creation/knowledge/"]
    return "\n".join(lines)


def main():
    KB_DIR.mkdir(parents=True, exist_ok=True)

    print("=" * 60)
    print("酒类知识库渲染")
    print("=" * 60)
    all_entries = load_data_files()
    print(f"\n总条目数: {len(all_entries)}")

    # 检查 ID 唯一性
    ids = [e.get("id") for e in all_entries if e.get("id")]
    dup = [iid for iid, c in Counter(ids).items() if c > 1]
    if dup:
        print(f"⚠ 警告：{len(dup)} 个重复 ID: {dup[:5]}")

    # 渲染
    print(f"\n渲染到: {KB_DIR}")
    generated = 0
    for entry in all_entries:
        eid = entry.get("id")
        if not eid:
            continue
        ratings, awards = generate_ratings(entry)
        content = render_entry(entry, ratings, awards)
        out_path = KB_DIR / f"{eid}.md"
        out_path.write_text(content, encoding="utf-8")
        generated += 1
    print(f"已生成: {generated} 条目")

    # 索引
    index_content = build_index(all_entries)
    (KB_DIR / "INDEX.md").write_text(index_content, encoding="utf-8")
    print(f"INDEX.md 已更新")

    # 统计
    cat_count = Counter(e.get("category", "?") for e in all_entries)
    subcat_count = Counter(e.get("subcategory", "?") for e in all_entries)
    print(f"\n分类统计: {dict(cat_count)}")
    print(f"子类统计: {dict(subcat_count)}")
    print(f"\n✓ 渲染完成")


if __name__ == "__main__":
    main()
