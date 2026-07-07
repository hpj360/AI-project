"""同义词词典 + 拼写纠错（检索增强）。

能力：
- SYNONYMS: 中英同义词映射，检索时扩展查询
- TYPO_CORRECTIONS: 常见拼写错误纠正
- expand_query: 扩展查询（同义词展开）
- correct_query: 纠正拼写错误
- normalize_query: 综合处理（纠错 + 同义词展开）
"""
from __future__ import annotations

import re


# ============================================================
# 同义词词典（中英互译 + 别名）
# ============================================================

SYNONYMS = {
    # 烈酒大类
    "威士忌": ["威士卡", "whisky", "whiskey", "威士忌酒"],
    "威士卡": ["威士忌", "whisky", "whiskey"],
    "白兰地": ["brandy", "白兰地酒", "干邑", "cognac"],
    "干邑": ["cognac", "白兰地"],
    "伏特加": ["vodka", "伏特加酒", "俄得克"],
    "金酒": ["gin", "琴酒", "杜松子酒", "毡酒", "gin酒"],
    "琴酒": ["gin", "金酒", "杜松子酒"],
    "杜松子酒": ["gin", "金酒", "琴酒"],
    "朗姆": ["rum", "朗姆酒", "兰姆酒", "萊姆酒"],
    "朗姆酒": ["rum", "朗姆", "兰姆酒"],
    "龙舌兰": ["tequila", "特基拉", "特奎拉", "龙舌兰酒", "梅斯卡尔", "mezcal"],
    "梅斯卡尔": ["mezcal", "梅斯卡尔酒", "龙舌兰"],
    "白酒": ["baijiu", "中国白酒", "烧酒"],
    "利口酒": ["liqueur", "力乔酒", "力口酒"],

    # 葡萄酒
    "葡萄酒": ["wine", "红酒", "葡萄酒"],
    "红酒": ["red wine", "红葡萄酒", "wine red"],
    "白葡萄酒": ["white wine", "白酒", "wine white"],
    "起泡酒": ["sparkling wine", "气泡酒", "sparkling"],
    "香槟": ["champagne", "香槟酒"],
    "桃红": ["rose wine", "玫瑰红", "粉红葡萄酒"],
    "甜酒": ["dessert wine", "甜葡萄酒"],
    "加强酒": ["fortified wine", "波特", "波特酒", "port"],
    "波特酒": ["port", "波特", "加强酒"],
    "雪莉": ["sherry", "雪莉酒", "赫雷斯"],
    "味美思": ["vermouth", "苦艾酒"],

    # 亚洲酒
    "清酒": ["sake", "日本酒", "清酒"],
    "sake": ["清酒", "日本酒"],
    "黄酒": ["yellow wine", "huangjiu", "老酒"],
    "米酒": ["rice wine", "日本米酒", "韩式米酒"],
    "梅酒": ["umeshu", "梅子酒", "plum wine"],

    # 啤酒
    "啤酒": ["beer", "ale", "lager", "麦酒"],
    "精酿": ["craft beer", "精酿啤酒"],
    "世涛": ["stout", "黑啤", "stout啤酒"],
    "ipa": ["india pale ale", "ipa啤酒", "印度淡色艾尔"],

    # 鸡尾酒
    "鸡尾酒": ["cocktail", "混合饮料"],
    "马提尼": ["martini", "马天尼", "马丁尼"],
    "马天尼": ["martini", "马提尼", "马丁尼"],
    "莫吉托": ["mojito", "莫希托", "莫吉多"],
    "莫希托": ["mojito", "莫吉托"],
    "古典": ["old fashioned", "古典鸡尾酒", "老式"],
    "曼哈顿": ["manhattan", "曼哈顿鸡尾酒"],
    "代基里": ["daiquiri", "得其利", "黛克瑞"],
    "得其利": ["daiquiri", "代基里"],

    # 风味术语
    "泥煤": ["peat", "泥煤味", "烟熏"],
    "烟熏": ["smoke", "smoked", "泥煤"],
    "雪莉桶": ["sherry cask", "sherry oak", "雪莉橡木桶"],
    "波本桶": ["bourbon cask", "bourbon oak", "波本橡木桶"],
    "单宁": ["tannin", "单宁酸"],

    # 品牌
    "茅台": ["maotai", "茅台酒", "moutai"],
    "拉菲": ["lafite", "拉菲古堡", "lafite rothschild"],
    "麦卡伦": ["macallan", "麦卡伦威士忌"],
    "轩尼诗": ["hennessy", "轩尼诗干邑"],
    "人头马": ["remy martin", "rémy martin"],
    "马爹利": ["martell", "马爹利干邑"],
    "百龄坛": ["ballantine", "ballantines", "百龄坛威士忌"],
    "芝华士": ["chivas", "chivas regal", "芝华士威士忌"],
    "杰克丹尼": ["jack daniels", "jack daniel's", "杰克·丹尼"],
    "约翰走路": ["johnnie walker", "johnny walker", "尊尼获加"],
    "尊尼获加": ["johnnie walker", "约翰走路"],

    # 产区
    "苏格兰": ["scotland", "scotch", "苏格兰威士忌"],
    "scotch": ["苏格兰", "苏格兰威士忌"],
    "波本": ["bourbon", "波本威士忌", "美国威士忌"],
    "日本威士忌": ["japanese whisky", "日威"],
    "斯佩塞": ["speyside", "斯佩塞威士忌"],
    "艾雷岛": ["islay", "艾拉岛"],
    "干邑区": ["cognac region", "cognac"],
}


