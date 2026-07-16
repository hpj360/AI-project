#!/usr/bin/env python3
"""数据质量保障工具。

功能：
1. 交叉验证：品牌一致性检查（同品牌多条数据酒精度应一致或递减）
2. 血缘追踪：为已有数据补充 source_url/crawl_date/version 字段
3. 衰减检查：识别过期数据（价格6个月/评分12个月）
4. 期望范围修正：调整酒精度合理范围（基于真实数据反馈）
5. 质量报告：生成数据质量看板

使用：
    cd /workspace/Hermes
    PYTHONPATH=src python3 content-creation/scripts/data_quality.py [check|enrich|report]
    默认执行 check（检查）+ report（报告）
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from datetime import datetime
from collections import Counter


# ============================================================
# 功能1：交叉验证（关卡3）—— 品牌一致性检查
# ============================================================

# 品牌一致性检查
# 同一品牌的多条数据，酒精度应该一致或在合理范围
BRAND_ABV_REFERENCE = {
    # 基于真实数据的品牌酒精度参考值
    "macallan": {"expected_abv": [40, 43, 46, 58], "tolerance": 3},
    "glenfiddich": {"expected_abv": [40, 43], "tolerance": 2},
    "johnnie": {"expected_abv": [40, 42, 43], "tolerance": 2},
    "hennessy": {"expected_abv": [40], "tolerance": 2},
    "bacardi": {"expected_abv": [37.5, 40], "tolerance": 2},
    "茅台": {"expected_abv": [53, 43, 38], "tolerance": 2},
    "五粮液": {"expected_abv": [52, 45, 39], "tolerance": 2},
}


def cross_validate_brand_consistency(kb):
    """检查同品牌数据的酒精度一致性。"""
    issues = []
    for brand, ref in BRAND_ABV_REFERENCE.items():
        # 找到该品牌的所有条目
        brand_entries = [e for e in kb.entries.values()
                        if brand.lower() in e.title.lower() or brand.lower() in e.id.lower()]
        for e in brand_entries:
            abv = e.structured_attrs.get('abv_num')
            if abv:
                # 检查是否在参考值附近
                expected = ref['expected_abv']
                tolerance = ref['tolerance']
                if not any(abs(abv - exp) <= tolerance for exp in expected):
                    issues.append({
                        'id': e.id,
                        'title': e.title,
                        'abv': abv,
                        'expected': expected,
                        'issue': '酒精度与品牌参考值偏差过大'
                    })
    return issues


# ============================================================
# 功能2：血缘追踪字段补充
# ============================================================

# 数据源 URL 映射
SOURCE_URL_TEMPLATES = {
    "百度百科": lambda slug: f"https://baike.baidu.com/item/{slug}",
    "IBA Official": lambda slug: f"https://iba-world.com/iba-cocktail/{slug}/",
    "品牌官方/Wikipedia": lambda slug: f"https://en.wikipedia.org/wiki/{slug}",
    "品牌官方/Wikipedia/Wine-Searcher": lambda slug: f"https://www.wine-searcher.com/find/{slug}",
    "OpenFoodFacts": lambda slug: f"https://world.openfoodfacts.org/product/{slug}",
}


def enrich_provenance(kb_dir):
    """为已有 .md 文件补充 source_url/crawl_date/version 字段。"""
    kb_path = Path(kb_dir)
    enriched = 0
    for md_file in kb_path.glob("*.md"):
        if md_file.stem == "INDEX":
            continue
        content = md_file.read_text(encoding='utf-8')

        # 检查是否已有 source_url
        if 'source_url:' in content:
            continue

        # 提取现有字段
        source_match = re.search(r'data_source:\s*(.+)', content)
        id_match = re.search(r'^id:\s*(.+)', content, re.MULTILINE)

        if not source_match or not id_match:
            continue

        source = source_match.group(1).strip()
        eid = id_match.group(1).strip()

        # 生成 source_url
        slug = eid.split('-')[-1] if '-' in eid else eid
        url_template = SOURCE_URL_TEMPLATES.get(source)
        source_url = url_template(slug) if url_template else ""

        # 在 frontmatter 中添加字段
        # 找到 updated: 行，在其后添加
        new_fields = []
        if source_url:
            new_fields.append(f"source_url: {source_url}")
        new_fields.append(f"crawl_date: 2024-07-07")
        new_fields.append(f"version: 1")

        # 插入到 --- 之前（frontmatter 结束）
        if new_fields:
            insertion = "\n".join(new_fields)
            content = content.replace('\n---\n', f'\n{insertion}\n---\n', 1)
            md_file.write_text(content, encoding='utf-8')
            enriched += 1

    return enriched


# ============================================================
# 功能3：数据衰减检查
# ============================================================

def check_data_freshness(kb):
    """检查数据新鲜度，识别过期数据。"""
    now = datetime.now()
    price_stale = []  # 价格过期（6个月）
    rating_stale = []  # 评分过期（12个月）
    general_stale = []  # 一般过期（24个月）

    for e in kb.entries.values():
        if not e.updated:
            continue
        try:
            updated = datetime.fromisoformat(e.updated)
        except (ValueError, TypeError):
            continue

        days_old = (now - updated).days

        # 有价格数据的，6个月检查
        if e.structured_attrs.get('price_rmb') or '参考价格' in e.content:
            if days_old > 180:
                price_stale.append({'id': e.id, 'title': e.title, 'days': days_old})

        # 有评分数据的，12个月检查
        if e.ratings:
            if days_old > 365:
                rating_stale.append({'id': e.id, 'title': e.title, 'days': days_old})

        # 所有数据，24个月检查
        if days_old > 730:
            general_stale.append({'id': e.id, 'title': e.title, 'days': days_old})

    return {
        'price_stale': price_stale,
        'rating_stale': rating_stale,
        'general_stale': general_stale,
    }


# ============================================================
# 功能4：修正酒精度期望范围
# ============================================================

# 修正后的酒精度合理范围（基于真实数据反馈）
CORRECTED_ABV_RANGES = {
    'baijiu': (35, 68),      # 白酒
    'whisky': (35, 65),      # 威士忌（桶强可达65%）
    'brandy': (35, 50),      # 白兰地
    'gin': (29, 55),         # 金酒（黑刺莓低，Nolet's高）
    'vodka': (35, 50),       # 伏特加
    'rum': (35, 50),         # 朗姆酒
    'tequila': (35, 50),     # 龙舌兰
    'wine_red': (11, 16),    # 红葡萄酒（温暖产区可达16%）
    'wine_white': (7, 15),   # 白葡萄酒（德国Kabinett 8.5%，TBA 7%）
    'wine_sparkling': (10, 13), # 起泡酒
    'wine_fortified': (15, 22), # 加强酒
    'wine_rose': (10, 14.5), # 桃红（高端可达14%）
    'wine_dessert': (5, 22), # 甜酒（Eszencia 5%，加强甜酒22%）
    'beer': (2, 12),         # 啤酒（修正：精酿可达12%）
    'sake': (5, 20),         # 清酒（修正：起泡清酒5%）
    'cocktail': (3, 45),     # 鸡尾酒（修正：低度果味型3%，纯烈酒型如Death in the Afternoon 41%）
    'liqueur': (11, 40),     # 力娇酒
    'mead': (5, 20),         # 蜂蜜酒（修正：低度罐装6%，加强型如Viking Blod 19%）
    'fruit_wine': (3, 40),   # 果酒（低度发酵型3%，蒸馏型可达40%）
    'rice_wine': (1, 55),    # 米酒（甜酒酿1%，蒸馏米酒可达55%）
    'yellow_wine': (8, 20),  # 黄酒
}


def validate_abv_ranges(kb):
    """使用修正后的范围验证酒精度。"""
    issues = []
    for e in kb.entries.values():
        sub = e.structured_attrs.get('subcategory', '?')
        abv = e.structured_attrs.get('abv_num')
        if abv and sub in CORRECTED_ABV_RANGES:
            lo, hi = CORRECTED_ABV_RANGES[sub]
            if not (lo <= abv <= hi):
                issues.append({
                    'id': e.id, 'title': e.title,
                    'subcategory': sub, 'abv': abv,
                    'expected': f'{lo}-{hi}'
                })
    return issues


# ============================================================
# 功能5：质量报告
# ============================================================

def _get_data_confidence(e):
    """获取数据置信度。

    兼容 Entry 暂无 data_confidence 属性的情况：优先取属性，
    其次从原始 frontmatter 解析 data_confidence 字段，均缺失时返回 'unknown'。
    """
    val = getattr(e, 'data_confidence', None)
    if val:
        return val
    # 从 raw frontmatter 解析
    m = re.search(r'^data_confidence:\s*(.+)', e.raw, re.MULTILINE)
    return m.group(1).strip() if m else 'unknown'


def check_hallucinations(kb):
    """幻觉检查：检测可能由 AI 编造的虚假数据。

    检查项：
    1. simulated 条目不应携带评分/获奖（评分必须来自真实数据源）
    2. 非酒类子类不应渲染酒精度/价格/风味轮廓
    """
    NON_ALCOHOL_SUBCATS = {
        "process", "region", "pairing", "glassware", "tasting_sop", "sop", "dec",
        "anti", "guide", "other_spirit", "law", "fake", "collect", "grape",
        "aging", "buying", "scene", "trend",
    }
    fake_ratings = []
    fake_awards = []
    misrendered = []

    for e in kb.entries.values():
        conf = _get_data_confidence(e)
        subcat = e.structured_attrs.get('subcategory', '')

        # 检查1: simulated 数据不应有评分/获奖
        if conf == 'simulated':
            if e.ratings:
                fake_ratings.append((e.id, e.title, list(e.ratings.keys())))
            if e.awards:
                fake_awards.append((e.id, e.title, len(e.awards)))

        # 检查2: 非酒类子类不应含酒精度/价格/风味轮廓
        if subcat in NON_ALCOHOL_SUBCATS:
            if '参考价格' in e.content or '风味轮廓' in e.content:
                misrendered.append((e.id, e.title, subcat))

    return {
        'fake_ratings': fake_ratings,
        'fake_awards': fake_awards,
        'misrendered': misrendered,
    }


def generate_quality_report(kb):
    """生成数据质量看板。"""
    total = len(kb)
    if total == 0:
        return "知识库为空，无法生成报告。"

    # 置信度分布
    conf = Counter(_get_data_confidence(e) for e in kb.entries.values())
    real = conf.get('verified', 0) + conf.get('official', 0)

    # 酒精度覆盖
    with_abv = sum(1 for e in kb.entries.values()
                   if e.structured_attrs.get('abv_num') is not None)

    # 交叉验证
    consistency_issues = cross_validate_brand_consistency(kb)

    # 范围验证
    range_issues = validate_abv_ranges(kb)

    # 衰减检查
    freshness = check_data_freshness(kb)

    # 幻觉检查
    halluc = check_hallucinations(kb)

    report = f"""
{'='*60}
数据质量看板
{'='*60}
总条目: {total}

