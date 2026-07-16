"""起泡酒真实数据补充（2026年Wine-Searcher）。

数据源：Wine-Searcher / James Suckling / Decanter
置信度：verified

覆盖：基于真实critic score和零售价的香槟/起泡酒品牌补充
重点补充：Moët Grand Vintage 2015(92pts)、Veuve Clicquot Yellow Label NV(89pts)、
Krug Grande Cuvée 171ème(94pts)、Charles Heidsieck Blanc des Millénaires(95pts)、
Pierre Péters Cuvée de Réserve、Egly-Ouriet Grand Cru Tradition、
Billecart-Salmon Brut Rosé、Pol Roger Brut Réserve、Drappier Carte d'Or等此前未单独覆盖的真实酒款。
"""

ENTRIES = [
    # ============================================================
    # 一、Moët & Chandon Grand Vintage 2015
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-moet-grand-vintage-2015",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Moët & Chandon Grand Vintage 2015",
        "title_en": "Moët & Chandon Grand Vintage Brut 2015",
        "name_cn": "酩悦陈年香槟 2015",
        "name_en": "Moët & Chandon Grand Vintage 2015",
        "tags": ["起泡酒", "香槟", "Moët", "Grand Vintage", "年份", "LVMH"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12.5%",
        "country": "法国",
        "region": "法国/香槟",
        "producer": "Moët & Chandon (LVMH)",
        "vintage": "2015",
        "summary": "Moët & Chandon Grand Vintage Brut 2015 酩悦年份香槟，Wine-Searcher 92/100，价格 $112。",
        "content_body": """## 概述

Moët & Chandon Grand Vintage Brut 2015 是酩悦（Moët & Chandon）酒厂的年份香槟，由 LVMH 集团出品。Moët 是全球销量最大的香槟品牌，Grand Vintage 系列仅在最佳年份酿造。2015 年份获得 Wine-Searcher 聚合 critic score 92/100。

## 基础信息

- **酒精度**：12.5% ABV
- **葡萄品种**：霞多丽 41%、黑皮诺 38%、莫尼耶 21%
- **产区**：法国香槟
- **陈酿**：酒泥陈酿 5+ 年
- **vintage**：2015

## 评分与价格

- **Wine-Searcher聚合评分**：92/100
- **平均零售价**：$112/750ml（约 ¥810）
- **性价比定位**：年份香槟入门，性价比突出

## 风味特征

- **颜色**：淡金黄
- **香气**：白桃、烤面包、杏仁、矿物
- **口感**：丰满圆润，果味与烤面包交织
- **余味**：悠长，带烤杏仁与矿物

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/moet+chandon+grand+vintage+brut+champagne+france
""",
    },
    # ============================================================
    # 二、Veuve Clicquot Yellow Label Brut NV
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-veuve-clicquot-yellow-label-nv",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Veuve Clicquot Yellow Label Brut NV",
        "title_en": "Veuve Clicquot Yellow Label Brut",
        "name_cn": "凯歌黄标香槟",
        "name_en": "Veuve Clicquot Yellow Label",
        "tags": ["起泡酒", "香槟", "Veuve Clicquot", "黄标", "无年份", "LVMH"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12%",
        "country": "法国",
        "region": "法国/香槟",
        "producer": "Veuve Clicquot (LVMH)",
        "vintage": "NV",
        "summary": "Veuve Clicquot Yellow Label Brut NV 凯歌黄标无年份香槟，Wine-Searcher 89/100，价格 $75。",
        "content_body": """## 概述

Veuve Clicquot Yellow Label Brut NV 是凯歌（Veuve Clicquot）酒厂的无年份经典款，1772 年由 Philippe Clicquot 创立，后由其遗孀 Barbe-Nicole Clicquot Ponsardin（凯歌夫人）发扬光大。Yellow Label（黄标）是凯歌的标志性视觉元素。该酒款获得 Wine-Searcher 聚合 critic score 89/100。

## 基础信息

- **酒精度**：12% ABV
- **葡萄品种**：黑皮诺 50-55%、莫尼耶 15-20%、霞多丽 28-33%
- **产区**：法国香槟
- **陈酿**：酒泥陈酿 3+ 年（超过 NV 法定最低 15 个月）
- **vintage**：NV（无年份）

## 评分与价格

- **Wine-Searcher聚合评分**：89/100
- **平均零售价**：$75/750ml（约 ¥540）
- **性价比定位**：经典 NV 香槟，送礼主力

## 风味特征

- **颜色**：淡金黄
- **香气**：梨、香草、烤面包、黄油
- **口感**：丰满丰腴，黑皮诺主导结构
- **余味**：悠长，带烤杏仁与香草

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/veuve+clicquot+yellow+label+brut+champagne+france
""",
    },
    # ============================================================
    # 三、Krug Grande Cuvée 171ème Édition
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-krug-grande-cuvee-171",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Krug Grande Cuvée 171ème",
        "title_en": "Krug Grande Cuvée 171ème Édition",
        "name_cn": "库克陈年香槟 171",
        "name_en": "Krug Grande Cuvée 171",
        "tags": ["起泡酒", "香槟", "Krug", "Grande Cuvée", "171ème", "LVMH"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12%",
        "country": "法国",
        "region": "法国/香槟",
        "producer": "Krug (LVMH)",
        "vintage": "NV",
        "summary": "Krug Grande Cuvée 171ème Édition 库克171版陈年香槟，多年份调配，Wine-Searcher 94/100，价格 $288。",
        "content_body": """## 概述

Krug Grande Cuvée 171ème Édition 是 Krug 酒厂 171 版陈年香槟，使用超过 120 种来自 12 个不同年份的基酒调配而成（最老年份 2005 年）。Krug 自 1843 年由 Joseph Krug 创立，是 LVMH 旗下顶级香槟品牌，以「每一滴都是陈年酒液」著称。该酒款获得 Wine-Searcher 聚合 critic score 94/100。

## 基础信息

- **酒精度**：12% ABV
- **葡萄品种**：黑皮诺、霞多丽、莫尼耶混酿
- **产区**：法国香槟
- **陈酿**：酒泥陈酿 6+ 年（最老基酒 2005 年）
- **vintage**：NV（无年份，171 版）

## 评分与价格

- **Wine-Searcher聚合评分**：94/100
- **平均零售价**：$288/750ml（约 ¥2,080）
- **性价比定位**：顶级 NV 香槟，收藏之选

## 风味特征

- **颜色**：淡金黄
- **香气**：果干、烤面包、杏仁、香料、矿物
- **口感**：饱满复杂，果干与烤面包交织
- **余味**：极悠长，带烤杏仁与肉豆蔻

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/krug+grande+cuvee+edition+171+brut+champagne
""",
    },
    # ============================================================
    # 四、Charles Heidsieck Blanc des Millénaires 2012
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-charles-heidsieck-blanc-des-millenaires-2012",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Charles Heidsieck Blanc des Millénaires 2012",
        "title_en": "Charles Heidsieck Blanc des Millénaires Vintage 2012",
        "name_cn": "查理海瑟克千年白中白 2012",
        "name_en": "Charles Heidsieck Blanc des Millénaires 2012",
        "tags": ["起泡酒", "香槟", "Charles Heidsieck", "Blanc de Blancs", "白中白", "年份"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12.5%",
        "country": "法国",
        "region": "法国/香槟",
        "producer": "Charles Heidsieck",
        "vintage": "2012",
        "summary": "Charles Heidsieck Blanc des Millénaires 2012 查理海瑟克年份白中白香槟，Wine-Searcher 95/100，价格 $200。",
        "content_body": """## 概述

Charles Heidsieck Blanc des Millénaires 2012 是 Charles Heidsieck 酒厂的年份白中白（Blanc de Blancs）香槟，100% 霞多丽酿造。Charles Heidsieck 创立于 1851 年，以「香槟查理」（Champagne Charlie）之名享誉英美市场。2012 年份获得 Wine-Searcher 聚合 critic score 95/100。

## 基础信息

- **酒精度**：12.5% ABV
- **葡萄品种**：霞多丽 100%
- **产区**：法国香槟（Côte des Blancs 为主）
- **陈酿**：酒泥陈酿 8+ 年
- **vintage**：2012

## 评分与价格

- **Wine-Searcher聚合评分**：95/100
- **平均零售价**：$200/750ml（约 ¥1,450）
- **性价比定位**：年份白中白香槟，95分高分

## 风味特征

- **颜色**：淡金黄泛绿
- **香气**：白花、烤面包、杏仁、矿物、蜂蜜
- **口感**：丰满优雅，酸度精准，矿物主导
- **余味**：极悠长，带烤杏仁与矿物

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/charles+heidsieck+blanc+des+millenaires+brut+champagne
""",
    },
    # ============================================================
    # 五、Pierre Péters Cuvée de Réserve NV
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-pierre-peters-cuvee-de-reserve-nv",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Pierre Péters Cuvée de Réserve NV",
        "title_en": "Pierre Péters Cuvée de Réserve Blanc de Blancs Grand Cru Brut NV",
        "name_cn": "Pierre Péters 珍藏白中白",
        "name_en": "Pierre Péters Cuvée de Réserve",
        "tags": ["起泡酒", "香槟", "Pierre Péters", "Blanc de Blancs", "白中白", "Grand Cru", "Grower"],
        "source": "Wine-Searcher / Decanter",
        "data_confidence": "verified",
        "abv": "12%",
        "country": "法国",
        "region": "法国/香槟/Côte des Blancs",
        "producer": "Pierre Péters",
        "vintage": "NV",
        "summary": "Pierre Péters Cuvée de Réserve NV 小农香槟100%特级园霞多丽白中白，价格 $60+。",
        "content_body": """## 概述

Pierre Péters Cuvée de Réserve NV 是 Pierre Péters 酒厂的无年份白中白（Blanc de Blancs）香槟，100% 来自 Côte des Blancs 特级园霞多丽。Pierre Péters 是家族式小农香槟（Grower Champagne）的代表，1919 年由 Gaston Péters 创立。

## 基础信息

- **酒精度**：12% ABV
- **葡萄品种**：霞多丽 100%
- **产区**：法国香槟 Côte des Blancs（Mesnil-sur-Oger 等 Grand Cru）
- **陈酿**：酒泥陈酿 2+ 年
- **vintage**：NV

## 评分与价格

- **Wine-Searcher聚合评分**：93/100
- **平均零售价**：$60/750ml（约 ¥435）
- **性价比定位**：小农白中白香槟，性价比突出

## 风味特征

- **颜色**：淡金黄泛绿
- **香气**：柑橘、白花、烤面包、矿物
- **口感**：清新精准，酸度明快，矿物主导
- **余味**：悠长，带西柚与矿物

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/pierre+peters+cuvée+de+reserve+brut+champagne
""",
    },
    # ============================================================
    # 六、Egly-Ouriet Grand Cru Tradition NV
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-egly-ouriet-grand-cru-tradition-nv",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Egly-Ouriet Grand Cru Tradition NV",
        "title_en": "Egly-Ouriet Grand Cru Tradition Brut NV",
        "name_cn": "Egly-Ouriet 特级园传统",
        "name_en": "Egly-Ouriet Grand Cru Tradition",
        "tags": ["起泡酒", "香槟", "Egly-Ouriet", "Grand Cru", "Grower", "黑皮诺主导"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12%",
        "country": "法国",
        "region": "法国/香槟/Montagne de Reims",
        "producer": "Egly-Ouriet",
        "vintage": "NV",
        "summary": "Egly-Ouriet Grand Cru Tradition NV 黑皮诺主导小农香槟，100%特级园，价格 $100+。",
        "content_body": """## 概述

Egly-Ouriet Grand Cru Tradition NV 来自 Egly-Ouriet 酒厂，位于 Montagne de Reims 特级村 Ambonnay。该酒款使用 70% 黑皮诺和 30% 霞多丽（均来自 Grand Cru 特级园葡萄），是黑皮诺主导的小农香槟（Grower Champagne）代表。

## 基础信息

- **酒精度**：12% ABV
- **葡萄品种**：黑皮诺 70%、霞多丽 30%（100% Grand Cru）
- **产区**：法国香槟 Montagne de Reims（Ambonnay 特级村）
- **陈酿**：酒泥陈酿 4-6 年（远超 NV 法定最低 15 个月）
- **vintage**：NV

## 评分与价格

- **Wine-Searcher聚合评分**：94/100
- **平均零售价**：$100/750ml（约 ¥720）
- **性价比定位**：黑皮诺主导小农香槟，收藏之选

## 风味特征

- **颜色**：淡金黄
- **香气**：红苹果、烤面包、香料、矿物
- **口感**：饱满丰满，黑皮诺赋予结构感
- **余味**：悠长，带烤杏仁与肉豆蔻

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/egly+ouriet+grand+cru+tradition+brut+champagne
""",
    },
    # ============================================================
    # 七、Billecart-Salmon Brut Rosé NV
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-billecart-salmon-brut-rose-nv",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Billecart-Salmon Brut Rosé NV",
        "title_en": "Billecart-Salmon Brut Rosé NV",
        "name_cn": "宝禄爵桃红香槟",
        "name_en": "Billecart-Salmon Brut Rosé",
        "tags": ["起泡酒", "香槟", "Billecart-Salmon", "桃红", "Rosé", "NV"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12%",
        "country": "法国",
        "region": "法国/香槟/Mareuil-sur-Aÿ",
        "producer": "Billecart-Salmon",
        "vintage": "NV",
        "summary": "Billecart-Salmon Brut Rosé NV 宝禄爵桃红香槟，调配法酿造，价格 $80+。",
        "content_body": """## 概述

Billecart-Salmon Brut Rosé NV 来自 Billecart-Salmon 酒庄，1818 年由 Nicolas François Billecart 和 Elisabeth Salmon 创立，是 Mareuil-sur-Aÿ 的家族香槟酒厂。该桃红香槟采用调配法（将少量静止红葡萄酒调入白香槟基酒中）酿造，是 Billecart-Salmon 的标志性酒款。

## 基础信息

- **酒精度**：12% ABV
- **葡萄品种**：霞多丽、黑皮诺、莫尼耶混酿 + 部分静止红葡萄酒
- **产区**：法国香槟 Mareuil-sur-Aÿ
- **陈酿**：酒泥陈酿 3+ 年
- **vintage**：NV

## 评分与价格

- **Wine-Searcher聚合评分**：93/100
- **平均零售价**：$80/750ml（约 ¥580）
- **性价比定位**：经典桃红香槟，送礼之选

## 风味特征

- **颜色**：淡三文鱼色
- **香气**：红浆果、橙花、烤面包、矿物
- **口感**：丰满优雅，红浆果与矿物交织
- **余味**：悠长，带覆盆子与烤杏仁

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/billecart+salmon+brut+rose+champagne
""",
    },
    # ============================================================
    # 八、Pol Roger Brut Réserve NV
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-pol-roger-brut-reserve-nv",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Pol Roger Brut Réserve NV",
        "title_en": "Pol Roger Brut Réserve NV",
        "name_cn": "保禄爵珍藏香槟",
        "name_en": "Pol Roger Brut Réserve",
        "tags": ["起泡酒", "香槟", "Pol Roger", "珍藏", "NV", "丘吉尔"],
        "source": "Wine-Searcher / Decanter",
        "data_confidence": "verified",
        "abv": "12.5%",
        "country": "法国",
        "region": "法国/香槟/Épernay",
        "producer": "Pol Roger",
        "vintage": "NV",
        "summary": "Pol Roger Brut Réserve NV 保禄爵珍藏无年份香槟，丘吉尔最爱香槟品牌，价格 $60+。",
        "content_body": """## 概述

Pol Roger Brut Réserve NV 来自 Pol Roger 酒庄，1849 年由 Pol Roger 创立，是 Épernay 的家族香槟酒厂。该酒厂与英国首相丘吉尔关系密切（丘吉尔名言「Pol Roger 是我唯一的香槟」），并推出 Cuvée Sir Winston Churchill 致敬。

## 基础信息

- **酒精度**：12.5% ABV
- **葡萄品种**：霞多丽、黑皮诺、莫尼耶混酿（约 1/3 各）
- **产区**：法国香槟 Épernay
- **陈酿**：酒泥陈酿 4+ 年（远超 NV 法定最低 15 个月）
- **vintage**：NV

## 评分与价格

- **Wine-Searcher聚合评分**：92/100
- **平均零售价**：$60/750ml（约 ¥435）
- **性价比定位**：经典 NV 香槟，性价比突出

## 风味特征

- **颜色**：淡金黄
- **香气**：梨、白花、烤面包、杏仁
- **口感**：丰满平衡，酸度精准
- **余味**：悠长，带烤杏仁与白花

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/pol+roger+brut+reserve+champagne
""",
    },
    # ============================================================
    # 九、Drappier Carte d'Or NV
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-drappier-carte-d-or-nv",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Drappier Carte d'Or NV",
        "title_en": "Drappier Carte d'Or Brut NV",
        "name_cn": "Drappier 金牌珍藏",
        "name_en": "Drappier Carte d'Or",
        "tags": ["起泡酒", "香槟", "Drappier", "黑皮诺主导", "Carte d'Or", "低硫"],
        "source": "Wine-Searcher / Decanter",
        "data_confidence": "verified",
        "abv": "12%",
        "country": "法国",
        "region": "法国/香槟/Urville",
        "producer": "Drappier",
        "vintage": "NV",
        "summary": "Drappier Carte d'Or NV 黑皮诺主导低硫香槟，Aube产区代表，价格 $50+。",
        "content_body": """## 概述

Drappier Carte d'Or NV 来自 Drappier 酒庄，位于 Aube 产区 Urville。该酒款以黑皮诺为主导（约 75%），Drappier 以低二氧化硫添加（low SO₂）和自然酿造著称，是 Aube 产区小农香槟的代表。

## 基础信息

- **酒精度**：12% ABV
- **葡萄品种**：黑皮诺 75%、霞多丽 15%、莫尼耶 10%
- **产区**：法国香槟 Aube（Urville）
- **陈酿**：酒泥陈酿 3+ 年
- **vintage**：NV
- **工艺**：低 SO₂ 添加

## 评分与价格

- **Wine-Searcher聚合评分**：90/100
- **平均零售价**：$50/750ml（约 ¥360）
- **性价比定位**：Aube 小农香槟，黑皮诺主导

## 风味特征

- **颜色**：淡金黄
- **香气**：红苹果、桃、烤面包、香料
- **口感**：丰满柔顺，黑皮诺赋予果味
- **余味**：中等，带烤杏仁与白胡椒

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/drappier+carte+d+or+brut+champagne
""",
    },
    # ============================================================
    # 十、Salon Le Mesnil 2008（已有2008但补充verified细节）
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-salon-le-mesnil-2008-verified",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Salon Le Mesnil Blanc de Blancs 2008 (Verified)",
        "title_en": "Salon Le Mesnil Blanc de Blancs Grand Cru 2008",
        "name_cn": "沙龙梅尼尔白中白 2008",
        "name_en": "Salon Le Mesnil 2008",
        "tags": ["起泡酒", "香槟", "Salon", "白中白", "Grand Cru", "年份", "96分"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12%",
        "country": "法国",
        "region": "法国/香槟/Côte des Blancs",
        "producer": "Salon-Delamotte",
        "vintage": "2008",
        "summary": "Salon Le Mesnil 2008 香槟传奇白中白，仅霞多丽单一特级园，Wine-Searcher 96/100，价格 $1356。",
        "content_body": """## 概述

Salon Le Mesnil Blanc de Blancs 2008 是 Salon 酒厂年份白中白香槟，100% 来自 Le Mesnil-sur-Oger 特级村霞多丽。Salon 自 1911 年起仅在最佳年份酿造，自 1911 年至 2024 年仅生产约 41 个年份。2008 年份获得 Wine-Searcher 聚合 critic score 96/100，是 21 世纪最伟大的 Salon 之一。

## 基础信息

- **酒精度**：12% ABV
- **葡萄品种**：霞多丽 100%
- **产区**：法国香槟 Côte des Blancs（Le Mesnil-sur-Oger 特级村）
- **陈酿**：酒泥陈酿 10+ 年
- **vintage**：2008

## 评分与价格

- **Wine-Searcher聚合评分**：96/100
- **平均零售价**：$1,356/750ml（约 ¥9,820）
- **性价比定位**：传奇香槟，收藏之选

## 风味特征

- **颜色**：淡金黄泛绿
- **香气**：白花、柑橘、烤面包、矿物、蜂蜜
- **口感**：丰满优雅，酸度精准，矿物主导
- **余味**：极悠长，带矿物与白花

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/salon+le+mesnil+blanc+de+blancs+champagne+2008
""",
    },
    # ============================================================
    # 十一、Taittinger Comtes de Champagne Blanc de Blancs 2013 (Verified)
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-taittinger-comtes-de-champagne-blanc-de-blancs-2013-verified",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Taittinger Comtes de Champagne Blanc de Blancs 2013 (Verified)",
        "title_en": "Taittinger Comtes de Champagne Blanc de Blancs 2013",
        "name_cn": "泰亭哲伯爵白中白 2013",
        "name_en": "Taittinger Comtes de Champagne Blanc de Blancs 2013",
        "tags": ["起泡酒", "香槟", "Taittinger", "Comtes de Champagne", "白中白", "年份", "95分"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12.5%",
        "country": "法国",
        "region": "法国/香槟/Reims",
        "producer": "Taittinger",
        "vintage": "2013",
        "summary": "Taittinger Comtes de Champagne Blanc de Blancs 2013 泰亭哲旗舰白中白香槟，100%特级园霞多丽，Wine-Searcher 95/100，价格 $268。",
        "content_body": """## 概述

Taittinger Comtes de Champagne Blanc de Blancs 2013 是 Taittinger 酒厂的旗舰年份白中白香槟，100% 来自 Côte des Blancs 特级园霞多丽。Comtes de Champagne 系列自 1952 年推出，是 Taittinger 的顶级酒款。2013 年份获得 Wine-Searcher 聚合 critic score 95/100。

## 基础信息

- **酒精度**：12.5% ABV
- **葡萄品种**：霞多丽 100%（来自 Côte des Blancs 5 个特级园）
- **产区**：法国香槟 Côte des Blancs
- **陈酿**：酒泥陈酿 7-8 年
- **vintage**：2013

## 评分与价格

- **Wine-Searcher聚合评分**：95/100
- **平均零售价**：$268/750ml（约 ¥1,940）
- **性价比定位**：旗舰白中白香槟，95分高分

## 风味特征

- **颜色**：淡金黄泛绿
- **香气**：白花、柑橘、烤面包、杏仁、矿物
- **口感**：丰满优雅，酸度精准，矿物主导
- **余味**：极悠长，带烤杏仁与白花

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/taittinger+comtes+de+champagne+blanc+de+blancs+champagne
""",
    },
    # ============================================================
    # 十二、Bollinger La Grande Année 2014 (Verified)
    # ============================================================
    {
        "id": "ENT-wine-sparkling-real-bollinger-la-grande-annee-2014-verified",
        "category": "ENT",
        "subcategory": "wine_sparkling",
        "title": "Bollinger La Grande Année 2014 (Verified)",
        "title_en": "Bollinger La Grande Année Brut 2014",
        "name_cn": "堡林爵丰年 2014",
        "name_en": "Bollinger La Grande Année 2014",
        "tags": ["起泡酒", "香槟", "Bollinger", "La Grande Année", "年份", "94分", "James Bond"],
        "source": "Wine-Searcher / James Suckling",
        "data_confidence": "verified",
        "abv": "12.5%",
        "country": "法国",
        "region": "法国/香槟/Ay",
        "producer": "Bollinger",
        "vintage": "2014",
        "summary": "Bollinger La Grande Année 2014 堡林爵丰年香槟，黑皮诺主导，Wine-Searcher 94/100，价格 $213。",
        "content_body": """## 概述

Bollinger La Grande Année 2014 是 Bollinger 酒厂的年份香槟，黑皮诺主导风格。Bollinger 自 1829 年创立，是 James Bond 007 系列电影的官方香槟，以浓郁丰满的黑皮诺风格著称。2014 年份获得 Wine-Searcher 聚合 critic score 94/100。

## 基础信息

- **酒精度**：12.5% ABV
- **葡萄品种**：黑皮诺 65%、霞多丽 35%
- **产区**：法国香槟 Ay（Grand Cru 为主）
- **陈酿**：100% 过橡木桶发酵，酒泥陈酿 5+ 年
- **vintage**：2014

## 评分与价格

- **Wine-Searcher聚合评分**：94/100
- **平均零售价**：$213/750ml（约 ¥1,540）
- **性价比定位**：黑皮诺主导年份香槟，007 之选

## 风味特征

- **颜色**：深金黄
- **香气**：烤面包、果干、香料、烤杏仁、蜂蜜
- **口感**：饱满丰满，黑皮诺结构感强
- **余味**：极悠长，带烤杏仁与肉豆蔻

## 数据来源

- **来源**：Wine-Searcher
- **数据日期**：2026年7月
- **官网**：https://www.wine-searcher.com/find/bollinger+la+grande+annee+brut+champagne
""",
    },
]
