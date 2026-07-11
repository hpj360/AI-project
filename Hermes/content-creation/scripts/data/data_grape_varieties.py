"""葡萄品种百科数据 - 权威来源。

数据源：
- Wine Grapes (Jancis Robinson)
- WSET教材
- Wikipedia

置信度：official
"""

ENTRIES = [
    {
        "id": "GRAPE-cabernet-sauvignon",
        "category": "ENT",
        "subcategory": "grape",
        "title": "赤霞珠",
        "title_en": "Cabernet Sauvignon",
        "name_cn": "赤霞珠",
        "name_en": "Cabernet Sauvignon",
        "tags": ["葡萄品种", "红品种", "赤霞珠", "波尔多"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "世界种植最广泛的红葡萄品种，原产波尔多，以单宁强、骨架感著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国波尔多
- **亲本**：品丽珠 × 长相思（DNA验证，1997年确认）
- **果串**：中等大小，圆锥形，松散
- **果粒**：小，皮厚，色深
- **成熟期**：晚熟品种（萌芽晚，采收晚）

### 风味特征

#### 冷凉产区（波尔多/纳帕海岸）
- **香气**：黑醋栗、雪松、薄荷、青椒
- **单宁**：高，结构感强
- **酸度**：高
- **酒体**：饱满

#### 温暖产区（纳帕谷/库纳瓦拉）
- **香气**：黑莓、黑樱桃、香草、甘草
- **单宁**：高但更柔和
- **酸度**：中等
- **酒体**：饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 波尔多左岸 | 骨架感强，陈年潜力大 | 拉菲、拉图、玛歌 |
| 纳帕谷 | 果味浓郁，酒体饱满 | 作品一号、银橡木 |
| 库纳瓦拉 | 薄荷特征，单宁细腻 | 奔酒庄 |
| 托斯卡纳 | 意大利风格，酸度高 | 天娜、西施佳雅 |
| 宁夏 | 新兴产区，果味纯净 | 迦南美地、银色高地 |

### 混酿搭配

- **波尔多混酿**：赤霞珠+美乐+品丽珠+小维多
- **超级托斯卡纳**：赤霞珠+桑娇维塞
- **澳洲风格**：赤霞珠+西拉

### 陈年潜力

- 优质波尔多列级庄：15-30年+
- 纳帕谷顶级：10-20年
- 普通餐酒：3-5年""",
    },
    {
        "id": "GRAPE-merlot",
        "category": "ENT",
        "subcategory": "grape",
        "title": "美乐",
        "title_en": "Merlot",
        "name_cn": "美乐",
        "name_en": "Merlot",
        "tags": ["葡萄品种", "红品种", "美乐", "波尔多"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "早熟的红葡萄品种，原产波尔多右岸，以圆润柔和、李子风味著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国波尔多
- **亲本**：品丽珠 × Madeleine Noire des Charentes（2009年确认）
- **果串**：中等大小，圆柱形，较松散
- **果粒**：中等，皮中等厚度，蓝黑色
- **成熟期**：早熟品种（比赤霞珠早1-2周）

### 风味特征

#### 冷凉产区（波尔多右岸/智利冷凉区）
- **香气**：红色李子、黑樱桃、紫罗兰、雪松
- **单宁**：中等
- **酸度**：中等
- **酒体**：中等至饱满

#### 温暖产区（加州/澳大利亚）
- **香气**：黑莓、李子酱、巧克力、香草
- **单宁**：柔和
- **酸度**：中低
- **酒体**：饱满，圆润

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 波美侯 | 丝滑细腻，陈年潜力强 | 柏图斯、里鹏 |
| 圣埃美隆 | 结构与优雅并存 | 白马、欧颂 |
| 纳帕谷 | 果味奔放，酒体饱满 | 鹿跃、Duckhorn |
| 智利中央山谷 | 性价比高，果味纯净 | Concha y Toro、Errázuriz |
| 华盛顿州 | 结构紧实，平衡度高 | L'Ecole 41、Chateau Ste. Michelle |

### 混酿搭配

- **波尔多右岸混酿**：美乐为主+品丽珠+赤霞珠
- **超级托斯卡纳**：可作主力，搭配桑娇维塞
- **新世界单品种**：常单独装瓶，体现圆润风格

### 陈年潜力

- 波美侯顶级酒庄：15-25年+
- 圣埃美隆列级庄：10-20年
- 新世界单品种：3-8年""",
    },
    {
        "id": "GRAPE-pinot-noir",
        "category": "ENT",
        "subcategory": "grape",
        "title": "黑皮诺",
        "title_en": "Pinot Noir",
        "name_cn": "黑皮诺",
        "name_en": "Pinot Noir",
        "tags": ["葡萄品种", "红品种", "黑皮诺", "勃艮第"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "娇贵的红葡萄品种，原产勃艮第，被誉为红葡萄之王，喜冷凉气候。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国勃艮第
- **亲本**：古老品种，可能为黑皮诺 × Gouais Blanc杂交祖先
- **果串**：小，圆柱形，紧密
- **果粒**：小，皮薄，色浅
- **成熟期**：早熟品种

### 风味特征

#### 勃艮第（金丘）
- **香气**：红色樱桃、覆盆子、紫罗兰、林地、蘑菇（陈年）
- **单宁**：低至中等
- **酸度**：高
- **酒体**：轻至中等

#### 新世界（俄勒冈/新西兰/加州）
- **香气**：红樱桃、草莓、香料的橡木
- **单宁**：低
- **酸度**：中高
- **酒体**：中等

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 勃艮第夜丘 | 复杂优雅，陈年潜力强 | 罗曼尼康帝、乐华 |
| 勃艮第博讷丘 | 圆润柔和，果味突出 | 飞马、路易亚都 |
| 俄勒冈威拉米特 | 平衡优雅，类似勃艮第 | Domaine Drouhin、Beaux Frères |
| 新西兰中奥塔哥 | 果味奔放，集中度高 | 飞马湾、Felton Road |
| 加州俄罗斯河谷 | 饱满丰富，香气浓郁 | Kistler、Williams Selyem |

### 混酿搭配

- 几乎都为单品种酿造
- 香槟产区用作香槟混酿的主要红品种
- 偶尔与佳美混酿（勃艮第Passe-tout-grains）

### 陈年潜力

- 勃艮第特级园：15-30年+
- 勃艮第一级园：8-15年
- 新世界黑皮诺：3-8年""",
    },
    {
        "id": "GRAPE-syrah",
        "category": "ENT",
        "subcategory": "grape",
        "title": "西拉",
        "title_en": "Syrah",
        "name_cn": "西拉",
        "name_en": "Syrah / Shiraz",
        "tags": ["葡萄品种", "红品种", "西拉", "Shiraz", "罗纳河谷"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "法国称Syrah、澳洲称Shiraz的红葡萄品种，以胡椒香料风味和深色著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国北罗纳河谷（争议：可能源自罗纳或西西里）
- **亲本**：Dureza × Mondeuse Blanche（DNA验证，2001年）
- **果串**：中等大小，圆柱形，紧凑
- **果粒**：小，皮厚，色深
- **成熟期**：中晚熟

### 风味特征

#### 北罗纳河谷（冷凉风格）
- **香气**：黑莓、紫罗兰、黑胡椒、培根脂、橄榄
- **单宁**：高
- **酸度**：中高
- **酒体**：饱满

#### 澳大利亚（温暖风格 Shiraz）
- **香气**：黑莓酱、李子、黑巧克力、甘草、桉树
- **单宁**：中等
- **酸度**：中低
- **酒体**：饱满，浓郁

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 北罗纳罗第丘 | 胡椒脂香，优雅深邃 | 吉佳乐、Chapoutier |
| 北罗纳埃米塔日 | 浓郁复杂，陈年强 | Jaboulet、Chave |
| 巴罗萨谷 | 浓郁奔放，高酒精 | 奔富葛兰许、Henschke |
| 猎人谷 | 中等酒体，陈年优雅 | Tyrrell's、Brokenwood |
| 华盛顿州 | 平衡丰富，结构紧实 | Cayuse、Charles Smith |

### 混酿搭配

- **罗纳河谷GSM混酿**：歌海娜+西拉+慕合怀特
- **澳洲风格**：西拉+赤霞珠
- **南非风格**：常与歌海娜、慕合怀特混酿

### 陈年潜力

- 罗第丘顶级：10-20年+
- 埃米塔日顶级：20-40年
- 巴罗萨顶级Shiraz：15-25年
- 普通餐酒：3-5年""",
    },
    {
        "id": "GRAPE-grenache",
        "category": "ENT",
        "subcategory": "grape",
        "title": "歌海娜",
        "title_en": "Grenache",
        "name_cn": "歌海娜",
        "name_en": "Grenache / Garnacha",
        "tags": ["葡萄品种", "红品种", "歌海娜", "教皇新堡", "Garnacha"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "西班牙原产的红葡萄品种，高酒精低单宁，是教皇新堡和南罗纳的主角。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：西班牙阿拉贡
- **亲本**：古老品种，与Cannonau（撒丁岛）同源
- **果串**：大，圆锥形，松散
- **果粒**：中等，皮薄，色浅
- **成熟期**：晚熟

### 风味特征

#### 南罗纳河谷
- **香气**：红色浆果、白胡椒、甘草、百里香、皮革
- **单宁**：中低
- **酸度**：低
- **酒体**：饱满，高酒精

#### 西班牙（Garnacha）
- **香气**：草莓、覆盆子、橙皮、香料
- **单宁**：中等
- **酸度**：中低
- **酒体**：中等至饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 教皇新堡 | 浓郁复杂，香料丰富 | Château de Beaucastel、Clos des Papes |
| 普里奥拉托 | 浓郁集中，矿物感 | Alvaro Palacios、Clos Mogador |
| 卡里涅纳/纳瓦拉 | 性价比高的果味风格 | Borsao、Aragon |
| 澳洲麦克拉伦谷 | 浓郁丰富，陈年潜力 | d'Arenberg、Torbreck |
| 加州圣罗莎山 | 老藤风格，集中度高 | Tablas Creek、Saxon Brown |

### 混酿搭配

- **南罗纳GSM**：歌海娜为主+西拉+慕合怀特
- **教皇新堡**：最多可含13个品种
- **里奥哈**：少量与丹魄混酿增加酒体

### 陈年潜力

- 教皇新堡顶级：10-20年
- 普里奥拉托顶级：15-30年+
- 老藤Garnacha：8-15年
- 普通餐酒：2-5年""",
    },
    {
        "id": "GRAPE-malbec",
        "category": "ENT",
        "subcategory": "grape",
        "title": "马尔贝克",
        "title_en": "Malbec",
        "name_cn": "马尔贝克",
        "name_en": "Malbec",
        "tags": ["葡萄品种", "红品种", "马尔贝克", "阿根廷", "Côt"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "阿根廷旗舰红葡萄品种，原产法国卡奥尔，以深色紫罗兰色泽和果味著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国西南部（卡奥尔）
- **亲本**：Magdeleine Noire des Charentes × Prunelart
- **果串**：中等大小，圆锥形，较松散
- **果粒**：中等，皮厚，色深
- **成熟期**：中熟

### 风味特征

#### 阿根廷（高海拔）
- **香气**：黑莓、紫罗兰、李子、可可、皮革
- **单宁**：中高
- **酸度**：中等
- **酒体**：饱满

#### 法国卡奥尔
- **香气**：黑樱桃、李子、香料、泥土、雪松
- **单宁**：高
- **酸度**：中高
- **酒体**：饱满，骨架感强

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 门多萨（阿根廷） | 果味浓郁，紫罗兰香 | Catena Zapata、Achaval-Ferrer |
| 乌科谷（阿根廷） | 高酸度，结构紧实 | Zuccardi、Salentein |
| 卡奥尔（法国） | 深色，单宁强，陈年 | Clos Triguedina、Château Lagrézette |
| 卢瓦尔河谷（Côt） | 轻盈风格 | Domaine de la Charbonnière |
| 华盛顿州 | 平衡丰富 | Seven Hills、Reynvaan |

### 混酿搭配

- **波尔多混酿**：少量添加（曾广泛种植）
- **阿根廷单品种**：通常单独装瓶
- **卡奥尔混酿**：马尔贝克为主+美乐+丹拿

### 陈年潜力

- 阿根廷顶级单园：10-15年+
- 卡奥尔传统酒：10-20年
- 普通餐酒：3-5年""",
    },
    {
        "id": "GRAPE-tempranillo",
        "category": "ENT",
        "subcategory": "grape",
        "title": "丹魄",
        "title_en": "Tempranillo",
        "name_cn": "丹魄",
        "name_en": "Tempranillo",
        "tags": ["葡萄品种", "红品种", "丹魄", "里奥哈", "西班牙"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "西班牙国宝级红葡萄品种，里奥哈和杜罗河岸的主角，以陈年潜力著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：西班牙北部
- **亲本**：Albillo Mayor × Benedicto（2012年DNA确认）
- **果串**：大，圆柱形，紧凑
- **果粒**：中等，皮厚，色深
- **成熟期**：早熟（Tempranillo意为"小早熟"）

### 风味特征

#### 里奥哈（传统风格）
- **香气**：红色樱桃、李子、皮革、香草、椰子（美国桶）
- **单宁**：中等
- **酸度**：中低
- **酒体**：中等

#### 杜罗河岸（现代风格）
- **香气**：黑莓、黑樱桃、甘草、香料、矿物
- **单宁**：高
- **酸度**：中等
- **酒体**：饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 里奥哈 | 优雅传统，橡木桶陈年 | 洛佩兹、Muga、Artadi |
| 杜罗河岸 | 浓郁强劲，单宁紧实 | Vega Sicilia、Pingus、Pesquera |
| 托罗 | 浓郁奔放，高酒精 | Termanthia、El Picaro |
| 葡萄牙杜罗 | 波特酒原料 | Quinta do Crasto、Niepoort |
| 加州/澳洲 | 新世界尝试 | Abacela、Kalleske |

### 混酿搭配

- **里奥哈混酿**：丹魄为主+歌海娜+马苏埃罗+格拉西亚诺
- **杜罗河岸**：常为单品种或与少量赤霞珠混酿
- **波特酒**：混酿原料之一

### 陈年潜力

- 里奥哈Gran Reserva：20-30年+
- Vega Sicilia Unico：30-50年+
- 杜罗河岸顶级：10-20年
- Crianza级别：3-5年""",
    },
    {
        "id": "GRAPE-nebbiolo",
        "category": "ENT",
        "subcategory": "grape",
        "title": "内比奥罗",
        "title_en": "Nebbiolo",
        "name_cn": "内比奥罗",
        "name_en": "Nebbiolo",
        "tags": ["葡萄品种", "红品种", "内比奥罗", "巴罗洛", "巴巴莱斯科"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "意大利皮埃蒙特的贵族品种，巴罗洛和巴巴莱斯科的主角，以高单宁高酸著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：意大利皮埃蒙特
- **亲本**：古老品种，亲本未完全确定
- **果串**：中等大小，圆柱形，紧凑
- **果粒**：中等，皮厚，色浅（表面有雾状蜡质，"Nebbia"意为雾）
- **成熟期**：极晚熟

### 风味特征

#### 巴罗洛（结构型）
- **香气**：红色樱桃、玫瑰花瓣、焦油、松露、皮革
- **单宁**：极高
- **酸度**：高
- **酒体**：饱满，骨架感强

#### 巴巴莱斯科（优雅型）
- **香气**：红樱桃、紫罗兰、茴香、白胡椒
- **单宁**：高
- **酸度**：高
- **酒体**：中等至饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 巴罗洛 | 强劲复杂，陈年潜力强 | Giacomo Conterno、Gaja、Bruno Giacosa |
| 巴巴莱斯科 | 优雅细腻，成熟较快 | Gaja、Produttori del Barbaresco |
| 朗格 | 较早饮风格 | Vietti、Pio Cesare |
| 加蒂纳拉/盖梅 | 北皮埃蒙特风格 | Travaglini、Antoniolo |
| 加州/澳洲 | 新世界尝试少 | Palmina、DaVero |

### 混酿搭配

- 几乎都为单品种酿造（法律要求95%-100%）
- 朗格Nebbiolo d'Alba可少量混酿
- 偶尔与 Vespolina、Bonarda 混酿（北皮埃蒙特）

### 陈年潜力

- 巴罗洛顶级：20-40年+
- 巴巴莱斯科顶级：15-25年+
- 朗格普通级别：5-10年
- 必须陈年才能软化单宁""",
    },
    {
        "id": "GRAPE-sangiovese",
        "category": "ENT",
        "subcategory": "grape",
        "title": "桑娇维塞",
        "title_en": "Sangiovese",
        "name_cn": "桑娇维塞",
        "name_en": "Sangiovese",
        "tags": ["葡萄品种", "红品种", "桑娇维塞", "基安蒂", "托斯卡纳"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "意大利种植最广泛的红葡萄品种，基安蒂和布鲁奈罗的主角，高酸高单宁。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：意大利托斯卡纳
- **亲本**：Ciliegiolo × Calabrese Montenuovo（DNA验证，2004年）
- **果串**：大，圆柱形，松散
- **果粒**：中等，皮中等厚度，色中等
- **成熟期**：中晚熟

### 风味特征

#### 基安蒂Classico
- **香气**：红色樱桃、酸樱桃、紫罗兰、草本、茶叶
- **单宁**：高
- **酸度**：高
- **酒体**：中等

#### 布鲁奈罗 di Montalcino
- **香气**：黑樱桃、李子、皮革、烟草、香料
- **单宁**：高
- **酸度**：高
- **酒体**：饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 基安蒂Classico | 优雅酸度高，樱桃香 | Castello di Ama、Felsina |
| 布鲁奈罗 di Montalcino | 浓郁复杂，陈年强 | Biondi-Santi、Il Poggione |
| 贵族蒙特普尔恰诺 | 圆润平衡 | Avignonesi、Poliziano |
| 超级托斯卡纳 | 与赤霞珠混酿 | 天娜、Tignanello |
| 罗马涅桑娇维塞 | 简单易饮 | Tre Monti、San Valentino |

### 混酿搭配

- **基安蒂混酿**：桑娇维塞为主（80%+）+ Canaiolo + Colorino
- **超级托斯卡纳**：桑娇维塞+赤霞珠/美乐
- **传统贵族蒙特普尔恰诺**：桑娇维塞为主

### 陈年潜力

- 布鲁奈诺 Riserva：20-30年+
- 基安蒂Classico Riserva：10-15年
- 普通基安蒂：3-5年
- 超级托斯卡纳：10-20年+""",
    },
    {
        "id": "GRAPE-cabernet-franc",
        "category": "ENT",
        "subcategory": "grape",
        "title": "品丽珠",
        "title_en": "Cabernet Franc",
        "name_cn": "品丽珠",
        "name_en": "Cabernet Franc",
        "tags": ["葡萄品种", "红品种", "品丽珠", "卢瓦尔河谷", "波尔多"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "波尔多混酿的重要配角，卢瓦尔河谷独立主角，赤霞珠的亲本之一。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国波尔多/巴斯克地区
- **亲本**：古老品种，为赤霞珠的父本
- **果串**：中等大小，圆柱形，松散
- **果粒**：小，皮中等厚度，色中等
- **成熟期**：早熟（比赤霞珠早）

### 风味特征

#### 卢瓦尔河谷（单品种）
- **香气**：红色覆盆子、紫罗兰、青椒、石墨、甘草
- **单宁**：中等
- **酸度**：中高
- **酒体**：中等

#### 波尔多（混酿）
- **香气**：增加香料感和草本香
- **单宁**：贡献柔和单宁
- **酸度**：提升酸度
- **酒体**：增加复杂度

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 希农 | 优雅细致，香气馥郁 | Charles Joguet、Coulée de Serrant |
| 布尔格伊 | 结构感强，陈年潜力 | Domaine de la Chevalerie |
| 索米尔-尚皮尼 | 平衡优雅 | Clos Rougeard |
| 圣埃美隆 | 混酿重要角色 | 白马、Figeac |
| 加州/华盛顿州 | 新世界尝试 | Lang & Reed、Chinook |

### 混酿搭配

- **波尔多右岸混酿**：与美乐、赤霞珠搭配
- **波尔多左岸混酿**：少量使用，增加复杂度
- **卢瓦尔河谷**：通常单品种装瓶

### 陈年潜力

- 卢瓦尔河谷顶级：10-15年+
- 圣埃美隆顶级混酿：15-25年
- 普通餐酒：3-5年
- Clos Rougeard：20年+""",
    },
    {
        "id": "GRAPE-zinfandel",
        "category": "ENT",
        "subcategory": "grape",
        "title": "增芳德",
        "title_en": "Zinfandel",
        "name_cn": "增芳德",
        "name_en": "Zinfandel",
        "tags": ["葡萄品种", "红品种", "增芳德", "美国", "Primitivo"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "美国特色红葡萄品种，与意大利Primitivo同源，以老藤丰富果味著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：克罗地亚（与Tribidrag/Crljenak Kaštelanski同源）
- **亲本**：古老品种，与意大利Primitivo同源
- **果串**：大，圆柱形，紧凑（果粒成熟不均）
- **果粒**：中等，皮中等厚度，色深
- **成熟期**：中晚熟，成熟不均匀

### 风味特征

#### 加州老藤
- **香气**：黑莓、覆盆子果酱、肉桂、丁香、皮革
- **单宁**：中高
- **酸度**：中等
- **酒体**：饱满，高酒精

#### 意大利Primitivo
- **香气**：黑樱桃、李子、甘草、香料
- **单宁**：中等
- **酸度**：中低
- **酒体**：饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 索诺玛干溪谷 | 浓郁奔放，老藤丰富 | Ridge、Ravenswood、Turley |
| 纳帕谷 | 饱满丰富，结构感强 | Storybook Mountain、Robert Biale |
| 帕索罗布尔斯 | 集中浓郁，酒体饱满 | Turley、Tablas Creek |
| 普利亚（意大利Primitivo） | 性价比高，果味丰富 | Rivera、Cosimo Taurino |
| 克罗地亚 | 原产地风格 | BIBICh、Korta Katarina |

### 混酿搭配

- 通常为单品种装瓶
- 加州"老藤混酿"：常多个老藤地块混酿
- 普利亚：可与Negroamaro混酿

### 陈年潜力

- 索诺玛老藤顶级：10-15年
- 普通加州Zinfandel：3-5年
- 普利亚Primitivo：3-5年
- Ridge Monte Bello：15-25年+（含其他品种）""",
    },
    {
        "id": "GRAPE-mourvedre",
        "category": "ENT",
        "subcategory": "grape",
        "title": "慕合怀特",
        "title_en": "Mourvèdre",
        "name_cn": "慕合怀特",
        "name_en": "Mourvèdre / Monastrell",
        "tags": ["葡萄品种", "红品种", "慕合怀特", "Monastrell", "邦多尔"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "南罗纳和邦多尔的红葡萄品种，西班牙称Monastrell，以肉类野味和结构感著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：西班牙（与Monastrell同源）
- **亲本**：古老品种
- **果串**：中等大小，圆锥形，紧凑
- **果粒**：中等，皮厚，色深
- **成熟期**：极晚熟（需要充足热量）

### 风味特征

#### 南罗纳河谷
- **香气**：黑色浆果、野味、肉类、皮革、胡椒
- **单宁**：高
- **酸度**：中等
- **酒体**：饱满

#### 西班牙（Monastrell）
- **香气**：黑莓、李子、黑巧克力、甘草、矿物
- **单宁**：高
- **酸度**：中低
- **酒体**：饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 邦多尔 | 单品种为主，陈年强 | Domaine Tempier、Castillon |
| 教皇新堡 | 混酿重要角色 | Château de Beaucastel |
| 西班牙胡米亚 | Monastrell旗舰产区 | Casa Castillo、Bodegas Iniesta |
| 西班牙耶克拉 | 浓郁奔放 | Castaño |
| 澳洲巴罗萨/麦克拉伦 | 老藤丰富 | d'Arenberg、Turkey Flat |

### 混酿搭配

- **南罗纳GSM混酿**：歌海娜+西拉+慕合怀特
- **邦多尔**：慕合怀特为主（50-95%）+西拉+歌海娜
- **澳洲GSM**：经典三剑客混酿

### 陈年潜力

- 邦多尔顶级：15-25年+
- 教皇新堡顶级：10-20年
- 西班牙Monastrell顶级：8-15年
- 普通餐酒：3-5年""",
    },
    {
        "id": "GRAPE-chardonnay",
        "category": "ENT",
        "subcategory": "grape",
        "title": "霞多丽",
        "title_en": "Chardonnay",
        "name_cn": "霞多丽",
        "name_en": "Chardonnay",
        "tags": ["葡萄品种", "白品种", "霞多丽", "勃艮第"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "世界上最百搭的白葡萄品种，勃艮第白之王，可适应多种气候和酿造风格。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国勃艮第（霞多丽村）
- **亲本**：黑皮诺 × Gouais Blanc（DNA验证）
- **果串**：小到中等，圆柱形，紧凑
- **果粒**：小，皮薄，黄绿色
- **成熟期**：早熟

### 风味特征

#### 勃艮第夏布利（冷凉，无橡木）
- **香气**：青苹果、柑橘、燧石、矿物质
- **酸度**：高
- **酒体**：轻至中等
- **橡木**：无或极少

#### 勃艮第金丘（温和，橡木桶）
- **香气**：白桃、柠檬、黄油、烤面包、坚果
- **酸度**：中高
- **酒体**：饱满
- **橡木**：法国新桶陈酿

#### 加州/澳洲（温暖，橡木桶）
- **香气**：热带水果、菠萝、芒果、香草、奶油
- **酸度**：中低
- **酒体**：饱满
- **橡木**：重橡木风格

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 勃艮第夏布利 | 矿物感强，高酸 | Domaine Laroche、Raveneau |
| 勃艮第默尔索 | 饱满丰富，奶油香 | Coche-Dury、Comte Lafon |
| 勃艮第蒙哈榭 | 顶级优雅，陈年强 | Domaine Leflaive、Ramonet |
| 加州俄罗斯河谷 | 浓郁丰富，平衡 | Kistler、Marcassin |
| 澳洲雅拉谷 | 优雅内敛，类似勃艮第 | Giaconda、Leeuwin Estate |

### 混酿搭配

- 几乎都为单品种酿造
- **香槟混酿**：与黑皮诺、Pinot Meunier混酿
- **勃艮第Crémant**：起泡酒主要原料

### 陈年潜力

- 蒙哈榭特级园：15-30年+
- 默尔索一级园：8-15年
- 夏布利特级园：10-20年
- 加州顶级：5-10年""",
    },
    {
        "id": "GRAPE-sauvignon-blanc",
        "category": "ENT",
        "subcategory": "grape",
        "title": "长相思",
        "title_en": "Sauvignon Blanc",
        "name_cn": "长相思",
        "name_en": "Sauvignon Blanc",
        "tags": ["葡萄品种", "白品种", "长相思", "卢瓦尔河谷", "马尔堡"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "清新草本风味的白葡萄品种，原产波尔多，卢瓦尔河谷和新西兰马尔堡的旗舰。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国波尔多
- **亲本**：Savagnin × 与Trousaris相关（DNA研究）
- **果串**：小到中等，圆柱形，紧凑
- **果粒**：小，皮中等厚度，黄绿色
- **成熟期**：早中熟

### 风味特征

#### 卢瓦尔河谷（桑塞尔/普伊芙美）
- **香气**：醋栗、青草、荨麻、燧石、柑橘
- **酸度**：高
- **酒体**：轻至中等
- **橡木**：通常无

#### 新西兰马尔堡
- **香气**：百香果、西柚、黑加仑叶、热带水果
- **酸度**：极高
- **酒体**：中等
- **橡木**：通常无

#### 波尔多（混酿）
- **香气**：柑橘、青草、矿物
- **酸度**：中高
- **酒体**：中等
- **橡木**：常与赛美蓉混酿，可经橡木

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 桑塞尔 | 矿物优雅，高酸 | Henri Bourgeois、Didier Dagueneau |
| 普伊芙美 | 烟熏矿物，结构感 | Domaine de Ladoucette |
| 波尔多佩萨克-雷奥良 | 混酿经典 | Domaine de Chevalier、Haut-Brion |
| 新西兰马尔堡 | 热带奔放 | Cloudy Bay、Villa Maria |
| 加州纳帕Fumé Blanc | 橡木风格 | Robert Mondavi、Spottswoode |

### 混酿搭配

- **波尔多干白**：长相思+赛美蓉+密斯卡岱
- **苏玳贵腐甜白**：与赛美蓉混酿
- **新西兰**：通常单品种装瓶

### 陈年潜力

- 普伊芙美顶级：10-15年
- 桑塞尔顶级：5-10年
- 新西兰长相思：1-3年（建议早饮）
- 波尔多干白顶级：8-15年""",
    },
    {
        "id": "GRAPE-riesling",
        "category": "ENT",
        "subcategory": "grape",
        "title": "雷司令",
        "title_en": "Riesling",
        "name_cn": "雷司令",
        "name_en": "Riesling",
        "tags": ["葡萄品种", "白品种", "雷司令", "德国", "高酸"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "德国之王白葡萄品种，从干型到甜型风格多变，以高酸度和陈年潜力著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：德国莱茵高
- **亲本**：Heunisch (Gouais Blanc) × 杂交品种（亲本之一为Traminer相关）
- **果串**：小，圆柱形，松散
- **果粒**：小，皮薄，黄绿色带斑点
- **成熟期**：晚熟

### 风味特征

#### 德国（干型到甜型）
- **香气**：青苹果、青柠、白桃、茉莉花、矿物、汽油（陈年）
- **酸度**：极高
- **酒体**：轻至中等
- **甜度**：从干型到Trockenbeerenauslese

#### 阿尔萨斯（干型为主）
- **香气**：柑橘、白桃、杏、燧石
- **酸度**：高
- **酒体**：中等至饱满
- **甜度**：多为干型，少量Vendange Tardive

#### 澳大利亚（克莱尔谷/伊甸谷）
- **香气**：青柠、烤面包、花香、汽油
- **酸度**：高
- **酒体**：中等
- **甜度**：多为干型

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 德国摩泽尔 | 轻盈优雅，矿物感强 | Egon Müller、Dr. Loosen |
| 德国莱茵高 | 饱满丰富，陈年强 | Schloss Johannisberg、Robert Weil |
| 德国普法尔茨 | 多样风格 | Dr. Bürklin-Wolf、Bassermann-Jordan |
| 阿尔萨斯 | 干型饱满，结构感 | Trimbach、Hugel |
| 澳洲克莱尔谷 | 干型优雅，石灰岩矿物 | Grosset、Jim Barry |

### 混酿搭配

- 几乎都为单品种酿造
- 德国 occasionally 与少量其他品种混酿
- 起泡酒（Sekt）：可作原料

### 陈年潜力

- 德国TBA/BA：50年+
- 德国Beerenauslese：30-50年
- 德国Auslese/Spätlese：15-30年
- 阿尔萨斯Grand Cru：10-20年
- 干型雷司令：5-10年""",
    },
    {
        "id": "GRAPE-semillon",
        "category": "ENT",
        "subcategory": "grape",
        "title": "赛美蓉",
        "title_en": "Sémillon",
        "name_cn": "赛美蓉",
        "name_en": "Sémillon",
        "tags": ["葡萄品种", "白品种", "赛美蓉", "苏玳", "波尔多"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "波尔多白混酿的核心品种，苏玳贵腐甜白的主角，猎人谷独特单品种风格。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国波尔多
- **亲本**：古老品种，与长相思有亲缘关系
- **果串**：中等大小，圆柱形，较紧凑
- **果粒**：中等，皮薄，金黄色
- **成熟期**：中熟

### 风味特征

#### 苏玳贵腐甜白
- **香气**：杏子、菠萝、蜂蜜、藏红花、无花果、橘子酱
- **酸度**：中高（平衡甜度）
- **酒体**：饱满，浓郁粘稠
- **甜度**：极高

#### 波尔多干白（混酿）
- **香气**：柠檬、青苹果、蜂蜡、柠檬草
- **酸度**：中等
- **酒体**：中等
- **橡木**：常经橡木桶

#### 澳洲猎人谷（单品种干白）
- **香气**：青柠、蜂蜡、烤面包、皮革（陈年）
- **酸度**：低
- **酒体**：中等至饱满
- **陈年**：独特陈年能力

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 苏玳/巴萨克 | 贵腐甜白，陈年极强 | 滴金、Climens、Suduiraut |
| 佩萨克-雷奥良 | 干白混酿经典 | Domaine de Chevalier、Haut-Brion |
| 猎人谷 | 单品种干白，独特陈年 | Tyrrell's、Brokenwood |
| 巴罗萨谷 | 单品种丰富风格 | Peter Lehmann |
| 华盛顿州 | 单品种饱满 | L'Ecole 41 |

### 混酿搭配

- **波尔多干白**：赛美蓉+长相思+密斯卡岱
- **苏玳贵腐**：赛美蓉为主（80%+）+长相思+密斯卡岱
- **猎人谷**：通常单品种装瓶

### 陈年潜力

- 滴金贵腐甜白：50-100年+
- 苏玳顶级：30-50年
- 猎人谷单品种：20-30年+
- 波尔多干白顶级：10-15年""",
    },
    {
        "id": "GRAPE-gewurztraminer",
        "category": "ENT",
        "subcategory": "grape",
        "title": "琼瑶浆",
        "title_en": "Gewürztraminer",
        "name_cn": "琼瑶浆",
        "name_en": "Gewürztraminer",
        "tags": ["葡萄品种", "白品种", "琼瑶浆", "阿尔萨斯", "芳香品种"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "阿尔萨斯的芳香白葡萄品种，以荔枝、玫瑰花瓣香气著称，低酸高酒精。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：意大利特伦蒂诺（Tramin村）
- **亲本**：Savagnin 变种（粉色果皮变种）
- **果串**：小到中等，圆锥形，紧凑
- **果粒**：小，皮粉色，果肉染色
- **成熟期**：早中熟

### 风味特征

#### 阿尔萨斯（典型风格）
- **香气**：荔枝、玫瑰花瓣、芒果、肉桂、丁香、姜
- **酸度**：低
- **酒体**：饱满
- **酒精**：高（13-14%）

#### 意大利/德国（较轻盈）
- **香气**：玫瑰、荔枝、香料
- **酸度**：中低
- **酒体**：中等
- **酒精**：中等

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 阿尔萨斯 | 浓郁芳香，高酒精 | Zind-Humbrecht、Trimbach、Hugel |
| 德国巴登/法尔兹 | 较轻盈，香料风格 | Dr. Heger、Friedrich Becker |
| 意大利特伦蒂诺/上阿迪杰 | 原产地风格 | Tramin、Nals Margreid |
| 新西兰/澳洲 | 新世界尝试 | Millton、Giaconda |
| 加州/俄勒冈 | 新世界芳香风格 | Navarro、Claiborne & Churchill |

### 混酿搭配

- 几乎都为单品种酿造
- 阿尔萨斯Gentil混酿：少量混入
- 甜型VT/SGN：单品种晚收

### 陈年潜力

- 阿尔萨斯Selection de Grains Nobles：15-25年
- 阿尔萨斯Vendange Tardive：8-15年
- 普通干型：2-4年（建议早饮）
- 不适合长期陈年""",
    },
    {
        "id": "GRAPE-pinot-gris",
        "category": "ENT",
        "subcategory": "grape",
        "title": "灰皮诺",
        "title_en": "Pinot Gris",
        "name_cn": "灰皮诺",
        "name_en": "Pinot Gris / Pinot Grigio",
        "tags": ["葡萄品种", "白品种", "灰皮诺", "Pinot Grigio", "阿尔萨斯"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "黑皮诺的突变品种，意大利称Pinot Grigio轻盈风格，阿尔萨斯浓郁饱满风格。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国勃艮第（黑皮诺突变）
- **亲本**：黑皮诺的色素突变
- **果串**：小，圆柱形，紧凑
- **果粒**：小，皮灰粉色，果肉略染色
- **成熟期**：早中熟

### 风味特征

#### 意大利 Pinot Grigio（轻盈风格）
- **香气**：青苹果、柠檬、白花、矿物
- **酸度**：中高
- **酒体**：轻
- **风格**：清新简单

#### 阿尔萨斯 Pinot Gris（浓郁风格）
- **香气**：蜂蜜、杏子、肉桂、姜、烟熏
- **酸度**：低中
- **酒体**：饱满
- **风格**：复杂丰富

#### 俄勒冈/德国（中间风格）
- **香气**：梨、白桃、香料、矿物
- **酸度**：中等
- **酒体**：中等
- **风格**：平衡优雅

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 意大利威尼托/上阿迪杰 | 清新轻盈，高酸 | Santa Margherita、Abbazia di Novacella |
| 阿尔萨斯 | 浓郁饱满，可陈年 | Domaine Weinbach、Zind-Humbrecht |
| 俄勒冈 | 中等酒体，平衡 | King Estate、A to Z |
| 德国（Grauburgunder） | 中等酒体，优雅 | Friedrich Becker、Ökonomierat Rebholz |
| 澳洲 | 阿尔萨斯风格 | Grosset、Pikes |

### 混酿搭配

- 通常为单品种酿造
- 阿尔萨斯Gentil混酿：少量加入
- 意大利有时与其他白品种混酿

### 陈年潜力

- 阿尔萨斯Selection de Grains Nobles：15-20年
- 阿尔萨斯Vendange Tardive：8-12年
- 俄勒冈顶级：3-5年
- 意大利Pinot Grigio：1-2年（早饮）""",
    },
    {
        "id": "GRAPE-viognier",
        "category": "ENT",
        "subcategory": "grape",
        "title": "维欧尼",
        "title_en": "Viognier",
        "name_cn": "维欧尼",
        "name_en": "Viognier",
        "tags": ["葡萄品种", "白品种", "维欧尼", "北罗纳", "Condrieu"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "北罗纳河谷的芳香白葡萄品种，以杏子花香和低酸著称，Condrieu的旗舰品种。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国北罗纳河谷
- **亲本**：古老品种，可能与白诗南有亲缘关系
- **果串**：小，圆柱形，紧凑
- **果粒**：小，皮厚，黄绿色
- **成熟期**：中熟

### 风味特征

#### 孔德里约（北罗纳经典）
- **香气**：杏子、白桃、紫罗兰、金银花、蜂蜜、麝香
- **酸度**：低
- **酒体**：饱满
- **酒精**：高（13.5-15%）

#### 新世界（加州/澳洲）
- **香气**：杏子、梨、姜、茉莉、香料
- **酸度**：低中
- **酒体**：饱满
- **橡木**：常经橡木桶

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 孔德里约 | 浓郁芳香，花香四溢 | Georges Vernay、Yves Cuilleron、Guigal |
| 罗纳丘（混酿） | 与玛珊/胡珊混酿 | Beaucastel、Chapoutier |
| 加州中央海岸 | 饱满丰富，新世界风格 | Alban、Tablas Creek、Qupé |
| 澳洲伊甸谷/阿德莱德山 | 优雅芳香 | Henschke、Yalumba |
| 华盛顿州 | 平衡丰富 | Dunham、Syncline |

### 混酿搭配

- **罗纳河谷白混酿**：维欧尼+玛珊+胡珊
- **与红品种混酿**：少量加入西拉（如Côte-Rôtie，<5%）
- **新世界**：常单品种装瓶

### 陈年潜力

- 孔德里约顶级：5-8年（不宜久存）
- 加州顶级：3-5年
- 普通餐酒：1-3年（建议早饮）
- 与西拉混酿的红酒：10-15年""",
    },
    {
        "id": "GRAPE-chenin-blanc",
        "category": "ENT",
        "subcategory": "grape",
        "title": "白诗南",
        "title_en": "Chenin Blanc",
        "name_cn": "白诗南",
        "name_en": "Chenin Blanc",
        "tags": ["葡萄品种", "白品种", "白诗南", "卢瓦尔河谷", "高酸"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "卢瓦尔河谷的多面手白葡萄品种，以高酸度和多变风格著称，从干型到甜型皆可。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国卢瓦尔河谷（安茹）
- **亲本**：古老品种，可能源自Pineau d'Aunis相关
- **果串**：中等大小，圆锥形，较松散
- **果粒**：小，皮薄，黄绿色
- **成熟期**：中晚熟

### 风味特征

#### 卢瓦尔河谷（干型）
- **香气**：青苹果、柑橘、白花、蜂蜜、矿物
- **酸度**：极高
- **酒体**：中等
- **风格**：清瘦矿物

#### 卢瓦尔河谷（甜型）
- **香气**：杏子、蜂蜜、橘子酱、姜、无花果
- **酸度**：高（平衡甜度）
- **酒体**：饱满
- **风格**：贵腐或晚收

#### 南非（多样风格）
- **香气**：热带水果、番石榴、杏、蜂蜜
- **酸度**：中高
- **酒体**：中等至饱满
- **风格**：从干型到甜型

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 武弗雷 | 多样风格，从干到甜 | Domaine Huet、Marc Brédif |
| 萨维涅尔 | 干型矿物，陈年强 | Nicolas Joly、Domaine des Baumard |
| 莱昂丘 | 甜型为主，贵腐 | Domaine de la Rouletière |
| 南非斯泰伦博斯 | 多样风格 | Ken Forrester、Mullineux |
| 加州（少量） | 通用混酿 | Chappellet、Pine Ridge |

### 混酿搭配

- 通常为单品种酿造
- 南非：常与少量其他品种混酿
- 加州：传统用作平价混酿原料
- Crémant de Loire：起泡酒原料

### 陈年潜力

- 武弗雷甜型Moelleux：30-50年+
- 萨维涅尔干白顶级：15-25年
- 武弗雷干型顶级：10-15年
- 南非顶级：5-10年""",
    },
    {
        "id": "GRAPE-muscat",
        "category": "ENT",
        "subcategory": "grape",
        "title": "密斯卡岱",
        "title_en": "Muscat",
        "name_cn": "密斯卡岱",
        "name_en": "Muscat",
        "tags": ["葡萄品种", "白品种", "密斯卡岱", "麝香葡萄", "芳香品种"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "最古老的芳香葡萄品种家族，以独特的麝香葡萄香气著称，从干型到甜型皆可。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：古希腊/中东（最古老品种家族之一）
- **亲本**：古老品种家族，含多个变种
- **果串**：中等大小，圆柱形，紧凑
- **果粒**：中等，皮厚，黄绿色或粉红色
- **成熟期**：早中熟

### 主要变种

- **Muscat Blanc à Petits Grains**：最优质，小粒
- **Muscat of Alexandria**：品质次之，大粒
- **Muscat Ottonel**：最轻盈，用于阿尔萨斯
- **Yellow Muscat / Moscato Giallo**：意大利特色

### 风味特征

#### 阿斯蒂Moscato（微甜微气泡）
- **香气**：玫瑰、橘子、蜜桃、麝香葡萄
- **酸度**：中高
- **酒体**：轻
- **甜度**：微甜
- **酒精**：低（5-6%）

#### 阿尔萨斯（干型）
- **香气**：玫瑰、荔枝、肉桂、麝香
- **酸度**：低中
- **酒体**：中等
- **风格**：干型饱满

#### 吕内麝香甜酒（VDN）
- **香气**：橘子酱、核果、咖啡、坚果、无花果
- **酸度**：中等
- **酒体**：饱满
- **甜度**：高

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 意大利阿斯蒂 | 微甜微气泡，清新 | Martini & Rossi、Moscato d'Asti |
| 阿尔萨斯 | 干型芳香，可陈年 | Domaine Weinbach、Zind-Humbrecht |
| 法国吕内-里韦萨特 | 加强甜酒VDN | Domaine de la Rectorie、Mas Amiel |
| 澳洲路斯格兰 | 加强甜酒Liqueur Muscat | Chambers、Campbells |
| 希腊Samos | 甜型风格 | Samos Cooperative |

### 混酿搭配

- 通常为单品种酿造
- 阿尔萨斯Gentil混酿：少量加入增香
- 意大利Moscato d'Asti：单品种
- 西班牙/葡萄牙：少量用作混酿增香

### 陈年潜力

- 吕内VDN顶级：30-50年+
- 澳洲Liqueur Muscat：30年+
- 阿尔萨斯干型顶级：5-10年
- Moscato d'Asti：1-2年（建议早饮）""",
    },
    {
        "id": "GRAPE-gruner-veltliner",
        "category": "ENT",
        "subcategory": "grape",
        "title": "绿维特利纳",
        "title_en": "Grüner Veltliner",
        "name_cn": "绿维特利纳",
        "name_en": "Grüner Veltliner",
        "tags": ["葡萄品种", "白品种", "绿维特利纳", "奥地利", "白胡椒"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "奥地利旗舰白葡萄品种，以白胡椒香气和高酸度著称，从清新到浓郁多变。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：奥地利（自然杂交，亲本之一可能为Traminer）
- **亲本**：与Traminer相关 × 未知品种
- **果串**：中等大小，圆柱形，紧凑
- **果粒**：中等，皮薄，黄绿色
- **成熟期**：中熟

### 风味特征

#### 下奥地利（清新风格）
- **香气**：青苹果、白胡椒、芹菜、柑橘、矿物
- **酸度**：高
- **酒体**：轻至中等
- **风格**：清瘦矿物

#### 瓦豪/凯普谷（浓郁风格）
- **香气**：白桃、梨、白胡椒、烟熏、蜂蜜
- **酸度**：高
- **酒体**：饱满
- **风格**：复杂丰富

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 瓦豪 | DAC顶级，浓郁复杂 | F.X. Pichler、Knoll、Hirtzberger |
| 凯普谷 | 多样风格，性价比高 | Bründlmayer、Schloss Gobelsburg |
| 瓦格拉姆 | 矿物感强，优雅 | Pfaffl、Wittmann |
| 维也纳 | 传统Gemischter Satz | Wieninger、Mayer am Pfarrplatz |
| 斯洛伐克/捷克 | 邻国种植 | Elesko、Sekt原酒 |

### 混酿搭配

- 通常为单品种酿造
- 维也纳Gemischter Satz（混酿）：传统风格
- 起泡酒原料
- 偶尔与雷司令、威尔士雷司令混酿

### 陈年潜力

- 瓦豪顶级Smaragd：15-25年+
- 凯普谷顶级Reserve：10-15年
- 普通Federspiel：3-5年
- 基础Qualitätswein：1-3年""",
    },
    {
        "id": "GRAPE-marselan",
        "category": "ENT",
        "subcategory": "grape",
        "title": "马瑟兰",
        "title_en": "Marselan",
        "name_cn": "马瑟兰",
        "name_en": "Marselan",
        "tags": ["葡萄品种", "红品种", "马瑟兰", "中国新兴", "杂交品种"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "赤霞珠与歌海娜的杂交品种，法国育成，在中国新兴产区表现优异。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国（1961年由INRA育成，Marseillan村）
- **亲本**：赤霞珠 × 歌海娜
- **果串**：大，圆锥形，松散
- **果粒**：小，皮厚，色深
- **成熟期**：中晚熟

### 培育背景

- 培育目标：结合赤霞珠的结构与歌海娜的抗病性
- 初期未受重视（产量较低）
- 21世纪在海外（尤其中国）获得重视
- 现已成为中国葡萄酒的"明星品种"

### 风味特征

#### 中国宁夏/山东
- **香气**：黑莓、黑樱桃、紫罗兰、香料、薄荷
- **单宁**：中高，柔顺
- **酸度**：中等
- **酒体**：饱满

#### 法国南部
- **香气**：红色浆果、香料、皮革
- **单宁**：中等
- **酸度**：中等
- **酒体**：中等至饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 中国宁夏 | 浓郁复杂，紫罗兰香 | 迦南美地、长城、贺兰晴雪 |
| 中国山东 | 平衡优雅 | 张裕、君顶 |
| 中国河北怀来 | 结构感强 | 桑干、中法庄园 |
| 法国朗格多克 | 性价比餐酒 | 多个合作社 |
| 西班牙/阿根廷 | 新兴尝试 | 少量种植 |

### 混酿搭配

- 通常为单品种酿造
- 可与赤霞珠、美乐混酿
- 中国马瑟兰：常单独装瓶展示特色

### 陈年潜力

- 中国顶级马瑟兰：8-12年
- 普通餐酒：3-5年
- 因品种较新，陈年数据有限
- 单宁结构支持中期陈年""",
    },
    {
        "id": "GRAPE-petit-verdot",
        "category": "ENT",
        "subcategory": "grape",
        "title": "小维多",
        "title_en": "Petit Verdot",
        "name_cn": "小维多",
        "name_en": "Petit Verdot",
        "tags": ["葡萄品种", "红品种", "小维多", "波尔多", "调色"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "波尔多混酿的调色品种，晚熟高单宁，为混酿增添颜色、单宁和香料感。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国波尔多
- **亲本**：古老品种
- **果串**：小，圆柱形，紧凑
- **果粒**：小，皮厚，色深
- **成熟期**：极晚熟

### 风味特征

#### 波尔多（混酿角色）
- **香气**：黑莓、紫罗兰、香料、咖啡、皮革
- **单宁**：极高
- **酸度**：高
- **酒体**：饱满

#### 新世界单品种（澳洲/加州）
- **香气**：黑樱桃、香料、紫罗兰、黑巧克力
- **单宁**：高
- **酸度**：中高
- **酒体**：饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 波尔多左岸 | 混酿少量使用 | 拉菲、木桐、玛歌 |
| 波尔多右岸 | 少量使用 | 白马、Figeac |
| 澳洲玛格丽特河 | 单品种尝试 | Vasse Felix、Cullen |
| 加州纳帕谷 | 单品种或混酿 | Ridge、Joseph Phelps |
| 西班牙/智利 | 新兴尝试 | 少量种植 |

### 混酿搭配

- **波尔多混酿**：少量加入（2-5%），增色增单宁
- **新世界赤霞珠混酿**：可增至5-10%
- **单品种**：澳洲、加州有少量单品种装瓶

### 陈年潜力

- 波尔多顶级混酿：20-30年+
- 澳洲单品种顶级：10-15年
- 普通餐酒：3-5年
- 由于晚熟，仅在温暖年份完全成熟""",
    },
    {
        "id": "GRAPE-carmenere",
        "category": "ENT",
        "subcategory": "grape",
        "title": "佳美娜",
        "title_en": "Carménère",
        "name_cn": "佳美娜",
        "name_en": "Carménère",
        "tags": ["葡萄品种", "红品种", "佳美娜", "智利", "波尔多原产"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "智利旗舰红葡萄品种，原产波尔多，长期被误认为美乐，以香料和深色著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国波尔多（Grande Vidure）
- **亲本**：Cabernet Franc × Gros Cabernet
- **果串**：中等大小，圆柱形，较松散
- **果粒**：小，皮厚，色深
- **成熟期**：极晚熟

### 风味特征

#### 智利（典型风格）
- **香气**：黑莓、黑樱桃、青椒、可可、香料、皮革
- **单宁**：中高
- **酸度**：中等
- **酒体**：饱满

#### 意大利/美国（新兴）
- **香气**：红色浆果、香料、香草
- **单宁**：中等
- **酸度**：中等
- **酒体**：中等至饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 智利中央山谷 | 浓郁丰富，性价比高 | Concha y Toro、Santa Rita |
| 智利空加瓜谷 | 顶级风格，结构紧实 | Carmen、Montes、APaltas |
| 智利卡恰布谷 | 优雅平衡 | Morandé、Casas del Bosque |
| 意大利威尼托/弗留利 | 新兴尝试 | 多家酒庄小规模种植 |
| 美国/华盛顿州 | 新兴尝试 | Gesa、Severino Cellars |

### 混酿搭配

- 通常为单品种酿造
- 智利：可与赤霞珠、美乐混酿
- 波尔多传统：曾为混酿一员，现已极少

### 陈年潜力

- 智利顶级佳美娜：8-12年
- 普通智利餐酒：3-5年
- 必须完全成熟才能避免青椒过重
- 完全成熟时展现丰富香料""",
    },
    {
        "id": "GRAPE-tannat",
        "category": "ENT",
        "subcategory": "grape",
        "title": "丹拿",
        "title_en": "Tannat",
        "name_cn": "丹拿",
        "name_en": "Tannat",
        "tags": ["葡萄品种", "红品种", "丹拿", "马迪朗", "乌拉圭"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "单宁王红葡萄品种，原产法国马迪朗，乌拉圭国酒，以极高单宁和深色著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：法国西南部（马迪朗）
- **亲本**：古老品种，亲本未明
- **果串**：中等大小，圆柱形，紧凑
- **果粒**：小，皮厚，色极深
- **成熟期**：晚熟

### 风味特征

#### 法国马迪朗（传统风格）
- **香气**：黑莓、黑樱桃、李子干、咖啡、烟熏、皮革
- **单宁**：极高
- **酸度**：中高
- **酒体**：饱满

#### 乌拉圭（柔和风格）
- **香气**：黑莓、李子、香料、巧克力、紫罗兰
- **单宁**：高（比马迪朗柔顺）
- **酸度**：中等
- **酒体**：饱满

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 法国马迪朗 | 单宁强劲，陈年强 | Château Montus、Domaine Brumont |
| 乌拉圭卡内洛内斯 | 国酒地位，柔和风格 | Bouza、Narbona、Pisano |
| 乌拉圭加尔松 | 现代风格，平衡 | Bodega Garzón |
| 阿根廷/巴西 | 邻国种植 | 少量 |
| 加州/澳洲 | 新兴尝试 | Tablas Creek、少量 |

### 混酿搭配

- **马迪朗传统**：单品种为主，少量加Cabernet Sauvignon/Cabernet Franc软化
- **乌拉圭**：单品种或与美乐/赤霞珠混酿
- **Madiran传统**：与Fer Servadou混酿

### 陈年潜力

- 马迪朗顶级：15-25年+
- 乌拉圭顶级：8-15年
- 普通餐酒：3-5年
- 单宁极强，必须陈年软化""",
    },
    {
        "id": "GRAPE-koshu",
        "category": "ENT",
        "subcategory": "grape",
        "title": "甲州",
        "title_en": "Koshu",
        "name_cn": "甲州",
        "name_en": "Koshu",
        "tags": ["葡萄品种", "白品种", "甲州", "日本", "本土品种"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "日本本土特色白葡萄品种，淡红皮白汁，以清新优雅和日本料理搭配著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：日本（通过丝绸之路传入，DNA显示欧洲种Vitis vinifera杂交后代）
- **亲本**：Vitis vinifera × Vitis thunbergii等亚洲种（多次回交）
- **果串**：中等大小，圆柱形，较松散
- **果粒**：中等，皮淡粉色，果肉白汁
- **成熟期**：中晚熟

### 历史背景

- 1000多年前经丝绸之路传入日本
- 长期作为鲜食葡萄
- 19世纪末开始用于酿酒
- 2010年获得OIV国际认可
- 现为日本葡萄酒的旗舰品种

### 风味特征

#### 山梨县（典型风格）
- **香气**：柑橘、白桃、柚子皮、白花、矿物
- **酸度**：中高
- **酒体**：轻至中等
- **风格**：清新优雅

#### 不同酿造方式
- **不锈钢罐**：清新果味，矿物感
- **橡木桶**：增加复杂度，烟熏香
- **橘酒（浸皮）**：单宁结构，茶香

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 山梨县 | 主产区，清新风格 | Suntory、Mercian、Grace |
| 长野 | 高海拔，酸度优雅 | Cave d'Iwate、Ikeda |
| 山形 | 冷凉产区 | Takahata、Ohsawa |
| 北海道 | 试种阶段 | 各酒庄尝试 |
| 中国/韩国 | 少量试种 | 实验阶段 |

### 混酿搭配

- 通常为单品种酿造
- 可与Chardonnay等白品种混酿
- 日本料理的天然搭配
- 偶尔用于起泡酒

### 陈年潜力

- 顶级甲州：3-5年
- 普通餐酒：1-2年（建议早饮）
- 不适合长期陈年
- 强调新鲜果味""",
    },
    {
        "id": "GRAPE-feteasca-regala",
        "category": "ENT",
        "subcategory": "grape",
        "title": "贵人香",
        "title_en": "Fetească Regală",
        "name_cn": "贵人香",
        "name_en": "Fetească Regală",
        "tags": ["葡萄品种", "白品种", "贵人香", "罗马尼亚", "东欧"],
        "source": "Wine Grapes (Jancis Robinson)/WSET",
        "data_confidence": "official",
        "summary": "东欧特色白葡萄品种，罗马尼亚广泛种植，以花香果香和清新酸度著称。",
        "content_body": """## 品种概况

### 基本信息

- **原产地**：罗马尼亚（特兰西瓦尼亚地区，1930年代自然杂交）
- **亲本**：Fetească Albă × Grasă de Cotnari（推测）
- **果串**：中等大小，圆柱形，紧凑
- **果粒**：中等，皮薄，黄绿色
- **成熟期**：中熟

### 风味特征

#### 罗马尼亚（典型风格）
- **香气**：青苹果、柑橘、白花、蜂蜜、杏子
- **酸度**：中高
- **酒体**：中等
- **风格**：清新优雅

#### 摩尔多瓦/匈牙利
- **香气**：白桃、梨、茉莉、矿物
- **酸度**：中等
- **酒体**：中等
- **风格**：平衡

### 主要产区

| 产区 | 风格特征 | 代表酒庄 |
|------|----------|----------|
| 罗马尼亚特兰西瓦尼亚 | 原产地，清新风格 | Jidvei、Davino、Budureasca |
| 罗马尼亚蒙特尼亚 | 平衡丰富 | SERVE、Halewood |
| 罗马尼亚摩尔达维亚 | 传统风格 | Cotnari、Craiului |
| 摩尔多瓦 | 邻国种植 | Château Vartely、Cricova |
| 匈牙利/保加利亚 | 少量种植 | 各酒庄 |

### 混酿搭配

- 通常为单品种酿造
- 可与其他白品种混酿
- 起泡酒原料（传统法）
- 偶尔用于甜型晚收

### 陈年潜力

- 顶级干白：3-5年
- 普通餐酒：1-2年（建议早饮）
- 甜型晚收：5-8年
- 强调新鲜风格，不宜久存""",
    },
]
