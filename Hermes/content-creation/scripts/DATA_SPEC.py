"""酒类知识库数据规范 v3.0

定义：
- SUBCATEGORY_CN: 子类中文名映射
- HIGH/MID_PROFILE_BRANDS: 知名品牌（用于自动评分）
- PRICE_TIERS: 价格档位 RMB 区间
- RATING_SOURCES: 各子类的评分机构
- AWARD_TEMPLATES: 奖项模板
- COCKTAIL_FIELDS: 鸡尾酒扩展字段定义
"""

# ============================================================
# 子类中文名映射
# ============================================================

SUBCATEGORY_CN = {
    # 烈酒
    "baijiu": "白酒",
    "whisky": "威士忌",
    "brandy": "白兰地",
    "gin": "金酒",
    "vodka": "伏特加",
    "rum": "朗姆酒",
    "tequila": "龙舌兰",
    "liqueur": "利口酒",
    "other_spirit": "其他烈酒",
    # 葡萄酒
    "wine_red": "红葡萄酒",
    "wine_white": "白葡萄酒",
    "wine_sparkling": "起泡酒",
    "wine_fortified": "加强酒",
    "wine_rose": "桃红葡萄酒",
    "wine_dessert": "甜酒",
    # 亚洲酒
    "sake": "清酒",
    "yellow_wine": "黄酒",
    "rice_wine": "米酒",
    "beer": "啤酒",
    "fruit_wine": "果酒",
    "mead": "蜂蜜酒",
    # 鸡尾酒
    "cocktail": "鸡尾酒",
    # 知识类（非酒类）
    "grape": "葡萄品种",
    "region": "产区风土",
    "process": "酿造工艺",
    "law": "法律法规",
    "fake": "假酒鉴别",
    "collect": "收藏投资",
    "glassware": "酒具器皿",
    "pairing": "餐酒搭配",
    "buying": "购买指南",
    "scene": "场景推荐",
    "trend": "行业趋势",
    "aging": "陈年潜力",
    "guide": "指导性知识",
}


# ============================================================
# 知名品牌（用于自动评分档次判定）
# ============================================================

HIGH_PROFILE_BRANDS = [
    # 威士忌
    "macallan", "lagavulin", "talisker", "yamazaki", "hibiki", "nikka",
    "glenfiddich", "glenlivet", "jackdaniels", "jameson",
    # 白兰地
    "hennessy", "remy", "martell", "courvoisier", "camus",
    # 白酒
    "maotai", "wuliangye", "fenjiu", "luzhou", "jiannanchun",
    # 葡萄酒
    "lafite", "mouton", "margaux", "latour", "hautbrion",
    "petrus", "lepin", "romanee", "opusone",
    # 清酒
    "dassai", "juyondai", "kubota", "hakkaisan",
    # 龙舌兰
    "donjulio", "patron",
    # 朗姆
    "zacapa", "diplomatico",
    # 金酒
    "monkey47", "tanqueray", "bombay",
]

MID_PROFILE_BRANDS = [
    "chivas", "ballantines", "glenmorangie", "ardbeg", "bruichladdich",
    "suntory", "kavalan", "amrut",
    "remymartin", "hennessyvsop", "bibber",
    "jiugui", "shuijingfang", "tuopai",
    "catena", "concha", "penfolds", "yellowtail", "castillo",
    "ozeki", "gekkeikan", "sawanotsuru",
    "olmeca", "sauza", "espolon",
    "bacardi", "havana", "captain",
    "beefeater", "ginmare", "aviation",
    "absolut", "beluga", "stoli",
]


# ============================================================
# 价格档位（RMB 区间）
# ============================================================

DEFAULT_PRICE = {
    "daily": [50, 200],
    "advanced": [200, 600],
    "premium": [600, 2000],
    "collection": [2000, 10000],
}

