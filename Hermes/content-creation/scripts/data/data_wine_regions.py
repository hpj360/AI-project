"""产区风土地图数据 - 权威来源。

数据源：
- WSET教材
- Wine Searcher
- 各产区官方协会

置信度：official
"""

ENTRIES = [
    {
        "id": "REGION-france-bordeaux",
        "category": "ENT",
        "subcategory": "region",
        "title": "波尔多产区",
        "title_en": "Bordeaux",
        "name_cn": "波尔多",
        "name_en": "Bordeaux",
        "tags": ["产区风土", "法国", "波尔多", "赤霞珠", "美乐"],
        "source": "WSET/Wine Searcher",
        "data_confidence": "official",
        "summary": "世界最著名的葡萄酒产区，以赤霞珠和美乐混酿闻名，分左岸右岸两大风格。",
        "content_body": """## 地理与气候

### 位置
- 法国西南部，靠近大西洋
- 吉伦特河口将产区分为左岸和右岸

### 气候
- 海洋性气候
- 冬季温和，夏季温暖
- 降雨分布均匀，收获季有风险

### 土壤
- **左岸**：砾石土壤（排水好，储热，适合赤霞珠）
- **右岸**：黏土和石灰岩（保水，适合美乐和品丽珠）
- **两海之间**：冲积土（白葡萄品种）

## 法定等级

### 1855年梅多克分级
- 一级庄（5家）：拉菲、拉图、玛歌、侯伯王、木桐
- 二至五级庄（共61家）

### 圣埃美隆分级
- 一级A等（2家）：白马、欧颂
- 一级B等（11家）

## 主要子产区

| 子产区 | 位置 | 主要品种 | 风格 |
|--------|------|----------|------|
| 梅多克 | 左岸 | 赤霞珠为主 | 骨架感强，陈年潜力大 |
| 波美侯 | 右岸 | 美乐为主 | 圆润丰腴，产量稀少 |
| 圣埃美隆 | 右岸 | 美乐+品丽珠 | 优雅细腻 |
| 玛歌 | 左岸 | 赤霞珠 | 芳香优雅 |
| 波亚克 | 左岸 | 赤霞珠 | 强劲有力 |
| 苏玳 | 两海之间 | 赛美蓉 | 贵腐甜酒 |

## 代表酒庄
- 左岸：拉菲、拉图、玛歌、木桐、侯伯王
- 右岸：柏图斯、白马、欧颂、里鹏""",
    },
    {
        "id": "REGION-france-burgundy",
        "category": "ENT",
        "subcategory": "region",
        "title": "勃艮第产区",
        "title_en": "Burgundy",
        "name_cn": "勃艮第",
        "name_en": "Burgundy",
        "tags": ["产区风土", "法国", "勃艮第", "黑皮诺", "霞多丽"],
        "source": "WSET/BIVB",
        "data_confidence": "official",
        "summary": "以单一品种葡萄酒闻名的顶级产区，黑皮诺与霞多丽的圣地，风土分级最为精细。",
        "content_body": """## 地理与气候

### 位置
- 法国东部，从第戎到里昂
- 核心产区为金丘（Côte d'Or）
- 金丘分为夜丘（Côte de Nuits）和伯恩丘（Côte de Beaune）

### 气候
- 大陆性气候
- 冬季寒冷，春季霜冻风险大
- 夏季温暖但短促，秋季雨水影响收获

### 土壤
- 侏罗纪石灰岩和泥灰岩
- 金丘以石灰岩为主，赋予矿物感
- 夏布利（Chablis）为启莫里奇阶土壤（Kimmeridgian）
- 风土差异决定地块等级

## 法定等级（四级金字塔）

| 等级 | 数量 | 占比 |
|------|------|------|
| 特级园 Grand Cru | 33块 | 约1% |
| 一级园 Premier Cru | 约640块 | 约10% |
| 村庄级 Village | 44个 | 约23% |
| 大区级 Régional | - | 约52% |

## 主要子产区

- **夏布利**：霞多丽白，矿物感强，高酸
- **夜丘**：黑皮诺红为主（伏旧、罗曼尼、热夫雷）
- **伯恩丘**：霞多丽白为主（默尔索、蒙哈榭），亦有黑皮诺
- **夏隆内丘**：吕利、梅尔居雷
- **马孔内**：普伊-富赛（霞多丽）

## 代表酒庄
- 罗曼尼·康帝酒庄（DRC）
- 亨利·贾耶（Henri Jayer）
- 乐华酒庄（Leroy）
- 法维莱（Faiveley）
- 路易亚都（Louis Jadot）""",
    },
    {
        "id": "REGION-france-champagne",
        "category": "ENT",
        "subcategory": "region",
        "title": "香槟产区",
        "title_en": "Champagne",
        "name_cn": "香槟",
        "name_en": "Champagne",
        "tags": ["产区风土", "法国", "香槟", "起泡酒", "传统法"],
        "source": "WSET/CIVC",
        "data_confidence": "official",
        "summary": "世界最著名的起泡酒产区，白垩土壤与传统法酿造造就独一无二的香槟。",
        "content_body": """## 地理与气候

### 位置
- 法国最北的葡萄产区，距巴黎约150公里
- 五大子产区：兰斯山、马恩河谷、白丘、奥布、塞扎纳丘

### 气候
- 凉爽的大陆性气候，处于葡萄种植北界
- 年均温10.8℃，极端冬季霜冻风险
- 降雨适中，成熟期长，保留高酸

### 土壤
- 白垩岩（Chalk）为主，形成于中生代
- 含箭石和海胆化石
- 排水极佳，保水同时反射光照
- 为葡萄提供矿物感和天然高酸

## 法定等级

### 葡萄村等级（Échelle des Crus）
- **特级村 Grand Cru**：17个村，100%评分
- **一级村 Premier Cru**：44个村，90-99%评分
- 其他村庄：80-89%

## 主要葡萄品种

| 品种 | 占比 | 特点 |
|------|------|------|
| 霞多丽 | 30% | 白丘主栽，骨架酸度 |
| 黑皮诺 | 38% | 兰斯山主栽，结构果味 |
| 莫尼耶 | 32% | 马恩河谷，芳香柔和 |

## 香槟风格

- **无年份NV**：基酒调配，风格稳定
- **年份香槟**：优秀年份单独酿造
- **白中白**：100%霞多丽
- **黑中白**：100%红葡萄品种
- **桃红**：调配法或放血法

## 代表酒庄
- 唐·培里侬（Dom Pérignon）
- 库克（Krug）
- 沙龙（Salon）
- 水晶路易王妃（Louis Roederer Cristal）
- 堡林爵（Bollinger）""",
    },
    {
        "id": "REGION-france-rhone",
        "category": "ENT",
        "subcategory": "region",
        "title": "罗纳河谷产区",
        "title_en": "Rhône Valley",
        "name_cn": "罗纳河谷",
        "name_en": "Rhône Valley",
        "tags": ["产区风土", "法国", "罗纳河谷", "西拉", "歌海娜"],
        "source": "WSET/InterRhône",
        "data_confidence": "official",
        "summary": "南北风格迥异的法国第二大AOC产区，北罗纳西拉独秀，南罗纳歌海娜混酿称王。",
        "content_body": """## 地理与气候

### 位置
- 法国东南部，沿罗纳河从里昂到阿维尼翁
- 以蒙特利马为界分南北两段

### 气候
- **北罗纳**：大陆性气候，凉爽，受密斯特拉风影响
- **南罗纳**：地中海气候，温暖干燥，阳光充足
- 密斯特拉风（Mistral）干冷北风，防病关键

### 土壤
- **北罗纳**：花岗岩、片岩（陡坡梯田）
- **南罗纳**：鹅卵石（galets roulées）、沙土、黏土
- 鹅卵石白天储热夜间释放，促进成熟

## 主要子产区

### 北罗纳（北纬45°）

| 产区 | 主要品种 | 特点 |
|------|----------|------|
| 罗第丘 Côte-Rôtie | 西拉（+5%维欧尼） | 优雅细腻，带花香 |
| 埃米塔日 Hermitage | 西拉 | 强劲深厚，陈年潜力大 |
| 孔得里约 Condrieu | 维欧尼 | 芳香白葡萄酒 |
| 格里叶堡 Château-Grillet | 维欧尼 | 法国最小AOC之一 |

### 南罗纳

| 产区 | 主要品种 | 特点 |
|------|----------|------|
| 教皇新堡 Châteauneuf-du-Pape | 歌海娜混酿（13种） | 醇厚复杂，砾石土壤 |
| 塔维尔 Tavel | 歌海娜 | 法国桃红之王 |
| 利哈克 Lirac | 歌海娜混酿 | 性价比之选 |
| 吉贡达斯 Gigondas | 歌海娜混酿 | 接近教皇新堡风格 |

## 等级体系
- 罗纳河谷丘（Côtes du Rhône）：大区级
- 罗纳河谷村庄级（Côtes du Rhône Villages）：95个村
- 特级村庄（Cru）：17个独立AOC

## 代表酒庄
- 北罗纳：吉佳乐（Guigal）、嘉伯乐（Jaboulet）、沙普蒂埃（Chapoutier）
- 南罗纳：哈雅斯（Rayas）、博卡斯特尔（Beaucastel）""",
    },
    {
        "id": "REGION-france-loire",
        "category": "ENT",
        "subcategory": "region",
        "title": "卢瓦尔河谷产区",
        "title_en": "Loire Valley",
        "name_cn": "卢瓦尔河谷",
        "name_en": "Loire Valley",
        "tags": ["产区风土", "法国", "卢瓦尔河谷", "长相思", "白诗南", "品丽珠"],
        "source": "WSET/InterLoire",
        "data_confidence": "official",
        "summary": "法国最长的葡萄酒产区，横跨1000公里，白葡萄酒王国，三大白品种各据一方。",
        "content_body": """## 地理与气候

### 位置
- 沿卢瓦尔河绵延近1000公里
- 从大西洋沿岸到中央山脉边缘
- 分为四个主要区域：南特、安茹-索米尔、都兰、中央产区

### 气候
- 西部：海洋性气候，温和湿润
- 东部：过渡为大陆性气候
- 整体凉爽，葡萄成熟缓慢，保留清新酸度

### 土壤
- 多样：片岩、黏土、石灰岩、燧石（Silex）
- 桑塞尔的terres blanches（白垩土）和caillottes（石灰岩）
- 武弗雷的Tuffeau（石灰华）

## 主要子产区与品种

### 南特区（Muscadet）
- 品种：勃艮第香瓜（Melon de Bourgogne）
- 风格：清冽矿物，常配酒泥陈年（sur lie）

### 安茹-索米尔区
- 萨韦涅尔（Savennières）：白诗南干白，强劲矿物
- 莱昂丘（Coteaux du Layon）：白诗南甜酒
- 索米尔：起泡酒（Crémant de Loire）

### 都兰区
- 武弗雷（Vouvray）：白诗南，从干到甜多种风格
- 希农（Chinon）、布尔格伊（Bourgueil）：品丽珠红

### 中央产区
- 桑塞尔（Sancerre）：长相思白、黑皮诺红
- 普伊-富美（Pouilly-Fumé）：长相思，烟熏矿物

## 代表酒庄
- 迪迪埃·达格诺（Didier Dagueneau）- 普伊-富美
- 亨利·博诺（Henri Bourgeois）- 桑塞尔
- 于埃（Huet）- 武弗雷
- 朗德勒-吉罗（Landron-Girard）- 马斯凯特""",
    },
    {
        "id": "REGION-france-alsace",
        "category": "ENT",
        "subcategory": "region",
        "title": "阿尔萨斯产区",
        "title_en": "Alsace",
        "name_cn": "阿尔萨斯",
        "name_en": "Alsace",
        "tags": ["产区风土", "法国", "阿尔萨斯", "雷司令", "琼瑶浆", "灰皮诺"],
        "source": "WSET/CIVA",
        "data_confidence": "official",
        "summary": "法国白葡萄酒之乡，以芳香品种著称，雷司令、琼瑶浆、灰皮诺三足鼎立。",
        "content_body": """## 地理与气候

### 位置
- 法国东北部，与德国隔莱茵河相望
- 沿孚日山脉东麓南北延伸约170公里

### 气候
- 半大陆性气候
- 孚日山脉形成雨影效应，年降雨量低（500mm）
- 日照充足，秋季长，葡萄成熟充分
- 干燥少病，适合晚收

### 土壤
- 法国土壤最多样产区之一
- 花岗岩、片岩、石灰岩、黏土、砂岩、火山岩
- 不同土壤赋予不同品种典型性

## 等级体系

### AOC等级
- **阿尔萨斯AOC**（74%）：单一品种或调配
- **阿尔萨克特级园**（Alsace Grand Cru）：51个特级园（4%）
- **晚收甜酒VT**（Vendanges Tardives）
- **贵腐粒选SGN**（Sélection de Grains Nobles）

### "贵族品种"（Noble Varieties）
仅这4种可进入特级园：
- 雷司令（Riesling）
- 琼瑶浆（Gewürztraminer）
- 灰皮诺（Pinot Gris）
- 麝香（Muscat）

## 主要品种

| 品种 | 占比 | 风格 |
|------|------|------|
| 雷司令 | 21% | 干型为主，矿物酸度高 |
| 琼瑶浆 | 18% | 荔枝玫瑰花香，酒体丰满 |
| 灰皮诺 | 15% | 圆润丰腴，香辛味 |
| 白皮诺 | 21% | 中性，清新 |
| 西尔瓦纳 | - | 早熟芳香 |
| 黑皮诺 | 9% | 唯一红品种 |

## 代表酒庄
- 婷芭克世家（Trimbach）- Clos Sainte Hune
- 雨果酒庄（Hugel）
- 温巴赫酒庄（Weinbach）
- 兹恩-洪布尔格（Zind-Humbrecht）""",
    },
    {
        "id": "REGION-france-provence",
        "category": "ENT",
        "subcategory": "region",
        "title": "普罗旺斯产区",
        "title_en": "Provence",
        "name_cn": "普罗旺斯",
        "name_en": "Provence",
        "tags": ["产区风土", "法国", "普罗旺斯", "桃红", "歌海娜"],
        "source": "WSET/CIVP",
        "data_confidence": "official",
        "summary": "世界桃红之乡，桃红产量占88%，地中海阳光与古老葡萄园的代名词。",
        "content_body": """## 地理与气候

### 位置
- 法国东南部地中海沿岸
- 从罗纳河口到尼斯
- 法国最古老的葡萄酒产区（2600年前希腊人引入）

### 气候
- 典型地中海气候
- 夏季炎热干燥，日照充足（年2750小时）
- 米斯特拉尔北风清洁葡萄园，减少病害
- 海风调节温度

### 土壤
- 多样：石灰岩、片岩、砂岩、砾石、黏土
- 海岸带以石英岩和片岩为主
- 内陆以黏土和石灰岩为主

## 主要子产区

| 产区 | 类型 | 特点 |
|------|------|------|
| 普罗旺斯丘 Côteaux d'Aix-en-Provence | 红桃白 | 最大子产区 |
| 瓦尔丘 Côteaux Varois en Provence | 红桃白 | 内陆中心 |
| 邦多勒 Bandol | 红为主 | 慕合怀特主栽 |
| 卡西斯 Cassis | 白为主 | 玛珊混酿 |
| 帕莱特 Palette | 红桃白 | 法国最小AOC |

## 主要品种

### 红葡萄品种
- **歌海娜**（Grenache）：桃红主力，果香饱满
- **神索**（Cinsault）：桃红主力，轻盈果香
- **慕合怀特**（Mourvèdre）：邦多勒主栽，结构强
- **堤布宏**（Tibouren）：本地品种，桃红精致
- 西拉、赤霞珠（辅助）

### 白葡萄品种
- 玛珊、胡珊、克莱雷特、布布兰克

## 桃红酿造特点
- 直接压榨法为主（saignée比例少）
- 浅三文鱼色至淡粉色
- 强调清新果香（柑橘、桃、红色莓果）
- 干型，酸度活泼

## 代表酒庄
- 悦钟（Château d'Esclans）- Whispering Angel、Garrus
- 米拉维尔（Miraval）- Pitt-Jolie合作
- 坦木索（Tempier）- 邦多勒标杆
- 多玛士（Domaines Ott）""",
    },
    {
        "id": "REGION-france-languedoc",
        "category": "ENT",
        "subcategory": "region",
        "title": "朗格多克产区",
        "title_en": "Languedoc",
        "name_cn": "朗格多克",
        "name_en": "Languedoc",
        "tags": ["产区风土", "法国", "朗格多克", "歌海娜", "西拉", "佳丽酿"],
        "source": "WSET/CIVL",
        "data_confidence": "official",
        "summary": "法国最大的葡萄酒产区，世界最古老的葡萄园之一，性价比之王与新派风潮并行。",
        "content_body": """## 地理与气候

### 位置
- 法国南部地中海沿岸
- 从罗纳河口到西班牙边境
- 横跨奥克西塔尼大区三个省份

### 气候
- 典型地中海气候
- 夏季炎热干燥，日照充足（年300天）
- 干燥少病害，有机/生物动力法盛行
- 内陆海拔高的子产区受大陆性影响

### 土壤
- 法国土壤最多样产区
- 砾石、砂岩、石灰岩、泥灰岩、片岩、火山岩
- 不同地形造就多元风格

## 等级与子产区

### 大区级
- 奥克地区IGP（Pays d'Oc）：法国最大IGP，品种酒主力

### AOC村庄级与特级（部分）

| 产区 | 主要品种 | 特点 |
|------|----------|------|
| 朗格多克丘 AOC | 歌海娜、西拉、慕合怀特、佳丽酿 | 大区AOC |
| 科比埃 Corbières | 佳丽酿为主 | 红为主 |
| 米内瓦 Minervois | 西拉、歌海娜 | 红为主，风格丰富 |
| 圣希尼安 Saint-Chinian | 片岩土壤 | 矿物感强 |
| 菲图 Fitou | 佳丽酿、歌海娜 | 法国最老VDQS之一 |
| 利穆 Limoux | 霞多丽、白诗南 | 起泡酒 Blanquette de Limoux |
| 皮克-圣-卢 Pic Saint-Loup | 西拉、歌海娜 | 高品质新兴产区 |

### 利穆起泡酒
- Blanquette de Limoux：世界最早的起泡酒（1531年）
- 传统法，霞多丽+白诗南+莫扎克

## 主要品种

- **红**：歌海娜、西拉、慕合怀特、佳丽酿、神索
- **白**：胡珊、玛珊、白歌海娜、维欧尼、克莱雷特
- 历史：19世纪根瘤蚜前以皮克普尔、特蕾等为主

## 代表酒庄
- 哈雅斯（Grange des Pères）
- 马赛兰庄园（Mas de Daumas Gassac）- "朗格多克的拉图"
- 蒙佩拉（Montpeyroux）
- 阿拉里克（Domaine de l'Horte）""",
    },
    {
        "id": "REGION-italy-tuscany",
        "category": "ENT",
        "subcategory": "region",
        "title": "托斯卡纳产区",
        "title_en": "Tuscany",
        "name_cn": "托斯卡纳",
        "name_en": "Tuscany",
        "tags": ["产区风土", "意大利", "托斯卡纳", "桑娇维塞", "基安蒂"],
        "source": "WSET/Consorzio Vino Chianti Classico",
        "data_confidence": "official",
        "summary": "意大利最著名的葡萄酒产区，桑娇维塞的故乡，基安蒂与布鲁内罗闻名世界。",
        "content_body": """## 地理与气候

### 位置
- 意大利中部，亚平宁山脉西麓
- 西临第勒尼安海
- 丘陵地貌，海拔100-500米为主

### 气候
- 地中海气候为主
- 沿海温暖湿润，内陆丘陵大陆性增强
- 海拔与昼夜温差保证酸度与香气

### 土壤
- **基安蒂地区**：Galestro（泥灰岩-片岩），透气好
- **蒙塔奇诺**：Alberese（钙质泥灰岩），结构感强
- **海岸博格利**：黏土、冲积土，适合赤霞珠等国际品种
- **莫雷利诺**：黏土、石灰岩、燧石

## 等级与主要DOCG

| 产区 | 主要品种 | 等级 |
|------|----------|------|
| 基安蒂经典 Chianti Classico | 桑娇维塞≥80% | DOCG |
| 基安蒂 Chianti | 桑娇维塞≥75% | DOCG |
| 布鲁内罗·蒙塔奇诺 Brunello | 100%桑娇维塞大克隆 | DOCG |
| 贵族蒙特普尔恰诺 Vino Nobile | 桑娇维塞≥70% | DOCG |
| 卡尔米尼亚诺 Carmignano | 桑娇维塞+赤霞珠 | DOCG |
| 莫雷利诺·斯坎萨诺 | 桑娇维塞≥85% | DOCG |
| 博格利 Bolgheri | 波尔多混酿 | DOC |
| 玛勒玛 Toscana IGT | 国际品种 | IGT |

### 基安蒂经典分级
- Annata（基础）
- Riserva（陈年）
- Gran Selezione（顶尖，2014新增）

## 超级托斯卡纳（Super Tuscans）
- 起源于1960-70年代，突破传统DOCG法规
- 引入赤霞珠、美乐等国际品种
- 最初只能降级为VdT/IGT
- 代表：天娜（Tignanello）、索拉雅（Solaia）、西施佳雅（Sassicaia）
- 西施佳雅2013获授Bolgheri Sassicaia DOC

## 代表酒庄
- 安东尼世家（Antinori）- 天娜、索拉雅
- 花思蝶（Frescobaldi）- Castelgiocondo
- 碧安帝山迪（Biondi-Santi）- 布鲁内罗创始者
- 圣圭托（Tenuta San Guido）- 西施佳雅
- 卡斯特洛·班菲（Castello Banfi）""",
    },
    {
        "id": "REGION-italy-piedmont",
        "category": "ENT",
        "subcategory": "region",
        "title": "皮德蒙特产区",
        "title_en": "Piedmont",
        "name_cn": "皮德蒙特",
        "name_en": "Piedmont",
        "tags": ["产区风土", "意大利", "皮德蒙特", "内比奥罗", "巴罗洛"],
        "source": "WSET/Consorzio di Tutela Barolo Barbaresco",
        "data_confidence": "official",
        "summary": "意大利西北部的"酒王之乡"，巴罗洛与巴巴莱斯科的内比奥罗享誉全球。",
        "content_body": """## 地理与气候

### 位置
- 意大利西北部，与法国、瑞士接壤
- 阿尔卑斯山与亚平宁山脉环抱
- 波河平原以南的丘陵地带

### 气候
- 大陆性气候，受山脉影响明显
- 冬季寒冷漫长，夏季温暖
- 秋季多雾（nebbia，内比奥罗名称由来）
- 内比奥罗晚熟，需漫长生长季

### 土壤
- **巴罗洛**：Helvetian期灰蓝色泥灰岩（Tortonian-Messinian）
- 东部Serralunga山谷：Serravallian期黄色砂质泥灰岩，结构更强
- **巴巴莱斯科**：更古老的Tortonian泥灰岩，更早成熟
- Asti地区：沙质、钙质

## 主要DOCG

| 产区 | 主要品种 | 特点 |
|------|----------|------|
| 巴罗洛 Barolo | 100%内比奥罗 | "酒王"，需陈年38个月 |
| 巴巴莱斯科 Barbaresco | 100%内比奥罗 | 更优雅，陈年26个月 |
| 阿斯蒂-巴贝拉 Barbera d'Asti | 巴贝拉 | 高酸多汁 |
| 多尔赛托 Dolcetto d'Alba | 多尔赛托 | 早熟易饮 |
| 阿斯蒂 moscato d'Asti | 小粒白麝香 | 微起泡甜白 |
| 加蒂纳拉 Gattinara | 内比奥罗≥90% | 北部火山岩产区 |
| 佳薇 Gastronomia | 内比奥罗 | 历史产区 |

## 巴罗洛风格流派

### 传统派
- 长期浸渍（30+天）
- 大型斯洛文尼亚橡木桶陈年
- 单宁强劲，需漫长瓶陈

### 现代派
- 短浸渍
- 法国小橡木桶（barrique）
- 果味更突出，更早适饮

### 中间派（主流）
- 结合两者优点
- 代表多数顶级生产商

## 代表酒庄
- 嘉雅（Gaja）- 巴巴莱斯科
- 孔特诺（Giacomo Conterno）- Monfortino传统派标杆
- 维加诺（Giuseppe Mascarello）- Monprivato
- 布鲁诺·嘉科萨（Bruno Giacosa）
- 嘉科萨·孔特诺（Vietti）""",
    },
    {
        "id": "REGION-italy-veneto",
        "category": "ENT",
        "subcategory": "region",
        "title": "威尼托产区",
        "title_en": "Veneto",
        "name_cn": "威尼托",
        "name_en": "Veneto",
        "tags": ["产区风土", "意大利", "威尼托", "阿玛罗尼", "普罗塞克"],
        "source": "WSET/Consorzio Tutela Vini Valpolicella",
        "data_confidence": "official",
        "summary": "意大利产量最大的产区之一，阿玛罗尼与普罗塞克两大旗舰风格并存。",
        "content_body": """## 地理与气候

### 位置
- 意大利东北部，以威尼斯为中心
- 北部阿尔卑斯山，东部亚得里亚海
- 三个主要区域：威尼托东部平原、瓦波利切拉丘陵、科内利亚诺-瓦尔多比亚德内

### 气候
- 北部山区：大陆性，凉爽
- 南部平原：亚得里亚海调节，温和
- 瓦波利切拉丘陵：受Lessini山脉遮蔽，温和

### 土壤
- **瓦波利切拉**：火山玄武岩、石灰岩
- **苏瓦维**：火山岩（黑色玄武岩），矿物感强
- **普罗塞克产区**：泥灰岩、砂岩、黏土

## 主要产区

### 瓦波利切拉系列

| 产区 | 工艺 | 特点 |
|------|------|------|
| Valpolicella Classico | 常规红 | Corvina为主，樱桃果香 |
| Valpolicella Superiore | 陈年≥1年 | 酒体更深 |
| Recioto della Valpolicella | 风干葡萄甜红 | 历史源头 |
| Amarone della Valpolicella | 风干葡萄干红 | 浓郁强劲，高酒精度 |

#### Amarone工艺
- 葡萄采摘后于通风晾房Appassimento风干100-120天
- 失水30-40%，糖分浓缩
- 缓慢发酵至干型，保留残糖极少
- 橡木桶陈年≥2年（Riserva≥4年）

#### 主要品种
- Corvina（45-95%）：骨架、樱桃
- Corvinone（≤50%替代Corvina）：结构
- Rondinella（5-30%）：颜色

### 普罗塞克（Prosecco）
- 产区：Conegliano-Valdobbiadene DOCG、Asolo DOCG
- 品种：Glera（≥85%）
- 工艺：Charmat法（大罐二次发酵）
- 风格：清新花香、梨苹果
- Cartizze：最顶尖单一园

### 苏瓦维（Soave）
- 品种：Garganega（≥70%）
- Soave Classico：原产区，火山岩
- Recioto di Soave：风干甜白

## 代表酒庄
- 阿列格里（Allegrini）- Amarone
- 昆达维尼（Quintarelli）- Amarone传统派标杆
- 达尔福诺（Dal Forno Romano）- 顶级Amarone
- 瓦尔多比亚德内奈里格（Nino Franco）- Prosecco
- 安塞尔米（Anselmi）- Soave""",
    },
    {
        "id": "REGION-italy-friuli",
        "category": "ENT",
        "subcategory": "region",
        "title": "弗留利产区",
        "title_en": "Friuli-Venezia Giulia",
        "name_cn": "弗留利",
        "name_en": "Friuli",
        "tags": ["产区风土", "意大利", "弗留利", "白葡萄酒", "灰皮诺"],
        "source": "WSET/Consorzio Tutela Vini Friuli",
        "data_confidence": "official",
        "summary": "意大利白葡萄酒之乡，斯洛文尼亚边境的精致产区，灰皮诺与弗留拉诺的故乡。",
        "content_body": """## 地理与气候

### 位置
- 意大利东北角，与奥地利、斯洛文尼亚接壤
- 北部阿尔卑斯山，南部亚得里亚海
- 东部边境的Collio与斯洛文尼亚Brda连成同一片风土

### 气候
- 受阿尔卑斯与亚得里亚海双重影响
- 白天温暖，夜晚凉爽
- 昼夜温差大，保留芳香与酸度
- 降雨适中，bora风干燥防病

### 土壤
- **Collio**：泥灰岩-砂岩（flysch di Cormòns），称为ponca
- **Colli Orientali**：泥灰岩与砂岩
- 平原产区：冲积土、砾石
- ponca土赋予矿物感与结构

## 主要白品种

| 品种 | 来源 | 特点 |
|------|------|------|
| 弗留拉诺 Friulano | 本地 | 梨、杏仁、苦杏仁余味 |
| 灰皮诺 Pinot Grigio | 国际 | 意大利最具代表性产区 |
- 长相思 Sauvignon | 国际 | 芳香浓郁，矿物感
- 霞多丽 Chardonnay | 国际 | 优雅平衡
- 白皮诺 Pinot Bianco | 国际 | 清新柔和
- 维多佐 Verduzzo | 本地 | 微甜，杏香
- 丽波拉·贾拉 Ribolla Gialla | 本地 | 高酸矿物，橙酒常用
- 马尔维萨 Malvasia Istriana | 本地 | 花香，Istria半岛

## 主要DOC

| 产区 | 等级 | 特点 |
|------|------|------|
| Collio DOC | 丘陵 | 顶级白葡萄酒 |
| Colli Orientali del Friuli DOC | 丘陵 | Ramandolo甜酒 |
| Friuli Isonzo DOC | 平原 | 砾石，品种丰富 |
| Friuli Grave DOC | 平原 | 大产量 |
| Carso DOC | 石灰岩高原 | Terrano红，维多佐白 |

## 酿造特点
- 现代派：不锈钢罐低温发酵，强调品种香气
- 传统派（新兴）：橡木桶发酵、酒泥陈年、橙酒
- 橙酒运动：Radikon、Damijan等酒庄复兴浸皮白葡萄酒

## 代表酒庄
- 拉迪空（Radikon）- 橙酒先驱
- 耶科（Jermann）- Vintage Tunina
- 利维奥·费尔加（Livio Felluga）
- 马尔科·莫尔（Marco Moser）
- 斯基奥佩托（Schiopetto）- 现代白葡萄酒之父""",
    },
    {
        "id": "REGION-italy-sicily",
        "category": "ENT",
        "subcategory": "region",
        "title": "西西里产区",
        "title_en": "Sicily",
        "name_cn": "西西里",
        "name_en": "Sicily",
        "tags": ["产区风土", "意大利", "西西里", "黑珍珠", "火山土壤"],
        "source": "WSET/Assovini Sicilia",
        "data_confidence": "official",
        "summary": "地中海最大的岛屿产区，黑珍珠与火山土壤的埃特纳新星，葡萄酒复兴代表。",
        "content_body": """## 地理与气候

### 位置
- 地中海最大岛屿，意大利最南端
- 与非洲仅隔140公里
- 三角形岛屿，海岸线长

### 气候
- 典型地中海气候
- 夏季炎热干燥，年日照2500小时
- 沿海温暖，内陆海拔高区域凉爽
- 埃特纳火山高海拔：温差极大，延缓成熟

### 土壤
- 多样：石灰岩、黏土、砂岩、火山岩
- **埃特纳火山**：玄武质熔岩，富含矿物质
- **维多利亚**：红土钙质
- 西部：黏土和石灰岩

## 主要子产区

| 产区 | 主要品种 | 特点 |
|------|----------|------|
| 埃特纳 Etna DOC | 红Nerello Mascalese、白Carricante | 火山高海拔，酒体细腻 |
| 黑珍珠 d'Avola Noto | Nero d'Avola | 西西里旗舰红 |
| 维多利亚 Vittoria DOCG | Frappato+Nero d'Avola | Cerasuolo di Vittoria |
| 马沙拉 Marsala | 加泰罗内托等 | 加强酒 |
| 帕塞蒂纳 Passito di Pantelleria | Zibibbo（亚历山大麝香） | 风干甜酒 |
| 西西里岛 Sicilia DOC | 多品种 | 大区级 |

## 主要品种

### 红品种
- **黑珍珠 Nero d'Avola**：西西里旗舰，李子、黑胡椒
- **Nerello Mascalese**：埃特纳主栽，优雅如黑皮诺
- **Frappato**：轻盈芳香，樱桃
- **Nerello Cappuccio**：埃特纳混酿

### 白品种
- **Carricante**：埃特纳白，矿物高酸
- **Grillo**：马沙拉主力，现代干白
- **Inzolia（Ansonica）**：白诗南近亲，柔和
- **Catarratto**：传统主力，清新
- **Zibibbo**：亚历山大麝香，Pantelleria甜酒

## 埃特纳火山（Etna DOC）
- 海拔600-1000米梯田
- 火山熔岩土壤，富含矿物质
- 北坡：Nerello Mascalese红
- 东坡：Carricante白
- "地中海的勃艮第"

## 代表酒庄
- 帕索皮西亚罗（Passopisciaro）- 埃特纳顶级
- 科斯（COS）- Cerasuolo di Vittoria
- 多娜佳塔（Donnafugata）- 多元化
- 萨德拉·穆托利（Arianna Occhipinti）- Vittoria自然派
- 塔斯卡（Tasca d'Almerita）""",
    },
    {
        "id": "REGION-italy-abruzzo",
        "category": "ENT",
        "subcategory": "region",
        "title": "阿布鲁佐产区",
        "title_en": "Abruzzo",
        "name_cn": "阿布鲁佐",
        "name_en": "Abruzzo",
        "tags": ["产区风土", "意大利", "阿布鲁佐", "蒙特普尔恰诺"],
        "source": "WSET/Consorzio Tutela Vini d'Abruzzo",
        "data_confidence": "official",
        "summary": "意大利中部产区，蒙特普尔恰诺的家园，性价比突出的红葡萄酒产区。",
        "content_body": """## 地理与气候

### 位置
- 意大利中部，亚得里亚海与亚平宁山脉之间
- 东临亚得里亚海，西接拉齐奥、马尔凯
- 内陆多为山地丘陵

### 气候
- 沿海：亚得里亚海调节，温和
- 内陆山区：大陆性，温差大
- 阿泰尔诺河等谷地：小气候多样
- 整体温暖，日照充足

### 土壤
- 沿海平原：冲积土、黏土、石灰岩
- 丘陵：钙质泥灰岩、黏土
- 山区：沙质、岩石
- 含丰富矿物质，排水良好

## 主要产区

| 产区 | 主要品种 | 等级 | 特点 |
|------|----------|------|------|
| 蒙特普尔恰诺·阿布鲁佐 Montepulciano d'Abruzzo | 蒙特普尔恰诺 | DOC | 旗舰红，性价比 |
| Colline Teramane | 蒙特普尔恰诺≥90% | DOCG | 顶级子产区 |
| Trebbiano d'Abruzzo | Trebbiano（实际Bombino Bianco） | DOC | 白葡萄酒 |
| Cerasuolo d'Abruzzo | 蒙特普尔恰诺 | DOC | 桃红 |
| Abruzzo | 多品种 | DOC | 大区级 |

## 主要品种

### 红品种
- **蒙特普尔恰诺 Montepulciano**（注意：与托斯卡纳Vino Nobile di Montepulciano同名不同物）
  - 阿布鲁佐旗舰红品种
  - 深紫红色，单宁柔和
  - 黑樱桃、黑莓、辛香
  - 酒体丰满，酸度适中
  - 适饮期早，亦有陈年潜力

### 白品种
- **Trebbiano d'Abruzzo**：实际多为Bombino Bianco
  - 清新柔和，性价比白
- **Pecorino**：本地芳香品种，高酸矿物
- **Passerina**：清新柔和
- **Cocciola**：本地稀有品种

## 蒙特普尔恰诺·阿布鲁佐分级
- 基础款：易饮果味，无需陈年
- Riserva：陈年≥2年（其中橡木桶≥6个月）
- Colline Teramane DOCG：陈年≥3年（橡木桶≥1年）

## 代表酒庄
- 瓦伦蒂尼（Valentini）- Trebbiano传奇，价格惊人
- 埃米迪·佩佩（Emidio Pepe）- 传统自然派
- 法尔内塞（Farnese）- 大众市场主力
- 拉维（La Val）- 高品质
- 托雷（Torre dei Beati）""",
    },
    {
        "id": "REGION-spain-rioja",
        "category": "ENT",
        "subcategory": "region",
        "title": "里奥哈产区",
        "title_en": "Rioja",
        "name_cn": "里奥哈",
        "name_en": "Rioja",
        "tags": ["产区风土", "西班牙", "里奥哈", "丹魄", "美国橡木桶"],
        "source": "WSET/Consejo Regulador DOCa Rioja",
        "data_confidence": "official",
        "summary": "西班牙最著名的葡萄酒产区，丹魄与美国橡木桶的传奇结合，分级体系完善。",
        "content_body": """## 地理与气候

### 位置
- 西班牙北部，埃布罗河流域
- 跨越三个自治区：拉里奥哈、巴斯克、纳瓦拉
- 分为三个子区域：Rioja Alta、Rioja Alavesa、Rioja Oriental

### 气候
- **Rioja Alta & Alavesa**：受大西洋与地中海影响，温和
- **Rioja Oriental**：地中海气候，温暖干燥
- 北部坎塔布连山脉阻挡大西洋湿气
- 整体昼夜温差大，酸度保留好

### 土壤
- 多样：钙质黏土、铁质黏土、冲积土
- **Rioja Alavesa**：石灰岩黏土，排水好
- **Rioja Alta**：黏土-石灰岩混合
- **Rioja Oriental**：冲积土、铁质黏土

## 等级体系

### 葡萄园分类（2018新规）
- Viñedo Singular（单一园）
- 村庄级 Vino de Municipio
- 大区级 Rioja DOCa

### 陈年等级

| 等级 | 橡木桶 | 瓶陈 | 总陈年 | 特点 |
|------|--------|------|--------|------|
| Joven | 无/短期 | 无 | - | 果味清新 |
| Crianza | 12个月 | 6个月 | 24个月 | 平衡易饮 |
| Reserva | 12个月 | 24个月 | 36个月 | 复杂优雅 |
| Gran Reserva | 24个月 | 36个月 | 60个月 | 顶级，仅在好年份 |

白葡萄酒陈年要求略低

## 主要品种

### 红品种
- **丹魄 Tempranillo**（≥主栽）：里奥哈灵魂，红色水果、香辛、陈年后皮革蘑菇
- **歌海娜 Garnacha**：高酒精、红色果香
- **格拉西亚诺 Graciano**：高酸深色，调配用
- **马苏埃洛 Mazuelo（Carignan）**：高酸单宁
- **马图拉纳 Maturana**：稀有本地

### 白品种
- **Viura（Macabeo）**：主力，清新
- **Malvasía**：传统调配，复杂度
- **Garnacha Blanca**：丰满
- **Tempranillo Blanco**：突变品种，新派

## 美国橡木桶传统
- 美国白橡Quercus alba
- 香草、椰子、甜辛香
- 传统里奥哈标志
- 现代派：法国橡木桶混用

## 代表酒庄
- 罗德里格斯·拉维嘉（La Rioja Alta）- 904、890
- 马克斯·里斯卡尔（Marqués de Riscal）- 1858创立
- 美宇侯（Marqués de Murrieta）- 1852创立
- 阿塔迪（Artadi）- 现代单一园
- 洛佩兹·埃雷迪亚（R. López de Heredia）- 传统派""",
    },
    {
        "id": "REGION-spain-ribera-del-duero",
        "category": "ENT",
        "subcategory": "region",
        "title": "杜罗河岸产区",
        "title_en": "Ribera del Duero",
        "name_cn": "杜罗河岸",
        "name_en": "Ribera del Duero",
        "tags": ["产区风土", "西班牙", "杜罗河岸", "丹魄", "维奇亚"],
        "source": "WSET/Consejo Regulador DO Ribera del Duero",
        "data_confidence": "official",
        "summary": "西班牙顶级红葡萄酒产区，与里奥哈并称双雄，以强劲的丹魄（Tinto Fino）闻名。",
        "content_body": """## 地理与气候

### 位置
- 西班牙中部卡斯蒂利亚-莱昂大区
- 沿杜罗河两岸，长约115公里、宽35公里
- 海拔750-950米的高原

### 气候
- 极端大陆性气候
- 夏季白天35°C+，夜晚可降至10°C
- 昼夜温差达20°C以上，酸度与香气保留
- 冬季严寒，春季霜冻风险大
- 年降雨450mm，干旱压力

### 土壤
- 多样：沙土、黏土、石灰岩、砾石
- 不同地块差异大
- 高海拔沙质土壤有抗根瘤蚜老藤

## 等级与陈年体系

### 陈年等级

| 等级 | 橶木桶 | 瓶陈 | 总陈年 |
|------|--------|------|--------|
| Joven Roble | 3-12个月 | - | 12个月内 |
| Crianza | 12个月 | 12个月 | 24个月 |
| Reserva | 12个月 | 24个月 | 36个月 |
| Gran Reserva | 24个月 | 36个月 | 60个月 |

## 主要品种

### 红品种
- **Tinto Fino / Tinta del País**（丹魄当地克隆）≥75%
  - 与里奥哈丹魄同种，但克隆差异
  - 葡萄串更松散，皮更厚
  - 酒体更深，单宁更强
- **赤霞珠、美乐、马尔贝克**：辅助（≤25%）
- **阿比略 Albillo**：白品种，少量调配

### 与里奥哈对比

| 项目 | 里奥哈 | 杜罗河岸 |
|------|--------|----------|
| 气候 | 大西洋影响 | 极端大陆性 |
| 海拔 | 中等 | 高（750-950m） |
| 风格 | 优雅细腻，橡木主导 | 强劲浓郁，果味主导 |
| 单宁 | 中等柔和 | 强劲高单宁 |
| 酒精度 | 13-13.5% | 14%+ |

## 代表酒庄
- **维加·西西利亚（Vega Sicilia）**- 西班牙酒王，Único
- **平古斯（Pingus）**- Peter Sisseck，超顶级
- **帕果斯·卡蕾斯（Pago de Carraovejas）**
- **阿雷杭德罗·费尔南德斯（Tinto Pesquera）**- 现代派先驱
- **埃米利奥·莫罗（Emilio Moro）**""",
    },
    {
        "id": "REGION-spain-priorat",
        "category": "ENT",
        "subcategory": "region",
        "title": "普里奥拉托产区",
        "title_en": "Priorat",
        "name_cn": "普里奥拉托",
        "name_en": "Priorat",
        "tags": ["产区风土", "西班牙", "普里奥拉托", "老藤歌海娜", "板岩"],
        "source": "WSET/DOQ Priorat",
        "data_confidence": "official",
        "summary": "西班牙仅有的两个DOCa之一，老藤歌海娜与板岩土壤造就矿物感极强的强劲红酒。",
        "content_body": """## 地理与气候

### 位置
- 西班牙东北部加泰罗尼亚
- 塔拉戈纳省内陆山区
- 锯齿状山脉（Montsant环绕）中的小产区

### 气候
- 大陆性-地中海混合气候
- 夏季炎热干燥，冬季寒冷
- 海洋影响被Montsant山阻挡
- 日照强烈，昼夜温差大
- 年降雨500-600mm，干旱压力

### 土壤（灵魂要素）
- **Llicorella（板岩/片岩）**：普里奥拉托标志
  - 古老的变质岩，分层易碎
  - 反射热量，促进成熟
  - 根系深扎岩石缝隙吸取矿物
  - 排水极佳，迫使老藤深入
- 不同村土壤差异：Porrera（沙岩）、Gratallops（板岩为主）

## 等级

- **DOQ Priorat**（Denominació d'Origen Qualificada）
- 2009年升级，西班牙仅两个DOCa之一（另一为里奥哈）
- 子产区："Viles de la Garnatxa"等本地概念
- 单一园（Vinya Classificada）正在推进

## 主要品种

### 红品种
- **歌海娜 Garnacha**：旗舰，老藤（60-100年+）
- **佳丽酿 Cariñena（Samsó）**：结构、酸度、矿物
- **赤霞珠、西拉、美乐**：辅助（新派引入）

### 白品种
- **Garnacha Blanca、Macabeo、Pedro Ximénez**：少量白葡萄酒

## 历史
- 12世纪加尔都西会修士建修道院
- 19世纪根瘤蚜重创，葡萄园荒废
- 1989年"普里奥拉托五人组"（René Barbier等）复兴
- 老藤幸存，品质卓越

## 葡萄园特点
- 阶梯式梯田（costers陡坡）
- 老藤多为独立灌木头状修剪
- 产量极低（<1kg/株）
- 全部手工采摘

## 代表酒庄
- **帕拉西奥斯·洛斯·塞雷斯（Álvaro Palacios）**- L'Ermita、Finca Dofí
- **帕萨多·帕尔·德尔·马斯（Pasao del Mas）**- 老藤歌海娜
- **卡萨·马勒拉（Clos Mogador）**- René Barbier
- **特尔·米尼翁（Clos Erasmus）**- 100分常客
- **马赛特（Mas la Plana）**""",
    },
    {
        "id": "REGION-us-napa",
        "category": "ENT",
        "subcategory": "region",
        "title": "纳帕谷产区",
        "title_en": "Napa Valley",
        "name_cn": "纳帕谷",
        "name_en": "Napa Valley",
        "tags": ["产区风土", "美国", "纳帕", "赤霞珠", "火山土"],
        "source": "WSET/Napa Valley Vintners",
        "data_confidence": "official",
        "summary": "美国最著名的葡萄酒产区，赤霞珠的圣地，多样土壤与微气候造就顶级红酒。",
        "content_body": """## 地理与气候

### 位置
- 美国加利福尼亚州北部
- 旧金山以北约80公里
- 南北长约50公里，东西宽约8公里
- 两侧Mayacamas和Vaca山脉环绕

### 气候
- 地中海气候
- 南部San Pablo湾带来凉爽雾气
- 北端更温暖
- 昼夜温差大（10-15°C），酸度保留
- 生长季干燥少雨，灌溉可控

### 土壤
- 世界土壤最多样产区之一（半数世界土壤类型）
- **火山土**：Vaca山脉东侧（Howell Mountain、Atlas Peak）
- **冲积土**：谷底（砂砾、黏土）
- **海洋沉积岩**：Mayacamas西坡
- 不同AVA土壤差异显著

## 主要AVA子产区

| AVA | 主要品种 | 特点 |
|------|----------|------|
| Oakville | 赤霞珠 | 中心地带，均衡 |
| Rutherford | 赤霞珠 | "Rutherford Dust"风味 |
| Stags Leap District | 赤霞珠 | 优雅细腻 |
| Howell Mountain | 赤霞珠 | 高海拔强劲 |
| Mount Veeder | 赤霞珠 | 山地，结构紧实 |
| Carneros | 黑皮诺、霞多丽 | 最凉爽，雾气重 |
| St. Helena | 赤霞珠 | 温暖成熟 |
| Calistoga | 多品种 | 最热北端 |

### AVA体系
- 1981年纳帕谷成为加州第一个AVA
- 子AVA共16个
- 联邦法律保护"Napa"名称

## 主要品种

| 品种 | 占比 | 特点 |
|------|------|------|
| 赤霞珠 | 40%+ | 旗舰，深色强劲 |
| 霞多丽 | 20% | 苹果乳酸，橡木 |
| 美乐 | 10% | 圆润丰腴 |
| 黑皮诺 | <5% | 仅Carneros凉爽区 |
| 长相思 | - | 新派不锈钢清新 |

## 1976巴黎盲品
- Stag's Leap Wine Cellars赤霞珠夺冠
- Chateau Montelena霞多丽夺冠
- "Judgment of Paris"震惊酒界
- 纳帕谷登上世界舞台

## 代表酒庄
- **罗曼尼·康帝酒庄（Opus One）**- 蒙大维与罗斯柴尔德合作
- 啸鹰（Screaming Eagle）- 稀缺膜拜酒
- 鹿跃酒窖（Stag's Leap Wine Cellars）
- 蒙大维（Robert Mondavi）- 纳帕复兴之父
- 鸢尾花（Dominus Estate）- Christian Moueix
- 海德（Harlan Estate）""",
    },
    {
        "id": "REGION-us-sonoma",
        "category": "ENT",
        "subcategory": "region",
        "title": "索诺玛产区",
        "title_en": "Sonoma County",
        "name_cn": "索诺玛",
        "name_en": "Sonoma",
        "tags": ["产区风土", "美国", "索诺玛", "黑皮诺", "霞多丽"],
        "source": "WSET/Sonoma County Vintners",
        "data_confidence": "official",
        "summary": "气候多样的加州顶级产区，黑皮诺与霞多丽的优质产区，规模大于纳帕。",
        "content_body": """## 地理与气候

### 位置
- 加州北部，纳帕谷西侧
- 西临太平洋
- 面积约为纳帕2倍，葡萄园更多

### 气候
- 高度多样化，从凉爽到温暖
- **沿海**：太平洋冷凉雾气
- **内陆**：温暖干燥
- Russian River、Petaluma Gap带来凉爽气流
- 整体比纳帕凉爽，更适合黑皮诺、霞多丽

### 土壤
- 多样：火山岩、海洋沉积岩、冲积土、砂岩
- Sonoma Coast：海洋沉积岩
- Alexander Valley：冲积砾石
- 不同AVA土壤差异显著

## 主要AVA子产区

| AVA | 主要品种 | 特点 |
|------|----------|------|
| Russian River Valley | 黑皮诺、霞多丽 | 凉爽雾气，优质黑皮诺 |
| Sonoma Coast | 黑皮诺、霞多丽 | 最凉爽，矿物感 |
| Alexander Valley | 赤霞珠、美乐 | 温暖，圆润丰腴 |
| Dry Creek Valley | 金粉黛 | 砾石，老藤 |
| Sonoma Valley | 多品种 | 历史悠久 |
| Chalk Hill | 霞多丽 | 火山白垩土 |
| Green Valley | 黑皮诺 | 凉爽，Russian River子区 |
| Rockpile | 赤霞珠 | 高海拔 |

## 主要品种

### 红品种
- **黑皮诺**：旗舰，Russian River、Sonoma Coast
  - 红色莓果、香料、矿物
- **赤霞珠**：Alexander Valley主力
- **金粉黛（Zinfandel）**：Dry Creek老藤
  - 黑莓、辛香、高酒精
- **美乐、西拉**：辅助

### 白品种
- **霞多丽**：Russian River、Sonoma Coast
  - 苹果、柑橘、矿物
- **长相思**：清新风格
- **白诗南、Viognier**

## 历史地位
- 1824年俄罗斯人在Fort Ross种植
- 1857年Buena Vista Winery建立（加州最早商业酒庄之一）
- Agoston Haraszthy引入欧洲品种
- 1970年代黑皮诺复兴

## 代表酒庄
- **威廉·塞弗（Williams Selyem）**- 顶级黑皮诺
- **基斯勒（Kistler Vineyards）**- 单一园霞多丽
- **罗城（Rochioli）**- Russian River标杆
- **玛尔卡森（Marcassin）**- Helen Turley
- **雷文斯伍德（Ravenswood）**- 金粉黛专家
- **乔丹（Jordan）**- Alexander Valley赤霞珠""",
    },
    {
        "id": "REGION-us-oregon",
        "category": "ENT",
        "subcategory": "region",
        "title": "俄勒冈产区",
        "title_en": "Oregon",
        "name_cn": "俄勒冈",
        "name_en": "Oregon",
        "tags": ["产区风土", "美国", "俄勒冈", "威拉米特河谷", "黑皮诺"],
        "source": "WSET/Oregon Wine Board",
        "data_confidence": "official",
        "summary": "美国黑皮诺的优质产区，威拉米特河谷凉爽气候与火山土壤造就勃艮第风格。",
        "content_body": """## 地理与气候

### 位置
- 美国西北部太平洋沿岸
- 北邻华盛顿州，南接加州
- 主要葡萄园集中于威拉米特河谷

### 气候
- 凉爽海洋性气候
- 北纬45°，与勃艮第相近
- 太平洋冷凉气流，夏季温和
- 生长季长，成熟缓慢
- 昼夜温差大，酸度保留
- 收获期晚（9月底-10月）

### 土壤
- **威拉米特河谷**：火山玄武岩（Jory系列）、海洋沉积岩
- 土壤排水好，迫使根系深入
- 火山土壤赋予矿物感

## 主要AVA

### 威拉米特河谷Willamette Valley
- 俄勒冈旗舰产区，6个子AVA

| 子AVA | 特点 |
|-------|------|
| Dundee Hills | 火山岩Jory土壤，黑皮诺核心 |
| Yamhill-Carlton | 海洋沉积岩 |
| Ribbon Ridge | 最小AVA，温暖 |
| McMinnville | 海洋沉积 + 火山岩 |
| Eola-Amity Hills | 凉爽，太平洋风 |
| Chehalem Mountains | 多样土壤 |

### 其他俄勒冈产区
- **Southern Oregon**：温暖，罗纳品种、赤霞珠
- **Umpqua Valley**：过渡气候
- **Rogue Valley**：最温暖
- **Columbia Gorge**：凉爽，多样

## 主要品种

| 品种 | 占比 | 特点 |
|------|------|------|
| 黑皮诺 | 60%+ | 旗舰，勃艮第风格 |
| 灰皮诺 | 15% | 俄勒冈特色白 |
| 霞多丽 | - | 优雅矿物 |
| 雷司令 | - | 干型为主 |
- 黑皮诺：红色莓果、香料、土质矿物
- 酸度鲜活，酒精度比加州低

## 历史与特点
- 1965年David Lett（Eyrie Vineyards）首次种植黑皮诺
- 1979年Eyrie黑皮诺在巴黎盲品获前列
- 1987年Domaine Drouhin（勃艮第Drouhin家族）入驻
- 酒庄规模普遍较小，精品为主
- 强调可持续、有机、生物动力法

## 代表酒庄
- **艾瑞（Eyrie Vineyards）**- 俄勒冈黑皮诺之父
- **Domaine Drouhin**- 勃艮第传统
- **贝克（Beaux Frères）**- Michael Etzel
- **肯·赖特（Ken Wright Cellars）**- 单一园先驱
- **谢飞（Domaine Serene）**- 顶级黑皮诺
- **安吉（Archery Summit）**""",
    },
    {
        "id": "REGION-us-washington",
        "category": "ENT",
        "subcategory": "region",
        "title": "华盛顿州产区",
        "title_en": "Washington State",
        "name_cn": "华盛顿州",
        "name_en": "Washington State",
        "tags": ["产区风土", "美国", "华盛顿", "赤霞珠", "干燥气候"],
        "source": "WSET/Washington State Wine Commission",
        "data_confidence": "official",
        "summary": "美国第二大葡萄酒产区，干燥大陆性气候与灌溉系统造就饱满赤霞珠。",
        "content_body": """## 地理与气候

### 位置
- 美国西北部，与俄勒冈相邻
- 主要葡萄园在喀斯喀特山脉东侧（东部干旱区）
- 哥伦比亚河流域为核心

### 气候
- 干燥大陆性气候（山脉背风坡）
- 年降雨少（200-250mm）
- 夏季温暖，日照长（北纬46°）
- 昼夜温差大，酸度保留
- 冬季严寒，偶有冻害风险

### 土壤
- 冰川洪水Misson Beds形成的多样化土壤
- 砂质壤土、玄武岩、黄土
- 排水良好，矿物丰富
- 多数土壤无根瘤蚜，部分自根葡萄

## 主要AVA

| AVA | 主要品种 | 特点 |
|------|----------|------|
| Columbia Valley | 赤霞珠为主 | 大区AVA，占99%产量 |
| Yakima Valley | 赤霞珠、美乐 | 历史最久 |
| Red Mountain | 赤霞珠 | 强劲浓郁，顶级 |
| Walla Walla Valley | 赤霞珠、西拉 | 跨州AVA |
| Horse Heaven Hills | 赤霞珠 | 凉爽坡向 |
| Wahluke Slope | 赤霞珠 | 最温暖，成熟稳定 |
| Snipes Mountain | 多品种 | 古老土壤 |
| Ancient Lakes | 霞多丽、雷司令 | 凉爽，白为主 |
| Columbia Gorge | 多品种 | 太平洋影响 |

## 主要品种

### 红品种
- **赤霞珠**：旗舰，深色饱满
  - 黑加仑、薄荷、辛香
  - 单宁柔和，酸度均衡
- **美乐**：华盛顿传统强项
- **西拉**：新兴，Rhône风格
- **品丽珠、马尔贝克**：辅助

### 白品种
- **霞多丽**：主力白
- **雷司令**：优质干型
- **长相思、白皮诺**

## 酿造特点
- 干燥气候减少病害
- 灌溉可控，控制产量与成熟
- 多数酒庄位于西雅图附近，葡萄来自东部
- 现代设备与精品酿造结合

## 代表酒庄
- **奎塞达（Quilceda Creek Vintners）**- 100分常客
- **莱昂内提（Leonetti Cellar）**- 华盛顿最早精品酒庄
- **哥伦比亚峰（Columbia Crest）**- 大规模高质量
- **伍德沃德峡谷（Woodward Canyon）**- 早期先驱
- **德卢莱（Domaine Drouhin的姐妹）**
- **查尔斯·史密斯（Charles Smith Wines）**""",
    },
    {
        "id": "REGION-cn-ningxia",
        "category": "ENT",
        "subcategory": "region",
        "title": "宁夏贺兰山东麓产区",
        "title_en": "Ningxia Helan Mountain East",
        "name_cn": "宁夏贺兰山东麓",
        "name_en": "Ningxia Helan Mountain East",
        "tags": ["产区风土", "中国", "宁夏", "赤霞珠", "贺兰山"],
        "source": "宁夏贺兰山东麓葡萄产业园区管委会",
        "data_confidence": "official",
        "summary": "中国最具国际声誉的葡萄酒产区，"中国波尔多"，赤霞珠为主导的精品产区。",
        "content_body": """## 地理与气候

### 位置
- 中国宁夏回族自治区北部
- 贺兰山东麓冲积平原
- 北纬37°43'-39°23'，黄金酿酒带
- 黄河灌区

### 气候
- 大陆性干旱气候
- 年日照3000+小时
- 昼夜温差大（10-15°C）
- 年降雨200mm，干燥少病
- 冬季严寒，需埋藤越冬（关键挑战）

### 土壤
- 砾石沙壤土为主
- 含丰富矿物质
- 透气性好，排水佳
- 不同子产区土壤差异：砂砾、风沙土、灰钙土

## 产区划分

### 子产区（六大）
1. **石嘴山产区**：最北，温暖
2. **贺兰产区**：北部，砾石
3. **西夏王陵产区**：中部核心
4. **永宁产区**：南部
5. **青铜峡产区**：东南
6. **红寺堡产区**：最南，高海拔

### 列级酒庄体系
- 2013年实行酒庄酒分级
- 五级：一至五级（类似波尔多1855）
- 中国首个列级酒庄体系

## 主要品种

### 红品种
- **赤霞珠**：绝对主力，60%+
  - 颜色深，单宁成熟
  - 黑加仑、薄荷、辛香
- **美乐**：调配辅助
- **品丽珠**：辅助
- **马瑟兰（Marselan）**：中国特色杂交，表现优异
- **西拉**：少量

### 白品种
- **霞多丽**：主力白
- **长相思**：少量
- **雷司令**：少量

## 发展历程
- 1984年西夏王酒厂建立
- 2003年确立"葡萄酒产业"
- 2011年《Decanter》大赛首获国际金奖
- 2020年列级酒庄体系成熟
- 2020年获得"葡萄酒之都"称号

## 代表酒庄
- **加贝兰（Vice Versa / Helanqingxue）**- 2011 DWWA金奖
- **留世（Legacy Peak）**
- **迦南美地（Sino-Canada）**
- **银色高地（Silver Heights）**- Emma Gao
- **西夏王（Summer Palace）**
- **贺东庄园（Chandon China）**
- **张裕摩塞尔十五世（Changyu Moser）**""",
    },
    {
        "id": "REGION-cn-xinjiang",
        "category": "ENT",
        "subcategory": "region",
        "title": "新疆产区",
        "title_en": "Xinjiang",
        "name_cn": "新疆",
        "name_en": "Xinjiang",
        "tags": ["产区风土", "中国", "新疆", "高海拔", "冰酒"],
        "source": "新疆葡萄产业协会",
        "data_confidence": "official",
        "summary": "中国最大的葡萄酒产区，高海拔、强日照与极端温差造就浓郁风格，冰酒为亮点。",
        "content_body": """## 地理与气候

### 位置
- 中国西北新疆维吾尔自治区
- 天山山脉横贯，分南疆北疆
- 主要葡萄园集中于吐鲁番、焉耆、和硕、伊犁

### 气候
- 温带大陆性干旱气候
- 年日照2800-3200小时
- 昼夜温差极大（15-20°C）
- 年降雨少（50-200mm），需灌溉
- 干燥少病，冬季需埋藤

### 土壤
- 砂砾土、棕漠土、灰钙土
- 含丰富矿物质
- 透气排水良好
- 部分盐碱化需改良

## 主要子产区

| 子产区 | 位置 | 主要品种 | 特点 |
|--------|------|----------|------|
| 吐鲁番 | 东疆盆地 | 多品种，鲜食为主 | 极热，历史悠久 |
| 焉耆 | 南疆 | 赤霞珠、品丽珠 | 优质红酒 |
| 和硕 | 南疆 | 赤霞珠、霞多丽 | 坡地砾石 |
| 伊犁 | 北疆 | 雷司令、霞多丽 | 凉爽，冰酒 |
| 石河子 | 北疆 | 赤霞珠 | 大规模 |
| 五家渠 | 北疆 | 冰酒 | 高纬度冰酒 |

## 主要品种

### 红品种
- **赤霞珠**：主力，颜色深、酒体饱满
- **美乐**：辅助
- **马瑟兰**：表现优异
- **西拉**：少量

### 白品种
- **霞多丽**：主力白
- **雷司令**：伊犁冰酒
- **长相思**：少量

### 冰酒亮点
- 新疆伊犁、五家渠产冰酒
- 高纬度（北纬44°）保证冬季低温
- Vidal、雷司令为主
- 甜度高，酸度好

## 历史与发展
- 古代西域"葡萄美酒夜光杯"
- 1960年代现代葡萄酒业起步
- 1980年代大规模酒厂建立
- 2010年后精品酒庄兴起
- 新疆是中国葡萄栽培最古老区域

## 酿造特点
- 糖度高，酒精度自然偏高
- 酸度是挑战，需控制产量
- 干燥无病，有机潜力大
- 部分区域冬季埋藤成本高

## 代表酒庄
- **楼兰酒庄**- 吐鲁番历史
- **天塞酒庄（Tiansai）**- 和硕，精品
- **中菲酒庄**- 焉耆
- **国菲酒庄**- 精品
- **乡都酒业**- 焉耆
- **伊珠冰酒**- 伊犁冰酒""",
    },
    {
        "id": "REGION-cn-shandong",
        "category": "ENT",
        "subcategory": "region",
        "title": "山东烟台产区",
        "title_en": "Shandong Yantai",
        "name_cn": "山东烟台",
        "name_en": "Shandong Yantai",
        "tags": ["产区风土", "中国", "山东", "烟台", "海岸气候"],
        "source": "烟台市葡萄与葡萄酒局",
        "data_confidence": "official",
        "summary": "中国现代葡萄酒工业的摇篮，"国际葡萄·葡萄酒城"，张裕大本营。",
        "content_body": """## 地理与气候

### 位置
- 山东省东部烟台市
- 山东半岛北部，渤海与黄海之间
- 北纬37°，与波尔多同纬度
- 主要分布于蓬莱、龙口、莱山、海阳

### 气候
- 暖温带湿润季风气候
- 海洋调节，温和湿润
- 夏季温暖但不酷热
- 降水集中于夏季（700-800mm）
- 秋季成熟期湿润，病害风险需管理

### 土壤
- 多样：砾石、沙壤土、棕壤
- 蓬莱以砂砾和棕壤为主
- 含少量石灰岩
- 部分区域偏酸

## 主要子产区

| 子产区 | 位置 | 主要品种 | 特点 |
|--------|------|----------|------|
| 蓬莱 | 半岛北海岸 | 赤霞珠、霞多丽 | 海岸气候，精品聚集 |
| 龙口 | 半岛北部 | 赤霞珠 | 张裕大本营 |
| 海阳 | 半岛南部 | 赤霞珠 | 较温暖 |
| 栖霞 | 内陆 | 多品种 | 海拔较高 |
| 莱山 | 烟台市区南 | 霞多丽 | 张裕卡斯特酒庄 |

## 主要品种

### 红品种
- **赤霞珠**：主力，颜色深
- **蛇龙珠（Cabernet Gernischt）**：中国特色，张裕推广
- **美乐**：辅助
- **马瑟兰**：新兴

### 白品种
- **霞多丽**：主力白
- **贵人香（Italian Riesling）**：传统
- **长相思**：少量
- **小芒森（Petit Manseng）**：蓬莱特色，甜酒

## 历史与地位
- 1892年张弼士创办张裕
- 中国现代葡萄酒工业发源地
- 1987年烟台获"国际葡萄·葡萄酒城"称号（OIV）
- 张裕是中国最早、规模最大的葡萄酒企业
- 长期主导中国葡萄酒产业

## 发展特点
- 大企业（张裕、长城）+ 精品酒庄并行
- 海岸气候塑造清新风格
- "蓬莱海岸葡萄酒"地理标志
- 旅游与酒庄文化发达

## 代表酒庄
- **张裕卡斯特酒庄**- 中法合作旗舰
- **张裕爱斐堡北京**（虽在北京，张裕品牌）
- **君顶酒庄**- 蓬莱精品
- **瑞枫奥塞斯**- 蓬莱
- **国宾酒庄**- 蓬莱
- **苏各兰酒庄**- 苏格兰主题
- **龙亭酒庄**- 生物动力法""",
    },
    {
        "id": "REGION-cn-hebei-changli",
        "category": "ENT",
        "subcategory": "region",
        "title": "河北昌黎产区",
        "title_en": "Hebei Changli",
        "name_cn": "河北昌黎",
        "name_en": "Hebei Changli",
        "tags": ["产区风土", "中国", "河北", "昌黎", "赤霞珠", "花岗岩"],
        "source": "昌黎葡萄酒产区管理委员会",
        "data_confidence": "official",
        "summary": "中国干红葡萄酒之乡，长城葡萄酒发源地，赤霞珠与花岗岩土壤的经典组合。",
        "content_body": """## 地理与气候

### 位置
- 河北省秦皇岛市昌黎县
- 燕山山脉南麓，渤海北岸
- 北纬39°41'
- 距北京约300公里

### 气候
- 暖温带半湿润大陆性季风气候
- 海洋与山地双重影响
- 四季分明
- 年日照2800小时
- 昼夜温差较大
- 冬季需埋藤越冬

### 土壤
- **花岗岩风化土**：核心特色
  - 含石英、长石矿物
  - 排水极佳
  - 赋予矿物感与结构
- 砾质沙壤土
- 部分含砾石
- 微酸性，适合赤霞珠

## 主要子产区

| 子产区 | 位置 | 主要品种 | 特点 |
|--------|------|----------|------|
| 昌黎县城北 | 燕山南坡 | 赤霞珠 | 花岗岩核心 |
| 凤凰山 | 山地丘陵 | 赤霞珠 | 优质坡地 |
| 十里铺 | 平原 | 赤霞珠 | 大规模 |
| 卢龙 | 昌黎邻县 | 赤霞珠 | 扩展区 |
- "中国干红葡萄酒城"地理标志产区

## 主要品种

### 红品种
- **赤霞珠**：绝对主力，70%+
  - 颜色深，单宁成熟
  - 黑加仑、青椒、矿物
- **品丽珠**：辅助
- **美乐**：调配
- **西拉**：少量
- **马瑟兰**：新兴

### 白品种
- **霞多丽**：少量
- **贵人香**：传统

## 历史与发展
- 1979年长城葡萄酒（沙城）建立，昌黎为重要基地
- 1980年代大规模发展赤霞珠
- 1990年代成为"中国干红城"
- 2010年昌黎假酒事件重创
- 之后严格整顿，品质重建
- 中粮长城、华夏长城等大企业基地

## 酿造特点
- 花岗岩土壤赋予矿物感
- 海洋影响保留酸度
- 赤霞珠风格：颜色深，单宁紧实
- 多为企业化大规模生产
- 精品酒庄逐渐兴起

## 代表酒庄
- **华夏长城**- 中粮旗下，最大基地
- **朗格斯酒庄**- 奥地利Gernot Langes-Swarovski投资
- **施华洛世奇酒庄**
- **茅台葡萄酒庄**- 茅台集团
- **丘山论酒庄**- 精品
- **杰斯塔酒庄**""",
    },
    {
        "id": "REGION-cn-yunnan-shangri-la",
        "category": "ENT",
        "subcategory": "region",
        "title": "云南香格里拉产区",
        "title_en": "Yunnan Shangri-La",
        "name_cn": "云南香格里拉",
        "name_en": "Yunnan Shangri-La",
        "tags": ["产区风土", "中国", "云南", "香格里拉", "高海拔", "敖云"],
        "source": "迪庆州葡萄产业发展办公室",
        "data_confidence": "official",
        "summary": "世界海拔最高的精品葡萄酒产区之一，敖云（Ao Yun）为代表的梅里雪山传奇。",
        "content_body": """## 地理与气候

### 位置
- 云南省西北部迪庆藏族自治州
- 横断山脉梅里雪山区域
- 澜沧江、金沙江上游河谷
- 北纬28°，"三江并流"世界遗产地

### 气候
- 高海拔低纬度独特气候
- 海拔1800-2800米
- 立体气候，垂直差异大
- 干湿季分明
- 日照强烈，紫外线高
- 昼夜温差极大

### 土壤
- 河谷冲积土、沙壤土
- 含丰富矿物质
- 不同海拔、坡向差异显著
- 澜沧江峡谷砾石冲积

## 子产区特点

### 阿东村（Adong）
- 海拔2200米
- 敖云酒庄主葡萄园之一
- 西向坡，光照充足

### 斯农村（Sinong）
- 海拔2000-2200米
- 澜沧江河谷
- 沙质冲积土

### 西当村（Xitang）
- 海拔1900米
- 较温暖
- 早熟

### 朔日村（Shuori）
- 海拔2400米
- 高凉爽
- 晚熟

## 主要品种

### 红品种
- **赤霞珠**：主力，敖云核心
- **品丽珠**：调配
- **美乐**：辅助
- **西拉**：少量

### 白品种
- **霞多丽**：少量试验

## 高海拔特色
- 海拔2200米，世界最高葡萄酒产区之一
- 强紫外线促进花青素合成
- 昼夜温差延缓成熟，保留酸度
- 风味物质积累丰富
- 病害压力小，有机潜力大

## 敖云（Ao Yun）项目
- LVMH集团投资
- 2008年启动
- 首席酿酒师：Tony Jordan博士
- 2013年首发年份
- "云之上"寓意
- 多村葡萄园调配
- 国际市场售价逾300美元

## 历史与挑战
- 2000年前零星种植
- 2008年LVMH勘察启动
- 高海拔运输、管理困难
- 偏远地区基础设施薄弱
- 小农种植，需精细管理
- 冬季无需埋藤（高海拔但干冷抗寒）

## 代表酒庄
- **敖云酒庄（Ao Yun）**- LVMH旗舰中国项目
- **香格里拉酒业**- 本土企业
- **太阳魂酒庄**- 梅里雪山
- **扎西酒庄**- 藏式风情""",
    },
    {
        "id": "REGION-au-barossa",
        "category": "ENT",
        "subcategory": "region",
        "title": "巴罗萨谷产区",
        "title_en": "Barossa Valley",
        "name_cn": "巴罗萨谷",
        "name_en": "Barossa Valley",
        "tags": ["产区风土", "澳大利亚", "巴罗萨谷", "老藤西拉"],
        "source": "WSET/Barossa Grape & Wine Association",
        "data_confidence": "official",
        "summary": "澳大利亚最著名的葡萄酒产区，世界老藤西拉宝库，1840年代的活化石葡萄园。",
        "content_body": """## 地理与气候

### 位置
- 南澳大利亚州阿德莱德以北约60公里
- 巴罗萨谷与伊甸谷组成巴罗萨区域
- 谷底海拔200-300米

### 气候
- 地中海-大陆性混合
- 夏季炎热干燥（35°C+）
- 冬季温和湿润
- 昼夜温差中等
- 干燥少病，无需农药

### 土壤
- 多样：红棕壤、沙土、黏土、砾石
- **Barossa Valley**：谷底冲积壤土
- **Eden Valley**：高海拔砂质片岩
- 老藤多在贫瘠沙土，幸免于根瘤蚜

## 子产区

### 巴罗萨谷 Barossa Valley
- 谷底，温暖
- 老藤西拉核心
- 子区域：Nuriootpa、Tanunda、Angaston

### 伊甸谷 Eden Valley
- 东部高海拔（400-500米）
- 凉爽，雷司令优质
- 伊甸堡 sub-GI更高

### 高山区 High Eden
- Eden Valley最高处
- 凉爽，细致

## 主要品种

### 红品种
- **西拉 Shiraz**：旗舰
  - 1840年代老藤幸存
  - 浓郁黑莓、黑胡椒、辛香
  - 酒体饱满，单宁柔和
- **歌海娜**：老藤GSM混酿
- **慕合怀特（Mourvèdre/Mataro）**：GSM第三
- **赤霞珠**：辅助

### 白品种
- **雷司令**：Eden Valley旗舰
  - 干型，高酸，柑橘
  - 陈年能力强
- **赛美蓉**：少量
- **霞多丽**：少量

## 老藤分级体系

| 等级 | 树龄 | 称谓 |
|------|------|------|
| Old Vine | ≥35年 | 老藤 |
| Survivor Vine | ≥70年 | 幸存藤 |
| Centenarian Vine | ≥100年 | 百年藤 |
| Ancestor Vine | ≥125年 | 祖藤 |

世界最古老商业化西拉藤（1843年）在巴罗萨

## 历史与特点
- 1842年德国路德派移民建立
- 幸免于根瘤蚜（沙土隔离）
- 多代家族酒庄传承
- "澳大利亚的纳帕"
- 奔富Grange产区之一

## 代表酒庄
- **奔富（Penfolds）**- Grange、Bin 707
- **亨施克（Henschke）**- Hill of Grace
- **托布雷（Torbreck）**- RunRig
- **查尔斯·梅尔顿（Charles Melton）**
- **洛克福三一（Rockford）**- Basket Press
- **圣·哈利特（St Hallett）**""",
    },
    {
        "id": "REGION-au-hunter-valley",
        "category": "ENT",
        "subcategory": "region",
        "title": "猎人谷产区",
        "title_en": "Hunter Valley",
        "name_cn": "猎人谷",
        "name_en": "Hunter Valley",
        "tags": ["产区风土", "澳大利亚", "猎人谷", "赛美蓉"],
        "source": "WSET/Hunter Valley Wine & Tourism Association",
        "data_confidence": "official",
        "summary": "澳大利亚最古老的葡萄酒产区，独特的未嫁接赛美蓉造就世界级陈年白葡萄酒。",
        "content_body": """## 地理与气候

### 位置
- 新南威尔士州，悉尼以北约160公里
- 澳大利亚最古老葡萄酒产区
- 分为下猎人谷与上猎人谷

### 气候
- 亚热带湿润气候（罕见凉爽产区）
- 夏季炎热潮湿
- 降雨分布于全年，收获季风险
- 云层覆盖降低日照
- 短暂成熟期保留高酸

### 土壤
- **下猎人谷**：独特的红色火山壤土
- 含铁氧化物
- 排水良好
- 部分自根葡萄（无根瘤蚜）

## 主要子产区

### 下猎人谷 Lower Hunter
- 核心产区
- 三个主要区域：
  - **Pokolbin**：中心，主要葡萄园
  - **Mount View**：高海拔
  - **Broekera**：北部

### 上猎人谷 Upper Hunter
- 内陆更温暖
- 霞多丽、赛美蓉
- 较大规模生产

## 主要品种

### 白品种
- **赛美蓉 Semillon**：旗舰
  - 澳大利亚独有风格
  - 采摘早，低酒精度（10-11%）
  - 高酸，无橡木
  - 年轻时清淡，陈年后丰富
  - 蜂蜡、烤面包、蜂蜜香气
  - 陈年潜力50+年
- **霞多丽**：辅助
- **Verdelho**：传统白
- **雷司令**：少量

### 红品种
- **西拉**：旗舰红
  - 中等酒体
  - 黑莓、黑胡椒
- **赤霞珠**：辅助
- **黑皮诺**：少量

## 猎人谷赛美蓉特色
- 世界独一无二风格
- 早期采摘（糖度低）
- 不锈钢罐发酵
- 无苹果酸-乳酸
- 无橡木陈年
- 早装瓶
- 陈年发展惊人复杂性
- "澳大利亚的布朗兄弟"

## 历史与发展
- 1820年代葡萄种植
- 1825年第一棵葡萄藤
- 澳大利亚最古老产区
- 根瘤蚜未侵入
- 自根葡萄幸存
- 旅游与酒庄结合典范

## 代表酒庄
- **泰瑞尔（Tyrrell's）**- Vat 1 Semillon标杆
- **麦克威廉（McWilliam's）**- Lovedale Semillon
- **布鲁克（Brokenwood）**- Graveyard Shiraz
- **奥德托（Audrey Wilkinson）**
- **林德曼（Lindeman's）**- 创立于此
- **罗克福德（Mount Pleasant）**""",
    },
    {
        "id": "REGION-nz-marlborough",
        "category": "ENT",
        "subcategory": "region",
        "title": "马尔堡产区",
        "title_en": "Marlborough",
        "name_cn": "马尔堡",
        "name_en": "Marlborough",
        "tags": ["产区风土", "新西兰", "马尔堡", "长相思"],
        "source": "WSET/Marlborough Wine",
        "data_confidence": "official",
        "summary": "新西兰最大葡萄酒产区，长相思之都，1973年起步成为全球长相思标杆。",
        "content_body": """## 地理与气候

### 位置
- 新西兰南岛东北端
- 维拉河与阿沃特雷河谷平原
- 南纬41°，世界最南葡萄酒产区之一

### 气候
- 凉爽海洋性气候
- 太平洋影响，夏季凉爽
- 日照极长（年2400小时）
- 昼夜温差大
- 成熟缓慢，酸度保留
- 干燥，少病害

### 土壤
- 维拉河冲积砾石壤土
- 阿沃特雷河砂质壤土
- 排水极佳
- 不同子区域差异显著
- 矿物质丰富

## 子产区

### 南谷 Southern Valleys
- Waihopai、Omaka等
- 较温暖
- 长相思丰满

### 维拉河 Wairau Valley
- 核心产区
- 冲积平原
- 长相思主力

### 阿沃特雷 Awatere Valley
- 南部更凉爽
- 矿物感更强
- 高酸度

### 凯尔库迪 Kekerengu
- 海岸带
- 极凉爽

## 主要品种

### 白品种
- **长相思 Sauvignon Blanc**：绝对主力，80%+
  - 百香果、西番莲、黑加仑叶
  - 草本、番茄叶
  - 高酸，强烈芳香
  - 新西兰旗舰品种
- **霞多丽**：辅助
- **灰皮诺 Pinot Gris**：增长
- **雷司令**：少量
- **琼瑶浆**：少量

### 红品种
- **黑皮诺**：第二主力
  - 凉爽气候风格
  - 红色莓果、香料
- **黑皮诺**占新西兰黑皮诺产量大半

## 长相思风格
- **经典**：不锈钢罐低温发酵，年轻果味
- **橡木影响**：部分酒桶发酵/陈年
- **野生酵母**：复杂度更高
- **有机/生物动力**：风土表达
- 不同子产区风格差异明显

## 历史与奇迹
- 1973年Montana（现Brancott Estate）首次商业种植
- 1979年首款商业长相思
- 1980年代Cloudy Bay引爆国际市场
- 1990年代爆发式增长
- 短期内成为全球长相思标杆

## 代表酒庄
- **云湾（Cloudy Bay）**- 长相思标杆
- **布兰卡特（Brancott Estate）**- 先驱
- **维拉河（Wairau River）**
- **德意志（Dog Point）**- 自然派
- **费尔顿路（Felton Road的姐妹）**
- **Clos Marguerite**""",
    },
    {
        "id": "REGION-ar-mendoza",
        "category": "ENT",
        "subcategory": "region",
        "title": "门多萨产区",
        "title_en": "Mendoza",
        "name_cn": "门多萨",
        "name_en": "Mendoza",
        "tags": ["产区风土", "阿根廷", "门多萨", "马尔贝克", "高海拔"],
        "source": "WSET/Wines of Argentina",
        "data_confidence": "official",
        "summary": "阿根廷最重要的葡萄酒产区，马尔贝克的家园，安第斯山高海拔造就浓郁风味。",
        "content_body": """## 地理与气候

### 位置
- 阿根廷西部，安第斯山脉东麓
- 门多萨省
- 占阿根廷葡萄酒产量70%+
- 北纬33°，南半球核心产区

### 气候
- 大陆性干旱气候
- 高海拔调节温度
- 年日照300天+
- 年降雨200mm，全靠融雪灌溉
- 干燥无病，有机潜力大
- 昼夜温差大（15-20°C）

### 土壤
- 安第斯山冲积土
- 砂砾、黏土、石灰岩
- 排水极佳
- 矿物质丰富
- 不同海拔土壤差异

## 子产区（GI）

### Luján de Cuyo
- 海拔800-1100米
- 马尔贝克传统核心
- 顶级老藤

### Maipú
- 历史悠久
- 老酒庄聚集

### Uco Valley（图蓬加托Tupungato等）
- 海拔1000-1500米
- 凉爽，酸度高
- 新派高端核心
- 三个子区域：Tupungato、Tunuyán、San Carlos

### San Rafael
- 南部较温暖

## 主要品种

### 红品种
- **马尔贝克 Malbec**：旗舰
  - 颜色深紫
  - 黑莓、紫罗兰、李子
  - 单宁柔和，酒体饱满
  - 高海拔花青素丰富
- **赤霞珠**：辅助
- **伯纳达 Bonarda**：阿根廷第二红
- **西拉**：高海拔风格
- **坦普兰尼洛**：少量
- **品丽珠**：辅助

### 白品种
- **Torrontés**：芳香白
- **霞多丽**：高海拔
- **赛美蓉**：少量

## 高海拔特色
- 海拔600-1500米
- 高海拔紫外线强，皮厚
- 昼夜温差延缓成熟
- 酸度保留，香气复杂
- Uco Valley 1500米+为极境

## 灌溉传统
- 安第斯山融雪水
- 传统洪水灌溉
- 现代滴灌推广
- 干旱控制产量

## 历史与发展
- 16世纪西班牙传教士引入
- 19世纪欧洲移民带来马尔贝克
- 1853年法国农学家Pouget引入马尔贝克
- 1990年代出口爆发
- 马尔贝克成为阿根廷名片

## 代表酒庄
- **卡氏家族（Bodega Catena Zapata）**- 阿根廷酒王
- **诺顿（Bodega Norton）**
- **蔡普（Zuccardi）**- 单一园先锋
- **特拉皮切（Trapiche）**
- **路坦（Luigi Bosca）**
- **富内斯（Achaval-Ferrer）**""",
    },
    {
        "id": "REGION-cl-maipo",
        "category": "ENT",
        "subcategory": "region",
        "title": "迈坡产区",
        "title_en": "Maipo Valley",
        "name_cn": "迈坡",
        "name_en": "Maipo Valley",
        "tags": ["产区风土", "智利", "迈坡", "赤霞珠", "安第斯山"],
        "source": "WSET/Wines of Chile",
        "data_confidence": "official",
        "summary": "智利最古老的葡萄酒产区，"智利的波尔多"，赤霞珠与安第斯山融雪水的经典组合。",
        "content_body": """## 地理与气候

### 位置
- 智利中部，围绕圣地亚哥
- 迈坡河流域
- 安第斯山脉西麓
- 南纬33°

### 气候
- 地中海气候
- 夏季干燥温暖
- 冬季温和湿润
- 安第斯山冷风夜间下沉
- 昼夜温差大
- 干燥少病

### 土壤
- 安第斯山冲积土
- 砾石、沙壤土
- 排水良好
- 含丰富矿物质
- 不同子区域土壤差异

## 子产区

### Alto Maipo（上迈坡）
- 安第斯山脚
- 海拔600-800米
- 砾石土壤
- 顶级赤霞珠
- 冷凉气流

### Central Maipo（中迈坡）
- 平原
- 冲积壤土
- 历史产区

### Pacific Maipo（太平洋迈坡）
- 西部近海
- 受海洋影响
- 较凉爽

## 主要品种

### 红品种
- **赤霞珠 Cabernet Sauvignon**：旗舰
  - 安第斯山风格
  - 黑加仑、薄荷、桉树
  - 单宁紧实，结构强
- **佳美娜 Carménère**：智利特色
  - 波尔多原品种，智利幸存
  - 胡椒、红色浆果
  - 晚熟，需温暖长季
- **美乐**：辅助
- **西拉**：新兴
- **马尔贝克**：少量

### 白品种
- **霞多丽**：少量
- **长相思**：凉爽区

## 智利特色
- **天然隔离**：北部沙漠、西海岸海洋、东安第斯、南巴塔哥尼亚
- 无根瘤蚜，自根葡萄
- 干燥气候，有机潜力大
- 安第斯山融雪灌溉

## 历史与发展
- 1548年西班牙传教士引入
- 19世纪欧洲移民带来波尔多品种
- Don Silvestre Ochagavía（1851）引入法国品种
- 19世纪后期Concha y Toro等大酒厂建立
- 1980-90年代出口爆发

## 代表酒庄
- **干露酒庄（Concha y Toro）**- 智利最大，Don Melchor
- **桑塔丽塔（Santa Rita）**- Casa Real
- **圣佩德罗（San Pedro）**
- **塔拉巴（Santa Carolina）**
- **阿尔瓦维（Almaviva）**- 木桐与干露合作
- **佩拉尔（Pérez Cruz）**""",
    },
    {
        "id": "REGION-cl-casablanca",
        "category": "ENT",
        "subcategory": "region",
        "title": "卡萨布兰卡谷产区",
        "title_en": "Casablanca Valley",
        "name_cn": "卡萨布兰卡谷",
        "name_en": "Casablanca Valley",
        "tags": ["产区风土", "智利", "卡萨布兰卡", "黑皮诺", "霞多丽", "冷凉"],
        "source": "WSET/Wines of Chile",
        "data_confidence": "official",
        "summary": "智利冷凉产区代表，太平洋海风塑造的黑皮诺与霞多丽优质产区。",
        "content_body": """## 地理与气候

### 位置
- 智利中部海岸山脉西侧
- 圣地亚哥西北约75公里
- 太平洋沿岸
- 海拔200-400米

### 气候
- 冷凉海洋性气候
- 太平洋冷洪堡海流影响
- 晨雾（camanchaca）遮蔽阳光
- 海风下午穿透
- 夏季最高25°C
- 成熟缓慢，酸度保留

### 土壤
- 花岗岩、红色黏土
- 海洋沉积岩
- 排水良好
- 矿物质丰富
- 部分沙质

## 子产区

### 卡萨布兰卡谷整体
- 海岸山脉东麓
- 1980年代开发

### 邻近 San Antonio & Leyda
- 更近海
- 更冷凉
- 黑皮诺、长相思、霞多丽
- 智利最酷产区之一

## 主要品种

### 白品种
- **霞多丽 Chardonnay**：旗舰白
  - 矿物、柑橘、白桃
  - 高酸，橡木可控
- **长相思 Sauvignon Blanc**：增长
  - 草本、柑橘、矿物
- **雷司令**：少量试验
- **琼瑶浆**：少量

### 红品种
- **黑皮诺 Pinot Noir**：旗舰红
  - 红色莓果、香料
  - 凉爽气候风格
  - 智利最佳黑皮诺产区
- **西拉**：冷凉风格
- **美乐**：少量

## 冷凉产区特点
- 与阿根廷门多萨炎热形成对比
- 太平洋影响关键
- 晨雾延缓成熟
- 海风保持酸度
- 适合勃艮第品种

## 历史与发展
- 1982年Pablo Morandé首次种植
- 海岸山脉新产区开拓
- 1990年代快速发展
- 智利冷凉产区代表
- 高端黑皮诺、霞多丽标杆

## 酿造风格
- 强调矿物感与酸度
- 橡木使用克制
- 不锈钢罐低温发酵
- 单一园概念兴起
- 有机、生物动力法推广

## 代表酒庄
- **比库尼亚（Viña Morandé）**- 先驱
- **卡萨布兰卡酒庄（Viña Casablanca）**
- **拉索特（Veramonte）**
- **雷伊达（Leyda）**- San Antonio标杆
- **孟德斯（Montes）**- Outer Limits
- **马蒂尔（Matetic）**- 生物动力法""",
    },
    {
        "id": "REGION-jp-yamazaki",
        "category": "ENT",
        "subcategory": "region",
        "title": "山崎/白州威士忌产区",
        "title_en": "Yamazaki & Hakushu",
        "name_cn": "山崎/白州",
        "name_en": "Yamazaki & Hakushu",
        "tags": ["产区风土", "日本", "山崎", "白州", "威士忌"],
        "source": "三得利官方资料",
        "data_confidence": "official",
        "summary": "日本威士忌两大旗舰蒸馏所，山崎的柔和细腻与白州的森林清新并称双璧。",
        "content_body": """## 地理与气候

### 山崎蒸馏所 Yamazaki Distillery
- 京都府大山崎町
- 桂川、宇治川、木津川三川汇流
- 海拔约50米
- 湿润温和气候
- 雾气丰富，适合陈年

### 白州蒸馏所 Hakushu Distillery
- 山梨县北杜市
- 甲斐驹岳山麓
- 海拔约700米
- 日本最高的威士忌蒸馏所
- 森林环绕，凉爽清新

## 山崎蒸馏所

### 历史
- 1923年鸟井信治郎创立
- 日本第一座麦芽威士忌蒸馏所
- 首任酿酒师：竹鹤政孝（后创立Nikka）
- 1984年山崎单一麦芽威士忌上市

### 设备特点
- 不同形状铜壶蒸馏器（直颈、灯笼颈等）
- 木桶发酵槽（日本罕见）
- 多样原酒风格
- 不同橡木桶组合

### 风格
- 柔和细腻
- 花果香明显
- 水楢桶（Mizunara）使用
- 复杂平衡

## 白州蒸馏所

### 历史
- 1973年三得利建立
- 山崎50年后第二蒸馏所
- 海拔700米森林环境

### 设备特点
- 直火加热蒸馏器
- 不同蒸馏器组合
- 木桶发酵
- 森林微气候

### 风格
- 清新薄荷、森林气息
- 轻盈优雅
- 高酸度
- "森林蒸馏所"

## 日本威士忌特色
- **水楢橡木 Mizunara Oak**
  - 日本国产橡木
  - 香气：檀香、寺庙香
  - 透气性高，难加工
  - 长期陈年开发独特香气
- **柔和水质**：花岗岩过滤
- **精确工艺**：日本匠人精神
- **多样木桶**：波本、雪利、水楢

## 主要产品
- 山崎12年、18年、25年
- 白州12年、18年、25年
- 响 Hibiki（调和）：山崎+白州+知多
- 限量单桶

## 国际荣誉
- 2003年山崎12年获ISC金奖
- 2015年山崎Sherry Cask 2013获WWA世界最佳
- 日威价格全球飙升

## 代表产品
- 山崎18年、25年
- 白州18年、25年
- 响21年、30年
- 限量单桶Release""",
    },
    {
        "id": "REGION-jp-hokkaido",
        "category": "ENT",
        "subcategory": "region",
        "title": "北海道产区",
        "title_en": "Hokkaido",
        "name_cn": "北海道",
        "name_en": "Hokkaido",
        "tags": ["产区风土", "日本", "北海道", "清酒", "葡萄酒"],
        "source": "北海道葡萄酒协会",
        "data_confidence": "official",
        "summary": "日本最北端的葡萄酒与清酒产区，极寒气候与纯净水源造就清新精致风格。",
        "content_body": """## 地理与气候

### 位置
- 日本最北端岛屿
- 北纬41-45°
- 与欧洲北部产区纬度相近

### 气候
- 寒带-亚寒带湿润大陆性气候
- 冬季严寒漫长（-10°C至-20°C）
- 夏季凉爽短促
- 年日照1800-2000小时
- 昼夜温差大
- 干燥少湿，病害少

### 土壤
- 火山灰土（黒ポク土）
- 冲积壤土
- 含丰富矿物质
- 排水良好

## 子产区与特色

### 余市町（Yoichi）
- 日本葡萄酒先驱
- 北纬43°
- 海洋影响
- 北海道葡萄酒株式会社本部

### 富良野（Furano）
- 内陆盆地
- 昼夜温差极大
- 多品种试验

### 十胜（Tokachi）
- 大平原
- 冷凉气候
- 抗寒品种

### 池田町（Ikeda）
- 北海道葡萄酒起源地
- 1876年尝试酿酒
- 北海道葡萄酒（株）发源地

## 主要品种

### 葡萄品种
- **山葡萄 Vitis coignetiae**（Yamabudo）：本地野生
- **北海道Zweigelt**：抗寒红
- **清见（Kiyomi）**：本地杂交
- **Kerner**：德国抗寒白
- **Müller-Thurgau**：白
- **雷司令**：少量
- **山幸（Yamatosaku）**：北海道育成
- **清舞（Kiyomai）**：北海道育成抗寒

### 清酒米
- **山田锦、五百万石**：从外地调入
- **吟風 Ginpusaku**：北海道育成酒米
- 火山灰土培育酒米

## 北海道清酒特色
- 极寒气候保留酸度
- 纯净雪融水酿造
- 清新淡丽风格
- "吟酿王国"地位
- 高端纯米大吟酿聚集

## 北海道葡萄酒特色
- 抗寒品种与本地杂交
- 山葡萄独特风味
- 凉爽气候酸度好
- 白葡萄酒清新
- 红葡萄酒轻盈

## 历史与发展
- 1876年北海道开拓使尝试酿酒
- 1900年代初期酒米种植
- 1970年代现代葡萄酒业起步
- 2000年代精品酒庄兴起
- 国际比赛获奖增多

## 代表酒庄与酒造
- **北海道葡萄酒（株）**- 余市
- **十胜葡萄酒（株）**
- **富良野葡萄酒（株）**
- **国稀酒造（Kunimare）**- 清酒
- **男山（Otokoyama）**- 旭川，清酒
- **上川大雪（Kamikawa Taisetsu）**- 清酒""",
    },
    {
        "id": "REGION-uk-islay",
        "category": "ENT",
        "subcategory": "region",
        "title": "艾雷岛产区",
        "title_en": "Islay",
        "name_cn": "艾雷岛",
        "name_en": "Islay",
        "tags": ["产区风土", "苏格兰", "艾雷岛", "泥煤", "威士忌"],
        "source": "WSET/Islay Whisky Academy",
        "data_confidence": "official",
        "summary": "苏格兰威士忌泥煤风格的精神家园，八大蒸馏所聚集的小岛，烟熏威士忌圣地。",
        "content_body": """## 地理与气候

### 位置
- 苏格兰西海岸内赫布里底群岛
- 距格拉斯哥约200公里
- 岛长约40公里，宽约25公里
- "苏格兰威士忌之都"

### 气候
- 温带海洋性气候
- 冬季温和，夏季凉爽
- 多雨多雾，湿度高
- 海盐与海风浸润
- 极利于陈年缓慢蒸发

### 土壤
- 泥炭沼泽（Peat Bog）遍布
- 海岸带海带富集
- 花岗岩基底
- 不同区域泥炭特性差异

## 八大蒸馏所

| 蒸馏所 | 成立 | 风格 | 特点 |
|--------|------|------|------|
| Ardbeg | 1815 | 重泥煤 | 烟熏极致，阿贝十 |
| Laphroaig | 1815 | 重泥煤 | 药用碘酒，最 divisive |
| Lagavulin | 1816 | 重泥煤 | 优雅复杂，16年经典 |
| Bowmore | 1779 | 中泥煤 | 平衡，最古老 |
| Caol Ila | 1846 | 中泥煤 | 轻烟熏，轻盈 |
| Bunnahabhain | 1881 | 轻泥煤 | 轻柔，未泥煤 |
| Bruichladdich | 1881 | 轻泥煤 | 多元，自然派 |
| Kilchoman | 2005 | 重泥煤 | 农场蒸馏所，新派 |

## 风格区域

### 南部"三巨头"（Kildalton Cross）
- Ardbeg、Laphroaig、Lagavulin
- 重泥煤风格
- 海岸带强力海风
- 烟熏、海盐、药用

### 北部
- Bunnahabhain、Bruichladdich、Caol Ila
- 较轻泥煤
- 更优雅花果
- 部分未泥煤版本

### 中部
- Bowmore
- 平衡风格
- 烟熏与果香并重

### 西部
- Kilchoman
- 新派农场风格
- 大麦自种
- 重泥煤

## 泥煤工艺

### 泥煤来源
- 艾雷岛沼泽
- 石炭植物千年累积
- 含苯酚等化合物

### 泥煤烘烤
- 烘干麦芽时燃烧泥煤
- 烟雾附着麦芽
- 酚类化合物（PPM）衡量
- 艾雷岛典型PPM：20-50
- Ardbeg、Laphroaig可达50+

### 风味贡献
- 烟熏、灰烬
- 海藻、海带
- 碘酒、消毒水
- 焦油、皮革
- 海盐、咸鲜

## 历史与地位
- 14世纪起威士忌酿造
- 18世纪走私中心
- 19世纪合法蒸馏所建立
- 苏格兰威士忌产区之一
- 21世纪全球威士忌热潮

## 代表产品
- Ardbeg Ten 10年、Uigeadail
- Laphroaig 10年、Quarter Cask
- Lagavulin 16年、Distiller's Edition
- Bowmore 12年、15年
- Caol Ila 12年、18年
- Bruichladdich Classic Laddie、Octomore
- Kilchoman Machir Bay""",
    },
    {
        "id": "REGION-uk-speyside",
        "category": "ENT",
        "subcategory": "region",
        "title": "斯佩塞产区",
        "title_en": "Speyside",
        "name_cn": "斯佩塞",
        "name_en": "Speyside",
        "tags": ["产区风土", "苏格兰", "斯佩塞", "花果香", "威士忌"],
        "source": "WSET/Malt Whisky Association",
        "data_confidence": "official",
        "summary": "苏格兰威士忌最大产区，半数以上蒸馏所聚集，以花果香优雅风格闻名。",
        "content_body": """## 地理与气候

### 位置
- 苏格兰东北部
- 斯佩河流域（River Spey）
- 横跨Moray、Banffshire、Aberdeenshire
- 东北海岸内陆

### 气候
- 温带海洋性气候
- 比西部岛屿干燥
- 冬季寒冷，夏季温和
- 降雪常见
- 河谷微气候

### 土壤与水源
- 花岗岩基底
- 富含矿物质的泉水
- 斯佩河与支流提供纯净软水
- 不同水源赋予独特风味

## 蒸馏所数量
- 约50+蒸馏所
- 占苏格兰威士忌蒸馏所半数
- 苏格兰威士忌核心
- 产量占60%+

## 主要蒸馏所

| 蒸馏所 | 成立 | 风格 | 特点 |
|--------|------|------|------|
| The Glenlivet | 1824 | 轻盈花果 | 首家合法蒸馏所 |
| Macallan | 1824 | 丰满雪利 | "单一麦芽劳斯莱斯" |
| Glenfiddich | 1887 | 梨香轻盈 | 首推单一麦芽概念 |
| Balvenie | 1892 | 蜂蜜圆润 | 同源Glenfiddich |
| Aberlour | 1879 | 雪利圆润 | 性价比之选 |
| Glen Grant | 1840 | 轻盈苹果 | 意大利畅销 |
| Glenrothes | 1878 | 雪利复杂 | 按年份装瓶 |
| Craigellachie | 1891 | 烟熏硫磺 | 较重风格 |
| Knockando | 1898 | 轻盈花果 | 季节装瓶 |
| Cardhu | 1824 | 轻盈柔和 | Johnnie Walker核心 |

## 风格流派

### 轻盈花果派（主流）
- Glenlivet、Glenfiddich、Balvenie
- 梨、苹果、蜂蜜
- 香草、白花
- 波本桶为主

### 雪利浓郁派
- Macallan、Aberlour、Glenrothes
- 干果、黑巧克力
- 圣诞蛋糕、香料
- 雪利桶陈年

### 中等复杂派
- Glen Grant、Knockando
- 平衡花果与结构
- 优雅易饮

### 烟熏重风格（少数）
- Craigellachie、Aultmore
- 较重麦芽香
- 略带硫磺烟熏

## 酿造特色
- 多数使用蒸馏器Worm tub（虫桶冷凝）
- 蒸馏器形状多样
- 木桶发酵常见
- 水源纯净软水
- 部分蒸馏所自家地板发芽

## 雪利桶传统
- 19世纪雪利酒桶进口
- 西班牙雪利酒运输用桶
- 二手桶陈年威士忌
- Macallan以雪利桶闻名
- 雪利桶溢价显著

## 历史与地位
- 18世纪起威士忌酿造
- 1824年The Glenlivet获首张合法牌照
- 19世纪大规模扩张
- 1960-70年代单一麦芽概念兴起
- Glenfiddich首推单一麦芽营销

## 代表产品
- The Glenlivet 12年、18年、25年
- Macallan 12年Sherry Oak、18年、25年
- Glenfiddich 12年、15年、18年
- Balvenie 12年DoubleWood、17年
- Aberlour 12年、A'bunadh
- Glenrothes Vintage系列""",
    },
]
