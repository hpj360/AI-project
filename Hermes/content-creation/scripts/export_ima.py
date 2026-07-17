#!/usr/bin/env python3
"""Hermes 知识库 → IMA 知识库 导出脚本

两种导出模式：
1. 打包模式（默认，无需凭证）：
   - 将 Markdown 条目按子类分组整理到目录
   - 生成 IMA 友好的目录结构（01_白酒/02_红酒/...）
   - 打包为 ZIP 文件，直接拖入 IMA 客户端即可导入

2. API 模式（需配置 ClientID + APIKey）：
   - 通过 IMA OpenAPI 以笔记方式自动上传到指定知识库
   - 两步流程：notes/import_doc（创建笔记）→ wiki/add_knowledge（加入知识库）
   - 使用笔记方式（media_type=11），无需 COS 签名，稳定高效

IMA 支持的文件格式：.pdf/.doc/.docx/.txt/.wps/.pptx/.xlsx/.md/.json/jpg/jpeg/png
单个文件限制：150MB，普通用户知识库容量 36GB

使用方法：
  # 打包模式（默认）：
  PYTHONPATH=src python3 content-creation/scripts/export_ima.py --package

  # API 上传模式：
  IMA_CLIENT_ID=xxx IMA_API_KEY=xxx IMA_KB_ID=xxx \
  PYTHONPATH=src python3 content-creation/scripts/export_ima.py --upload

  # 指定子类过滤：
  PYTHONPATH=src python3 content-creation/scripts/export_ima.py --package --subcat cocktail,whisky,gin

  # 指定数据置信度过滤：
  PYTHONPATH=src python3 content-creation/scripts/export_ima.py --package --confidence verified,official
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import zipfile
import hashlib
from pathlib import Path
from collections import defaultdict
from urllib.request import Request, urlopen
from urllib.error import HTTPError

SCRIPTS_DIR = Path(__file__).parent
KB_DIR = SCRIPTS_DIR.parent / "knowledge"
OUTPUT_DIR = SCRIPTS_DIR.parent / "ima_export"

# IMA 友好的子类→目录名映射
SUBCAT_DIR_MAP = {
    "cocktail": "01_鸡尾酒",
    "whisky": "02_威士忌",
    "brandy": "03_白兰地",
    "gin": "04_金酒",
    "vodka": "05_伏特加",
    "rum": "06_朗姆酒",
    "tequila": "07_龙舌兰",
    "baijiu": "08_白酒",
    "wine_red": "09_红酒",
    "wine_white": "10_白酒(葡萄)",
    "wine_sparkling": "11_起泡酒",
    "wine_fortified": "12_加强酒",
    "wine_rose": "13_桃红葡萄酒",
    "wine_dessert": "14_甜酒",
    "beer": "15_啤酒",
    "sake": "16_清酒",
    "yellow_wine": "17_黄酒",
    "rice_wine": "18_米酒",
    "fruit_wine": "19_果酒",
    "mead": "20_蜂蜜酒",
    "liqueur": "21_利口酒",
    "other_spirit": "22_其他烈酒",
    "pairing": "23_佐餐搭配",
    "glassware": "24_酒杯指南",
    "grape": "25_葡萄品种",
    "region": "26_产区",
    "process": "27_酿造工艺",
    "aging": "28_陈年指南",
    "trend": "29_行业趋势",
    "guide": "30_品酒指南",
    "law": "31_法规标准",
    "fake": "32_鉴假指南",
    "collect": "33_收藏投资",
    "buying": "34_购买指南",
    "scene": "35_场景推荐",
    "anti": "36_健康提示",
}

IMA_WIKI_API_BASE = "https://ima.qq.com/openapi/wiki/v1"
IMA_NOTE_API_BASE = "https://ima.qq.com/openapi/note/v1"


def clean_markdown_for_ima(md_content: str, subcat: str = "", tags: list[str] | None = None) -> str:
    """将 Hermes 渲染的 Markdown 优化为 IMA 知识库友好格式。

    主要处理：
    1. 移除 YAML front matter（IMA 会自己解析，保留元数据为正文开头）
    2. 移除图片参考链接章节（WikiMedia/Unsplash/Google 图片搜索链接在 IMA 中无效）
    3. 将评分信息保留为表格格式
    4. 移除合规提示（IMA 自带合规提示）
    5. 移除参考资料中的图片搜索链接
    6. 如果 H1 标题是英文，替换为中文标题
    """
    # 先解析元数据
    meta, fm_title, fm_tags = parse_markdown_meta_zh(md_content)
    if not tags:
        tags = fm_tags
    if not subcat:
        subcat = meta.get("subcategory", "")

    lines = md_content.split("\n")
    result_lines = []
    in_front_matter = False
    fm_passed = False
    skip_section = False
    in_image_refs = False
    in_compliance = False
    h1_replaced = False

    for line in lines:
        # 跳过 YAML front matter
        if line.strip() == "---" and not fm_passed:
            if not in_front_matter:
                in_front_matter = True
                continue
            else:
                in_front_matter = False
                fm_passed = True
                continue
        if in_front_matter:
            continue

        # 替换英文 H1 为中文
        if not h1_replaced and line.startswith("# ") and not line.startswith("## "):
            original_h1 = line[2:].strip()
            zh_h1 = get_zh_title_for_ima(original_h1, subcat, tags)
            if zh_h1 != original_h1:
                result_lines.append(f"# {zh_h1}")
                h1_replaced = True
                continue
            else:
                h1_replaced = True

        # 跳过图片参考章节
        if line.startswith("## 图片参考"):
            in_image_refs = True
            continue
        if in_image_refs:
            if line.startswith("## "):
                in_image_refs = False
            else:
                continue

        # 跳过合规信息章节
        if line.startswith("## 合规信息"):
            in_compliance = True
            continue
        if in_compliance:
            if line.startswith("## "):
                in_compliance = False
            else:
                continue

        # 跳过 WikiMedia/Unsplash/Google 图片搜索行
        if "WikiMedia Commons" in line or "Unsplash 图库" in line or "Google 图片" in line:
            continue

        result_lines.append(line)

    # 清理多余空行
    text = "\n".join(result_lines)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text.strip()


def parse_markdown_meta(md_content: str) -> dict:
    """解析 Markdown 的 YAML front matter 元数据。"""
    meta = {}
    if not md_content.startswith("---"):
        return meta

    end_idx = md_content.find("---", 3)
    if end_idx == -1:
        return meta

    fm = md_content[3:end_idx]
    for line in fm.split("\n"):
        line = line.strip()
        if ":" in line and not line.startswith("#"):
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                val = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
            elif val.startswith("{") and val.endswith("}"):
                pass
            meta[key] = val
    return meta


def package_for_ima(
    kb_dir: Path,
    output_dir: Path,
    subcat_filter: set[str] | None = None,
    confidence_filter: set[str] | None = None,
    zip_name: str = "hermes_kb_for_ima.zip",
) -> Path:
    """将知识库 Markdown 文件整理为 IMA 友好的目录结构并打包为 ZIP。"""
    output_dir.mkdir(parents=True, exist_ok=True)
    package_dir = output_dir / "hermes_kb"
    if package_dir.exists():
        import shutil
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)

    # 统计
    stats = defaultdict(int)
    total = 0
    skipped = 0

    md_files = sorted(kb_dir.glob("*.md"))
    for md_path in md_files:
        content = md_path.read_text(encoding="utf-8")
        meta = parse_markdown_meta(content)

        subcat = meta.get("subcategory", "unknown")
        confidence = meta.get("data_confidence", "simulated")

        # 过滤
        if subcat_filter and subcat not in subcat_filter:
            skipped += 1
            continue
        if confidence_filter and confidence not in confidence_filter:
            skipped += 1
            continue

        # 目标目录
        dir_name = SUBCAT_DIR_MAP.get(subcat, f"99_{subcat}")
        target_dir = package_dir / dir_name
        target_dir.mkdir(parents=True, exist_ok=True)

        # 清理并写入（H1 标题自动转为中文）
        _, _, fm_tags = parse_markdown_meta_zh(content)
        cleaned = clean_markdown_for_ima(content, subcat=subcat, tags=fm_tags)
        target_path = target_dir / md_path.name
        target_path.write_text(cleaned, encoding="utf-8")

        stats[subcat] += 1
        total += 1

    # 生成索引文件
    index_lines = [
        "# Hermes 酒类知识库",
        "",
        f"共 **{total}** 条目，按品类分类整理。",
        "",
        "## 目录",
        "",
    ]
    for subcat, count in sorted(stats.items(), key=lambda x: SUBCAT_DIR_MAP.get(x[0], x[0])):
        dir_name = SUBCAT_DIR_MAP.get(subcat, f"99_{subcat}")
        index_lines.append(f"- {dir_name}（{count} 条）")
    index_lines.append("")
    index_lines.append("## 使用说明")
    index_lines.append("")
    index_lines.append("1. 打开 IMA 客户端（ima.qq.com）")
    index_lines.append("2. 创建或选择目标知识库")
    index_lines.append("3. 将本 ZIP 解压后的文件夹拖拽到 IMA 知识库页面")
    index_lines.append("4. IMA 会自动解析所有 Markdown 文件并建立索引")
    index_lines.append("5. 支持按自然语言提问，IMA 会从知识库检索答案并标注出处")
    index_lines.append("")
    index_lines.append(f"导出时间：{__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}")
    (package_dir / "README.md").write_text("\n".join(index_lines), encoding="utf-8")

    # 打包 ZIP
    zip_path = output_dir / zip_name
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for f in sorted(package_dir.rglob("*")):
            if f.is_file():
                arcname = f.relative_to(package_dir)
                zf.write(f, arcname)

    # 打印统计
    print(f"\n{'='*60}")
    print(f"IMA 打包完成")
    print(f"{'='*60}")
    print(f"总条目: {total}")
    print(f"跳过:   {skipped}")
    print(f"子类分布:")
    for subcat, count in sorted(stats.items(), key=lambda x: -x[1]):
        dir_name = SUBCAT_DIR_MAP.get(subcat, f"99_{subcat}")
        print(f"  {dir_name}: {count} 条")
    print(f"\n输出文件: {zip_path}")
    print(f"文件大小: {zip_path.stat().st_size / 1024 / 1024:.2f} MB")
    print(f"\n使用方法:")
    print(f"  1. 解压 {zip_name}")
    print(f"  2. 打开 IMA 客户端，进入知识库")
    print(f"  3. 将 hermes_kb/ 文件夹拖入知识库页面")
    print(f"  4. 等待 IMA 自动解析索引")
    return zip_path


def ima_api_request(endpoint: str, data: dict, client_id: str, api_key: str, base: str = IMA_WIKI_API_BASE, max_retries: int = 5) -> dict:
    """调用 IMA OpenAPI，支持频率限制自动重试退避。"""
    url = f"{base}/{endpoint}"
    body = json.dumps(data, ensure_ascii=False).encode("utf-8")
    last_err = None
    for attempt in range(max_retries):
        req = Request(url, data=body, method="POST")
        req.add_header("Content-Type", "application/json; charset=utf-8")
        req.add_header("ima-openapi-clientid", client_id)
        req.add_header("ima-openapi-apikey", api_key)
        try:
            with urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                if result.get("code") == 200001:
                    wait = 2 ** attempt + 1
                    print(f"频率限制，等待{wait}s...", end=" ", flush=True)
                    time.sleep(wait)
                    continue
                return result
        except HTTPError as e:
            error_body = e.read().decode("utf-8", errors="replace")
            try:
                err_json = json.loads(error_body)
                if err_json.get("code") == 200001:
                    wait = 2 ** attempt + 1
                    print(f"频率限制(403)，等待{wait}s...", end=" ", flush=True)
                    time.sleep(wait)
                    continue
            except json.JSONDecodeError:
                pass
            if attempt < max_retries - 1:
                wait = 2 ** attempt
                time.sleep(wait)
                last_err = RuntimeError(f"IMA API 错误 {e.code}: {error_body}")
                continue
            raise RuntimeError(f"IMA API 错误 {e.code}: {error_body}") from e
    if last_err:
        raise last_err
    return {"code": -1, "msg": "max retries exceeded"}


def extract_title_from_md(cleaned_content: str, fallback: str) -> str:
    """从 Markdown 内容中提取 H1 标题，没有则用 fallback。"""
    for line in cleaned_content.split("\n"):
        line = line.strip()
        if line.startswith("# ") and not line.startswith("## "):
            return line[2:].strip()
    return fallback


# 主流品牌/酒类中英对照表（按出现频次与中文市场通用度整理）
# 涵盖威士忌、白兰地、葡萄酒、啤酒、伏特加、金酒、朗姆酒、龙舌兰等
BRAND_ZH_MAP = {
    # 威士忌 - 苏格兰
    "Macallan": "麦卡伦", "Glenfiddich": "格兰菲迪", "Glenlivet": "格兰威特",
    "Laphroaig": "拉弗格", "Ardbeg": "阿贝", "Lagavulin": "拉加维林",
    "Bowmore": "波摩", "Talisker": "泰斯卡", "Highland Park": "高原骑士",
    "Aberlour": "亚伯乐", "Dalmore": "大摩", "Glenmorangie": "格兰杰",
    "Balvenie": "百富", "Auchentoshan": "欧肯特轩", "Oban": "欧本",
    "Cragganmore": "克拉格摩尔", "Cardhu": "卡杜", "Singleton": "苏格登",
    "Bunnahabhain": "布纳哈本", "Caol Ila": "卡尔里拉", "Bruichladdich": "布赫拉迪",
    "Springbank": "云顶", "Glen Scotia": "格兰帝", "Blair Athol": "布莱尔阿瑟尔",
    "Deanston": "汀思顿", "Glenkinchie": "格兰昆奇", "Clynelish": "克里尼利基",
    "Brora": "布拉尔", "Port Ellen": "波特艾伦", "Rosebank": "罗斯班克",
    "Glen Ord": "格兰奥德", "Teaninich": "提纳尼奇", "Dailuaine": "达尔维尼",
    "Ben Nevis": "本尼维斯", "Tomatin": "汤玛丁", "Speyside": "斯佩塞",
    "Islay": "艾雷岛", "Speyburn": "盛贝本", "Glen Spey": "格兰斯佩",
    "Benriach": "本利亚克", "Benromach": "本罗蒙", "Glenglassaugh": "格兰格拉索",
    "Glendronach": "格兰多纳", "Glenfarclas": "格兰花格", "Glengoyne": "格兰哥尼",
    "Tamdhu": "坦杜", "Longmorn": "朗摩", "Linkwood": "林可伍德",
    "Glenlossie": "格兰洛西", "Mannochmore": "马诺克摩尔", "Craigellachie": "克莱拉奇",
    "Mortlach": "慕赫", "Knockando": "诺坎多", "Strathisla": "斯特拉赛斯拉",
    "AnCnoc": "安诺克", "Royal Lochnagar": "皇家蓝牌", "Balblair": "巴尔布蕾",
    "Old Pulteney": "老富特尼", "Wolfburn": "沃尔本", "Eden Mill": "伊登米勒",
    "Garnheath": "甘尼斯", "Inverleven": "英弗利文", "St. Magdalene": "圣玛格德琳",
    "Roseisle": "罗斯艾尔", "Carsebridge": "卡斯布里奇", "Glenflagler": "格兰法拉",
    "Killyloch": "基里洛赫", "Pittyvaich": "皮蒂维克", "Convalmore": "康瓦尔摩",
    "Imperial": "帝国", "Dumbarton": "邓巴顿", "Aultmore": "奥特摩",
    "Inchgower": "英志高尔", "Glen Elgin": "格兰爱琴", "Benrinnes": "本利尼斯",
    "Craggan": "克拉甘", "Aberfeldy": "亚伯菲迪", "Dewar's": "帝王",
    "Johnnie Walker": "尊尼获加", "J&B": "J&B", "Famous Grouse": "威雀",
    "Chivas": "芝华士", "Ballantine's": "百龄坛", "Cutty Sark": "顺风",
    "Grant's": "格兰", "Teacher's": "教师牌", "Buchanan's": "布坎南",
    "Whyte & Mackay": "怀特麦凯", "William Grant": "威廉格兰", "Monkey Shoulder": "猴子肩膀",
    "Compass Box": "罗盘盒", "John Dewar": "约翰帝王", "Dewars": "帝王",
    # 威士忌 - 爱尔兰
    "Jameson": "尊美醇", "Bushmills": "布什米尔", "Tullamore": "图拉莫尔",
    "Paddy": "派迪", "Redbreast": "红嘴", "Midleton": "米德尔顿",
    "Powers": "帕弗斯", "Green Spot": "绿点", "Yellow Spot": "黄点",
    "Connemara": "康尼马拉", "Teeling": "帝霖", "Kilbeggan": "基尔贝根",
    # 威士忌 - 美国
    "Jack Daniel's": "杰克丹尼", "Jim Beam": "金宾", "Maker's Mark": "美格",
    "Wild Turkey": "野火鸡", "Bulleit": "布利特", "Woodford Reserve": "伍德福德",
    "Four Roses": "四玫瑰", "Evan Williams": "伊万威廉斯", "Old Forester": "老森林人",
    "Blanton's": "布兰顿", "Buffalo Trace": "布法罗足迹", "Pappy Van Winkle": "帕普范温克尔",
    "George Dickel": "乔治迪克尔", "Knob Creek": "诺布溪", "Basil Hayden": "巴西尔海登",
    "Booker's": "布克", "Baker's": "贝克", "Elijah Craig": "以利亚克雷格",
    "Larceny": "拉森尼", "W.L. Weller": "韦勒", "Old Crow": "老乌鸦",
    "Eagle Rare": "鹰牌珍稀", "1792": "1792", "1792 Ridgemont Reserve": "1792 山脊庄园",
    "1792 Small Batch": "1792 小批量", "Henry McKenna": "亨利麦肯纳",
    "Very Old Barton": "老巴顿", "Ancient Age": "古时代", "Ancient Ancient Age": "古时代",
    "Benchmark": "基准", "Old Grand-Dad": "老大爷", "Rebel": "叛军",
    "Ezra Brooks": "以斯拉布鲁克斯", "Old Heaven Hill": "老天堂山",
    "Rittenhouse": "里登豪斯", "Michter's": "米歇尔", "Sazerac": "萨泽拉",
    "Russell": "拉塞尔", "Wild Turkey Rare Breed": "野火鸡珍稀品种",
    "Russell Reserve": "拉塞尔珍藏", "1792 12 Year": "1792 12年",
    # 威士忌 - 日本
    "Yamazaki": "山崎", "Hakushu": "白州", "Hibiki": "响",
    "Nikka": "日果", "Yoichi": "余市", "Miyagikyo": "宫城峡",
    "Taketsuru": "竹鹤", "Mars": "火星", "Ichiro": "一郎",
    "Chichibu": "秩父", "Kavalan": "噶玛兰", "Suntory": "三得利",
    # 威士忌 - 加拿大/其他
    "Canadian Club": "加拿大俱乐部", "Crown Royal": "皇冠", "Alberta Premium": "阿尔伯塔至尊",
    "Forty Creek": "四十溪", "Lot 40": "40号", "Wiser's": "怀瑟",
    "Glen Breton": "格兰布雷顿", "Kornog": "科诺格", "Armorik": "阿莫里克",
    "Kavalan Solist": "噶玛兰独奏", "Paul John": "保罗约翰", "Amrut": "阿姆鲁特",
    "Amrut Fusion": "阿姆鲁特融合", "Starward": "星航", "Sullivan's Cove": "沙利文湾",
    "Hellyers Road": "海勒斯路", "Old Kempton": "老肯普顿", "Overeem": "奥弗里姆",
    "Lark": "云雀", "Nant": "南特", "Bakery Hill": "面包山",
    "Belgrove": "贝尔格罗夫", "Hobart": "霍巴特", "Fleurieu": "弗勒里厄",
    "Kingston": "金斯敦", "Spring Bay": "春湾", "McHenry": "麦克亨利",
    # 白兰地
    "Hennessy": "轩尼诗", "Rémy Martin": "人头马", "Martell": "马爹利",
    "Courvoisier": "拿破仑", "Camus": "卡慕", "Hardy": "哈迪",
    "Hine": "御鹿", "Delamain": "德拉曼", "Frapin": "法拉宾",
    "A. de Fussigny": "富西尼", "Château de Beaulon": "博隆城堡",
    "Paul Giraud": "保罗吉罗", "Ragnaud-Sabourin": "拉尼奥-萨布林",
    "Pierre Voisin": "皮埃尔瓦赞", "Ragnaud": "拉尼奥", "Leyrat": "雷拉",
    "Pasquet": "帕斯凯", "Guillon-Painturaud": "吉永-潘托罗",
    "Maison Surrenne": "叙兰之家", "Cognac Park": "帕克干邑", "Bache-Gabrielsen": "巴什-加布里埃尔森",
    "Braastad": "布拉斯塔", "Cognac Hardy": "哈迪干邑", "Barton & Guestier": "巴顿&盖斯蒂埃",
    "Larsen": "拉森", "Godet": "歌德", "Reviseur": "雷弗瑟",
    "Jean Grosperrin": "让格罗佩兰", "Normandin-Mercier": "诺曼丁-梅西耶",
    "Brillet": "布里耶", "Bonneton": "伯内顿", "J. Normandin-Mercier": "诺曼丁-梅西耶",
    "Yvon vs Cognac": "伊冯干邑", "Maison Surrenne Grande Champagne": "叙兰大香槟",
    # 雅文邑
    "Armagnac": "雅文邑", "Bas-Armagnac": "下雅文邑", "Laberdolive": "拉贝多利夫",
    "Château de Laubade": "洛巴德城堡", "Domaine Boingnères": "布瓦涅尔酒庄",
    "Darroze": "达罗兹", "Baron de Lustrac": "吕斯特拉克男爵",
    "Janneau": "雅诺", "Marquis de Caussade": "科萨德侯爵",
    # 葡萄酒 - 法国波尔多
    "Château Lafite Rothschild": "拉菲古堡", "Lafite": "拉菲",
    "Château Margaux": "玛歌酒庄", "Château Latour": "拉图酒庄",
    "Château Haut-Brion": "侯伯王", "Château Mouton Rothschild": "木桐酒庄",
    "Petrus": "柏图斯", "Cheval Blanc": "白马酒庄", "Ausone": "欧颂",
    "Angélus": "金钟", "Le Pin": "里鹏", "Lafleur": "花堡",
    "Château Palmer": "宝玛酒庄", "Château Léoville Las Cases": "雄狮酒庄",
    "Château Ducru-Beaucaillou": "宝嘉龙酒庄", "Château Lynch-Bages": "靓茨伯",
    "Château Cos d'Estournel": "爱士图尔", "Château Calon-Segur": "凯隆世家",
    "Château Talbot": "大宝酒庄", "Château Gruaud-Larose": "金玫瑰",
    "Château Saint-Julien": "圣朱利安", "Château Pauillac": "波亚克",
    "Château Saint-Estèphe": "圣埃斯泰夫", "Château Margaux": "玛歌",
    "Château Pessac-Léognan": "佩萨克-雷奥良", "Château Sauternes": "苏玳",
    "Château d'Yquem": "滴金酒庄", "Yquem": "滴金", "Bordeaux": "波尔多",
    "Médoc": "梅多克", "Saint-Émilion": "圣埃美隆", "Pomerol": "波美侯",
    "Saint-Julien": "圣朱利安", "Pauillac": "波亚克", "Saint-Estèphe": "圣埃斯泰夫",
    "Margaux": "玛歌", "Graves": "格拉夫", "Pessac": "佩萨克",
    "Fronsac": "弗龙萨克", "Côtes de Bordeaux": "波尔多山坡",
    "Côtes de Bourg": "布尔丘", "Côtes de Castillon": "卡斯蒂永丘",
    # 勃艮第
    "Bourgogne": "勃艮第", "Burgundy": "勃艮第", "Domaine de la Romanée-Conti": "罗曼尼康帝",
    "Romanée-Conti": "罗曼尼康帝", "La Tâche": "拉塔什", "Richebourg": "里奇堡",
    "Romanée-Saint-Vivant": "罗曼尼-圣维旺", "Échezeaux": "埃雪索",
    "Grands Échezeaux": "大埃雪索", "Musigny": "慕西尼", "Chambertin": "香贝丹",
    "Clos de Vougeot": "武若园", "Vosne-Romanée": "沃恩-罗曼尼", "Gevrey-Chambertin": "热夫雷-香贝丹",
    "Chambolle-Musigny": "香波-慕西尼", "Morey-Saint-Denis": "莫雷-圣丹尼",
    "Nuits-Saint-Georges": "夜圣乔治", "Pommard": "波玛", "Volnay": "沃尔奈",
    "Meursault": "默尔索", "Puligny-Montrachet": "普利尼-蒙哈榭",
    "Chassagne-Montrachet": "夏山-蒙哈榭", "Côte de Beaune": "博恩丘",
    "Côte de Nuits": "夜丘", "Hautes-Côtes de Beaune": "上博恩丘",
    "Hautes-Côtes de Nuits": "上夜丘", "Mâcon": "马孔", "Beaujolais": "博若莱",
    "Chablis": "夏布利", "Sancerre": "桑塞尔", "Pouilly-Fumé": "普伊-富美",
    # 香槟
    "Champagne": "香槟", "Moët & Chandon": "酩悦", "Dom Pérignon": "唐培里侬",
    "Veuve Clicquot": "凯歌", "Bollinger": "堡林爵", "Krug": "库克",
    "Ruinart": "瑞纳特", "Pol Roger": "宝禄爵", "Louis Roederer": "路易王妃",
    "Perrier-Jouët": "巴黎之花", "Taittinger": "蒂芙尼", "Piper-Heidsieck": "白雪",
    "Laurent-Perrier": "罗兰百悦", "Deutz": "德茨", "Pommery": "宝玛",
    "Lanson": "岚轩", "Mumm": "玛姆", "G.H. Mumm": "玛姆",
    # 普罗塞克/卡瓦
    "Prosecco": "普罗塞克", "Cava": "卡瓦", "Franciacorta": "弗朗齐亚柯达",
    "Asti": "阿斯蒂", "Lambrusco": "蓝布鲁斯科",
    # 意大利/西班牙/其他
    "Barolo": "巴罗洛", "Barbaresco": "巴巴莱斯科", "Chianti": "基安蒂",
    "Brunello di Montalcino": "布鲁内罗", "Vino Nobile di Montepulciano": "贵族酒",
    "Amarone": "阿玛罗尼", "Valpolicella": "瓦波利切拉", "Soave": "索阿维",
    "Rioja": "里奥哈", "Ribera del Duero": "杜罗河岸", "Priorat": "普里奥拉托",
    "Tempranillo": "丹魄", "Garnacha": "歌海娜", "Albariño": "阿尔巴利诺",
    "Port": "波特", "Porto": "波特", "Sherry": "雪利", "Marsala": "马萨拉",
    "Madeira": "马德拉", "Vermouth": "苦艾酒/味美思", "Noilly Prat": "诺瓦丽",
    "Dolin": "多林", "Carpano": "卡尔帕诺", "Martini": "马天尼",
    "Cinzano": "仙山露", "Lillet": "丽蕾", "Quinquina": "金鸡纳",
    "Moscatel": "麝香", "Pedro Ximénez": "佩德罗-希梅内斯", "PX": "佩德罗-希梅内斯",
    # 啤酒
    "Heineken": "喜力", "Budweiser": "百威", "Corona": "科罗娜",
    "Stella Artois": "时代", "Guinness": "健力士", "Punk IPA": "朋克IPA",
    "BrewDog": "酿酒狗", "Chimay": "智美", "Leffe": "莱福",
    "Hoegaarden": "福佳", "Carlsberg": "嘉士伯", "Tsingtao": "青岛",
    "Snow": "雪花", "Yanjing": "燕京", "Harbin": "哈尔滨",
    "Zhujiang": "珠江", "Taishan": "泰山", "Asahi": "朝日",
    "Kirin": "麒麟", "Sapporo": "三宝乐", "Coors": "库尔斯",
    "Miller": "米勒", "Pabst": "蓝带", "Blue Moon": "蓝月",
    "Samuel Adams": "山姆亚当斯", "Sierra Nevada": "内华达山脉",
    "Stone": "石头", "Lagunitas": "拉古尼塔斯", "IPA": "印度淡色艾尔",
    "Pilsner": "皮尔森", "Stout": "世涛", "Porter": "波特",
    "Lager": "拉格", "Ale": "艾尔", "Weissbier": "小麦啤",
    "Hefeweizen": "酵母小麦", "Witbier": "白啤", "Pale Ale": "淡色艾尔",
    "Amber Ale": "琥珀艾尔", "Belgian": "比利时", "Trappist": "特拉普",
    "Abbey": "修道院", "Lambic": "兰比克", "Saison": "赛松",
    "Kölsch": "科隆", "Altbier": "老啤", "Bock": "博克",
    "Doppelbock": "双料博克", "Märzen": "三月", "Oktoberfest": "慕尼黑啤酒节",
    "Boxing Cat": "拳击猫", "Jing-A": "京A", "Master Gao": "高大师",
    "Slow Boat": "慢船", "Panda Brew": "熊猫精酿", "Taste Room": "品味室",
    # 伏特加
    "Absolut": "绝对", "Grey Goose": "灰雁", "Belvedere": "雪树",
    "Smirnoff": "斯米诺", "Stolichnaya": "红牌", "Ketel One": "坎特一号",
    "Tito's": "蒂托", "Cîroc": "诗珞珂", "Beluga": "白鲸",
    "Russian Standard": "俄罗斯标准", "Finlandia": "芬兰", "Skyy": "蓝天",
    "Three Olives": "三橄榄", "Hangar 1": "机库一号", "Chopin": "肖邦",
    "Zubrówka": "野牛草", "Żubrówka": "野牛草", "Luksusowa": "卢克苏索瓦",
    "Wyborowa": "维波罗瓦", "Sobieski": "索别斯基", "U'Luvka": "乌卢夫卡",
    "Konik's Tail": "科尼克之尾", "Belenkaya": "白杨", "Imperator": "统治者",
    "Mamont": "猛犸", "Russian Vodka": "俄罗斯伏特加", "Original": "原创",
    # 金酒
    "Beefeater": "必富达", "Tanqueray": "添加利", "Bombay": "孟买蓝宝石",
    "Hendrick's": "亨利爵士", "Gin Mare": "海风金酒", "Sipsmith": "西普史密斯",
    "Monkey 47": "猴子47", "Roku": "六", "Malfy": "玛尔菲",
    "Malfy Gin": "玛尔菲金酒", "Citadelle": "城堡", "Plymouth": "普利茅斯",
    "Gordon's": "歌顿金酒", "Gilbey's": "吉尔贝", "Seagram's": "西格姆",
    "Boodles": "布德尔斯", "Broker's": "布洛克", "Edinburgh": "爱丁堡",
    "Martin Miller's": "马丁米勒", "Hayman's": "海曼", "Whitley Neill": "惠特利尼尔",
    "Bulldog": "斗牛犬", "Oxley": "奥克斯利", "Fords": "福特", "The Botanist": "植物学家",
    # 朗姆酒
    "Bacardi": "百加得", "Havana Club": "哈瓦那俱乐部", "Captain Morgan": "摩根船长",
    "Mount Gay": "盖伊山", "Appleton": "阿普尔顿", "Diplomático": "外交官",
    "Zacapa": "萨卡帕", "Flor de Caña": "甘蔗花", "Kraken": "海妖",
    "Sailor Jerry": "水手杰瑞", "Malibu": "马利宝", "Lamb's": "兰姆",
    "Pusser's": "帕瑟", "Gosling's": "高斯林", "Myers's": "迈尔斯",
    "Plantation": "种植园", " Clément": "克莱蒙", "J.M": "J.M",
    "Rhum J.M": "J.M 朗姆", "Negrita": "内格里塔", "St-Roch": "圣罗克",
    "Saint James": "圣詹姆斯", "Rhum Saint James": "圣詹姆斯朗姆", "Rhum Damoiseau": "达莫瓦索",
    "Damoiseau": "达莫瓦索", "Bologne": "布洛涅", "Longueteau": "隆格托",
    "Neisson": "内松", "La Favorite": "最爱", "HSE": "HSE",
    "Trois Rivières": "三河", "Depaz": "德帕", "La Mauny": "拉莫尼",
    "A1710": "A1710", "Chairman's": "主席", "Chairman's Reserve": "主席珍藏",
    "Angostura": "安格斯特拉", "Lemon Hart": "莱蒙哈特", "Forres Park": "福雷斯公园",
    "Caroni": "卡罗尼", "Long Pond": "长池", "Worthy Park": "沃西公园",
    "Foursquare": "四方", "Doorly's": "多利", "Mount Gay Eclipse": "盖伊山日食",
    "Mount Gay XO": "盖伊山XO", "Clément Canne Bleue": "克莱蒙蓝甘蔗",
    "Rhum JM": "J.M朗姆", "Caroni 2000": "卡罗尼2000", "Damoiseau": "达莫瓦索",
    # 龙舌兰
    "Jose Cuervo": "豪帅快活", "Patron": "培恩", "Don Julio": "唐胡里奥",
    "Casamigos": "卡萨米格斯", "Herradura": "马蹄", "El Jimador": "艾尔吉玛多",
    "Sauza": "索查", "Olmeca": "奥美加", "Lunazul": "月狼",
    "Cazadores": "猎人", "Milagro": "奇迹", "Corzo": "科尔佐",
    "Clase Azul": "蓝阶级", "Avión": "飞机", "Casa Dragones": "龙宫",
    "Fortaleza": "堡垒", "Tapatio": "塔帕蒂奥", "Siete Leguas": "七里格",
    "G4": "G4", "Lalo": "拉洛", "Arette": "阿雷特", "Volcán": "火山",
    "Gran Patrón": "大培恩", "Don Julio 1942": "唐胡里奥1942",
    "Patrón Añejo": "培恩陈年", "Patrón Reposado": "培恩微陈",
    "Don Julio Blanco": "唐胡里奥白", "Don Julio Reposado": "唐胡里奥微陈",
    # 梅斯卡尔
    "Mezcal": "梅斯卡尔", "Del Maguey": "巫师", "Clase Azul Mezcal": "蓝阶级梅斯卡尔",
    "Los Amantes": "恋人", "Monte Alban": "阿尔班山", "Ojo de Tigre": "虎眼",
    "Amarás": "你将爱", "Illegal": "非法", "La Niña": "女孩",
    "Vago": "流浪者", "Real Minero": "真矿", "Sacred": "神圣",
    # 利口酒
    "Aperol": "阿佩罗", "Campari": "金巴利", "Cointreau": "君度",
    "Grand Marnier": "柑曼怡", "Kahlua": "甘露", "Baileys": "百利甜",
    "Disaronno": "帝萨诺", "Amaretto": "杏仁利口酒", "Frangelico": "榛果利口酒",
    "Midori": "蜜多丽", "Peach Schnapps": "桃子力娇酒", "Jagermeister": "野格",
    "Chartreuse": "查特", "Bénédictine": "廊酒", "Drambuie": "杜林标",
    "St-Germain": "圣日尔曼", "Limoncello": "柠檬酒", "Galliano": "加利亚诺",
    "Sambuca": "萨姆布卡", "Anisette": "茴香酒", "Pernod": "派诺",
    "Pastis": "普罗旺斯茴香酒", "Ricard": "里卡尔", "Raki": "拉克",
    "Ouzo": "乌佐", "Arak": "阿拉克", "Sake": "清酒",
    "Soju": "烧酒", "Shochu": "烧酒", "Baijiu": "白酒",
    # 日本清酒
    "Junmai": "纯米", "Ginjo": "吟酿", "Daiginjo": "大吟酿",
    "Honjozo": "本酿造", "Nigori": "浊酒", "Namazake": "生酒",
    "Dassai": "獭祭", "Hakkaisan": "八海山", "Kubota": "久保田",
    "Kikumasamune": "菊正宗", "Gekkeikan": "月桂冠", "Ozeki": "大关",
    "Joto": "上东", "Born": "梵", "Nabeshima": "锅岛",
    "Kura no Hana": "仓の花", "Shuzhouzhai": "酒心斋", "Tyku": "大关",
    # 鸡尾酒名
    "Margarita": "玛格丽特", "Daiquiri": "得其利", "Manhattan": "曼哈顿",
    "Martini": "马天尼", "Negroni": "尼格罗尼", "Old Fashioned": "古典",
    "Whiskey Sour": "威士忌酸", "Amaretto Sour": "杏仁酸", "Mojito": "莫吉托",
    "Cosmopolitan": "大都会", "Bloody Mary": "血腥玛丽", "Mimosa": "含羞草",
    "Bellini": "贝利尼", "Sidecar": "边车", "French 75": "法兰西75",
    "Aperol Spritz": "阿佩罗气泡", "Moscow Mule": "莫斯科骡子",
    "Espresso Martini": "浓缩马天尼", "Porn Star Martini": "性感马天尼",
    "Pisco Sour": "皮斯科酸", "Mai Tai": "迈泰", "Pina Colada": "椰林飘香",
    "Zombie": "僵尸", "Hurricane": "飓风", "Long Island Iced Tea": "长岛冰茶",
    "Tom Collins": "汤姆柯林斯", "Gin Fizz": "金菲士", "Dark 'n' Stormy": "黑色风暴",
    "Penicillin": "盘尼西林", "Paper Plane": "纸飞机", "Last Word": "遗言",
    "Corpse Reviver": "亡者复甦", "Boulevardier": "林荫大道", "Americano": "美式咖啡",
    "Aperol Sour": "阿佩罗酸", "Tommy's Margarita": "汤米玛格丽特",
    "Bramble": "荆棘", "Southside": "南边", "Bee's Knees": "蜜蜂膝盖",
    "Penicillina": "盘尼西林", "Final Ward": "最后病房", "Ramos Gin Fizz": "拉莫斯金菲士",
    "French Martini": "法式马天尼", "Breakfast Martini": "早餐马天尼",
    "Vesper": "维斯帕", "Gibson": "吉布森", "Hanky Panky": "汉基潘基",
    "Aviation": "航空", "The Last Word": "最后遗言", "Alaska": "阿拉斯加",
    "Remember the Maine": "记住缅因", "Brooklyn": "布鲁克林", "Rob Roy": "罗布罗伊",
    "Sazerac": "萨泽拉克", "Rattlesnake": "响尾蛇", "Suffering Bastard": "受苦混蛋",
    "Jungle Bird": "丛林鸟", "Naked & Famous": "裸名流", "Division Bell": "分割钟",
    "Tuxedo": "燕尾服", "Champs-Élysées": "香榭丽舍", "Between the Sheets": "床笫之间",
    "Death in the Afternoon": "午后之死", "Monkey Gland": "猴子腺体",
    "Clover Club": "三叶草俱乐部", "Mary Pickford": "玛丽璧克馥",
    "Hemingway Special": "海明威特调", "Chartreuse Sour": "查特酸",
    "Bijou": "宝石", "Casino": "卡西诺", "Jasmine": "茉莉",
    "Negroni Sbagliato": "尼格罗尼斯巴利亚托", "Garibaldi": "加里波第",
    "Crodino": "克罗迪诺", "Select": "精选", "Aperol": "阿佩罗",
    "Sarti": "萨蒂", "Luxardo": "卢萨多", "Stock": "斯托克",
    "Ramazzotti": "罗马佐", "Averna": "阿韦纳", "Fernet-Branca": "飞马比特",
    "Branca Menta": "薄荷比特", "Montenegro": "黑山", "Cynar": "西娜",
    "Cynar 70": "西娜70", "Strega": "斯特雷加", "Nonino": "诺尼诺",
    "Amaro": "苦味利口酒", "Amaro Averna": "阿韦纳苦味酒",
}


def translate_to_chinese_title(title: str, subcat: str = "") -> str:
    """将英文标题转换为中文（保留品牌/专有名词+中文译名）。"""
    if not title:
        return title

    # 已经是中文（含中文字符）则跳过
    if re.search(r'[\u4e00-\u9fff]', title):
        return title

    title_clean = title.strip()

    # 1. 精确匹配
    if title_clean in BRAND_ZH_MAP:
        return f"{BRAND_ZH_MAP[title_clean]}（{title_clean}）"

    # 2. 大小写不敏感匹配
    for k, v in BRAND_ZH_MAP.items():
        if k.lower() == title_clean.lower():
            return f"{v}（{title_clean}）"

    # 3. 子串匹配（标题中包含品牌关键词）
    for k, v in BRAND_ZH_MAP.items():
        if k.lower() in title_clean.lower():
            # 避免过短关键词误匹配
            if len(k) >= 4 and k.lower() in title_clean.lower():
                return f"{v}（{title_clean}）"
            # 完全包含（如品牌+产品名）
            if title_clean.lower().startswith(k.lower()) or title_clean.lower().endswith(k.lower()):
                return f"{v}（{title_clean}）"

    # 4. 没有匹配则保留原标题
    return title_clean


def get_zh_title_for_ima(title: str, subcat: str, tags: list[str] | None = None) -> str:
    """为 IMA 展示生成中文标题。

    策略：
    1. 如果 title 已是中文 → 直接用
    2. 如果在品牌词典中 → 用译名+原名
    3. 如果 tags 含中文 → 用 tags 中的中文类别描述
    4. 否则保留原 title
    """
    zh = translate_to_chinese_title(title, subcat)
    if zh != title:
        return zh

    # 尝试从 tags 推断（tags 中通常含类别）
    if tags:
        cat_keywords = {
            "威士忌": "威士忌", "白酒": "白酒", "红酒": "红酒", "葡萄酒": "葡萄酒",
            "啤酒": "啤酒", "朗姆酒": "朗姆酒", "伏特加": "伏特加", "金酒": "金酒",
            "龙舌兰": "龙舌兰", "梅斯卡尔": "梅斯卡尔", "清酒": "清酒", "黄酒": "黄酒",
            "米酒": "米酒", "果酒": "果酒", "白兰地": "白兰地", "干邑": "干邑",
            "雅文邑": "雅文邑", "苦艾酒": "苦艾酒", "味美思": "味美思",
        }
        for tag in tags:
            for kw, zh_name in cat_keywords.items():
                if kw in tag:
                    return f"{title}（{zh_name}）"

    return title


def parse_markdown_meta_zh(md_content: str) -> tuple[dict, str, list[str]]:
    """解析 YAML front matter，返回 (meta, title, tags)。"""
    meta = {}
    title = ""
    tags = []
    if not md_content.startswith("---"):
        return meta, title, tags
    end_idx = md_content.find("---", 3)
    if end_idx == -1:
        return meta, title, tags
    fm = md_content[3:end_idx]
    for line in fm.split("\n"):
        line = line.strip()
        if line.startswith("#"):
            continue
        if ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            val = val.strip()
            if val.startswith("[") and val.endswith("]"):
                arr = [v.strip().strip("'\"") for v in val[1:-1].split(",") if v.strip()]
                if key == "tags":
                    tags = arr
                meta[key] = arr
            else:
                if key == "title":
                    title = val
                meta[key] = val
    return meta, title, tags


def create_ima_folder(client_id: str, api_key: str, kb_id: str, folder_name: str, parent_id: str = "") -> str:
    """在 IMA 知识库中创建文件夹，返回 folder_id。已存在则直接返回。"""
    try:
        resp = ima_api_request("create_folder", {
            "knowledge_base_id": kb_id,
            "name": folder_name,
            "parent_folder_id": parent_id,
        }, client_id, api_key)
        if resp.get("code") == 0:
            return resp.get("data", {}).get("folder_id", "")
    except Exception:
        pass
    return ""


def upload_to_ima(
    kb_dir: Path,
    client_id: str,
    api_key: str,
    kb_id: str,
    subcat_filter: set[str] | None = None,
    confidence_filter: set[str] | None = None,
    folder_id: str = "",
    dry_run: bool = False,
    delay: float = 0.15,
) -> dict:
    """通过 IMA OpenAPI 以笔记方式上传到知识库。

    两步流程（每篇笔记）：
    1. notes/import_doc: 创建 Markdown 笔记（content_format=1）
    2. wiki/add_knowledge: 将笔记关联到知识库（media_type=11）

    按子类自动创建文件夹分类。
    """
    print("验证 IMA API 凭证...")
    try:
        kb_list = ima_api_request("get_addable_knowledge_base_list", {
            "cursor": "", "limit": 50
        }, client_id, api_key)
        if kb_list.get("code") != 0:
            print(f"凭证验证失败: {kb_list.get('msg', kb_list)}")
            return {"success": 0, "failed": 0, "errors": [str(kb_list)]}
        kbs = kb_list.get("data", {}).get("addable_knowledge_base_list", [])
        target_kb_name = ""
        for kb in kbs:
            if kb.get("id") == kb_id:
                target_kb_name = kb.get("name", "")
                break
        print(f"✓ API 连接成功，目标知识库: {target_kb_name}")
    except Exception as e:
        print(f"✗ API 连接失败: {e}")
        return {"success": 0, "failed": 0, "errors": [str(e)]}

    if dry_run:
        print("\n[DRY RUN] 仅验证连接，实际上传跳过")
        return {"success": 0, "failed": 0, "errors": []}

    md_files = sorted(kb_dir.glob("*.md"))

    to_upload = []
    for md_path in md_files:
        content = md_path.read_text(encoding="utf-8")
        meta, fm_title, fm_tags = parse_markdown_meta_zh(content)
        subcat = meta.get("subcategory", "unknown")
        confidence = meta.get("data_confidence", "simulated")
        if subcat_filter and subcat not in subcat_filter:
            continue
        if confidence_filter and confidence not in confidence_filter:
            continue
        cleaned = clean_markdown_for_ima(content)
        base_title = extract_title_from_md(cleaned, fm_title or md_path.stem)
        # 为 IMA 转换中文标题
        title = get_zh_title_for_ima(base_title, subcat, fm_tags)
        # 如果翻译后还是英文，强制使用 fm_title 或文件名
        if title == base_title and not re.search(r'[\u4e00-\u9fff]', title):
            # 尝试更激进的翻译（用 tags 中的中文类别）
            for tag in fm_tags:
                if any(c in tag for c in '酒'):
                    title = f"{title}（{tag}）"
                    break
        dir_name = SUBCAT_DIR_MAP.get(subcat, f"99_{subcat}")
        to_upload.append((md_path.name, title, cleaned, dir_name))

    total = len(to_upload)
    print(f"待上传条目: {total}")
    if total == 0:
        return {"success": 0, "failed": 0, "errors": []}

    folder_cache: dict[str, str] = {}

    success = 0
    failed = 0
    errors = []
    subcat_stats: dict[str, int] = defaultdict(int)
    t0 = time.time()

    for i, (file_name, title, cleaned, dir_name) in enumerate(to_upload, 1):
        target_folder_id = folder_id
        if not folder_id and dir_name not in folder_cache:
            fid = create_ima_folder(client_id, api_key, kb_id, dir_name, "")
            folder_cache[dir_name] = fid
        if not folder_id:
            target_folder_id = folder_cache.get(dir_name, "")

        pct = i / total * 100
        elapsed = time.time() - t0
        rate = i / elapsed if elapsed > 0 else 0
        eta = (total - i) / rate if rate > 0 else 0
        print(f"[{i}/{total} {pct:.0f}% ETA:{eta:.0f}s] {title[:40]}...", end=" ", flush=True)

        try:
            r1 = ima_api_request("import_doc", {
                "content_format": 1,
                "content": cleaned,
                "title": title,
            }, client_id, api_key, base=IMA_NOTE_API_BASE)

            if r1.get("code") != 0:
                msg = r1.get("msg", "unknown")
                print(f"失败(import_doc): {msg}")
                failed += 1
                errors.append(f"{file_name}: import_doc - {msg}")
                continue

            note_id = r1.get("data", {}).get("note_id", "")
            if not note_id:
                print(f"失败: 未返回 note_id")
                failed += 1
                errors.append(f"{file_name}: no note_id returned")
                continue

            r2 = ima_api_request("add_knowledge", {
                "media_type": 11,
                "title": title,
                "knowledge_base_id": kb_id,
                "folder_id": target_folder_id,
                "note_info": {
                    "content_id": note_id,
                },
            }, client_id, api_key)

            if r2.get("code") != 0:
                msg = r2.get("msg", "unknown")
                print(f"失败(add_knowledge): {msg}")
                failed += 1
                errors.append(f"{file_name}: add_knowledge - {msg}")
                continue

            print("✓")
            success += 1
            subcat_stats[dir_name] += 1

        except Exception as e:
            print(f"失败: {e}")
            failed += 1
            errors.append(f"{file_name}: {e}")

        if delay > 0 and i < total:
            time.sleep(delay)

    print(f"\n{'='*60}")
    print(f"IMA API 上传完成（笔记方式）")
    print(f"{'='*60}")
    print(f"成功: {success}")
    print(f"失败: {failed}")
    print(f"耗时: {time.time()-t0:.1f}s")
    print(f"文件夹分布:")
    for d, c in sorted(subcat_stats.items(), key=lambda x: -x[1]):
        print(f"  {d}: {c} 条")
    if errors:
        print(f"\n错误详情 (前20条):")
        for err in errors[:20]:
            print(f"  - {err}")

    return {"success": success, "failed": failed, "errors": errors}


def main():
    parser = argparse.ArgumentParser(description="Hermes 知识库 → IMA 知识库导出工具")
    parser.add_argument("--package", action="store_true", help="打包为 ZIP 文件（手动导入 IMA）")
    parser.add_argument("--upload", action="store_true", help="通过 API 自动上传到 IMA")
    parser.add_argument("--subcat", type=str, default="", help="子类过滤，逗号分隔（如 cocktail,whisky,gin）")
    parser.add_argument("--confidence", type=str, default="", help="置信度过滤，逗号分隔（如 official,verified）")
    parser.add_argument("--dry-run", action="store_true", help="API 模式下仅验证连接，不实际上传")
    parser.add_argument("--kb-dir", type=str, default=str(KB_DIR), help="知识库 Markdown 目录")
    parser.add_argument("--output-dir", type=str, default=str(OUTPUT_DIR), help="输出目录")
    parser.add_argument("--zip-name", type=str, default="hermes_kb_for_ima.zip", help="ZIP 文件名")
    parser.add_argument("--delay", type=float, default=0.1, help="API 请求间隔秒数（默认0.1）")
    args = parser.parse_args()

    kb_dir = Path(args.kb_dir)
    output_dir = Path(args.output_dir)

    subcat_filter = set(s.strip() for s in args.subcat.split(",")) if args.subcat else None
    confidence_filter = set(s.strip() for s in args.confidence.split(",")) if args.confidence else None

    if not args.package and not args.upload:
        args.package = True

    if args.package:
        package_for_ima(
            kb_dir=kb_dir,
            output_dir=output_dir,
            subcat_filter=subcat_filter,
            confidence_filter=confidence_filter,
            zip_name=args.zip_name,
        )

    if args.upload:
        client_id = os.environ.get("IMA_CLIENT_ID", "")
        api_key = os.environ.get("IMA_API_KEY", "")
        kb_id = os.environ.get("IMA_KB_ID", "")
        folder_id = os.environ.get("IMA_FOLDER_ID", "")

        if not client_id or not api_key or not kb_id:
            print("错误: API 上传模式需要设置环境变量:")
            print("  IMA_CLIENT_ID: 在 https://ima.qq.com/agent-interface 获取")
            print("  IMA_API_KEY:   在 https://ima.qq.com/agent-interface 获取")
            print("  IMA_KB_ID:     目标知识库 ID（通过 get_addable_knowledge_base_list 获取）")
            print("  IMA_FOLDER_ID: 目标文件夹 ID（可选，留空上传到根目录）")
            sys.exit(1)

        upload_to_ima(
            kb_dir=kb_dir,
            client_id=client_id,
            api_key=api_key,
            kb_id=kb_id,
            folder_id=folder_id,
            subcat_filter=subcat_filter,
            confidence_filter=confidence_filter,
            dry_run=args.dry_run,
            delay=args.delay,
        )


if __name__ == "__main__":
    main()
