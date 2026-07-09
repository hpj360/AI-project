#!/usr/bin/env python3
"""百度百科中国酒类品牌抓取器。

数据源：百度百科开放 API（免费、无需 key）
输出：data/data_baike_china.py
"""
import urllib.request
import urllib.parse
import json
import time
import sys
import re
from pathlib import Path

BAIKE_API = "https://baike.baidu.com/api/openapi/BaikeLemmaCardApi"
APPID = 379020
SCOPE = 103

# HTTP 头：伪装普通浏览器，避免被识别为爬虫
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.9",
    "Referer": "https://baike.baidu.com/",
}

# 子类 → 关键词列表（共 100 个品牌）
BRANDS = {
    "baijiu": [
        # 品牌系列
        "茅台酒", "五粮液", "剑南春", "泸州老窖", "汾酒",
        "西凤酒", "古井贡酒", "洋河大曲", "董酒", "郎酒",
        "习酒", "水井坊", "舍得酒", "酒鬼酒", "衡水老白干",
        "牛栏山二锅头", "红星二锅头", "宋河粮液", "宝丰酒", "武陵酒",
        # 具体产品
        "茅台飞天", "五粮液普五", "五粮液1618", "剑南春水晶剑", "泸州老窖特曲",
        "泸州老窖国窖1573", "汾酒青花30", "汾酒老白汾", "西凤酒华山论剑", "洋河海之蓝",
        "洋河天之蓝", "洋河梦之蓝", "古井贡酒年份原浆", "郎酒红花郎", "习酒窖藏1988",
        "水井坊井台", "舍得品味", "酒鬼酒内参", "牛栏山百年", "红星蓝花十五",
    ],
    "yellow_wine": [
        "古越龙山", "会稽山", "塔牌黄酒", "即墨老酒", "沙洲优黄",
        "丹阳黄酒", "福建老酒", "无锡老酒", "嘉兴黄酒", "黑米酒",
        # 具体产品
        "古越龙山三年陈", "古越龙山十年陈", "塔牌冬酿", "会稽山纯生", "即墨老酒十年陈",
    ],
    "rice_wine": [
        "桂林三花酒", "客家娘酒", "广东老米酒", "日本清酒", "韩国马格利",
    ],
    "fruit_wine": [
        "竹叶青酒", "劲酒", "五加皮酒", "桂花酒", "菊花酒",
    ],
    "wine": [
        "张裕葡萄酒", "张裕解百纳", "长城葡萄酒", "王朝葡萄酒", "威龙葡萄酒",
        "莫高葡萄酒", "尼雅葡萄酒", "贺兰山葡萄酒", "通化葡萄酒", "龙徽葡萄酒",
    ],
    "beer": [
        "青岛啤酒", "燕京啤酒", "雪花啤酒", "哈尔滨啤酒", "珠江啤酒",
        "重庆啤酒", "乌苏啤酒", "泰山啤酒", "兰州黄河", "金威啤酒",
    ],
    "sake": [
        "獺祭", "久保田", "八海山", "十四代", "白鹤",
    ],
    "spirits_intl": [
        "麦卡伦18年", "格兰菲迪15年", "百龄坛12年", "芝华士18年", "轩尼诗XO",
        "人头马CLUB", "马爹利蓝带", "杰克丹尼蜂蜜", "金宾黑麦", "尊美醇18年",
    ],
}

# 非中国品牌的关键词 → 国家（用于覆盖默认 "中国"）
KEYWORD_COUNTRY = {
    # 清酒（日本）
    "獺祭": "日本", "久保田": "日本", "八海山": "日本", "十四代": "日本", "白鹤": "日本",
    # 国际烈酒
    "麦卡伦18年": "英国", "格兰菲迪15年": "英国", "百龄坛12年": "英国", "芝华士18年": "英国",
    "轩尼诗XO": "法国", "人头马CLUB": "法国", "马爹利蓝带": "法国",
    "杰克丹尼蜂蜜": "美国", "金宾黑麦": "美国", "尊美醇18年": "爱尔兰",
}