PRICE_TIERS = {
    "whisky": {
        "daily": [150, 400],
        "advanced": [400, 1200],
        "premium": [1200, 5000],
        "collection": [5000, 50000],
    },
    "baijiu": {
        "daily": [100, 300],
        "advanced": [300, 800],
        "premium": [800, 3000],
        "collection": [3000, 30000],
    },
    "brandy": {
        "daily": [200, 500],
        "advanced": [500, 1500],
        "premium": [1500, 6000],
        "collection": [6000, 40000],
    },
    "wine_red": {
        "daily": [80, 250],
        "advanced": [250, 800],
        "premium": [800, 3000],
        "collection": [3000, 20000],
    },
    "wine_white": {
        "daily": [80, 250],
        "advanced": [250, 700],
        "premium": [700, 2500],
        "collection": [2500, 15000],
    },
    "wine_sparkling": {
        "daily": [100, 300],
        "advanced": [300, 800],
        "premium": [800, 3000],
        "collection": [3000, 20000],
    },
    "wine_fortified": {
        "daily": [100, 300],
        "advanced": [300, 800],
        "premium": [800, 3000],
        "collection": [3000, 15000],
    },
    "sake": {
        "daily": [80, 250],
        "advanced": [250, 600],
        "premium": [600, 2000],
        "collection": [2000, 10000],
    },
    "gin": {
        "daily": [100, 250],
        "advanced": [250, 500],
        "premium": [500, 1500],
        "collection": [1500, 8000],
    },
    "vodka": {
        "daily": [80, 200],
        "advanced": [200, 500],
        "premium": [500, 1500],
        "collection": [1500, 6000],
    },
    "rum": {
        "daily": [100, 250],
        "advanced": [250, 600],
        "premium": [600, 2000],
        "collection": [2000, 10000],
    },
    "tequila": {
        "daily": [150, 350],
        "advanced": [350, 800],
        "premium": [800, 2500],
        "collection": [2500, 12000],
    },
    "liqueur": {
        "daily": [80, 200],
        "advanced": [200, 500],
        "premium": [500, 1500],
        "collection": [1500, 6000],
    },
    "beer": {
        "daily": [10, 30],
        "advanced": [30, 80],
        "premium": [80, 250],
        "collection": [250, 1500],
    },
    "yellow_wine": {
        "daily": [30, 100],
        "advanced": [100, 300],
        "premium": [300, 800],
        "collection": [800, 5000],
    },
    "rice_wine": {
        "daily": [20, 80],
        "advanced": [80, 200],
        "premium": [200, 600],
        "collection": [600, 3000],
    },
}


# ============================================================
# 评分机构
# ============================================================

RATING_SOURCES = {
    "whisky": ["whisky_fun", "whisky_bible"],
    "baijiu": ["csl"],
    "brandy": ["wine_enthusiast"],
    "wine_red": ["parker", "wine_spectator", "james_suckling", "vivino", "cellar_tracker"],
    "wine_white": ["parker", "wine_spectator", "vivino", "cellar_tracker"],
    "wine_sparkling": ["wine_spectator", "vivino"],
    "wine_fortified": ["wine_spectator", "vivino"],
    "wine_rose": ["parker", "vivino"],
    "wine_dessert": ["parker", "wine_spectator"],
    "sake": ["sake_revue"],
    "gin": ["wine_enthusiast"],
    "vodka": ["wine_enthusiast"],
    "rum": ["wine_enthusiast"],
    "tequila": ["wine_enthusiast"],
    "liqueur": ["wine_enthusiast"],
    "beer": ["ratebeer"],
    "yellow_wine": ["csl", "vivino"],
    "rice_wine": ["csl"],
    "fruit_wine": ["wine_enthusiast", "vivino"],
    "mead": ["wine_enthusiast", "ratebeer"],
    "cocktail": ["diffords", "iba"],
    "other_spirit": [],
}


# ============================================================
# 奖项模板（按子类）
# ============================================================

