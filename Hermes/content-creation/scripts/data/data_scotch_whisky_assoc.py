"""Scotch Whisky Association官方类别定义数据。

数据源：Scotch Whisky Association (https://scotch-whisky.org.uk/)
置信度：official

覆盖：苏格兰威士忌5大法定类别 + 2024年出口数据
依据：UK law定义的Scotch Whisky Regulations 2009
"""

ENTRIES = [
    {
        "id": "ENT-whisky-swa-single-malt",
        "category": "ENT",
        "subcategory": "whisky",
        "title": "单一麦芽苏格兰威士忌 Single Malt Scotch Whisky",
        "title_en": "Single Malt Scotch Whisky",
        "name_cn": "单一麦芽苏格兰威士忌",
        "name_en": "Single Malt Scotch Whisky",
        "tags": ["威士忌", "苏格兰", "单一麦芽", "法规定义", "SWA"],
        "source": "Scotch Whisky Association / scotch-whisky.org.uk",
        "data_confidence": "official",
        "abv": "40%+",
        "country": "英国",
        "region": "苏格兰",
        "summary": "单一酒厂、仅水和发芽大麦、壶式蒸馏器批次蒸馏、必须在苏格兰装瓶的苏格兰威士忌。",
        "content_body": """## 法定定义

单一麦芽苏格兰威士忌（Single Malt Scotch Whisky）是指在**单一酒厂**内完成糖化、发酵和蒸馏的苏格兰威士忌，原料仅使用水和发芽大麦（malted barley），不得添加任何其他谷物，且必须使用**壶式蒸馏器（copper pot stills）**进行批次蒸馏。单一麦芽苏格兰威士忌必须在苏格兰装瓶。

## 法律依据

- **Scotch Whisky Regulations 2009**：英国法律定义的5大苏格兰威士忌类别之一
- **最低酒精度**：40% ABV
- **最低陈年**：在苏格兰的橡木桶中陈年至少3年

## 生产要求

| 要素 | 要求 |
|------|------|
| 原料 | 水 + 发芽大麦（不得添加其他谷物） |
| 蒸馏 | 壶式蒸馏器（copper pot stills）批次蒸馏 |
| 酒厂 | 必须在单一酒厂完成糖化、发酵、蒸馏 |
| 陈年 | 在苏格兰橡木桶中陈年≥3年 |
| 装瓶 | 必须在苏格兰装瓶 |
| 最低酒精度 | 40% ABV |

## 2024年出口数据

- **出口额**：£17亿（-17.2% vs 2023）
- **占全球出口比例**：31.0%（按价值计）
- **地位**：苏格兰威士忌第二大出口类别

## 代表品牌

- The Macallan（麦卡伦）
- Glenfiddich（格兰菲迪）
- Glenlivet（格兰威特）
- Lagavulin（乐加维林）
- Laphroaig（雅柏）

## 数据来源

- **来源**：Scotch Whisky Association（苏格兰威士忌协会）
- **官网**：https://scotch-whisky.org.uk/
- **法律依据**：The Scotch Whisky Regulations 2009
""",
    },
    {
        "id": "ENT-whisky-swa-blended",
        "category": "ENT",
        "subcategory": "whisky",
        "title": "调配型苏格兰威士忌 Blended Scotch Whisky",
        "title_en": "Blended Scotch Whisky",
        "name_cn": "调配型苏格兰威士忌",
        "name_en": "Blended Scotch Whisky",
        "tags": ["威士忌", "苏格兰", "调配", "法规定义", "SWA"],
        "source": "Scotch Whisky Association / scotch-whisky.org.uk",
        "data_confidence": "official",
        "abv": "40%+",
        "country": "英国",
        "region": "苏格兰",
        "summary": "一种或多种单一麦芽威士忌与一种或多种单一谷物威士忌的调配，是苏格兰威士忌最大出口类别。",
        "content_body": """## 法定定义

调配型苏格兰威士忌（Blended Scotch Whisky）是指将**一种或多种单一麦芽苏格兰威士忌**与**一种或多种单一谷物苏格兰威士忌**调配而成的苏格兰威士忌。

## 法律依据

- **Scotch Whisky Regulations 2009**
- **最低酒精度**：40% ABV
- **最低陈年**：在苏格兰的橡木桶中陈年至少3年

## 生产要求

| 要素 | 要求 |
|------|------|
| 原料 | 单一麦芽威士忌 + 单一谷物威士忌调配 |
| 调配 | 可来自不同酒厂的麦芽和谷物威士忌 |
| 陈年 | 在苏格兰橡木桶中陈年≥3年 |
| 最低酒精度 | 40% ABV |

## 2024年出口数据

- **瓶装出口额**：£32亿（+4.4% vs 2023）
- **占全球出口比例**：59.4%（按价值计）
- **地位**：苏格兰威士忌第一大出口类别
- **散装出口额**：£1.89亿（+9.1% vs 2023）

## 代表品牌

- Johnnie Walker（尊尼获加）
- Chivas Regal（芝华士）
- Ballantine's（百龄坛）
- Dewar's（帝王）
- Grant's（格兰）

## 数据来源

- **来源**：Scotch Whisky Association（苏格兰威士忌协会）
- **官网**：https://scotch-whisky.org.uk/
- **法律依据**：The Scotch Whisky Regulations 2009
""",
    },
    {
        "id": "ENT-whisky-swa-single-grain",
        "category": "ENT",
        "subcategory": "whisky",
        "title": "单一谷物苏格兰威士忌 Single Grain Scotch Whisky",
        "title_en": "Single Grain Scotch Whisky",
        "name_cn": "单一谷物苏格兰威士忌",
        "name_en": "Single Grain Scotch Whisky",
        "tags": ["威士忌", "苏格兰", "谷物", "法规定义", "SWA"],
        "source": "Scotch Whisky Association / scotch-whisky.org.uk",
        "data_confidence": "official",
        "abv": "40%+",
        "country": "英国",
        "region": "苏格兰",
        "summary": "在单一酒厂蒸馏、可含发芽大麦和其他谷物的苏格兰威士忌，不符合单一麦芽定义。",
        "content_body": """## 法定定义

单一谷物苏格兰威士忌（Single Grain Scotch Whisky）是指在**单一酒厂**内蒸馏的苏格兰威士忌，原料使用水和发芽大麦，可添加或不添加其他发芽或未发芽的谷物（如玉米、小麦、黑麦），且不符合单一麦芽苏格兰威士忌的定义。

## 法律依据

- **Scotch Whisky Regulations 2009**
- **最低酒精度**：40% ABV
- **最低陈年**：在苏格兰的橡木桶中陈年至少3年

## 生产要求

| 要素 | 要求 |
|------|------|
| 原料 | 水 + 发芽大麦 + 可选其他谷物（玉米/小麦/黑麦） |
| 蒸馏 | 通常使用柱式蒸馏器（continuous still） |
| 酒厂 | 必须在单一酒厂完成蒸馏 |
| 陈年 | 在苏格兰橡木桶中陈年≥3年 |
| 最低酒精度 | 40% ABV |

## 2024年出口数据

- **瓶装出口额**：£1400万（-45.3% vs 2023）
- **散装出口额**：£7400万（+37.9% vs 2023）
- **占全球出口比例**：0.3%（瓶装）/ 1.4%（散装）

## 代表品牌

- Cameronbrig（卡梅伦桥）
- Haig Club（黑格俱乐部）
- Compass Box（指南针盒，独立装瓶商）

## 数据来源

- **来源**：Scotch Whisky Association（苏格兰威士忌协会）
- **官网**：https://scotch-whisky.org.uk/
""",
    },
    {
        "id": "ENT-whisky-swa-blended-grain",
        "category": "ENT",
        "subcategory": "whisky",
        "title": "调配谷物苏格兰威士忌 Blended Grain Scotch Whisky",
        "title_en": "Blended Grain Scotch Whisky",
        "name_cn": "调配谷物苏格兰威士忌",
        "name_en": "Blended Grain Scotch Whisky",
        "tags": ["威士忌", "苏格兰", "谷物", "调配", "法规定义", "SWA"],
        "source": "Scotch Whisky Association / scotch-whisky.org.uk",
        "data_confidence": "official",
        "abv": "40%+",
        "country": "英国",
        "region": "苏格兰",
        "summary": "将来自多家酒厂的单一谷物威士忌调配而成的苏格兰威士忌。",
        "content_body": """## 法定定义

调配谷物苏格兰威士忌（Blended Grain Scotch Whisky）是指将**来自多家酒厂**（more than one distillery）的单一谷物苏格兰威士忌调配而成的苏格兰威士忌。

## 法律依据

- **Scotch Whisky Regulations 2009**
- **最低酒精度**：40% ABV
- **最低陈年**：在苏格兰的橡木桶中陈年至少3年

## 生产要求

| 要素 | 要求 |
|------|------|
| 原料 | 多家酒厂的单一谷物威士忌调配 |
| 调配 | 必须来自两家以上酒厂 |
| 陈年 | 在苏格兰橡木桶中陈年≥3年 |
| 最低酒精度 | 40% ABV |

## 市场地位

调配谷物苏格兰威士忌是市场上较为稀少的类别，主要面向威士忌爱好者和收藏家。

## 代表品牌

- Compass Box Hedonism（享乐主义）
- Johnnie Walker Select Casks Grain

## 数据来源

- **来源**：Scotch Whisky Association（苏格兰威士忌协会）
- **官网**：https://scotch-whisky.org.uk/
""",
    },
    {
        "id": "ENT-whisky-swa-blended-malt",
        "category": "ENT",
        "subcategory": "whisky",
        "title": "调配麦芽苏格兰威士忌 Blended Malt Scotch Whisky",
        "title_en": "Blended Malt Scotch Whisky",
        "name_cn": "调配麦芽苏格兰威士忌",
        "name_en": "Blended Malt Scotch Whisky",
        "tags": ["威士忌", "苏格兰", "麦芽", "调配", "法规定义", "SWA"],
        "source": "Scotch Whisky Association / scotch-whisky.org.uk",
        "data_confidence": "official",
        "abv": "40%+",
        "country": "英国",
        "region": "苏格兰",
        "summary": "将来自多家酒厂的单一麦芽威士忌或麦芽蒸馏酒调配而成的苏格兰威士忌。",
        "content_body": """## 法定定义

调配麦芽苏格兰威士忌（Blended Malt Scotch Whisky）是指将**两种或多种**来自不同酒厂的单一麦芽苏格兰威士忌调配而成，或将单一麦芽蒸馏酒调配而成的苏格兰威士忌。

## 法律依据

- **Scotch Whisky Regulations 2009**
- **最低酒精度**：40% ABV
- **最低陈年**：在苏格兰的橡木桶中陈年至少3年

## 生产要求

| 要素 | 要求 |
|------|------|
| 原料 | 多家酒厂的单一麦芽威士忌调配 |
| 调配 | 必须来自两家以上酒厂 |
| 陈年 | 在苏格兰橡木桶中陈年≥3年 |
| 最低酒精度 | 40% ABV |

## 2024年出口数据

- **瓶装出口额**：£1.03亿（-25.6% vs 2023）
- **散装出口额**：£1.37亿（+17.1% vs 2023）
- **占全球出口比例**：1.9%（瓶装）/ 2.5%（散装）

## 命名演变

- 旧称：vatted malt / pure malt
- 2009年起法定名称：Blended Malt Scotch Whisky
- 更名目的：避免消费者与"Blended Scotch Whisky"（含谷物威士忌）混淆

## 代表品牌

- Johnnie Walker Green Label（绿牌）
- Monkey Shoulder（猴子肩膀）
- Famous Grouse Malt（威雀麦芽）

## 数据来源

- **来源**：Scotch Whisky Association（苏格兰威士忌协会）
- **官网**：https://scotch-whisky.org.uk/
""",
    },
    {
        "id": "ENT-whisky-swa-export-2024",
        "category": "ENT",
        "subcategory": "whisky",
        "title": "苏格兰威士忌2024年出口数据 Scotch Whisky Exports 2024",
        "title_en": "Scotch Whisky Exports 2024",
        "name_cn": "苏格兰威士忌2024年出口数据",
        "name_en": "Scotch Whisky Exports 2024",
        "tags": ["威士忌", "苏格兰", "出口数据", "2024", "SWA", "行业报告"],
        "source": "Scotch Whisky Association / scotch-whisky.org.uk",
        "data_confidence": "official",
        "country": "英国",
        "region": "苏格兰",
        "summary": "2024年苏格兰威士忌全球出口数据按类别细分，瓶装调配威士忌占59.4%居首。",
        "content_body": """## 2024年苏格兰威士忌全球出口数据

苏格兰威士忌协会（SWA）发布的2024年出口统计数据，按类别细分（按价值计）：

## 按类别出口额

| 类别 | 出口额 | 同比变化 | 占比 |
|------|--------|---------|------|
| 瓶装调配 Blended (Bottled) | £32亿 | +4.4% | 59.4% |
| 单一麦芽 Single Malt | £17亿 | -17.2% | 31.0% |
| 散装调配 Blended (Bulk) | £1.89亿 | +9.1% | 3.5% |
| 散装调配麦芽 Blended Malt (Bulk) | £1.37亿 | +17.1% | 2.5% |
| 瓶装调配麦芽 Blended Malt (Bottled) | £1.03亿 | -25.6% | 1.9% |
| 散装单一及调配谷物 Single & Blended Grain (Bulk) | £7400万 | +37.9% | 1.4% |
| 瓶装单一及调配谷物 Single & Blended Grain (Bottled) | £1400万 | -45.3% | 0.3% |

## 关键趋势

1. **瓶装调配威士忌**仍是绝对主力，占近60%出口额
2. **单一麦芽**虽有17.2%下滑，但仍占31%份额，是第二大类别
3. **散装类别**整体增长强劲，尤其散装谷物威士忌+37.9%
4. 瓶装小众类别（调配麦芽、谷物）下滑明显

## 数据来源

- **来源**：Scotch Whisky Association（苏格兰威士忌协会）
- **官网**：https://scotch-whisky.org.uk/
- **数据年份**：2024年全年
""",
    },
]