# 关键词 → URL 友好 slug（拼音/英文）
SLUGS = {
    # 白酒
    "茅台酒": "maotai", "五粮液": "wuliangye", "剑南春": "jiannanchun",
    "泸州老窖": "luzhou-laojiao", "汾酒": "fenjiu", "西凤酒": "xifeng-jiu",
    "古井贡酒": "gujing-gongjiu", "洋河大曲": "yanghe-daqu", "董酒": "dongjiu",
    "郎酒": "langjiu", "习酒": "xijiu", "水井坊": "shuijingfang",
    "舍得酒": "shede-jiu", "酒鬼酒": "jiugui-jiu", "衡水老白干": "hengshui-laobaigan",
    "牛栏山二锅头": "niulanshan-erguotou", "红星二锅头": "hongxing-erguotou",
    "宋河粮液": "songhe-liangye", "宝丰酒": "baofeng-jiu", "武陵酒": "wuling-jiu",
    # 黄酒
    "古越龙山": "guyue-longshan", "会稽山": "kuaiji-shan", "塔牌黄酒": "tapai-huangjiu",
    "即墨老酒": "jimo-laojiu", "沙洲优黄": "shazhou-youhuang",
    "丹阳黄酒": "danyang-huangjiu", "福建老酒": "fujian-laojiu",
    "无锡老酒": "wuxi-laojiu", "嘉兴黄酒": "jiaxing-huangjiu",
    "黑米酒": "heimi-jiu",
    # 米酒
    "桂林三花酒": "guilin-sanhua-jiu", "客家娘酒": "kejia-niangjiu",
    "广东老米酒": "guangdong-lao-mijiu", "日本清酒": "riben-qingjiu",
    "韩国马格利": "hanguo-makgeolli",
    # 果酒/其他
    "竹叶青酒": "zhuyeqing-jiu", "劲酒": "jinjiu", "五加皮酒": "wujiapi-jiu",
    "桂花酒": "guihua-jiu", "菊花酒": "juhua-jiu",
    # 白酒具体产品
    "茅台飞天": "maotai-feitian", "五粮液普五": "wuliangye-puwu",
    "五粮液1618": "wuliangye-1618", "剑南春水晶剑": "jiannanchun-shuijingjian",
    "泸州老窖特曲": "luzhou-laojiao-tequ", "泸州老窖国窖1573": "luzhou-laojiao-guojiao-1573",
    "汾酒青花30": "fenjiu-qinghua-30", "汾酒老白汾": "fenjiu-laobaifen",
    "西凤酒华山论剑": "xifeng-jiu-huashanlunjian", "洋河海之蓝": "yanghe-haizhilan",
    "洋河天之蓝": "yanghe-tianzhilan", "洋河梦之蓝": "yanghe-mengzhilan",
    "古井贡酒年份原浆": "gujing-gongjiu-nianfenyuanjiang",
    "郎酒红花郎": "langjiu-honghualang", "习酒窖藏1988": "xijiu-jiaocang-1988",
    "水井坊井台": "shuijingfang-jingtai", "舍得品味": "shede-pinwei",
    "酒鬼酒内参": "jiugui-jiu-neican", "牛栏山百年": "niulanshan-bainian",
    "红星蓝花十五": "hongxing-lanhua-shiwu",
    # 黄酒具体产品
    "古越龙山三年陈": "guyue-longshan-sannianchen",
    "古越龙山十年陈": "guyue-longshan-shinianchen",
    "塔牌冬酿": "tapai-dongniang", "会稽山纯生": "kuaiji-shan-chunsheng",
    "即墨老酒十年陈": "jimo-laojiu-shinianchen",
    # 葡萄酒（国产）
    "张裕葡萄酒": "zhangyu-putaojiu", "张裕解百纳": "zhangyu-jiebaina",
    "长城葡萄酒": "changcheng-putaojiu", "王朝葡萄酒": "wangchao-putaojiu",
    "威龙葡萄酒": "weilong-putaojiu", "莫高葡萄酒": "mogao-putaojiu",
    "尼雅葡萄酒": "niya-putaojiu", "贺兰山葡萄酒": "helanshan-putaojiu",
    "通化葡萄酒": "tonghua-putaojiu", "龙徽葡萄酒": "longhui-putaojiu",
    # 啤酒（国产）
    "青岛啤酒": "qingdao-pijiu", "燕京啤酒": "yanjing-pijiu",
    "雪花啤酒": "xuehua-pijiu", "哈尔滨啤酒": "haerbin-pijiu",
    "珠江啤酒": "zhujiang-pijiu", "重庆啤酒": "chongqing-pijiu",
    "乌苏啤酒": "wusu-pijiu", "泰山啤酒": "taishan-pijiu",
    "兰州黄河": "lanzhou-huanghe", "金威啤酒": "jinwei-pijiu",
    # 清酒（日本）
    "獺祭": "dassai", "久保田": "kubota", "八海山": "hakkaisan",
    "十四代": "juyondai", "白鹤": "hakutsuru",
    # 国际烈酒
    "麦卡伦18年": "macallan-18", "格兰菲迪15年": "glenfiddich-15",
    "百龄坛12年": "ballantines-12", "芝华士18年": "chivas-18",
    "轩尼诗XO": "hennessy-xo", "人头马CLUB": "remy-martin-club",
    "马爹利蓝带": "martell-cordon-bleu", "杰克丹尼蜂蜜": "jack-daniels-honey",
    "金宾黑麦": "jim-beam-rye", "尊美醇18年": "jameson-18",
}

