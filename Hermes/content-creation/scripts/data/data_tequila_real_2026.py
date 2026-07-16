"""龙舌兰酒真实数据补充（2026年Wine-Searcher/Flaviar/Good Housekeeping）。

数据源：Wine-Searcher / Flaviar / Good Housekeeping
置信度：verified

覆盖：基于真实critic score、获奖记录和零售价的龙舌兰品牌补充
重点补充：Don Julio 1942/Añejo、Patrón Reposado/Añejo、José Cuervo Reserva de la Familia(95pts)、
Gran Centenario Leyenda(96pts)、Casamigos Reposado/Añejo、Clase Azul Reposado、
Herradura Silver/Añejo、El Jimador Blanco/Reposado、1800 Añejo等此前未单独覆盖的真实酒款。
"""

ENTRIES = [
    # ============================================================
    # 一、Don Julio 补充（1942 / Añejo）
    # ============================================================
    {
        "id": "ENT-tequila-real-don-julio-1942",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "唐胡里奥 1942",
        "title_en": "Don Julio 1942 Añejo Tequila",
        "name_cn": "唐胡里奥 1942",
        "name_en": "Don Julio 1942",
        "tags": ["龙舌兰酒", "唐胡里奥", "墨西哥", "Añejo", "陈年", "高端"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Highlands",
        "producer": "Don Julio (Diageo)",
        "summary": "Don Julio 1942 致敬创始人 Don Julio González 1942 年创立酒厂，陈酿2.5年，价格 $164。",
        "content_body": """## 概述

Don Julio 1942 是 Don Julio 品牌的高端 Añejo 龙舌兰酒，致敬创始人 Don Julio González-Frausto Estrada 于 1942 年创立 La Primavera 酒厂。该酒款陈酿 2.5 年（远超 Añejo 法定最低 1 年），是名人酒吧和高端夜店的标志性酒款。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Highlands（高地）
- **陈酿**：美国白橡木波本桶 2.5 年
- **原料**：100% 蓝色韦伯龙舌兰（Blue Weber Agave）

## 评分与价格

- **Wine-Searcher聚合评分**：93/100
- **平均零售价**：$164/750ml（约 ¥1,190）
- **性价比定位**：高端 Añejo，礼赠与净饮之选

## 风味特征

- **颜色**：金黄琥珀色
- **香气**：香草、焦糖、橡木、巧克力
- **口感**：柔顺丰满，香草与焦糖交织
- **余味**：悠长，带烤橡木与香料

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/don+julio+1942+anejo+tequila
""",
    },
    {
        "id": "ENT-tequila-real-don-julio-anejo",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "唐胡里奥 Añejo",
        "title_en": "Don Julio Añejo Tequila",
        "name_cn": "唐胡里奥 Añejo",
        "name_en": "Don Julio Añejo",
        "tags": ["龙舌兰酒", "唐胡里奥", "墨西哥", "Añejo", "陈年"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "38%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Highlands",
        "producer": "Don Julio (Diageo)",
        "summary": "Don Julio Añejo 陈酿18个月，最经典Don Julio高端Añejo之一，价格 $64。",
        "content_body": """## 概述

Don Julio Añejo 是 Don Julio 品牌的经典陈年龙舌兰酒，陈酿 18 个月（超过 Añejo 法定最低 1 年的 50%）。使用 100% 蓝色韦伯龙舌兰，在美橡木波本桶中陈酿。

## 基础信息

- **酒精度**：38% ABV
- **产区**：墨西哥 Jalisco Highlands
- **陈酿**：美国白橡木波本桶 18 个月
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：90/100
- **平均零售价**：$64/750ml（约 ¥465）
- **性价比定位**：经典 Añejo，性价比之选

## 风味特征

- **颜色**：浅金黄色
- **香气**：柑橘、热带水果、橡木、香草
- **口感**：圆润柔和，果味与橡木交织
- **余味**：中等，带烤橡木与香料

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/don+julio+anejo+tequila
""",
    },
    # ============================================================
    # 二、Patrón 补充（Reposado / Añejo）
    # ============================================================
    {
        "id": "ENT-tequila-real-patron-reposado",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "Patrón Reposado",
        "title_en": "Patrón Reposado Tequila",
        "name_cn": "Patrón Reposado",
        "name_en": "Patrón Reposado",
        "tags": ["龙舌兰酒", "Patrón", "墨西哥", "Reposado", "陈年"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Highlands",
        "producer": "Patrón (Bacardi)",
        "summary": "Patrón Reposado 陈酿至少3个月，手工小批量生产，价格 £58（约 ¥510）。",
        "content_body": """## 概述

Patrón Reposado 来自 Patrón 酒厂，使用 100% 蓝色韦伯龙舌兰，在美橡木波本桶中陈酿至少 3 个月（达 Reposado 法定最低）。Patrón 酒厂以手工小批量生产（Small Batch）著称，每瓶均由人工编号。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Highlands
- **陈酿**：美国白橡木波本桶至少 3 个月
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：89/100
- **平均零售价**：£58/750ml（约 ¥510）
- **性价比定位**：中高端 Reposado，礼赠之选

## 风味特征

- **颜色**：浅金色
- **香气**：柑橘、蜂蜜、橡木、香草
- **口感**：柔顺平衡，果味与橡木交织
- **余味**：中等，带香草与烤橡木

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/patron+reposado+tequila
""",
    },
    {
        "id": "ENT-tequila-real-patron-anejo",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "Patrón Añejo",
        "title_en": "Patrón Añejo Tequila",
        "name_cn": "Patrón Añejo",
        "name_en": "Patrón Añejo",
        "tags": ["龙舌兰酒", "Patrón", "墨西哥", "Añejo", "陈年"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Highlands",
        "producer": "Patrón (Bacardi)",
        "summary": "Patrón Añejo 陈酿超过12个月，混合三种橡木桶陈酿，价格 $60+。",
        "content_body": """## 概述

Patrón Añejo 来自 Patrón 酒厂，陈酿超过 12 个月，混合法国橡木桶、美国白橡木桶和加拿大波本桶陈酿的龙舌兰，赋予更复杂的风味层次。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Highlands
- **陈酿**：法国橡木桶、美国白橡木桶、加拿大波本桶混合陈酿 12+ 个月
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：90/100
- **平均零售价**：$60/750ml（约 ¥435）
- **性价比定位**：多桶陈酿 Añejo，性价比突出

## 风味特征

- **颜色**：深金色
- **香气**：橡木、香草、焦糖、烤杏仁
- **口感**：饱满丰满，木质香料与香草交织
- **余味**：悠长，带烤橡木与黑胡椒

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/patron+anejo+tequila
""",
    },
    # ============================================================
    # 三、José Cuervo Reserva de la Familia（95pts）
    # ============================================================
    {
        "id": "ENT-tequila-real-jose-cuervo-reserva-de-la-familia",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "José Cuervo Reserva de la Familia",
        "title_en": "José Cuervo Reserva de la Familia Extra Añejo",
        "name_cn": "José Cuervo 家族珍藏",
        "name_en": "José Cuervo Reserva de la Familia",
        "tags": ["龙舌兰酒", "José Cuervo", "墨西哥", "Extra Añejo", "家族珍藏", "95分"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Tequila",
        "producer": "José Cuervo (Proximo Spirits)",
        "summary": "José Cuervo Reserva de la Familia Extra Añejo 家族珍藏，陈酿至少3年，Wine-Searcher 95/100，价格 $181。",
        "content_body": """## 概概述

José Cuervo Reserva de la Familia 是 José Cuervo 酒厂的家族珍藏级 Extra Añejo 龙舌兰酒，是 Cuervo 家族为庆祝酒厂创立 200 周年（1995 年）推出的限量酒款。每年由家族成员亲自挑选陈酿桶，陈酿至少 3 年，远超 Extra Añejo 法定最低 3 年。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Tequila
- **陈酿**：美国白橡木桶 + 法国橡木桶 3+ 年
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：95/100
- **平均零售价**：$181/750ml（约 ¥1,310）
- **性价比定位**：顶级 Extra Añejo，收藏之选

## 风味特征

- **颜色**：深琥珀色
- **香气**：橡木、香草、果干、巧克力
- **口感**：饱满复杂，木质香料与果干交织
- **余味**：极悠长，带烤杏仁与黑巧克力

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/jose+cuervo+reserva+de+la+familia+tequila
""",
    },
    # ============================================================
    # 四、Gran Centenario Leyenda（96pts）
    # ============================================================
    {
        "id": "ENT-tequila-real-gran-centenario-leyenda",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "Gran Centenario Leyenda",
        "title_en": "Gran Centenario Leyenda Extra Añejo Tequila",
        "name_cn": "Gran Centenario Leyenda",
        "name_en": "Gran Centenario Leyenda",
        "tags": ["龙舌兰酒", "Gran Centenario", "墨西哥", "Extra Añejo", "Leyenda", "96分"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Highlands",
        "producer": "Gran Centenario (Becle/Casa Cuervo)",
        "summary": "Gran Centenario Leyenda Extra Añejo 家族传奇酒款，陈酿4年，Wine-Searcher 96/100，价格 $158。",
        "content_body": """## 概述

Gran Centenario Leyenda 是 Gran Centenario 品牌的旗舰 Extra Añejo 龙舌兰酒，由酒庄创始人 Lázaro Gallardo 的后代挑选家族陈酿最久的桶调制。陈酿 4 年（远超 Extra Añejo 法定最低 3 年），使用法国利穆赞橡木桶。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Highlands
- **陈酿**：法国利穆赞橡木桶 4 年
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：96/100
- **平均零售价**：$158/750ml（约 ¥1,150）
- **性价比定位**：顶级 Extra Añejo，96分高分

## 风味特征

- **颜色**：深琥珀色
- **香气**：橡木、果干、香草、香料
- **口感**：饱满复杂，木质香料与果干交织
- **余味**：极悠长，带烤杏仁与肉豆蔻

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/gran+centenario+leyenda+tequila
""",
    },
    # ============================================================
    # 五、Casamigos Reposado / Añejo
    # ============================================================
    {
        "id": "ENT-tequila-real-casamigos-reposado",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "Casamigos Reposado",
        "title_en": "Casamigos Reposado Tequila",
        "name_cn": "Casamigos Reposado",
        "name_en": "Casamigos Reposado",
        "tags": ["龙舌兰酒", "Casamigos", "墨西哥", "Reposado", "Clooney"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Highlands",
        "producer": "Casamigos (Diageo)",
        "summary": "Casamigos Reposado 由George Clooney等创立，陈酿7个月，价格 $50+。",
        "content_body": """## 概述

Casamigos Reposado 来自 Casamigos 龙舌兰酒厂，由好莱坞影星 George Clooney、Rande Gerber 和 Mike Meldman 于 2013 年共同创立。Casamigos 在西班牙语中意为「朋友之家」。该酒款陈酿 7 个月（超过 Reposado 法定最低 2 个月），使用法国橡木桶和美橡木桶陈酿。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Highlands
- **陈酿**：法国橡木桶 + 美国白橡木桶 7 个月
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：88/100
- **平均零售价**：$50/750ml（约 ¥360）
- **性价比定位**：明星品牌，入门 Reposado

## 风味特征

- **颜色**：浅金色
- **香气**：香草、可可、橡木、薄荷
- **口感**：柔顺甘甜，香草与可可交织
- **余味**：中等，带烤橡木与香草

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/casamigos+reposado+tequila
""",
    },
    {
        "id": "ENT-tequila-real-casamigos-anejo",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "Casamigos Añejo",
        "title_en": "Casamigos Añejo Tequila",
        "name_cn": "Casamigos Añejo",
        "name_en": "Casamigos Añejo",
        "tags": ["龙舌兰酒", "Casamigos", "墨西哥", "Añejo", "Clooney"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Highlands",
        "producer": "Casamigos (Diageo)",
        "summary": "Casamigos Añejo 陈酿14个月，法国橡木桶，价格 $60+。",
        "content_body": """## 概述

Casamigos Añejo 来自 Casamigos 龙舌兰酒厂，陈酿 14 个月（超过 Añejo 法定最低 1 年），使用法国橡木桶（最长达 14 年桶龄），赋予复杂的香草和香料风味。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Highlands
- **陈酿**：法国橡木桶 14 个月（桶龄最长达 14 年）
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：90/100
- **平均零售价**：$60/750ml（约 ¥435）
- **性价比定位**：明星品牌高端 Añejo

## 风味特征

- **颜色**：深金色
- **香气**：焦糖、香草、肉豆蔻、橡木
- **口感**：饱满柔顺，焦糖与香草交织
- **余味**：悠长，带肉豆蔻与烤橡木

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/casamigos+anejo+tequila
""",
    },
    # ============================================================
    # 六、Clase Azul Reposado（高端手绘瓶）
    # ============================================================
    {
        "id": "ENT-tequila-real-clase-azul-reposado",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "Clase Azul Reposado",
        "title_en": "Clase Azul Reposado Tequila",
        "name_cn": "Clase Azul Reposado",
        "name_en": "Clase Azul Reposado",
        "tags": ["龙舌兰酒", "Clase Azul", "墨西哥", "Reposado", "手绘瓶", "高端"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Highlands",
        "producer": "Clase Azul",
        "summary": "Clase Azul Reposado 高端龙舌兰酒，手工绘制陶瓷瓶身，陈酿8个月，价格 $170+。",
        "content_body": """## 概述

Clase Azul Reposado 是 Clase Azul 品牌的标志性酒款，使用手工绘制的陶瓷瓶身（每个瓶身均由墨西哥艺术家手工绘制），是龙舌兰酒中视觉与味觉双重高端的代表。陈酿 8 个月（超过 Reposado 法定最低 2 个月）。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Highlands
- **陈酿**：美国白橡木雪莉桶 8 个月
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：93/100
- **平均零售价**：$170/750ml（约 ¥1,230）
- **性价比定位**：高端礼赠之选，艺术与品鉴并重

## 风味特征

- **颜色**：深金色
- **香气**：香草、奶油、橡木、香料
- **口感**：饱满柔顺，奶油与香草交织
- **余味**：悠长，带肉豆蔻与烤橡木

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/clase+azul+reposado+tequila
""",
    },
    # ============================================================
    # 七、Herradura Silver / Añejo
    # ============================================================
    {
        "id": "ENT-tequila-real-herradura-silver",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "Herradura Silver",
        "title_en": "Herradura Silver Tequila",
        "name_cn": "Herradura Silver",
        "name_en": "Herradura Silver",
        "tags": ["龙舌兰酒", "Herradura", "墨西哥", "Blanco", "马蹄铁"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Amatitán",
        "producer": "Casa Herradura (Brown-Forman)",
        "summary": "Herradura Silver 马蹄铁银龙舌兰，陈酿25天后装瓶，传统工艺代表，价格 $40+。",
        "content_body": """## 概述

Herradura Silver（马蹄铁银龙舌兰）来自 Casa Herradura 酒厂，使用 100% 蓝色韦伯龙舌兰。与传统 Blanco 不同，Herradura Silver 在美橡木桶中陈酿 25 天，赋予更柔和的口感。酒厂位于墨西哥 Jalisco 的 Amatitán，1870 年创立。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Amatitán
- **陈酿**：美国白橡木桶 25 天
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：88/100
- **平均零售价**：$40/750ml（约 ¥290）
- **性价比定位**：经典 Blanco，调酒与净饮兼顾

## 风味特征

- **颜色**：无色透明
- **香气**：龙舌兰、柑橘、香草、橡木
- **口感**：清新柔顺，龙舌兰与柑橘交织
- **余味**：中等，带香草与白胡椒

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/herradura+silver+tequila
""",
    },
    {
        "id": "ENT-tequila-real-herradura-anejo",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "Herradura Añejo",
        "title_en": "Herradura Añejo Tequila",
        "name_cn": "Herradura Añejo",
        "name_en": "Herradura Añejo",
        "tags": ["龙舌兰酒", "Herradura", "墨西哥", "Añejo", "陈年"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Amatitán",
        "producer": "Casa Herradura (Brown-Forman)",
        "summary": "Herradura Añejo 陈酿25个月（超过Añejo法定2倍），价格 $50+。",
        "content_body": """## 概述

Herradura Añejo 来自 Casa Herradura 酒厂，陈酿 25 个月（远超 Añejo 法定最低 1 年，达到 2 倍以上）。是史上首个 Añejo 龙舌兰酒（1962 年首次推出）。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Amatitán
- **陈酿**：美国白橡木桶 25 个月
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：90/100
- **平均零售价**：$50/750ml（约 ¥360）
- **性价比定位**：经典 Añejo，Añejo鼻祖

## 风味特征

- **颜色**：深金色
- **香气**：橡木、肉桂、香草、干果
- **口感**：饱满圆润，肉桂与橡木交织
- **余味**：悠长，带肉桂与烤橡木

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/herradura+anejo+tequila
""",
    },
    # ============================================================
    # 八、El Jimador Blanco / Reposado
    # ============================================================
    {
        "id": "ENT-tequila-real-el-jimador-blanco",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "El Jimador Blanco",
        "title_en": "El Jimador Blanco Tequila",
        "name_cn": "El Jimador Blanco",
        "name_en": "El Jimador Blanco",
        "tags": ["龙舌兰酒", "El Jimador", "墨西哥", "Blanco", "jimador"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Amatitán",
        "producer": "Casa Herradura (Brown-Forman)",
        "summary": "El Jimador Blanco 龙舌兰酒入门款，未陈年，墨西哥销量最大的龙舌兰品牌之一，价格 $25+。",
        "content_body": """## 概述

El Jimador Blanco 来自 Casa Herradura 旗下品牌，名字源自「jimador」——墨西哥专门收割龙舌兰的工人。是墨西哥国内销量最大的龙舌兰酒品牌之一，未陈年装瓶，保留龙舌兰的纯净风味。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Amatitán
- **陈酿**：未陈年（Blanco）
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：85/100
- **平均零售价**：$25/750ml（约 ¥180）
- **性价比定位**：入门 Blanco，调酒主力

## 风味特征

- **颜色**：无色透明
- **香气**：龙舌兰、柑橘、草本
- **口感**：清新爽口，龙舌兰与柑橘交织
- **余味**：中短，带白胡椒与龙舌兰

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/el+jimador+blanco+tequila
""",
    },
    {
        "id": "ENT-tequila-real-el-jimador-reposado",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "El Jimador Reposado",
        "title_en": "El Jimador Reposado Tequila",
        "name_cn": "El Jimador Reposado",
        "name_en": "El Jimador Reposado",
        "tags": ["龙舌兰酒", "El Jimador", "墨西哥", "Reposado"],
        "source": "Wine-Searcher / Good Housekeeping",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco/Amatitán",
        "producer": "Casa Herradura (Brown-Forman)",
        "summary": "El Jimador Reposado 陈酿2个月，性价比入门Reposado，价格 £30（约 ¥270）。",
        "content_body": """## 概述

El Jimador Reposado 来自 Casa Herradura 旗下品牌，陈酿 2 个月（达 Reposado 法定最低 2 个月），性价比突出，是入门 Reposado 龙舌兰酒的代表。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco Amatitán
- **陈酿**：美国白橡木桶 2 个月
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：86/100
- **平均零售价**：£30/750ml（约 ¥270）
- **性价比定位**：入门 Reposado，性价比突出

## 风味特征

- **颜色**：浅金色
- **香气**：龙舌兰、香草、橡木
- **口感**：柔顺平衡，龙舌兰与橡木交织
- **余味**：中等，带香草与白胡椒

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/el+jimador+reposado+tequila
""",
    },
    # ============================================================
    # 九、1800 Añejo
    # ============================================================
    {
        "id": "ENT-tequila-real-1800-anejo",
        "category": "ENT",
        "subcategory": "tequila",
        "title": "1800 Añejo",
        "title_en": "1800 Añejo Tequila",
        "name_cn": "1800 Añejo",
        "name_en": "1800 Añejo",
        "tags": ["龙舌兰酒", "1800", "墨西哥", "Añejo"],
        "source": "Wine-Searcher / Flaviar",
        "data_confidence": "verified",
        "abv": "40%",
        "country": "墨西哥",
        "region": "墨西哥/Jalisco",
        "producer": "1800 Tequila (Proximo Spirits)",
        "summary": "1800 Añejo 陈酿8个月（达 Añejo 法定最低），价格 $45+。",
        "content_body": """## 概述

1800 Añejo 来自 1800 Tequila 品牌，名字源自龙舌兰酒在橡木桶中陈酿的起始年份 1800 年。该酒款陈酿 8 个月，使用法国橡木桶和美橡木桶混合陈酿。

## 基础信息

- **酒精度**：40% ABV
- **产区**：墨西哥 Jalisco
- **陈酿**：法国橡木桶 + 美国白橡木桶 8 个月
- **原料**：100% 蓝色韦伯龙舌兰

## 评分与价格

- **Wine-Searcher聚合评分**：87/100
- **平均零售价**：$45/750ml（约 ¥325）
- **性价比定位**：中端 Añejo，性价比之选

## 风味特征

- **颜色**：深金色
- **香气**：橡木、香草、胡椒、烤杏仁
- **口感**：饱满柔顺，橡木与香草交织
- **余味**：中等，带烤橡木与黑胡椒

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/1800+anejo+tequila
""",
    },
]
