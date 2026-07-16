"""Wine-Searcher/VinePair 2026年葡萄酒评分数据补充。

数据源：Wine-Searcher / VinePair
置信度：verified

覆盖：从Wine-Searcher和VinePair 2026年度榜单获取的真实critic scores和价格数据
重点补充：意大利超级托斯卡纳、纳帕谷顶级赤霞珠、罗讷河谷西拉等此前未覆盖的品牌
"""

ENTRIES = [
    # ============================================================
    # 一、意大利超级托斯卡纳（Wine-Searcher真实评分）
    # ============================================================
    {
        "id": "ENT-wine-red-sassicaia-2021",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "西施佳雅 2021",
        "title_en": "Tenuta San Guido Sassicaia Bolgheri 2021",
        "name_cn": "西施佳雅",
        "name_en": "Sassicaia",
        "tags": ["葡萄酒", "红葡萄酒", "意大利", "超级托斯卡纳", "西施佳雅", "Bolgheri"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "13.5%",
        "country": "意大利",
        "region": "托斯卡纳/Bolgheri",
        "producer": "Tenuta San Guido",
        "vintage": "2021",
        "summary": "西施佳雅是意大利超级托斯卡纳的鼻祖，Wine-Searcher热度排名第10，critic score 96/100。",
        "content_body": """## 概述

西施佳雅（Sassicaia）由Tenuta San Guido酒庄出品，是意大利超级托斯卡纳（Super Tuscan）运动的先驱。1968年首个年份上市，以赤霞珠为主的波尔多混酿风格打破了意大利传统分级体系，最终促成Bolgheri DOC产区的创建。2021年份获得Wine-Searcher聚合critic score 96/100。

## 基础信息

- **酒精度**：13.5% ABV
- **葡萄品种**：赤霞珠85%、品丽珠15%
- **产区**：托斯卡纳/Bolgheri DOC
- **陈年**：法国橡木桶（1/3新桶）陈年24个月
- **年产量**：约15万瓶

## 评分

- **Wine-Searcher聚合评分**：96/100
- **热度排名**：Wine-Searcher全球第10位
- **平均零售价**：€330/750ml

## 风味特征

- **颜色**：深宝石红
- **香气**：黑醋栗、雪松、香料、烟草、薄荷
- **口感**：优雅细腻，单宁紧致，骨架分明
- **余味**：悠长矿物与香料感

## 陈年潜力

- **适饮期**：2026-2040+
- **最佳年份**：1985, 1990, 1998, 2001, 2006, 2010, 2015, 2016, 2018, 2021

## 酒庄历史

- **1940年代**：Mario Incisa della Rocchetta引入赤霞珠
- **1968年**：首个商业年份上市
- **1994年**：Bolgheri DOC产区创建，Sassicaia拥有独立子产区

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/tenute+st+guido+sassicaia+bolgheri+tuscany+italy
""",
    },
    {
        "id": "ENT-wine-red-tignanello-2021",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "天娜 2021",
        "title_en": "Marchesi Antinori Tignanello Toscana IGT 2021",
        "name_cn": "天娜",
        "name_en": "Tignanello",
        "tags": ["葡萄酒", "红葡萄酒", "意大利", "超级托斯卡纳", "天娜", "Antinori"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "14%",
        "country": "意大利",
        "region": "托斯卡纳/Chianti Classico",
        "producer": "Marchesi Antinori",
        "vintage": "2021",
        "summary": "天娜是Antinori家族的超级托斯卡纳旗舰，以桑娇维赛为主的混酿，Wine-Searcher热度排名第35，critic score 95/100。",
        "content_body": """## 概述

天娜（Tignanello）由Marchesi Antinori酒庄出品，1971年首个年份上市，是意大利超级托斯卡纳的另一先驱。以桑娇维赛为主，混酿赤霞珠和品丽珠，打破了Chianti传统配方规则。2021年份获得Wine-Searcher聚合critic score 95/100。

## 基础信息

- **酒精度**：14% ABV
- **葡萄品种**：桑娇维赛80%、赤霞珠15%、品丽珠5%
- **产区**：托斯卡纳/Toscana IGT
- **陈年**：法国橡木桶陈年12-14个月
- **年产量**：约30万瓶

## 评分

- **Wine-Searcher聚合评分**：95/100
- **热度排名**：Wine-Searcher全球第35位
- **平均零售价**：€167/750ml

## 风味特征

- **颜色**：深宝石红
- **香气**：红樱桃、黑莓、紫罗兰、香料、烟草
- **口感**：饱满丰富，单宁细腻，酸度明亮
- **余味**：悠长果味与香料感

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/marchesi+antinori+tignanello+tuscany+igp+italy
""",
    },
    {
        "id": "ENT-wine-red-masseto-2021",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "马赛托 2021",
        "title_en": "Masseto Toscana IGT 2021",
        "name_cn": "马赛托",
        "name_en": "Masseto",
        "tags": ["葡萄酒", "红葡萄酒", "意大利", "超级托斯卡纳", "马赛托", "100%美乐"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "14.5%",
        "country": "意大利",
        "region": "托斯卡纳/Bolgheri",
        "producer": "Frescobaldi家族",
        "vintage": "2021",
        "summary": "马赛托是意大利最著名的100%美乐葡萄酒，Wine-Searcher热度排名第58，critic score 97/100，价格€909。",
        "content_body": """## 概述

马赛托（Masseto）由Frescobaldi家族出品，是意大利最著名的100%美乐葡萄酒。灵感来源于柏图斯，产于Bolgheri海岸的Masseto单一葡萄园。2021年份获得Wine-Searcher聚合critic score 97/100。

## 基础信息

- **酒精度**：14.5% ABV
- **葡萄品种**：美乐100%
- **产区**：托斯卡纳/Toscana IGT
- **陈年**：法国橡木桶（100%新桶）陈年24个月
- **年产量**：约3.5万瓶

## 评分

- **Wine-Searcher聚合评分**：97/100
- **热度排名**：Wine-Searcher全球第58位
- **平均零售价**：€909/750ml

## 风味特征

- **颜色**：深紫红色
- **香气**：黑李子、黑巧克力、紫罗兰、松露、香料
- **口感**：饱满丰腴，单宁如丝绒，浓郁如奶油
- **余味**：悠长松露与黑巧感

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/masseto+tuscany+igp+italy
""",
    },
    {
        "id": "ENT-wine-red-ornellaia-2021",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "奥纳亚 2021",
        "title_en": "Ornellaia Bolgheri Superiore 2021",
        "name_cn": "奥纳亚",
        "name_en": "Ornellaia",
        "tags": ["葡萄酒", "红葡萄酒", "意大利", "超级托斯卡纳", "奥纳亚", "Bolgheri"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "14%",
        "country": "意大利",
        "region": "托斯卡纳/Bolgheri",
        "producer": "Frescobaldi家族",
        "vintage": "2021",
        "summary": "奥纳亚是Bolgheri产区另一顶级超级托斯卡纳，Wine-Searcher热度排名第59，critic score 95/100。",
        "content_body": """## 概述

奥纳亚（Ornellaia）由Frescobaldi家族出品，是Bolgheri产区与西施佳雅齐名的顶级超级托斯卡纳。1985年首个年份上市，以波尔多混酿风格著称。2021年份获得Wine-Searcher聚合critic score 95/100。

## 基础信息

- **酒精度**：14% ABV
- **葡萄品种**：赤霞珠、美乐、品丽珠、小维多混酿
- **产区**：托斯卡纳/Bolgheri DOC
- **陈年**：法国橡木桶（70%新桶）陈年18个月
- **年产量**：约15万瓶

## 评分

- **Wine-Searcher聚合评分**：95/100
- **热度排名**：Wine-Searcher全球第59位
- **平均零售价**：€243/750ml

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
""",
    },
    {
        "id": "ENT-wine-red-solaia-2021",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "索拉雅 2021",
        "title_en": "Marchesi Antinori Solaia Toscana IGT 2021",
        "name_cn": "索拉雅",
        "name_en": "Solaia",
        "tags": ["葡萄酒", "红葡萄酒", "意大利", "超级托斯卡纳", "索拉雅", "Antinori"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "14%",
        "country": "意大利",
        "region": "托斯卡纳/Chianti Classico",
        "producer": "Marchesi Antinori",
        "vintage": "2021",
        "summary": "索拉雅是Antinori家族的另一超级托斯卡纳旗舰，以赤霞珠为主，Wine-Searcher热度排名第83，critic score 96/100。",
        "content_body": """## 概述

索拉雅（Solaia）由Marchesi Antinori酒庄出品，是天娜的姐妹酒款，产自同一葡萄园的向阳坡地。1978年首个年份上市，以赤霞珠为主的混酿。2021年份获得Wine-Searcher聚合critic score 96/100。

## 基础信息

- **酒精度**：14% ABV
- **葡萄品种**：赤霞珠75%、桑娇维赛20%、品丽珠5%
- **产区**：托斯卡纳/Toscana IGT
- **陈年**：法国橡木桶（100%新桶）陈年18个月
- **年产量**：约10万瓶

## 评分

- **Wine-Searcher聚合评分**：96/100
- **热度排名**：Wine-Searcher全球第83位
- **平均零售价**：€350/750ml

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
""",
    },
    # ============================================================
    # 二、纳帕谷顶级赤霞珠（Wine-Searcher真实评分）
    # ============================================================
    {
        "id": "ENT-wine-red-opus-one-2019",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "作品一号 2019",
        "title_en": "Opus One Napa Valley 2019",
        "name_cn": "作品一号",
        "name_en": "Opus One",
        "tags": ["葡萄酒", "红葡萄酒", "美国", "纳帕谷", "作品一号", "赤霞珠"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "14.5%",
        "country": "美国",
        "region": "加州/纳帕谷",
        "producer": "Opus One Winery (Mondavi & Rothschild)",
        "vintage": "2019",
        "summary": "作品一号是纳帕谷最著名的波尔多混酿，Mondavi与罗斯柴尔德家族合资，Wine-Searcher热度排名第19，critic score 95/100。",
        "content_body": """## 概述

作品一号（Opus One）是美国纳帕谷最著名的葡萄酒，由Robert Mondavi与Baron Philippe de Rothschild于1979年共同创立，旨在打造美国版的顶级波尔多混酿。2019年份获得Wine-Searcher聚合critic score 95/100。

## 基础信息

- **酒精度**：14.5% ABV
- **葡萄品种**：赤霞珠为主，混酿美乐、品丽珠、小维多、马尔贝克
- **产区**：美国/加州/纳帕谷
- **陈年**：法国橡木桶（100%新桶）陈年18个月

## 评分

- **Wine-Searcher聚合评分**：95/100
- **热度排名**：Wine-Searcher全球第19位
- **平均零售价**：$468/750ml（€410）

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
""",
    },
    {
        "id": "ENT-wine-red-harlan-estate-2018",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "哈兰酒庄 2018",
        "title_en": "Harlan Estate Napa Valley 2018",
        "name_cn": "哈兰酒庄",
        "name_en": "Harlan Estate",
        "tags": ["葡萄酒", "红葡萄酒", "美国", "纳帕谷", "哈兰", "车库酒"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "14.5%",
        "country": "美国",
        "region": "加州/纳帕谷",
        "producer": "Harlan Estate",
        "vintage": "2018",
        "summary": "哈兰酒庄是纳帕谷最稀有的「车库酒」之一，Wine-Searcher热度排名第65，critic score 97/100，价格€1,405。",
        "content_body": """## 概述

哈兰酒庄（Harlan Estate）由H. William Harlan于1984年创立，是纳帕谷最稀有的「车库酒」（cult wine）之一。酒庄产量极少，采用波尔多混酿风格，是收藏家追捧的对象。2018年份获得Wine-Searcher聚合critic score 97/100。

## 基础信息

- **酒精度**：14.5% ABV
- **葡萄品种**：赤霞珠为主，混酿美乐、品丽珠、小维多
- **产区**：美国/加州/纳帕谷
- **陈年**：法国橡木桶（100%新桶）陈年24个月
- **年产量**：约1.5万瓶

## 评分

- **Wine-Searcher聚合评分**：97/100
- **热度排名**：Wine-Searcher全球第65位
- **平均零售价**：€1,405/750ml

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
""",
    },
    {
        "id": "ENT-wine-red-screaming-eagle-2019",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "啸鹰赤霞珠 2019",
        "title_en": "Screaming Eagle Cabernet Sauvignon 2019",
        "name_cn": "啸鹰",
        "name_en": "Screaming Eagle",
        "tags": ["葡萄酒", "红葡萄酒", "美国", "纳帕谷", "啸鹰", "车库酒", "赤霞珠"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "14.5%",
        "country": "美国",
        "region": "加州/纳帕谷/Oakville",
        "producer": "Screaming Eagle Winery",
        "vintage": "2019",
        "summary": "啸鹰是纳帕谷最昂贵的车库酒，Wine-Searcher热度排名第68，critic score 97/100，价格€3,282。",
        "content_body": """## 概述

啸鹰（Screaming Eagle）是纳帕谷最著名的「车库酒」，1992年首个年份上市即引起轰动。年产量仅500-800箱，是世界上最难买到、最昂贵的美国葡萄酒之一。2019年份获得Wine-Searcher聚合critic score 97/100。

## 基础信息

- **酒精度**：14.5% ABV
- **葡萄品种**：赤霞珠为主，少量品丽珠、美乐
- **产区**：美国/加州/纳帕谷/Oakville
- **陈年**：法国橡木桶陈年18个月
- **年产量**：约500-800箱（极度稀有）

## 评分

- **Wine-Searcher聚合评分**：97/100
- **热度排名**：Wine-Searcher全球第68位
- **平均零售价**：€3,282/750ml（全球最贵美国葡萄酒之一）

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
""",
    },
    {
        "id": "ENT-wine-red-dominus-2019",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "Dominus Christian Moueix 2019",
        "title_en": "Dominus Estate Christian Moueix Napa Valley 2019",
        "name_cn": "Dominus",
        "name_en": "Dominus Estate",
        "tags": ["葡萄酒", "红葡萄酒", "美国", "纳帕谷", "Dominus", "Moueix"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "14.5%",
        "country": "美国",
        "region": "加州/纳帕谷/Yountville",
        "producer": "Dominus Estate (Moueix家族)",
        "vintage": "2019",
        "summary": "Dominus由柏图斯的Moueix家族在纳帕谷打造，Wine-Searcher热度排名第80，critic score 97/100。",
        "content_body": """## 概述

Dominus由Jean Moueix（柏图斯的经营者）于1983年在纳帕谷创立，旨在以纳帕的葡萄酿造波尔多风格的顶级红酒。产自Yountville的Napanook葡萄园。2019年份获得Wine-Searcher聚合critic score 97/100。

## 基础信息

- **酒精度**：14.5% ABV
- **葡萄品种**：赤霞珠为主，混酿美乐、品丽珠
- **产区**：美国/加州/纳帕谷/Yountville
- **陈年**：法国橡木桶陈年18个月

## 评分

- **Wine-Searcher聚合评分**：97/100
- **热度排名**：Wine-Searcher全球第80位
- **平均零售价**：€310/750ml

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
""",
    },
    {
        "id": "ENT-wine-red-caymus-2021",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "Caymus赤霞珠 2021",
        "title_en": "Caymus Vineyards Cabernet Sauvignon 2021",
        "name_cn": "Caymus",
        "name_en": "Caymus Vineyards",
        "tags": ["葡萄酒", "红葡萄酒", "美国", "纳帕谷", "Caymus", "赤霞珠", "高性价比"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "14.8%",
        "country": "美国",
        "region": "加州/纳帕谷",
        "producer": "Caymus Vineyards (Wagner家族)",
        "vintage": "2021",
        "summary": "Caymus是纳帕谷最畅销的赤霞珠之一，Wine-Searcher热度排名第86，critic score 90/100，价格€74性价比突出。",
        "content_body": """## 概述

Caymus Vineyards由Chuck Wagner家族于1972年创立，是纳帕谷最畅销的赤霞珠品牌之一。以果味浓郁、口感柔顺著称，是入门纳帕赤霞珠的优选。2021年份获得Wine-Searcher聚合critic score 90/100。

## 基础信息

- **酒精度**：14.8% ABV
- **葡萄品种**：赤霞珠为主
- **产区**：美国/加州/纳帕谷
- **陈年**：法国和美国橡木桶陈年16个月

## 评分

- **Wine-Searcher聚合评分**：90/100
- **热度排名**：Wine-Searcher全球第86位
- **平均零售价**：€74/750ml

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
""",
    },
    # ============================================================
    # 三、罗讷河谷与其他（Wine-Searcher真实评分）
    # ============================================================
    {
        "id": "ENT-wine-red-chave-hermitage-2019",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "Jean-Louis Chave Hermitage 2019",
        "title_en": "Domaine Jean-Louis Chave Hermitage 2019",
        "name_cn": "Chave爱美园",
        "name_en": "Domaine Jean-Louis Chave Hermitage",
        "tags": ["葡萄酒", "红葡萄酒", "法国", "罗讷河谷", "Hermitage", "西拉", "Chave"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "13.5%",
        "country": "法国",
        "region": "罗讷河谷/Hermitage",
        "producer": "Domaine Jean-Louis Chave",
        "vintage": "2019",
        "summary": "Chave是罗讷河谷最著名的西拉生产商，传承500余年，Wine-Searcher热度排名第96，critic score 96/100。",
        "content_body": """## 概述

Domaine Jean-Louis Chave是罗讷河谷北部Hermitage产区最负盛名的酒庄，家族传承已超过500年（1481年至今）。以100%西拉酿造的Hermitage红葡萄酒是世界上最顶级的西拉之一。2019年份获得Wine-Searcher聚合critic score 96/100。

## 基础信息

- **酒精度**：13.5% ABV
- **葡萄品种**：西拉100%
- **产区**：法国/罗讷河谷/Hermitage
- **陈年**：橡木桶陈年18个月

## 评分

- **Wine-Searcher聚合评分**：96/100
- **热度排名**：Wine-Searcher全球第96位
- **平均零售价**：€398/750ml

## 酒庄历史

- **1481年**：Chave家族开始种植葡萄
- **500余年**：家族传承至今已超过15代人
- **风格**：以优雅、深沉、陈年潜力极强著称

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
""",
    },
    {
        "id": "ENT-wine-red-ridge-monte-bello-2019",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "Ridge Monte Bello 2019",
        "title_en": "Ridge Vineyards Monte Bello 2019",
        "name_cn": "Ridge Monte Bello",
        "name_en": "Ridge Vineyards Monte Bello",
        "tags": ["葡萄酒", "红葡萄酒", "美国", "圣克鲁兹山", "Ridge", "Monte Bello"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "13.5%",
        "country": "美国",
        "region": "加州/圣克鲁兹山",
        "producer": "Ridge Vineyards",
        "vintage": "2019",
        "summary": "Ridge Monte Bello是1976年巴黎审判的明星酒，圣克鲁兹山产区的顶级波尔多混酿。",
        "content_body": """## 概述

Ridge Vineyards Monte Bello产自加州圣克鲁兹山（Santa Cruz Mountains）的Monte Bello葡萄园，是1976年「巴黎审判」（Judgment of Paris）盲品中排名第五的加州赤霞珠，帮助加州葡萄酒一举成名。2019年份继续获得高分。

## 基础信息

- **酒精度**：13.5% ABV
- **葡萄品种**：赤霞珠为主，混酿美乐、品丽珠、小维多
- **产区**：美国/加州/圣克鲁兹山
- **陈年**：美国橡木桶陈年18个月

## 历史地位

- **1976年巴黎审判**：在盲品中排名第五，仅次于Stag's Leap、Mouton、Haut-Brion、Montrose
- **风格**：旧世界风格，优雅内敛，陈年潜力极强

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
""",
    },
    {
        "id": "ENT-wine-red-pontet-canet-2019",
        "category": "ENT",
        "subcategory": "wine_red",
        "title": "庞特卡奈 2019",
        "title_en": "Château Pontet-Canet Pauillac 2019",
        "name_cn": "庞特卡奈",
        "name_en": "Château Pontet-Canet",
        "tags": ["葡萄酒", "红葡萄酒", "波尔多", "波亚克", "庞特卡奈", "五级庄", "生物动力法"],
        "source": "Wine-Searcher / wine-searcher.com",
        "data_confidence": "verified",
        "abv": "13.5%",
        "country": "法国",
        "region": "波尔多/波亚克",
        "producer": "Alfred Tesseron",
        "vintage": "2019",
        "summary": "庞特卡奈是波尔多五级庄中最超班的酒庄，首个生物动力法列级庄，Wine-Searcher critic score 95/100，价格$133性价比极高。",
        "content_body": """## 概述

庞特卡奈（Château Pontet-Canet）是波尔多梅多克波亚克村的五级庄（1855分级），但实际上品质远超五级庄水平，被公认为「超二级庄」。酒庄是波尔多列级庄中第一个采用生物动力法（biodynamic）的酒庄。2019年份获得Wine-Searcher聚合critic score 95/100。

## 基础信息

- **酒精度**：13.5% ABV
- **葡萄品种**：赤霞珠60-65%、美乐30-33%、品丽珠4-5%、小维多1-2%
- **产区**：波尔多/波亚克
- **分级**：1855五级庄
- **种植**：生物动力法认证（Biodyvin）

## 评分

- **Wine-Searcher聚合评分**：95/100
- **平均零售价**：$133/750ml
- **性价比**：在95分波尔多中性价比极高

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/pontet+canet+pauillac+medoc+bordeaux+france
""",
    },
]