# 部分关键词直接查不到 lemma 时的备选查询词（按顺序尝试）
ALTERNATES = {
    "古越龙山": ["古越龙山黄酒", "绍兴黄酒"],
    "嘉兴黄酒": ["嘉善黄酒", "绍兴黄酒"],
    "五加皮酒": ["五加皮", "五加皮酒 (中药酒)"],
    "桂花酒": ["桂花酒", "桂花酿"],
    "无锡老酒": ["无锡黄酒", "惠山泉酒"],
    "广东老米酒": ["广东米酒", "老米酒"],
    "韩国马格利": ["马格利酒", "马格利"],
    "日本清酒": ["清酒", "日本清酒"],
    "塔牌黄酒": ["塔牌", "塔牌绍兴酒"],
    "黑米酒": ["黑糯米酒", "黑米酒"],
    "古井贡酒": ["古井贡"],
    "衡水老白干": ["衡水老白干酒", "老白干"],
    "会稽山": ["会稽山黄酒", "会稽山绍兴酒"],
    # 白酒具体产品备选
    "茅台飞天": ["飞天茅台"],
    "五粮液普五": ["普五"],
    "剑南春水晶剑": ["水晶剑"],
    "泸州老窖国窖1573": ["国窖1573"],
    "汾酒青花30": ["青花汾酒"],
    "汾酒老白汾": ["老白汾"],
    "洋河海之蓝": ["海之蓝"],
    "洋河天之蓝": ["天之蓝"],
    "洋河梦之蓝": ["梦之蓝"],
    "郎酒红花郎": ["红花郎"],
    "习酒窖藏1988": ["窖藏1988"],
    "酒鬼酒内参": ["内参酒"],
    # 清酒备选（繁简/别名）
    "獺祭": ["獭祭"],
    "白鹤": ["白鹤清酒"],
    # 国际烈酒备选
    "轩尼诗XO": ["轩尼诗X.O"],
    "人头马CLUB": ["人头马CLUB"],
    "金宾黑麦": ["金宾", "占边"],
}


def _strip_html(s):
    """去除 HTML 标签、<sup> 注释、多余空白，保留纯文本。"""
    if not isinstance(s, str):
        s = str(s) if s is not None else ""
    # 先去掉 <sup>...</sup> 引用标注块（含内部文字）
    s = re.sub(r"<sup[^>]*>.*?</sup>", "", s, flags=re.DOTALL)
    # 去掉 <a ...>链接</a> 等所有标签
    s = re.sub(r"<[^>]+>", "", s)
    # 去掉 HTML 实体
    s = re.sub(r"&[a-zA-Z]+;", " ", s)
    s = re.sub(r"&#\d+;", " ", s)
    # 折叠空白
    s = re.sub(r"\s+", " ", s)
    return s.strip()