AWARD_TEMPLATES = {
    "whisky": [
        ("ISC", ["Gold", "Silver", "Trophy"]),
        ("WWA", ["Best in Class", "Gold", "Silver"]),
        ("Malt Maniacs", ["Gold", "Silver"]),
    ],
    "baijiu": [
        ("布鲁塞尔大奖赛", ["大金奖", "金奖", "银奖"]),
        ("CMB", ["Gold", "Silver"]),
    ],
    "brandy": [
        ("ISC", ["Gold", "Silver"]),
        ("San Francisco", ["Gold", "Silver", "Double Gold"]),
    ],
    "wine_red": [
        ("Decanter", ["Gold", "Silver", "Bronze"]),
        ("IWSC", ["Gold", "Silver"]),
        ("Concours Mondial", ["Gold", "Silver"]),
    ],
    "wine_white": [
        ("Decanter", ["Gold", "Silver"]),
        ("IWSC", ["Gold", "Silver"]),
    ],
    "wine_sparkling": [
        ("Decanter", ["Gold", "Silver"]),
        ("IWSC", ["Gold", "Silver"]),
    ],
    "sake": [
        ("全国新酒鉴评会", ["金赏", "入赏"]),
        ("IWC", ["Gold", "Silver"]),
    ],
    "gin": [
        ("ISC", ["Gold", "Silver"]),
        ("San Francisco", ["Gold", "Silver"]),
    ],
    "tequila": [
        ("San Francisco", ["Gold", "Silver", "Double Gold"]),
    ],
    "rum": [
        ("ISC", ["Gold", "Silver"]),
        ("San Francisco", ["Gold", "Silver"]),
    ],
    "beer": [
        ("World Beer Cup", ["Gold", "Silver", "Bronze"]),
        ("WBA", ["Gold", "Silver"]),
    ],
    "yellow_wine": [
        ("布鲁塞尔大奖赛", ["金奖", "银奖"]),
        ("CMB", ["Gold", "Silver"]),
    ],
    "rice_wine": [
        ("全国酒类鉴评", ["金奖", "银奖"]),
    ],
    "fruit_wine": [
        ("IWSC", ["Gold", "Silver"]),
        ("San Francisco", ["Gold", "Silver"]),
    ],
    "mead": [
        ("Mazer Cup", ["Gold", "Silver", "Bronze"]),
    ],
    "cocktail": [
        ("Tales of the Cocktail", ["Best Cocktail", "Spirited Award"]),
        ("IBA World Competition", ["Gold", "Silver"]),
    ],
}


# ============================================================
# 鸡尾酒扩展字段定义
# ============================================================

# 鸡尾酒风格分类
COCKTAIL_STYLES = [
    "classic_iba",        # IBA 经典
    "classic_pre_prohibition",  # 禁酒令前
    "classic_prohibition",  # 禁酒令时代
    "classic_tiki",       # Tiki 经典
    "classic_sour",       # 酸酒
    "classic_julep",      # 薄荷茱莉普
    "classic_cobbler",    # 柯伯乐
    "classic_punch",      # 宾治
    "classic_flip",       # 翻转
    "classic_old_fashioned",  # 古典变体
    "signature_bartender",  # 调酒师签名
    "signature_bar",      # 酒吧签名
    "modern_classic",     # 现代经典
    "molecular_spherification",  # 球化
    "molecular_foam",     # 泡沫
    "molecular_nitrogen",  # 液氮
    "molecular_sous_vide",  # 真空低温
    "molecular_clarified",  # 澄清
]

# 调制技法
COCKTAIL_TECHNIQUES = [
    "shake",      # 摇和
    "stir",       # 搅和
    "blend",      # 搅拌
    "build",      # 直接注入
    "throw",      # 抛接
    "muddle",     # 捣碎
    "layer",      # 分层
    "smoke",      # 烟熏
]

# 难度星级
COCKTAIL_DIFFICULTY = {
    1: "入门（家庭可做）",
    2: "简单",
    3: "中等（需调酒基础）",
    4: "进阶（需专业设备）",
    5: "专业（酒吧级）",
}

# IBA 分类
IBA_CATEGORIES = [
    "The Unforgettables",  # 难忘系列
    "Contemporary Classics",  # 当代经典
    "New Era Drinks",  # 新时代饮品
]

# 分子技法
MOLECULAR_TECHNIQUES = [
    "spherification",        # 球化
    "reverse_spherification",  # 反向球化
    "foam",                  # 乳化泡沫
    "liquid_nitrogen",       # 液氮
    "sous_vide",             # 真空低温
    "centrifuge",            # 离心
    "clarified",             # 澄清
    "gelification",          # 胶化
    "fat_wash",              # 洗油
    "smoke_infusion",        # 烟熏浸渍
]

# 鸡尾酒扩展字段清单（供 render_kb.py 使用）
COCKTAIL_FIELDS = [
    "cocktail_style",        # 风格分类
    "recipe",                # 结构化配方表
    "garnish",               # 装饰
    "technique",             # 调制技法
    "difficulty",            # 难度（1-5）
    "creator",               # 创作者
    "year_created",          # 创制年份
    "iba_category",          # IBA 分类
    "flavor_profile",        # 5 维风味轮廓
    "abv_estimate",          # 估算酒精度
    "variations",            # 变体列表
    "molecular_technique",   # 分子技法
    "glass_size",            # 出品容量
    "serving_note",          # 饮用建议
]
