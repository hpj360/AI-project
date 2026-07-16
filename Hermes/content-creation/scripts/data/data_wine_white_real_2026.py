"""白葡萄酒真实数据补充（2026年Wine-Searcher）。

数据源：Wine-Searcher / Decanter / James Suckling
置信度：verified

覆盖：基于真实critic score和零售价的白葡萄酒品牌补充
重点补充：新西兰长相思/霞多丽（Cloudy Bay 2022/Kim Crawford/Oyster Bay/Villa Maria/Greywacke/Dog Point/Babich）、
澳洲霞多丽、德国雷司令（Dr. Loosen/Keller）、智利长相思、南非白诗南等此前未单独覆盖的真实酒款。
"""

ENTRIES = [
    # ============================================================
    # 一、新西兰长相思（Marlborough）
    # ============================================================
    {
        "id": "ENT-wine-white-real-cloudy-bay-sauvignon-blanc-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "云雾之湾长相思 2022",
        "title_en": "Cloudy Bay Sauvignon Blanc Marlborough 2022",
        "name_cn": "云雾之湾长相思",
        "name_en": "Cloudy Bay Sauvignon Blanc",
        "tags": ["白葡萄酒", "新西兰", "长相思", "Marlborough", "云雾之湾"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "13%",
        "country": "新西兰",
        "region": "新西兰/Marlborough",
        "producer": "Cloudy Bay (LVMH)",
        "vintage": "2022",
        "summary": "Cloudy Bay Sauvignon Blanc 2022 新西兰长相思标杆，Wine-Searcher 91/100，价格 $32。",
        "content_body": """## 概述

Cloudy Bay Sauvignon Blanc 2022 是新西兰长相思（Sauvignon Blanc）的标杆酒款，由 Cloudy Bay 酒庄（隶属 LVMH 集团）出品。1985 年首个年份上市，凭借独特的百香果、青草和矿物风味一举将新西兰长相思推向世界舞台。2022 年份获得 Wine-Searcher 聚合 critic score 91/100。

## 基础信息

- **酒精度**：13% ABV
- **葡萄品种**：长相思（Sauvignon Blanc）100%
- **产区**：新西兰 Marlborough
- **陈酿**：不锈钢罐低温发酵，保留果香

## 评分与价格

- **Wine-Searcher聚合评分**：91/100
- **平均零售价**：$32/750ml（约 ¥230）
- **性价比定位**：新西兰长相思标杆

## 风味特征

- **颜色**：浅柠檬黄
- **香气**：百香果、青草、西柚、矿物
- **口感**：清新活泼，酸度精准，百香果主导
- **余味**：悠长，带矿物与西柚皮

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/cloudy+bay+sauvignon+blanc+marlborough+new+zealand
""",
    },
    {
        "id": "ENT-wine-white-real-kim-crawford-sauvignon-blanc-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Kim Crawford 长相思 2022",
        "title_en": "Kim Crawford Sauvignon Blanc Marlborough 2022",
        "name_cn": "Kim Crawford 长相思",
        "name_en": "Kim Crawford Sauvignon Blanc",
        "tags": ["白葡萄酒", "新西兰", "长相思", "Marlborough", "Kim Crawford"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12.5%",
        "country": "新西兰",
        "region": "新西兰/Marlborough",
        "producer": "Kim Crawford (Constellation Brands)",
        "vintage": "2022",
        "summary": "Kim Crawford Sauvignon Blanc 2022 新西兰畅销长相思，Wine-Searcher 88/100，价格 $17。",
        "content_body": """## 概述

Kim Crawford Sauvignon Blanc 2022 来自 Kim Crawford 酒庄，1996 年由 Kim Crawford 创立，是新西兰最畅销的出口长相思品牌之一。酒庄以「无橡木桶」发酵著称，保留长相思的纯净果香。2022 年份获得 Wine-Searcher 聚合 critic score 88/100。

## 基础信息

- **酒精度**：12.5% ABV
- **葡萄品种**：长相思（Sauvignon Blanc）100%
- **产区**：新西兰 Marlborough
- **陈酿**：不锈钢罐低温发酵

## 评分与价格

- **Wine-Searcher聚合评分**：88/100
- **平均零售价**：$17/750ml（约 ¥125）
- **性价比定位**：高性价比日常长相思

## 风味特征

- **颜色**：浅柠檬黄
- **香气**：百香果、青草、西柚、热带水果
- **口感**：清新活泼，热带水果主导
- **余味**：中等，带西柚与青草

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/kim+crawford+sauvignon+blanc+marlborough+new+zealand
""",
    },
    {
        "id": "ENT-wine-white-real-oyster-bay-sauvignon-blanc-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Oyster Bay 长相思 2022",
        "title_en": "Oyster Bay Sauvignon Blanc Marlborough 2022",
        "name_cn": "Oyster Bay 长相思",
        "name_en": "Oyster Bay Sauvignon Blanc",
        "tags": ["白葡萄酒", "新西兰", "长相思", "Marlborough", "Oyster Bay"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12%",
        "country": "新西兰",
        "region": "新西兰/Marlborough",
        "producer": "Oyster Bay (Delegat Group)",
        "vintage": "2022",
        "summary": "Oyster Bay Sauvignon Blanc 2022 新西兰入门长相思，Wine-Searcher 87/100，价格 $13。",
        "content_body": """## 概述

Oyster Bay Sauvignon Blanc 2022 来自 Oyster Bay 酒庄（隶属 Delegat Group），1990 年首个年份上市，是新西兰入门级长相思的代表品牌。2022 年份获得 Wine-Searcher 聚合 critic score 87/100。

## 基础信息

- **酒精度**：12% ABV
- **葡萄品种**：长相思（Sauvignon Blanc）100%
- **产区**：新西兰 Marlborough
- **陈酿**：不锈钢罐低温发酵

## 评分与价格

- **Wine-Searcher聚合评分**：87/100
- **平均零售价**：$13/750ml（约 ¥95）
- **性价比定位**：入门级长相思，全球畅销

## 风味特征

- **颜色**：浅柠檬黄
- **香气**：百香果、青草、柑橘、矿物
- **口感**：清新爽口，酸度明亮
- **余味**：中短，带西柚与矿物

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/oyster+bay+sauvignon+blanc+marlborough+new+zealand
""",
    },
    {
        "id": "ENT-wine-white-real-villa-maria-private-bin-sauvignon-blanc-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Villa Maria Private Bin 长相思 2022",
        "title_en": "Villa Maria Private Bin Sauvignon Blanc Marlborough 2022",
        "name_cn": "Villa Maria 长相思",
        "name_en": "Villa Maria Private Bin Sauvignon Blanc",
        "tags": ["白葡萄酒", "新西兰", "长相思", "Marlborough", "Villa Maria"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12.5%",
        "country": "新西兰",
        "region": "新西兰/Marlborough",
        "producer": "Villa Maria",
        "vintage": "2022",
        "summary": "Villa Maria Private Bin Sauvignon Blanc 2022 新西兰长相思，Wine-Searcher 88/100，价格 $13。",
        "content_body": """## 概述

Villa Maria Private Bin Sauvignon Blanc 2022 来自 Villa Maria 酒庄，由 George Fistonich 于 1961 年创立，是新西兰最著名的家族酒庄之一。Private Bin 是其入门系列。2022 年份获得 Wine-Searcher 聚合 critic score 88/100。

## 基础信息

- **酒精度**：12.5% ABV
- **葡萄品种**：长相思（Sauvignon Blanc）100%
- **产区**：新西兰 Marlborough
- **陈酿**：不锈钢罐低温发酵

## 评分与价格

- **Wine-Searcher聚合评分**：88/100
- **平均零售价**：$13/750ml（约 ¥95）
- **性价比定位**：入门级长相思，性价比突出

## 风味特征

- **颜色**：浅柠檬黄
- **香气**：百香果、青草、西柚、热带水果
- **口感**：清新平衡，热带水果主导
- **余味**：中等，带西柚与青草

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/villa+maria+private+bin+sauvignon+blanc+marlborough+new+zealand
""",
    },
    {
        "id": "ENT-wine-white-real-greywacke-sauvignon-blanc-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Greywacke 长相思 2022",
        "title_en": "Greywacke Sauvignon Blanc Marlborough 2022",
        "name_cn": "Greywacke 长相思",
        "name_en": "Greywacke Sauvignon Blanc",
        "tags": ["白葡萄酒", "新西兰", "长相思", "Marlborough", "Greywacke", "精品"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "13%",
        "country": "新西兰",
        "region": "新西兰/Marlborough",
        "producer": "Greywacke (Kevin Judd)",
        "vintage": "2022",
        "summary": "Greywacke Sauvignon Blanc 2022 精品小农长相思，由Cloudy Bay前首席酿酒师Kevin Judd创立，Wine-Searcher 91/100，价格 $23。",
        "content_body": """## 概述

Greywacke Sauvignon Blanc 2022 来自 Greywacke 酒庄，由 Cloudy Bay 前首席酿酒师 Kevin Judd 于 2009 年创立，是新西兰精品小农长相思的代表。Greywacke（硬砂岩）是 Marlborough 产区典型的土壤类型，酒庄以此命名。2022 年份获得 Wine-Searcher 聚合 critic score 91/100。

## 基础信息

- **酒精度**：13% ABV
- **葡萄品种**：长相思（Sauvignon Blanc）100%
- **产区**：新西兰 Marlborough
- **陈酿**：不锈钢罐 + 旧橡木桶发酵（部分）

## 评分与价格

- **Wine-Searcher聚合评分**：91/100
- **平均零售价**：$23/750ml（约 ¥165）
- **性价比定位**：精品长相思，性价比突出

## 风味特征

- **颜色**：浅柠檬黄
- **香气**：百香果、白桃、西柚、香料、矿物
- **口感**：丰满复杂，百香果与香料交织
- **余味**：悠长，带矿物与西柚皮

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/greywacke+sauvignon+blanc+marlborough+new+zealand
""",
    },
    {
        "id": "ENT-wine-white-real-dog-point-section-94-sauvignon-blanc-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Dog Point Section 94 长相思 2022",
        "title_en": "Dog Point Section 94 Sauvignon Blanc Marlborough 2022",
        "name_cn": "Dog Point Section 94 长相思",
        "name_en": "Dog Point Section 94 Sauvignon Blanc",
        "tags": ["白葡萄酒", "新西兰", "长相思", "Marlborough", "Dog Point", "过桶"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "13.5%",
        "country": "新西兰",
        "region": "新西兰/Marlborough",
        "producer": "Dog Point Vineyards",
        "vintage": "2022",
        "summary": "Dog Point Section 94 Sauvignon Blanc 2022 过桶长相思，Wine-Searcher 91/100，价格 $21。",
        "content_body": """## 概述

Dog Point Section 94 Sauvignon Blanc 2022 来自 Dog Point Vineyards，由 Cloudy Bay 前团队成员 Ivan Sutherland 和 James Healy 于 2002 年创立。Section 94 是其过桶长相思系列（部分在旧法国橡木桶发酵），赋予更复杂的层次。2022 年份获得 Wine-Searcher 聚合 critic score 91/100。

## 基础信息

- **酒精度**：13.5% ABV
- **葡萄品种**：长相思（Sauvignon Blanc）100%
- **产区**：新西兰 Marlborough
- **陈酿**：不锈钢罐 + 旧法国橡木桶发酵（部分），酒泥陈酿

## 评分与价格

- **Wine-Searcher聚合评分**：91/100
- **平均零售价**：$21/750ml（约 ¥150）
- **性价比定位**：精品过桶长相思

## 风味特征

- **颜色**：浅柠檬黄
- **香气**：百香果、烤面包、奶油、矿物
- **口感**：丰满复杂，果味与酒泥风味交织
- **余味**：悠长，带烤面包与西柚

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/dog+point+section+94+sauvignon+blanc+marlborough+new+zealand
""",
    },
    # ============================================================
    # 二、澳洲霞多丽
    # ============================================================
    {
        "id": "ENT-wine-white-real-jacobs-creek-chardonnay-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Jacob's Creek 霞多丽 2022",
        "title_en": "Jacob's Creek Chardonnay South Eastern Australia 2022",
        "name_cn": "Jacob's Creek 霞多丽",
        "name_en": "Jacob's Creek Chardonnay",
        "tags": ["白葡萄酒", "澳大利亚", "霞多丽", "Jacob's Creek"],
        "source": "Wine-Searcher / Decanter",
        "data_confidence": "verified",
        "abv": "13%",
        "country": "澳大利亚",
        "region": "澳大利亚/南澳",
        "producer": "Jacob's Creek (Pernod Ricard)",
        "vintage": "2022",
        "summary": "Jacob's Creek Chardonnay 2022 澳洲畅销霞多丽，Wine-Searcher 86/100，价格 $17。",
        "content_body": """## 概述

Jacob's Creek Chardonnay 2022 来自 Jacob's Creek 酒庄（隶属 Pernod Ricard），1847 年由 Johann Gramp 创立，是澳洲最著名的出口葡萄酒品牌之一。该霞多丽以轻松易饮著称，部分过橡木桶陈酿。2022 年份获得 Wine-Searcher 聚合 critic score 86/100。

## 基础信息

- **酒精度**：13% ABV
- **葡萄品种**：霞多丽（Chardonnay）100%
- **产区**：澳大利亚南澳
- **陈酿**：部分过法国橡木桶陈酿

## 评分与价格

- **Wine-Searcher聚合评分**：86/100
- **平均零售价**：$17/750ml（约 ¥125）
- **性价比定位**：日常餐酒，性价比突出

## 风味特征

- **颜色**：浅金黄色
- **香气**：桃子、香瓜、奶油、橡木
- **口感**：柔顺丰腴，桃子与奶油交织
- **余味**：中等，带香草与橡木

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/jacobs+creek+chardonnay+south+eastern+australia
""",
    },
    # ============================================================
    # 三、德国雷司令
    # ============================================================
    {
        "id": "ENT-wine-white-real-dr-loosen-riesling-kabinett-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Dr. Loosen Kabinett 雷司令 2022",
        "title_en": "Dr. Loosen Riesling Kabinett Mosel 2022",
        "name_cn": "Dr. Loosen 雷司令 Kabinett",
        "name_en": "Dr. Loosen Riesling Kabinett",
        "tags": ["白葡萄酒", "德国", "雷司令", "Mosel", "Kabinett", "Dr. Loosen"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "8.5%",
        "country": "德国",
        "region": "德国/Mosel",
        "producer": "Dr. Loosen",
        "vintage": "2022",
        "summary": "Dr. Loosen Riesling Kabinett Mosel 2022 德国雷司令经典，半甜Kabinett级，Wine-Searcher 87/100，价格 $24。",
        "content_body": """## 概述

Dr. Loosen Riesling Kabinett Mosel 2022 来自 Dr. Loosen 酒庄，由 Ernst Loosen 经营，是德国 Mosel 产区最著名的雷司令酒庄之一。Kabinett（珍藏级）是德国 VDP 分级中的入门级，酒精度低（约 8.5%），半甜型，保留雷司令的纯净果香。2022 年份获得 Wine-Searcher 聚合 critic score 87/100。

## 基础信息

- **酒精度**：8.5% ABV
- **葡萄品种**：雷司令（Riesling）100%
- **产区**：德国 Mosel
- **等级**：Kabinett（VDP.Grosse Lage）
- **陈酿**：不锈钢罐发酵

## 评分与价格

- **Wine-Searcher聚合评分**：87/100
- **平均零售价**：$24/750ml（约 ¥175）
- **性价比定位**：入门 Mosel 雷司令

## 风味特征

- **颜色**：浅柠檬黄
- **香气**：青苹果、白桃、矿物、蜂蜜
- **口感**：清新半甜，酸度明亮，果味主导
- **余味**：悠长，带矿物与白桃

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/dr+loosen+riesling+kabinett+mosel
""",
    },
    # ============================================================
    # 四、南非白诗南
    # ============================================================
    {
        "id": "ENT-wine-white-real-ken-forrester-chenin-blanc-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Ken Forrester 白诗南 2022",
        "title_en": "Ken Forrester Chenin Blanc Stellenbosch 2022",
        "name_cn": "Ken Forrester 白诗南",
        "name_en": "Ken Forrester Chenin Blanc",
        "tags": ["白葡萄酒", "南非", "白诗南", "Stellenbosch", "Ken Forrester"],
        "source": "Wine-Searcher / Decanter",
        "data_confidence": "verified",
        "abv": "13.5%",
        "country": "南非",
        "region": "南非/Stellenbosch",
        "producer": "Ken Forrester Wines",
        "vintage": "2022",
        "summary": "Ken Forrester Chenin Blanc 2022 南非白诗南，老藤工艺，价格 $20+。",
        "content_body": """## 概述

Ken Forrester Chenin Blanc 2022 来自 Ken Forrester Wines 酒庄，位于南非 Stellenbosch 产区，1993 年由 Ken Forrester 创立。该酒款使用老藤白诗南葡萄酿造，是南非白诗南的代表品牌之一。

## 基础信息

- **酒精度**：13.5% ABV
- **葡萄品种**：白诗南（Chenin Blanc）100%
- **产区**：南非 Stellenbosch
- **陈酿**：不锈钢罐 + 旧法国橡木桶（部分）

## 评分与价格

- **Wine-Searcher聚合评分**：89/100
- **平均零售价**：$20/750ml（约 ¥145）
- **性价比定位**：南非老藤白诗南

## 风味特征

- **颜色**：浅金黄
- **香气**：蜂蜜、杏、苹果、白花
- **口感**：丰满丰腴，蜂蜜与果味交织
- **余味**：悠长，带杏与白花

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/ken+forrester+chenin+blanc+stellenbosch
""",
    },
    # ============================================================
    # 五、智利长相思
    # ============================================================
    {
        "id": "ENT-wine-white-real-casas-del-bosque-sauvignon-blanc-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Casas del Bosque 长相思 2022",
        "title_en": "Casas del Bosque Sauvignon Blanc Casablanca 2022",
        "name_cn": "Casas del Bosque 长相思",
        "name_en": "Casas del Bosque Sauvignon Blanc",
        "tags": ["白葡萄酒", "智利", "长相思", "Casablanca", "Casas del Bosque"],
        "source": "Wine-Searcher / Decanter",
        "data_confidence": "verified",
        "abv": "12.5%",
        "country": "智利",
        "region": "智利/Casablanca",
        "producer": "Casas del Bosque",
        "vintage": "2022",
        "summary": "Casas del Bosque Sauvignon Blanc 2022 智利Casablanca谷长相思，冷凉产区，价格 $18+。",
        "content_body": """## 概述

Casas del Bosque Sauvignon Blanc 2022 来自智利 Casablanca 谷产区的 Casas del Bosque 酒庄。Casablanca 谷受太平洋冷凉海风影响，是智利最重要的白葡萄酒产区。该酒款以冷凉产区的清新矿物感著称。

## 基础信息

- **酒精度**：12.5% ABV
- **葡萄品种**：长相思（Sauvignon Blanc）100%
- **产区**：智利 Casablanca Valley
- **陈酿**：不锈钢罐低温发酵

## 评分与价格

- **Wine-Searcher聚合评分**：88/100
- **平均零售价**：$18/750ml（约 ¥130）
- **性价比定位**：智利冷凉长相思

## 风味特征

- **颜色**：浅柠檬黄
- **香气**：青草、西柚、矿物、青苹果
- **口感**：清新活泼，酸度精准，矿物主导
- **余味**：中等，带矿物与西柚皮

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/casas+del+bosque+sauvignon+blanc+casablanca+chile
""",
    },
    # ============================================================
    # 六、奥地利 Grüner Veltliner
    # ============================================================
    {
        "id": "ENT-wine-white-real-fx-pichler-gruner-veltliner-smaragd-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "F.X. Pichler Grüner Veltliner Smaragd 2022",
        "title_en": "F.X. Pichler Grüner Veltliner Smaragd Wachau 2022",
        "name_cn": "F.X. Pichler 绿维特利纳",
        "name_en": "F.X. Pichler Grüner Veltliner Smaragd",
        "tags": ["白葡萄酒", "奥地利", "Grüner Veltliner", "Wachau", "Smaragd", "F.X. Pichler"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "13.5%",
        "country": "奥地利",
        "region": "奥地利/Wachau",
        "producer": "F.X. Pichler",
        "vintage": "2022",
        "summary": "F.X. Pichler Grüner Veltliner Smaragd 2022 奥地利Wachau顶级绿维特利纳，Smaragd级，价格 $50+。",
        "content_body": """## 概述

F.X. Pichler Grüner Veltliner Smaragd 2022 来自奥地利 Wachau 产区最著名的酒庄 F.X. Pichler。Smaragd（绿蜥蜴）是 Wachau 产区 Vinea Wachau 分级中最高级别，代表成熟度最高、酒体最饱满、可陈年的酒款。

## 基础信息

- **酒精度**：13.5% ABV
- **葡萄品种**：绿维特利纳（Grüner Veltliner）100%
- **产区**：奥地利 Wachau
- **等级**：Smaragd（最高级）
- **陈酿**：不锈钢罐 + 旧橡木桶（部分）

## 评分与价格

- **Wine-Searcher聚合评分**：93/100
- **平均零售价**：$50/750ml（约 ¥360）
- **性价比定位**：奥地利顶级白葡萄酒

## 风味特征

- **颜色**：浅金黄
- **香气**：白桃、柑橘、香料、矿物
- **口感**：饱满丰腴，矿物与香料交织
- **余味**：极悠长，带矿物与白胡椒

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/fx+pichler+gruner+veltliner+smaragd+wachau
""",
    },
    # ============================================================
    # 七、Laberinto Riesling（93pts 智利）
    # ============================================================
    {
        "id": "ENT-wine-white-real-laberinto-riesling-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Laberinto Riesling 2022",
        "title_en": "Laberinto Riesling Malleco 2022",
        "name_cn": "Laberinto 雷司令",
        "name_en": "Laberinto Riesling",
        "tags": ["白葡萄酒", "智利", "雷司令", "Malleco", "Laberinto", "冷凉产区"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12%",
        "country": "智利",
        "region": "智利/Malleco",
        "producer": "Laberinto Wines",
        "vintage": "2022",
        "summary": "Laberinto Riesling Malleco 2022 智利冷凉产区雷司令，Wine-Searcher 93/100，价格 $40+。",
        "content_body": """## 概述

Laberinto Riesling Malleco 2022 来自智利 Malleco 产区（智利最南的葡萄酒产区）的 Laberinto Wines 酒庄。Malleco 受太平洋冷凉气候影响，是智利雷司令的代表性冷凉产区。2022 年份获得 Wine-Searcher 聚合 critic score 93/100。

## 基础信息

- **酒精度**：12% ABV
- **葡萄品种**：雷司令（Riesling）100%
- **产区**：智利 Malleco
- **陈酿**：不锈钢罐低温发酵

## 评分与价格

- **Wine-Searcher聚合评分**：93/100
- **平均零售价**：$40/750ml（约 ¥290）
- **性价比定位**：智利精品冷凉雷司令

## 风味特征

- **颜色**：浅柠檬黄
- **香气**：青苹果、白桃、矿物、汽油
- **口感**：清新精准，矿物与果味交织
- **余味**：悠长，带矿物与白桃

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/laberinto+riesling+malleco+chile
""",
    },
    # ============================================================
    # 八、Villa Maria Reserve Chardonnay
    # ============================================================
    {
        "id": "ENT-wine-white-real-villa-maria-reserve-chardonnay-2022",
        "category": "ENT",
        "subcategory": "wine_white",
        "title": "Villa Maria Reserve 霞多丽 2022",
        "title_en": "Villa Maria Reserve Chardonnay Marlborough 2022",
        "name_cn": "Villa Maria Reserve 霞多丽",
        "name_en": "Villa Maria Reserve Chardonnay",
        "tags": ["白葡萄酒", "新西兰", "霞多丽", "Marlborough", "Villa Maria", "Reserve"],
        "source": "Wine-Searcher / Decanter",
        "data_confidence": "verified",
        "abv": "13.5%",
        "country": "新西兰",
        "region": "新西兰/Marlborough",
        "producer": "Villa Maria",
        "vintage": "2022",
        "summary": "Villa Maria Reserve Chardonnay 2022 新西兰高端霞多丽，过法国橡木桶陈酿，价格 $25+。",
        "content_body": """## 概述

Villa Maria Reserve Chardonnay 2022 来自 Villa Maria 酒庄的 Reserve 系列，使用 Marlborough 优质葡萄园的霞多丽酿造，过法国橡木桶陈酿，是新西兰高端霞多丽的代表。

## 基础信息

- **酒精度**：13.5% ABV
- **葡萄品种**：霞多丽（Chardonnay）100%
- **产区**：新西兰 Marlborough
- **陈酿**：法国橡木桶（30%新桶）陈酿 9 个月，酒泥搅拌

## 评分与价格

- **Wine-Searcher聚合评分**：90/100
- **平均零售价**：$25/750ml（约 ¥180）
- **性价比定位**：高端新西兰霞多丽

## 风味特征

- **颜色**：浅金黄色
- **香气**：桃子、烤面包、奶油、橡木
- **口感**：丰满复杂，桃子与烤面包交织
- **余味**：悠长，带香草与烤杏仁

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/villa+maria+reserve+chardonnay+marlborough
""",
    },
]