def _card_value(card, *names):
    """从 card 数组中按 name 匹配取值（多个候选名按顺序匹配），返回清洗后的字符串。"""
    if not isinstance(card, list):
        return ""
    name_set = {n for n in names}
    for item in card:
        if not isinstance(item, dict):
            continue
        nm = item.get("name", "")
        if nm in name_set:
            val = item.get("value", "")
            if isinstance(val, list):
                val = "、".join(_strip_html(v) for v in val if v)
            else:
                val = _strip_html(val)
            return val
    return ""


def fetch_baike(keyword):
    """请求百度百科 API，返回 dict 或 None。

    超时 10 秒，失败重试 2 次（共 3 次尝试）。
    空结果（疑似限流）采用更长的退避等待以恢复，网络异常同样重试。
    """
    params = {
        "scope": str(SCOPE),
        "format": "json",
        "appid": str(APPID),
        "bk_key": keyword,
        "bk_length": "2000",
    }
    url = BAIKE_API + "?" + urllib.parse.urlencode(params)
    max_retries = 2  # 失败重试 2 次
    for attempt in range(max_retries + 1):
        req = urllib.request.Request(url, headers=HEADERS)
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                raw = resp.read().decode("utf-8", errors="replace")
            data = json.loads(raw)
            # API 可能返回空对象或无 title（未命中词条 / 限流）
            if not data or not data.get("title"):
                # 空结果走重试（多为限流），用较长退避恢复
                if attempt < max_retries:
                    time.sleep(5 + attempt * 5)  # 5s, 10s
                    continue
                return None
            return data
        except Exception as e:
            if attempt < max_retries:
                time.sleep(5 + attempt * 5)
                continue
            print(f"  [网络错误] {keyword}: {e}", file=sys.stderr)
            return None
    return None


def parse_baike_to_entry(data, subcategory):
    """把百度百科 JSON 解析成 data_*.py 格式的 dict。

    提取：
      title   → title / name_cn
      desc    → summary（取前 200 字）
      card    → region / abv / ingredients / history / producer
    """
    if not isinstance(data, dict) or not data.get("title"):
        return None

    title = _strip_html(data.get("title", ""))
    if not title:
        return None

    desc = _strip_html(data.get("desc", "")) or _strip_html(data.get("abstract", ""))
    summary = (desc or "")[:200]

    card = data.get("card", [])

    region = _card_value(card, "产地名称", "产地", "原产地", "产地/厂家")
    abv = _card_value(card, "酒精度", "酒精含量", "度数")
    ingredients = _card_value(card, "主要原料", "原料", "配料", "原材料")
    history = _card_value(card, "创建时间", "创制时间", "创立", "创立时间", "始创时间", "诞生时间")
    producer = _card_value(card, "生产商", "生产厂家", "所属公司", "所属企业", "制造商", "所有者", "品牌所属")

    # 摘要兜底：若 desc 太短，用 abstract 补
    if len(summary) < 30:
        abstract = _strip_html(data.get("abstract", ""))
        if abstract:
            summary = (summary + " " + abstract)[:200].strip()

    return {
        "title": title,
        "name_cn": title,
        "summary": summary,
        "region": region,
        "country": "中国",
        "abv": abv,
        "ingredients": ingredients,
        "history": history,
        "producer": producer,
    }


def _render_value(v):
    """把 Python 值渲染为合法字面量字符串。"""
    if isinstance(v, str):
        return json.dumps(v, ensure_ascii=False)
    if isinstance(v, list):
        if not v:
            return "[]"
        return "[" + ", ".join(_render_value(x) for x in v) + "]"
    if isinstance(v, (int, float)):
        return repr(v)
    if isinstance(v, bool):
        return "True" if v else "False"
    if v is None:
        return "None"
    return json.dumps(str(v), ensure_ascii=False)


