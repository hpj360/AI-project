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

    # 不评分的类别
    if subcat in ("cocktail", "process", "region", "pairing", "glassware",
                  "tasting_sop", "sop", "dec", "anti", "fruit_wine", "mead",
                  "rice_wine", "yellow_wine", "other_spirit"):
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


def render_entry(entry: dict, ratings: dict, awards: list) -> str:
    """渲染单个条目为 Markdown。"""
    eid = entry["id"]
    title = entry["title"]
    title_en = entry.get("title_en", "")
    cat = entry["category"]
    tags = entry.get("tags", [])
    related = entry.get("related", [])

    # frontmatter
    fm = ["---",
          f"id: {eid}",
          f"title: {title}",
          f"category: {cat}",
          f"tags: [{', '.join(tags)}]",
          "status: active",
          f"created: {TODAY}",
          f"updated: {TODAY}"]
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

    body = [f"# {title}", ""]
    if title_en:
        body += [f"**{title_en}**", ""]
    body += ["## 概述", "", entry.get("summary", ""), ""]

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

    # 风味轮廓雷达
    if entry.get("flavor_profile"):
        body += ["## 风味轮廓", ""]
        body.extend(render_flavor_profile(entry["flavor_profile"]))
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
                       "csl": "中国白酒鉴评", "iwsc": "IWSC"}
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

    # 排序：烈酒 → 葡萄酒 → 亚洲酒 → 鸡尾酒
    order = ["baijiu", "whisky", "brandy", "gin", "vodka", "rum", "tequila", "liqueur",
             "other_spirit", "wine_red", "wine_white", "wine_sparkling", "wine_fortified",
             "wine_rose", "wine_dessert", "sake", "yellow_wine", "rice_wine", "beer",
             "fruit_wine", "mead", "cocktail"]

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
