"""餐酒搭配指南数据 - 权威来源。

数据源：
- WSET Food & Wine Pairing
- 各国餐饮文化资料

置信度：official
"""

ENTRIES = [
    {
        "id": "DEC-pairing-weight-match",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "餐酒搭配核心原则",
        "title_en": "Core Principles of Food and Wine Pairing",
        "name_cn": "餐酒搭配核心原则",
        "name_en": "Food Wine Pairing Principles",
        "tags": ["餐酒搭配", "原则", "方法论"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "餐酒搭配的六大核心原则：酒体匹配、酸度切脂、单宁解腻、甜度平衡等。",
        "content_body": """## 六大核心原则

### 1. 酒体与食物重量匹配

| 食物重量 | 推荐酒体 | 示例 |
|----------|----------|------|
| 轻盈（沙拉/刺身） | 轻酒体（长相思/灰皮诺） | 清蒸鱼+干白 |
| 中等（禽类/意面） | 中酒体（黑皮诺/梅洛） | 烤鸡+黑皮诺 |
| 重量（红肉/野味） | 重酒体（赤霞珠/西拉） | 牛排+赤霞珠 |

### 2. 酸度切脂

- 高脂食物（奶油/奶酪）需高酸度酒切割油腻感
- 香槟配炸鸡，雷司令配肥鹅肝

### 3. 单宁解腻

- 单宁与蛋白质结合，软化肉质
- 高单宁红酒配红肉，单宁使肉质更嫩

### 4. 甜度平衡

- 酒的甜度应≥食物的甜度
- 甜食配干酒会显得酸涩
- 甜酒配甜点，以甜制甜

### 5. 风味强度对等

- 浓味食物配浓味酒，淡味食物配淡味酒
- 麻辣川菜不宜配高酒精度的重酒

### 6. 酸咸互补

- 咸食使酒显得更柔顺
- 蓝纹奶酪+苏玳是经典搭配""",
    },
    {
        "id": "DEC-pairing-seafood",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "海鲜配酒指南",
        "title_en": "Seafood and Wine Pairing Guide",
        "name_cn": "海鲜配酒指南",
        "name_en": "Seafood Wine Pairing",
        "tags": ["海鲜", "白鱼", "贝类", "甲壳类", "深海鱼", "白葡萄酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按海鲜类型（白鱼/贝类/甲壳/深海鱼）分别给出配酒建议，主打白葡萄酒与起泡酒。",
        "content_body": """## 海鲜配酒分类指南

### 1. 白肉鱼（鲈鱼/鳕鱼/比目鱼）

| 烹饪方式 | 推荐酒款 | 理由 |
|----------|----------|------|
| 清蒸 | 长相思、灰皮诺 | 高酸衬托鲜味 |
| 香煎 | 霞多丽（未过桶） | 酒体中等不抢味 |
| 油炸 | 香槟、Cava | 气泡切割油腻 |

### 2. 贝类（生蚝/扇贝/青口）

- 生蚝：夏布利（Chablis）、密斯卡岱（Muscadet）
- 扇贝：过桶霞多丽、白皮诺
- 青口：白诗南、干型雪利 Fino

### 3. 甲壳类（龙虾/螃蟹/虾）

- 龙虾：勃艮第霞多丽、香槟（白中白）
- 螃蟹：灰皮诺、维欧尼
- 虾类：干型桃红、长相思

### 4. 深海鱼（三文鱼/金枪鱼/剑鱼）

- 三文鱼：黑皮诺、过桶霞多丽
- 金枪鱼：中酒体红酒（黑皮诺/品丽珠）
- 剑鱼：西拉、品丽珠

### 禁忌

- 高单宁红酒与鱼类结合产生铁锈腥味
- 重油酱汁海鲜避免过酸干白""",
    },
    {
        "id": "DEC-pairing-red-meat",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "红肉配酒指南",
        "title_en": "Red Meat and Wine Pairing Guide",
        "name_cn": "红肉配酒指南",
        "name_en": "Red Meat Wine Pairing",
        "tags": ["红肉", "牛排", "羊排", "猪肉", "野味", "红葡萄酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按红肉类型（牛排/羊排/猪肉/野味）搭配红酒，强调单宁与蛋白质的结合。",
        "content_body": """## 红肉配酒分类指南

### 1. 牛排

| 部位/熟度 | 推荐酒款 | 经典搭配 |
|----------|----------|----------|
| 菲力（瘦嫩） | 梅洛、黑皮诺 | 单宁柔和 |
| 肋眼（油花足） | 赤霞珠、马尔贝克 | 高单宁解腻 |
| T骨（厚实） | 波尔多混酿、西拉 | 酒体厚重 |
| 全熟 | 巴罗洛、布鲁奈罗 | 单宁强劲 |

### 2. 羊排

- 迷迭香烤羊排：赤霞珠、西拉
- 红酒炖羊肉：教皇新堡（Châteauneuf-du-Pape）
- 中东香料羊排：歌海娜、慕合怀特

### 3. 猪肉

- 烤猪排：黑皮诺、品丽珠
- 红烧肉：仙粉黛、阿玛罗尼
- 糖醋排骨：半干雷司令、桃红起泡

### 4. 野味（鹿肉/野猪/兔肉）

- 鹿肉：勃艮第特级园黑皮诺
- 野猪：北罗讷西拉、巴罗洛
- 兔肉：品丽珠、仙粉黛

### 配酒原则

- 单宁与蛋白质结合使肉质更嫩
- 酱汁浓郁度决定酒体轻重
- 野味宜选陈年红酒，复杂度匹配""",
    },
    {
        "id": "DEC-pairing-poultry",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "禽类配酒指南",
        "title_en": "Poultry and Wine Pairing Guide",
        "name_cn": "禽类配酒指南",
        "name_en": "Poultry Wine Pairing",
        "tags": ["禽类", "鸡肉", "鸭肉", "鹅肉", "火鸡", "白葡萄酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按禽类（鸡肉/鸭肉/鹅肉/火鸡）搭配红白酒，依烹饪方式调整酒体。",
        "content_body": """## 禽类配酒分类指南

### 1. 鸡肉

| 烹饪方式 | 推荐酒款 | 备注 |
|----------|----------|------|
| 白切/清蒸 | 长相思、灰皮诺 | 清爽干白 |
| 烤鸡 | 黑皮诺、霞多丽 | 中酒体 |
| 红烧/咖喱 | 西拉、歌海娜 | 香料呼应 |
| 油炸 | 香槟、Cava | 气泡解腻 |

### 2. 鸭肉

- 北京烤鸭：黑皮诺（勃艮第/俄勒冈）
- 樱桃酱鸭胸：黑皮诺、品丽珠
- 法式油封鸭：马尔贝克、梅洛
- 陈皮鸭：半甜雷司令、琼瑶浆

### 3. 鹅肉

- 烤鹅：赤霞珠、西拉
- 鹅肝（肥肝）：苏玳贵腐、迟摘雷司令
- 法式鹅肝酱：托卡伊、冰酒

### 4. 火鸡

- 感恩节烤火鸡：黑皮诺、仙粉黛
- 烟熏火鸡：桃红、歌海娜
- 火鸡胸肉：霞多丽、白皮诺

### 配酒要点

- 烹饪方式比肉类本身更影响选酒
- 酱汁甜咸度需与酒体匹配
- 油脂高的鹅鸭可选重酒体红酒""",
    },
    {
        "id": "DEC-pairing-cheese",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "奶酪配酒指南",
        "title_en": "Cheese and Wine Pairing Guide",
        "name_cn": "奶酪配酒指南",
        "name_en": "Cheese Wine Pairing",
        "tags": ["奶酪", "软质", "硬质", "蓝纹", "新鲜", "芝士"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按奶酪类型（软质/硬质/蓝纹/新鲜）搭配酒款，遵循产地相近原则。",
        "content_body": """## 奶酪配酒分类指南

### 1. 软质奶酪（布里/卡蒙贝尔）

| 奶酪类型 | 推荐酒款 | 搭配逻辑 |
|----------|----------|----------|
| 布里 Brie | 霞多丽、香槟 | 酸度切脂 |
| 卡蒙贝尔 Camembert | 苹果酒Cidre、灰皮诺 | 同乡风味 |
| 塔雷吉欧 Taleggio | 皱叶巴巴莱斯科 | 意式组合 |

### 2. 硬质奶酪（帕玛森/切达/孔泰）

- 帕玛森 Parmigiano：基安蒂 Chianti、Brunello
- 切达 Cheddar：赤霞珠、马尔贝克
- 孔泰 Comté：黄葡萄酒 Vin Jaune
- 格吕耶尔 Gruyère：黑皮诺、Savagnin

### 3. 蓝纹奶酪（洛克福/斯蒂尔顿/戈贡佐拉）

- 洛克福 Roquefort：苏玳 Sauternes（经典配）
- 斯蒂尔顿 Stilton：波特酒 Port
- 戈贡佐拉 Gorgonzola：Recioto、Amarone

### 4. 新鲜奶酪（莫扎瑞拉/瑞可塔/山羊奶酪）

- 莫扎瑞拉：Verdicchio、灰皮诺
- 山羊奶酪 Chèvre：桑塞尔 Sancerre、普伊-富美
- 瑞可塔 Ricotta：桃红起泡、Frascati

### 经典原则

- "土地上长的，配土地上酿的"：同产区搭配最稳
- 蓝纹+贵腐是经典咸甜组合
- 高盐奶酪使酒显得更柔顺""",
    },
    {
        "id": "DEC-pairing-spicy",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "辛辣菜肴配酒",
        "title_en": "Spicy Cuisine and Wine Pairing",
        "name_cn": "辛辣菜肴配酒",
        "name_en": "Spicy Food Wine Pairing",
        "tags": ["辛辣", "川菜", "泰餐", "印度菜", "麻辣", "甜白"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "辛辣菜肴配酒需避开高酒精度与高单宁，推荐甜白、低酒精度起泡或果香型酒。",
        "content_body": """## 辛辣菜肴配酒指南

### 配酒原则

- 辣味会放大酒精的灼烧感，避免高酒精度（>13.5%）
- 甜度可缓解辣感，半甜/甜白是首选
- 单宁与辣味冲突，避免重单宁红酒
- 起泡酒泡沫感能"清洗"辣味残留

### 1. 川菜

| 菜式 | 推荐酒款 | 说明 |
|------|----------|------|
| 麻婆豆腐 | 半甜雷司令、琼瑶浆 | 甜度解辣 |
| 水煮鱼 | 阿斯蒂 Moscato d'Asti | 低酒精+甜 |
| 回锅肉 | 半干白诗南、桃红 | 果香平衡 |
| 宫保鸡丁 | Prosecco、半干起泡 | 气泡解辣 |

### 2. 泰餐

- 冬阴功：长相思、干型雷司令
- 绿咖喱：琼瑶浆 Gewürztraminer
- 泰式炒河粉：半甜白诗南
- 青木瓜沙拉： Sauvignon Blanc、Albariño

### 3. 印度菜

- 咖喱鸡：半甜雷司令、Müller-Thurgau
- 坦杜里烤鸡：桃红、果香西拉
- 印度比尔亚尼：琼瑶浆、Viognier

### 4. 墨西哥菜

- 塔可：马尔贝克、仙粉黛
- 莎莎酱：Albariño、Verdejo

### 禁忌

- 高单宁赤霞珠+麻辣=灼烧难咽
- 高酒精加强酒+辣=火上浇油""",
    },
    {
        "id": "DEC-pairing-sichuan",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "川菜配酒指南",
        "title_en": "Sichuan Cuisine and Wine Pairing",
        "name_cn": "川菜配酒指南",
        "name_en": "Sichuan Food Wine Pairing",
        "tags": ["川菜", "麻辣", "鱼香", "怪味", "花椒", "甜白"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "针对川菜三大味型（麻辣/鱼香/怪味）的精准配酒建议。",
        "content_body": """## 川菜味型配酒指南

### 1. 麻辣味型

| 经典菜 | 推荐酒款 | 搭配理由 |
|--------|----------|----------|
| 麻婆豆腐 | 半甜雷司令 | 甜度中和辣 |
| 水煮牛肉 | Moscato d'Asti | 低酒精解辣 |
| 夫妻肺片 | 琼瑶浆 Gewürztraminer | 荔枝香呼应花椒 |
| 火锅底料 | 桃红起泡、Prosecco | 气泡清口 |

### 2. 鱼香味型

- 鱼香肉丝：半干白诗南、Viognier
- 鱼香茄子：长相思、Pinot Grigio
- 鱼香脆皮鱼：干型桃红、灰皮诺

### 3. 怪味味型

- 怪味鸡：琼瑶浆、半甜雷司令
- 怪味花生：阿斯蒂 Moscato d'Asti
- 怪味胡豆：冰酒、贵腐甜白

### 4. 其他经典川菜

- 回锅肉：黑皮诺、半干白诗南
- 宫保鸡丁：Prosecco、半干起泡
- 樟茶鸭：黑皮诺、Pinotage
- 开水白菜：霞多丽（未过桶）、灰皮诺

### 配酒要点

- 花椒的"麻"需要甜度+果香缓解
- 高油豆瓣酱需高酸度切脂
- 川菜复杂度高，避免复杂型陈年酒""",
    },
    {
        "id": "DEC-pairing-cantonese",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "粤菜配酒指南",
        "title_en": "Cantonese Cuisine and Wine Pairing",
        "name_cn": "粤菜配酒指南",
        "name_en": "Cantonese Food Wine Pairing",
        "tags": ["粤菜", "清蒸", "烧腊", "点心", "广式", "白葡萄酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "针对粤菜三大类（清蒸/烧腊/点心）的配酒建议，主打干白与中酒体红酒。",
        "content_body": """## 粤菜配酒分类指南

### 1. 清蒸类

| 经典菜 | 推荐酒款 | 搭配理由 |
|--------|----------|----------|
| 清蒸石斑 | 夏布利 Chablis | 矿物感衬鲜 |
| 清蒸鲈鱼 | 灰皮诺、长相思 | 高酸提鲜 |
| 白灼虾 |密斯卡岱 Muscadet | 同海风土 |
| 清蒸蟹 | 霞多丽（未过桶） | 酒体适中 |

### 2. 烧腊类

- 烧鹅：黑皮诺、品丽珠
- 烧鸭：黑皮诺（勃艮第）
- 蜜汁叉烧：半干雷司令、桃红
- 脆皮烧肉：香槟、Cava（气泡解腻）
- 油鸡：霞多丽、Viognier

### 3. 点心类

| 点心 | 推荐酒款 | 备注 |
|------|----------|------|
| 虾饺 | 长相思、灰皮诺 | 海鲜搭配 |
| 烧卖 | 黑皮诺、桃红 | 中酒体 |
| 叉烧包 | 半干雷司令 | 甜咸平衡 |
| 萝卜糕 | 香槟、Prosecco | 油炸解腻 |
| 肠粉 | 霞多丽、白皮诺 | 米浆质感 |

### 4. 老火汤与甜品

- 老火靓汤：干型雪利 Fino、Manzanilla
- 双皮奶：阿斯蒂 Moscato d'Asti
- 杨枝甘露：半甜雷司令

### 配酒原则

- 粤菜重食材本味，酒款以清爽型为主
- 烧腊有烟熏与甜度，需中酒体平衡
- 点心多样化，可选桃红作为"百搭"酒""",
    },
    {
        "id": "DEC-pairing-northern",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "北方菜配酒指南",
        "title_en": "Northern Chinese Cuisine and Wine Pairing",
        "name_cn": "北方菜配酒指南",
        "name_en": "Northern Chinese Food Wine Pairing",
        "tags": ["北方菜", "烤鸭", "涮羊肉", "鲁菜", "京菜", "红酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "针对北方菜（烤鸭/涮羊肉/鲁菜）的重口味特点，推荐中重酒体红酒。",
        "content_body": """## 北方菜配酒分类指南

### 1. 北京烤鸭

| 食用方式 | 推荐酒款 | 搭配理由 |
|----------|----------|----------|
| 蘸甜面酱 | 黑皮诺（勃艮第） | 经典配 |
| 卷葱黄瓜 | 梅洛、品丽珠 | 中酒体 |
| 鸭架汤 | 干型雪利 Fino | 提鲜 |
| 全聚德烤鸭 | 俄勒冈黑皮诺 | 果香呼应 |

### 2. 涮羊肉

- 清汤涮羊肉：西拉、马尔贝克
- 麻酱蘸料：赤霞珠、波尔多混酿
- 孜然羊肉：歌海娜、西拉
- 红焖羊肉：巴罗洛、Brunello

### 3. 鲁菜

| 经典菜 | 推荐酒款 | 备注 |
|--------|----------|------|
| 糖醋鲤鱼 | 半干雷司令、桃红 | 甜酸平衡 |
| 九转大肠 | 阿玛罗尼、仙粉黛 | 浓味配浓酒 |
| 葱烧海参 | 勃艮第霞多丽、Viognier | 海鲜质感 |
| 油爆双脆 | 香槟、Cava | 气泡解腻 |

### 4. 京菜与东北菜

- 京酱肉丝：黑皮诺、品丽珠
- 酱爆鸡丁：半干白诗南
- 锅包肉：半甜雷司令、Moscato
- 小鸡炖蘑菇：黑皮诺、Pinotage
- 东北乱炖：西拉、马尔贝克

### 配酒原则

- 北方菜口味偏重，需中重酒体红酒
- 葱蒜味浓，可选辛香型西拉
- 糖醋类菜需甜度匹配的酒""",
    },
    {
        "id": "DEC-pairing-japanese",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "日料配酒指南",
        "title_en": "Japanese Cuisine and Wine Pairing",
        "name_cn": "日料配酒指南",
        "name_en": "Japanese Food Wine Pairing",
        "tags": ["日料", "刺身", "寿司", "天妇罗", "烧鸟", "清酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按日料类型（刺身/寿司/天妇罗/烧鸟）搭配清酒、干白与气泡酒。",
        "content_body": """## 日料配酒分类指南

### 1. 刺身

| 鱼种 | 推荐酒款 | 备注 |
|------|----------|------|
| 金枪鱼大腹 | 纯米大吟酿、黑皮诺 | 脂肪丰富 |
| 三文鱼 | 吟酿、霞多丽（未过桶） | 酒体中等 |
| 鲷鱼 | 灰皮诺、长相思 | 清淡干白 |
| 鰤鱼 | 纯米酒、过桶霞多丽 | 醇厚搭配 |

### 2. 寿司

- 醋饭的酸度需匹配高酸度酒
- 江户前寿司：纯米酒、吟酿清酒
- 卷物：干型起泡、Cava
- 炙烤寿司：黑皮诺、Pinotage

### 3. 天妇罗

- 海老天妇罗：干型雪利 Fino、香槟
- 蔬菜天妇罗：灰皮诺、长相思
- 穴子天妇罗：纯米酒、霞多丽
- 关键：气泡感切割油炸

### 4. 烧鸟（ yakitori ）

| 部位 | 推荐酒款 | 备注 |
|------|----------|------|
| 葱香鸡腿 | 纯米酒、黑皮诺 | 经典搭配 |
| 盐烤鸡皮 | 香槟、Cava | 解腻 |
| 鸡胗/鸡心 | 西拉、马尔贝克 | 浓味配 |
| 酱烤鸡肉丸 | 半干白诗南、桃红 | 甜咸平衡 |

### 5. 其他日料

- 拉面：啤酒、冰镇干型起泡
- 寿喜烧：纯米酒、黑皮诺
- 大阪烧：啤酒、桃红起泡
- 怀石料理：纯米大吟酿（全程搭配）

### 配酒原则

- 清酒是日料首选，遵循"同风土"原则
- 西式酒款选高酸干白，避开重单宁
- 酱油味重时可选略甜的酒平衡""",
    },
    {
        "id": "DEC-pairing-french",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "法餐配酒指南",
        "title_en": "French Cuisine and Wine Pairing",
        "name_cn": "法餐配酒指南",
        "name_en": "French Food Wine Pairing",
        "tags": ["法餐", "勃艮第", "波尔多", "鹅肝", "松露", "经典"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "经典法餐菜式配酒建议，遵循"产地同源"原则。",
        "content_body": """## 法餐经典配酒指南

### 1. 前菜

| 经典菜 | 推荐酒款 | 产区 |
|--------|----------|------|
| 法式洋葱汤 Gratinée | 博若莱、黑皮诺 | 勃艮第 |
| 蜗牛 Escargots | 夏布利、Sancerre | 勃艮第/卢瓦尔 |
| 鹅肝 Foie Gras | 苏玳 Sauternes | 波尔多 |
| 生蚝 Huîtres | 密斯卡岱 Muscadet | 卢瓦尔 |

### 2. 主菜

- 红酒炖牛肉 Bœuf Bourguignon：勃艮第黑皮诺
- 普罗旺斯炖菜 Ratatouille：桃红、歌海娜
- 油封鸭腿 Confit de Canard：马尔贝克、Madiran
- 烤羊排 Carré d'Agneau：波尔多红酒、Châteauneuf-du-Pape
- 红酒炖公鸡 Coq au Vin：勃艮第黑皮诺

### 3. 奶酪

- 卡蒙贝尔 Camembert：苹果酒、灰皮诺
- 洛克福 Roquefort：苏玳 Sauternes
- 孔泰 Comté：黄葡萄酒 Vin Jaune
- 布里 Brie：香槟、霞多丽

### 4. 甜点

| 甜点 | 推荐酒款 | 备注 |
|------|----------|------|
| 可丽饼 Crêpes | 贵腐甜白、冰酒 | 甜上加甜 |
| 焦糖布丁 Crème Brûlée | 托卡伊、Sauternes | 经典 |
| 巧克力松露 | 班尼杜斯 Banyuls | 红加强酒 |
| 苹果挞 Tarte Tatin | 晚收雷司令、Cidre | 苹果呼应 |

### 经典原则

- "产地同源"：法国菜配法国酒
- 鹅肝+苏玳是法国国宝级搭配
- 勃艮第菜配勃艮第酒，最稳妥""",
    },
    {
        "id": "DEC-pairing-italian",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "意餐配酒指南",
        "title_en": "Italian Cuisine and Wine Pairing",
        "name_cn": "意餐配酒指南",
        "name_en": "Italian Food Wine Pairing",
        "tags": ["意餐", "意面", "披萨", "海鲜", "地方菜系", "经典"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按意大利地方菜系（北部/中部/南部/西西里）搭配本土葡萄酒。",
        "content_body": """## 意餐地方菜系配酒指南

### 1. 北部意大利（皮埃蒙特/伦巴第/威尼托）

| 经典菜 | 推荐酒款 | 产区 |
|--------|----------|------|
| 米兰炖牛膝 Ossobuco | 巴罗洛 Barolo | 皮埃蒙特 |
| 米兰式烩饭 Risotto | 阿内斯 Arneis、Gavi | 皮埃蒙特 |
| 威尼斯墨鱼面 | Soave、灰皮诺 | 威尼托 |
| 帕玛森奶酪烩饭 | Brunello di Montalcino | 托斯卡纳 |

### 2. 中部意大利（托斯卡纳/拉齐奥）

- 佛罗伦萨牛排 Bistecca：Brunello、Chianti Classico
- 猎人风味鸡 Cacciatore：Chianti、Sangiovese
- 罗马式培根蛋面 Carbonara：Frascati、白皮诺
- 烤野猪 Cinghiale：Nobile di Montepulciano

### 3. 南部意大利（坎帕尼亚/普利亚）

| 经典菜 | 推荐酒款 | 产区 |
|--------|----------|------|
| 那不勒斯披萨 | Aglianico、Falanghina | 坎帕尼亚 |
| 海鲜意面 | Verdicchio、Greco di Tufo | 南部 |
| 普利亚烤羊肉 | Primitivo、Negroamaro | 普利亚 |
| 茄子帕尔马干酪 | Nero d'Avola、Chianti | 西西里 |

### 4. 西西里与海岛

- 海鲜烩饭 Risotto al Nero：Grillo、Insolia
- 沙丁鱼意面：Nero d'Avola、Inzolia
- 卡萨塔蛋糕：Malvasia delle Lipari、Passito

### 配酒原则

- "意大利菜配意大利酒"是经典原则
- 番茄酱汁的酸度需匹配高酸度酒
- 海鲜菜肴多搭配干白，南部为主""",
    },
    {
        "id": "DEC-pairing-dessert",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "甜点配酒指南",
        "title_en": "Dessert and Wine Pairing Guide",
        "name_cn": "甜点配酒指南",
        "name_en": "Dessert Wine Pairing",
        "tags": ["甜点", "巧克力", "水果甜点", "奶酪蛋糕", "甜酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按甜点类型（巧克力/水果/奶酪蛋糕）搭配甜酒、加强酒与冰酒。",
        "content_body": """## 甜点配酒分类指南

### 1. 水果类甜点

| 甜点 | 推荐酒款 | 搭配理由 |
|------|----------|----------|
| 苹果挞 | 晚收雷司令、Cidre | 苹果呼应 |
| 柠檬挞 | Moscato d'Asti、托卡伊 | 酸甜平衡 |
| 草莓奶油蛋糕 | 桃红起泡、Asti | 浆果香 |
| 焦糖布丁 Crème Brûlée | Sauternes、托卡伊 | 焦糖香 |

### 2. 奶酪蛋糕

- 原味奶酪蛋糕：晚收雷司令、Auslese
- 蓝莓奶酪蛋糕：Recioto、桃红起泡
- 提拉米苏：Vin Santo、Recioto della Valpolicella
- 巴斯克奶酪蛋糕：Sauternes、Monbazillac

### 3. 坚果类甜点

- 核桃派：Oloroso 雪利、Tawny Port
- 杏仁饼干 Cantucci：Vin Santo（经典配）
- 开心果蛋糕：Recioto di Soave、Malvasia
- 焦糖核桃挞：Pedro Ximénez、Tawny Port

### 4. 巧克力甜点（详见巧克力专条）

- 黑巧慕斯：Banyuls、Maury
- 巧克力熔岩蛋糕：Ruby Port、Pedro Ximénez
- 白巧克力慕斯：冰酒、Moscato d'Asti

### 5. 亚洲甜点

- 杨枝甘露：半甜雷司令、Moscato
- 红豆沙：冰酒、贵腐甜白
- 椰汁西米露：Asti、半甜起泡
- 芒果糯米饭：迟摘琼瑶浆

### 配酒原则

- 酒的甜度≥甜点的甜度
- 以甜制甜，避免干酒配甜点
- 水果甜点选果香型甜酒""",
    },
    {
        "id": "DEC-pairing-chocolate",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "巧克力配酒",
        "title_en": "Chocolate and Wine Pairing",
        "name_cn": "巧克力配酒",
        "name_en": "Chocolate Wine Pairing",
        "tags": ["巧克力", "黑巧", "牛奶巧克力", "白巧", "加强酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按巧克力类型（黑巧/牛奶/白巧）搭配加强酒、甜酒与红酒。",
        "content_body": """## 巧克力配酒分类指南

### 1. 黑巧克力（可可含量≥70%）

| 可可含量 | 推荐酒款 | 搭配理由 |
|----------|----------|----------|
| 70-80% | 班尼杜斯 Banyuls | 红加强酒经典配 |
| 80-90% | Maury、Rasteau | 浓郁匹配 |
| 90%+ | Pedro Ximénez、Tawny Port | 极浓甜酒 |

#### 经典搭配

- 黑巧克力+波特酒（LBV或Vintage）
- 黑巧克力+Banyuls（法国经典配）
- 黑巧克力+阿玛罗尼 Amarone（干红配）
- 黑巧克力+西拉（胡椒香呼应）

### 2. 牛奶巧克力

- 牛奶巧克力慕斯：Ruby Port、Recioto
- 松露巧克力：Pedro Ximénez、Tawny Port
- 牛奶巧克力蛋糕：Malvasia、Moscato
- 焦糖牛奶巧克力：Banyuls、Maury

### 3. 白巧克力

| 形式 | 推荐酒款 | 搭配理由 |
|------|----------|----------|
| 白巧克力块 | 冰酒、Sauternes | 甜度匹配 |
| 白巧克力慕斯 | Moscato d'Asti、Asti | 果香清爽 |
| 覆盆子白巧 | 桃红起泡、Brachetto | 浆果呼应 |
| 开心果白巧 | Recioto di Soave | 坚果香 |

### 4. 巧克力甜品

- 熔岩蛋糕 Lava Cake：Banyuls、Pedro Ximénez
- 布朗尼 Brownie：Tawny Port、Amarone
- 巧克力挞：Maury、Pedro Ximénez
- 巧克力冰淇淋：黑朗姆、Pedro Ximénez

### 配酒原则

- 黑巧克力需强劲甜型加强酒
- 牛奶巧克力宜Ruby Port或Recioto
- 白巧克力配甜度更高的贵腐/冰酒
- 避免干型单宁红酒配白巧克力""",
    },
    {
        "id": "DEC-pairing-barbecue",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "烧烤配酒指南",
        "title_en": "Barbecue and Wine Pairing Guide",
        "name_cn": "烧烤配酒指南",
        "name_en": "Barbecue Wine Pairing",
        "tags": ["烧烤", "中式烧烤", "BBQ", "烟熏", "烤肉"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "针对中式烧烤与西式BBQ的烟熏烤味特点，推荐重酒体红酒与果香型酒。",
        "content_body": """## 烧烤配酒分类指南

### 1. 中式烧烤（北方烤串/新疆烤肉）

| 食材 | 推荐酒款 | 搭配理由 |
|------|----------|----------|
| 羊肉串 | 西拉、马尔贝克 | 孜然呼应 |
| 烤鸡翅 | 黑皮诺、仙粉黛 | 中酒体 |
| 烤五花肉 | 赤霞珠、西拉 | 解腻 |
| 烤韭菜/茄子 | 桃红、灰皮诺 | 清爽 |
| 烤鱼 | 长相思、干型桃红 | 高酸提鲜 |
| 烤馒头 | 香槟、Prosecco | 气泡搭配 |

### 2. 西式BBQ

- 美式烟熏猪肋排：仙粉黛 Zinfandel、西拉
- 德州牛胸肉 Brisket：赤霞珠、马尔贝克
- 卡罗来纳手撕猪肉：半干雷司令（甜酱需甜酒）
- 路易斯安那辣味烧烤：桃红、半甜白诗南

### 3. 日式烧鸟与炭烤

| 食材 | 推荐酒款 | 备注 |
|------|----------|------|
| 盐烤鸡腿 | 纯米酒、黑皮诺 | 经典 |
| 酱烤鸡肉丸 | 半干白诗南 | 甜咸平衡 |
| 烤鸡皮 | 香槟、Cava | 解腻 |
| 烤葱香猪五花 | 纯米酒、西拉 | 浓味配 |

### 4. 韩式烤肉

- 烤五花肉：烧酒 Soju、黑皮诺
- 烤牛排（腌制）：西拉、马尔贝克
- 烤猪颈肉：雷司令、桃红
- 韩式辣炒年糕：半甜雷司令

### 配酒原则

- 烟熏味需重酒体红酒呼应
- 辛辣烧烤需甜度平衡
- 烤蔬菜宜选清爽干白或桃红
- 油腻烤肉可气泡酒解腻""",
    },
    {
        "id": "DEC-pairing-hotpot",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "火锅配酒指南",
        "title_en": "Hotpot and Wine Pairing Guide",
        "name_cn": "火锅配酒指南",
        "name_en": "Hotpot Wine Pairing",
        "tags": ["火锅", "麻辣锅", "清汤锅", "潮汕牛肉锅", "气泡酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按火锅类型（麻辣/清汤/潮汕牛肉锅）搭配气泡酒、甜白与中酒体红酒。",
        "content_body": """## 火锅配酒分类指南

### 1. 麻辣火锅（重庆/四川）

| 搭配方式 | 推荐酒款 | 搭配理由 |
|----------|----------|----------|
| 主搭配 | 半甜雷司令、琼瑶浆 | 甜度解辣 |
| 气泡解辣 | Moscato d'Asti、Prosecco | 低酒精+气泡 |
| 油碟解腻 | 阿斯蒂 Asti、半干起泡 | 果香清口 |
| 冰镇选择 | 干型起泡、Cava | 冰镇清爽 |

#### 禁忌

- 高酒精重酒=灼烧感放大
- 高单宁红酒+麻辣=苦涩难咽

### 2. 清汤锅（菌汤/番茄/养生）

- 菌汤锅：黑皮诺、霞多丽（未过桶）
- 番茄锅：桑娇维塞、Sangiovese
- 椰子鸡锅：霞多丽、Viognier
- 药膳锅：干型雪利 Fino、灰皮诺

### 3. 潮汕牛肉锅

| 牛肉部位 | 推荐酒款 | 备注 |
|----------|----------|------|
| 吊龙（里脊） | 黑皮诺、梅洛 | 中酒体 |
| 雪花/脖仁 | 赤霞珠、西拉 | 重酒体 |
| 五花腱 | 巴罗洛、Brunello | 单宁强劲 |
| 匙皮/匙柄 | 霞多丽、Viognier | 干白搭配 |

### 4. 其他火锅

- 老北京铜锅涮羊肉：西拉、马尔贝克
- 云南菌子火锅：黑皮诺、过桶霞多丽
- 贵州酸汤鱼：长相思、干型雷司令
- 海鲜锅：密斯卡岱、夏布利

### 配酒原则

- 麻辣锅必须低酒精+甜度
- 潮汕牛肉锅按部位选酒，类似牛排
- 清汤锅依汤底口味决定
- 冰镇酒款是火锅良伴""",
    },
    {
        "id": "DEC-pairing-vegetarian",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "素食配酒指南",
        "title_en": "Vegetarian Cuisine and Wine Pairing",
        "name_cn": "素食配酒指南",
        "name_en": "Vegetarian Wine Pairing",
        "tags": ["素食", "豆制品", "菌菇", "蔬菜", "植物基"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按素食类型（豆制品/菌菇/蔬菜）搭配干白、中酒体红酒与橙酒。",
        "content_body": """## 素食配酒分类指南

### 1. 豆制品

| 食材 | 推荐酒款 | 搭配理由 |
|------|----------|----------|
| 麻婆豆腐 | 半甜雷司令 | 甜度解辣 |
| 家常豆腐 | 黑皮诺、品丽珠 | 中酒体 |
| 豆腐脑（咸） | 灰皮诺、长相思 | 高酸提鲜 |
| 臭豆腐 | 香槟、Cava | 气泡解腻 |
| 凉拌豆腐 | 干型雪利 Fino | 同发酵风味 |
| 腐乳 | Tawny Port、Oloroso | 浓厚搭配 |

### 2. 菌菇类

- 松露：勃艮第黑皮诺、巴罗洛（经典配）
- 牛肝菌：黑皮诺、Brunello
- 杏鲍菇（烤）：西拉、马尔贝克
- 香菇（红烧）：梅洛、品丽珠
- 金针菇（涮）：霞多丽、Viognier
- 茶树菇：歌海娜、Rhône混酿

### 3. 蔬菜类

| 蔬菜 | 推荐酒款 | 备注 |
|------|----------|------|
| 烤南瓜 | 霞多丽、Viognier | 香甜搭配 |
| 烤茄子 | 西拉、黑皮诺 | 烟熏匹配 |
| 朝鲜蓟 | 橙酒 Orange Wine | 朝鲜蓟难点 |
| 芦笋 | 长相思、绿酒 Vinho Verde | 经典配 |
| 番茄沙拉 | 桃红、Sangiovese | 高酸平衡 |
| 烤甜椒 | 歌海娜、桃红 | 甜椒香 |

### 4. 谷物与植物基

- 藜麦沙拉：长相思、Verdejo
- 烤蘑菇意面：黑皮诺、Sangiovese
- 植物肉汉堡：赤霞珠、马尔贝克
- 鹰嘴豆泥：干型雪利、Assyrtiko

### 配酒原则

- 朝鲜蓟使酒变甜，需选橙酒或高酸干白
- 芦笋含硫化合物，长相思是经典配
- 菌菇的鲜味与陈年红酒呼应
- 素食清淡，避免过重酒体""",
    },
    {
        "id": "DEC-pairing-appetizer",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "开胃菜配酒",
        "title_en": "Appetizer and Wine Pairing",
        "name_cn": "开胃菜配酒",
        "name_en": "Appetizer Wine Pairing",
        "tags": ["开胃菜", "前菜", "小食", "tapas", "起泡酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "开胃菜配酒主打高酸干白、起泡酒与干型雪利，激发食欲。",
        "content_body": """## 开胃菜配酒分类指南

### 1. 经典开胃酒

| 酒款类型 | 推荐选择 | 适用场景 |
|----------|----------|----------|
| 起泡酒 | 香槟、Cava、Prosecco | 通用开胃 |
| 干白 | 长相思、夏布利 | 海鲜前菜 |
| 干型雪利 | Fino、Manzanilla | 西班牙tapas |
| 加强酒 | Lillet、Vermouth | 经典 aperitif |

### 2. 西式前菜

- 生蚝：密斯卡岱 Muscadet、夏布利
- 鹅肝：苏玳 Sauternes（经典配）
- 烟熏三文鱼：香槟、勃艮第霞多丽
- 沙拉（油醋汁）：长相思、灰皮诺
- 帕尔马火腿蜜瓜：Prosecco、Lambrusco
- 卡布列兹 Caprese：桃红、Verdicchio

### 3. 西班牙 Tapas

| Tapas | 推荐酒款 | 产区 |
|-------|----------|------|
| 伊比利亚火腿 | Fino、Manzanilla | 赫雷斯 |
| 西班牙煎蛋 Tortilla | Verdejo、Albariño | 卢埃达 |
| 炸丸子 Croquetas | Cava、干型雪利 | 加泰罗尼亚 |
| 烤辣椒 Padrón | Txakoli、Albariño | 巴斯克 |
| 蒜香虾 Gambas | Fino、Manzanilla | 安达卢西亚 |

### 4. 中式冷菜

- 凉拌黄瓜：长相思、灰皮诺
- 白切鸡：霞多丽（未过桶）
- 卤水拼盘：干型雪利 Fino
- 凉拌海蜇：密斯卡岱、夏布利
- 蒜泥白肉：半干白诗南、桃红

### 5. 日式前菜

- 毛豆：啤酒、冰镇干型起泡
- 冷豆腐 Hiyyakko：纯米酒、灰皮诺
- 醋渍章鱼：吟酿清酒、干白
- 厚蛋烧：纯米酒、霞多丽

### 配酒原则

- 开胃菜需激发食欲，选高酸干型酒
- 起泡酒是万能开胃酒
- 油腻前菜可选干型雪利或气泡
- 量小味清，避免重酒体""",
    },
    {
        "id": "DEC-pairing-soup",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "汤品配酒",
        "title_en": "Soup and Wine Pairing",
        "name_cn": "汤品配酒",
        "name_en": "Soup Wine Pairing",
        "tags": ["汤品", "浓汤", "清汤", "炖汤", "白葡萄酒"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按汤品类型（浓汤/清汤/炖汤）搭配干白、雪利与中酒体红酒。",
        "content_body": """## 汤品配酒分类指南

### 1. 浓汤（奶油/浓稠）

| 汤品 | 推荐酒款 | 搭配理由 |
|------|----------|----------|
| 奶油蘑菇汤 | 霞多丽（过桶）、Viognier | 奶油质感 |
| 南瓜浓汤 | 霞多丽、琼瑶浆 | 香甜呼应 |
| 玉米浓汤 | 霞多丽、白诗南 | 圆润酒体 |
| 番茄浓汤 | 桃红、Sangiovese | 高酸平衡 |
| 海鲜周打汤 | 夏布利、密斯卡岱 | 海鲜搭配 |

### 2. 清汤

- 法式清汤 Consommé：干型雪利 Fino、干型马德拉
- 中式清汤（鸡汤）：霞多丽（未过桶）、灰皮诺
- 日式出汁 Dashi：纯米酒、吟酿
- 越式河粉汤：长相思、干型雷司令
- 泰式冬阴功：长相思、干型雷司令

### 3. 炖汤/煲汤

| 汤品 | 推荐酒款 | 备注 |
|------|----------|------|
| 老火靓汤 | 干型雪利 Fino | 提鲜 |
| 佛跳墙 | 勃艮第霞多丽、波尔多干白 | 复杂搭配 |
| 人参鸡汤 | 琼瑶浆、Viognier | 香料呼应 |
| 当归鸭汤 | 黑皮诺、Pinotage | 中酒体 |
| 牛肉炖汤 | 西拉、马尔贝克 | 重酒体 |

### 4. 甜汤

- 红豆沙：冰酒、贵腐甜白
- 绿豆汤：半甜雷司令、Moscato
- 银耳莲子羹：迟摘雷司令、Asti
- 芝麻糊：Tawny Port、Pedro Ximénez
- 燕窝：冰酒、贵腐甜白

### 配酒原则

- 浓汤需圆润酒体搭配
- 清汤选高酸干型酒提鲜
- 炖汤依主料决定（荤重素轻）
- 甜汤需甜度匹配的甜酒
- 汤品温度影响酒款选择，热汤宜冰镇酒""",
    },
    {
        "id": "DEC-pairing-sauce-based",
        "category": "ENT",
        "subcategory": "pairing",
        "title": "按酱汁配酒",
        "title_en": "Sauce-Based Food and Wine Pairing",
        "name_cn": "按酱汁配酒",
        "name_en": "Sauce-Based Wine Pairing",
        "tags": ["酱汁", "红酒汁", "奶油汁", "番茄酱", "搭配方法"],
        "source": "WSET Food & Wine Pairing",
        "data_confidence": "official",
        "summary": "按酱汁类型（红酒汁/奶油汁/番茄酱）搭配酒款，是高级配酒方法。",
        "content_body": """## 按酱汁配酒分类指南

### 核心原则

- "酱汁决定配酒"是法餐高级原则
- 食材本身其次，酱汁风味主导搭配
- 酱汁中若含酒，配同款酒最稳

### 1. 红酒汁类

| 酱汁 | 适用菜 | 推荐酒款 |
|------|--------|----------|
| 波尔多酱 Bordelaise | 牛排 | 赤霞珠、波尔多混酿 |
| 黑松露红酒汁 | 牛排 | 勃艮第黑皮诺 |
| 鹅肝红酒汁 | 红肉 | 苏玳、Pinot Noir |
- 同源原则：酱汁用什么酒，就配什么酒

### 2. 奶油汁类

- 奶油蘑菇汁：霞多丽（过桶）、Viognier
- 奶油芥末汁：雷司令（干型）、白皮诺
- 奶油龙蒿汁：长相思、Sancerre
- 奶油柠檬汁：长相思、Verdicchio
- 荷兰酱 Hollandaise：霞多丽、香槟

### 3. 番茄酱汁

| 酱汁 | 适用菜 | 推荐酒款 |
|------|--------|----------|
| 那不勒斯番茄酱 | 意面、披萨 | Sangiovese、Chianti |
| 普塔尼斯卡酱 Puttanesca | 意面 | Aglianico、Nero d'Avola |
| 阿拉比亚塔 Arrabbiata | 意面 | Montepulciano、Primitivo |
| 番茄罗勒酱 | 意面 | 桃红、Sangiovese |

### 4. 香草酱

- 香草酱 Chimichurri：马尔贝克（阿根廷经典）
- 罗勒青酱 Pesto：Vermentino、Pigato
- 莎莎酱 Salsa Verde：Albariño、Vinho Verde
- 薄荷酱：长相思、Sauvignon Blanc

### 5. 亚洲酱汁

| 酱汁 | 推荐酒款 | 备注 |
|------|----------|------|
| 黑椒汁 | 赤霞珠、西拉 | 浓味配 |
| X.O.酱 | 香槟、过桶霞多丽 | 鲜味搭配 |
| 沙茶酱 | 西拉、马尔贝克 | 重酒体 |
| 咖喱酱 | 琼瑶浆、半甜雷司令 | 甜度解辣 |
| 豆瓣酱 | 半干白诗南、桃红 | 平衡咸辣 |

### 配酒原则

- 酱汁含酒时，配同款酒最稳
- 奶油酱需圆润白葡萄酒
- 番茄酱需高酸度红酒
- 香草酱依香草类型选酒""",
    },
]