def main():
    out_path = Path(__file__).resolve().parent / "data" / "data_baike_china.py"
    out_path.parent.mkdir(parents=True, exist_ok=True)

    entries = []
    succeeded = []
    failed = []
    total = 0

    for subcategory, keywords in BRANDS.items():
        for kw in keywords:
            total += 1
            slug = SLUGS.get(kw, re.sub(r"[^a-z0-9]+", "-", kw.lower()).strip("-") or "brand")
            # 按主关键词 + 备选关键词顺序尝试
            candidates = [kw] + ALTERNATES.get(kw, [])
            data = None
            used_kw = None
            for cand in candidates:
                print(f"[{total}] 抓取 {subcategory}/{kw} (查询: {cand}) ...", flush=True)
                data = fetch_baike(cand)
                if data and data.get("title"):
                    used_kw = cand
                    break
                time.sleep(1)  # 避免被封
            if not data:
                print(f"  ✗ 失败：{kw}（所有候选词均无结果）", flush=True)
                failed.append(kw)
                time.sleep(1)
                continue
            parsed = parse_baike_to_entry(data, subcategory)
            if not parsed:
                print(f"  ✗ 失败：{kw}（解析为空）", flush=True)
                failed.append(kw)
                time.sleep(1)
                continue
            entry_id = f"ENT-baike-{subcategory}-{slug}"
            entry = {
                "id": entry_id,
                "category": "ENT",
                "subcategory": subcategory,
                "title": parsed["title"],
                "title_en": "",
                "name_cn": parsed["name_cn"],
                "name_en": "",
                "aliases": [],
                "tags": ["百度百科", subcategory, parsed["title"]],
                "summary": parsed["summary"],
                "country": KEYWORD_COUNTRY.get(kw, parsed["country"]),
                "region": parsed["region"],
                "producer": parsed["producer"],
                "abv": parsed["abv"],
                "volume": "",
                "price_tier": "",
                "price_rmb_range": [],
                "ingredients": parsed["ingredients"],
                "production_method": "",
                "distillation": "",
                "aging": "",
                "vintage": "",
                "appearance": "",
                "nose": "",
                "palate": "",
                "finish": "",
                "flavor_tags": [],
                "serving_temp": "",
                "glassware": "",
                "food_pairing": "",
                "cocktail_use": [],
                "history": parsed["history"],
                "appellation_law": "",
                "story": "",
                "related": [],
                "availability": "市售",
                "source": "百度百科",
                "source_keyword": used_kw or kw,
                "source_url": (
                    "https://baike.baidu.com/item/"
                    + urllib.parse.quote(parsed["title"])
                ),
            }
            entries.append(entry)
            succeeded.append(kw)
            print(f"  ✓ 成功：{parsed['title']}（查询词: {used_kw}）", flush=True)
            time.sleep(1)  # 每次成功后也 sleep 1 秒，避免被封

    # 写入文件
    lines = [
        '"""百度百科中国酒类品牌数据。',
        "",
        f"共 {len(entries)} 条目，由 crawl_baike_baijiu.py 自动生成。",
        "数据来源: 百度百科 openapi (https://baike.baidu.com/api/openapi/BaikeLemmaCardApi)",
        "subcategory: baijiu(白酒) / yellow_wine(黄酒) / rice_wine(米酒) / fruit_wine(果酒) / wine(葡萄酒) / beer(啤酒) / sake(清酒) / spirits_intl(国际烈酒)",
        '字段 source 标记为真实抓取数据。',
        '"""',
        "",
        "ENTRIES = [",
    ]
    for e in entries:
        lines.append("    {")
        for k, v in e.items():
            lines.append(f"        {_render_value(k)}: {_render_value(v)},")
        lines.append("    },")
    lines.append("]")
    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    # 统计
    print("\n" + "=" * 60)
    print(f"总计 {total} 个品牌：成功 {len(succeeded)}，失败 {len(failed)}")
    if failed:
        print("失败列表:", "、".join(failed))
    print(f"输出文件: {out_path}")
    print("=" * 60)


if __name__ == "__main__":
    main()