# ============================================================
# 常见拼写错误纠正
# ============================================================

TYPO_CORRECTIONS = {
    # 中文常见错别字
    "茅台酒": "茅台",
    "拉菲尔": "拉菲",
    "麦卡伦": "麦卡伦",  # 正确，但保留映射
    "威士忌酒": "威士忌",
    "白兰地酒": "白兰地",
    "伏特加酒": "伏特加",

    # 英文常见拼写错误
    "whisky": "whisky",  # 英式拼写，正确
    "wisky": "whisky",
    "wiskey": "whiskey",
    "whiskie": "whisky",
    "vodca": "vodka",
    "wodka": "vodka",
    "brandy": "brandy",  # 正确
    "brandi": "brandy",
    "teqila": "tequila",
    "tequilla": "tequila",
    "tekila": "tequila",
    "rum": "rum",  # 正确
    "rhum": "rum",  # 法语变体
    "gin": "gin",  # 正确
    "jinn": "gin",
    "sake": "sake",  # 正确
    "saki": "sake",
    "saki": "sake",
    "champagne": "champagne",  # 正确
    "champagn": "champagne",
    "champaige": "champagne",
    "shampagne": "champagne",

    # 品牌拼写错误
    "macalllan": "macallan",
    "macalan": "macallan",
    "glenfiddich": "glenfiddich",  # 正确
    "glenfiddic": "glenfiddich",
    "glenlivet": "glenlivet",  # 正确
    "glenlivit": "glenlivet",
    "henessy": "hennessy",
    "hennesy": "hennessy",
    "hennessey": "hennessy",
    "remy": "remy martin",
    "remymartin": "remy martin",

    # 鸡尾酒拼写
    "mojito": "mojito",  # 正确
    "mohito": "mojito",
    "mojhitos": "mojito",
    "margherita": "margarita",  # 鸡尾酒是 margarita 不是 margherita（披萨）
    "margharita": "margarita",
    "martinis": "martini",
    "cosmopolitans": "cosmopolitan",
}


# ============================================================
# 查询扩展与纠正
# ============================================================

def correct_query(query: str) -> tuple[str, list[str]]:
    """纠正查询中的拼写错误。

    返回 (纠正后的查询, 应用的纠正列表)。
    """
    if not query:
        return query, []
    query_lower = query.lower()
    applied = []
    for typo, correct in TYPO_CORRECTIONS.items():
        # 跳过自映射（正确拼写）
        if typo == correct.lower():
            continue
        if typo in query_lower:
            query_lower = query_lower.replace(typo, correct.lower())
            applied.append(f"{typo}→{correct}")
    # 恢复原 query 的大小写（简化：用纠正后的 lower）
    return query_lower, applied


def expand_query(query: str) -> list[str]:
    """扩展查询，返回包含原词和同义词的词列表。"""
    if not query:
        return []
    tokens = set()
    tokens.add(query)
    tokens.add(query.lower())

    # 中文同义词扩展
    for key, syns in SYNONYMS.items():
        if key in query or key.lower() in query.lower():
            for syn in syns:
                tokens.add(syn)
                tokens.add(syn.lower())

    # 反向查找：query 中的词是某个同义词列表的成员
    for key, syns in SYNONYMS.items():
        for syn in syns:
            if syn in query.lower() or syn.lower() in query.lower():
                tokens.add(key)
                tokens.add(key.lower())
                for s in syns:
                    tokens.add(s)
                    tokens.add(s.lower())

    return list(tokens)


def normalize_query(query: str) -> tuple[str, list[str], list[str]]:
    """综合处理：拼写纠正 + 同义词扩展。

    返回 (纠正后的查询, 应用的纠正, 扩展的同义词列表)。
    """
    corrected, applied = correct_query(query)
    expanded = expand_query(corrected)
    return corrected, applied, expanded


if __name__ == "__main__":
    # 测试
    tests = [
        "茅台酒",
        "wisky",
        "tequilla",
        "mohito",
        "苏格兰威士忌",
        "henessy",
        "莫希托",
        "马天尼",
    ]
    for q in tests:
        corrected, applied, expanded = normalize_query(q)
        print(f"[{q}]")
        if applied:
            print(f"  纠正: {applied}")
        if expanded:
            print(f"  扩展({len(expanded)}): {expanded[:5]}")