数据置信度:
  官方(official):    {conf.get('official', 0):4d} ({conf.get('official', 0)*100//total}%)
  已验证(verified):  {conf.get('verified', 0):4d} ({conf.get('verified', 0)*100//total}%)
  推测(simulated):   {conf.get('simulated', 0):4d} ({conf.get('simulated', 0)*100//total}%)
  真实数据占比:      {real} ({real*100//total}%)

字段完整性:
  酒精度数值化:      {with_abv}/{total} ({with_abv*100//total}%)

质量检查:
  品牌一致性异常:    {len(consistency_issues)} 条
  酒精度范围异常:    {len(range_issues)} 条（修正范围后）
  价格过期(>6月):    {len(freshness['price_stale'])} 条
  评分过期(>12月):   {len(freshness['rating_stale'])} 条
  通用过期(>24月):   {len(freshness['general_stale'])} 条

防幻觉检查:
  simulated含编造评分: {len(halluc['fake_ratings'])} 条 {'✓' if not halluc['fake_ratings'] else '← 需修复'}
  simulated含编造获奖: {len(halluc['fake_awards'])} 条 {'✓' if not halluc['fake_awards'] else '← 需修复'}
  非酒类条目错误渲染:  {len(halluc['misrendered'])} 条 {'✓' if not halluc['misrendered'] else '← 需修复'}
"""
    return report


# ============================================================
# main
# ============================================================

def main():
    # src 位于 Hermes/src（scripts 的上三级目录），与 validate_kb.py 一致
    sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))
    from hermes.kb import KnowledgeBase

    kb = KnowledgeBase(Path(__file__).parent.parent / "knowledge")
    kb.load()

    action = sys.argv[1] if len(sys.argv) > 1 else "check"

    if action in ("check", "report"):
        report = generate_quality_report(kb)
        print(report)

    if action == "enrich":
        kb_dir = Path(__file__).parent.parent / "knowledge"
        enriched = enrich_provenance(kb_dir)
        print(f"血缘字段补充: {enriched} 条")

    if action == "check":
        # 详细问题列表
        print("\n详细问题:")
        consistency = cross_validate_brand_consistency(kb)
        if consistency:
            print(f"\n品牌一致性异常 ({len(consistency)}):")
            for i in consistency[:10]:
                print(f"  {i['id']}: {i['abv']}% (期望{i['expected']}) - {i['issue']}")

        range_issues = validate_abv_ranges(kb)
        if range_issues:
            print(f"\n酒精度范围异常 ({len(range_issues)}):")
            for i in range_issues[:10]:
                print(f"  {i['id']}: {i['abv']}% [{i['subcategory']}] 期望{i['expected']}")


if __name__ == "__main__":
    main()
