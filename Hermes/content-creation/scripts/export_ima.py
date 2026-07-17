#!/usr/bin/env python3
"""Hermes 知识库 → IMA 知识库 导出脚本

两种导出模式：
1. 打包模式（默认，无需凭证）：
   - 将 Markdown 条目按子类分组整理到目录
   - 生成 IMA 友好的目录结构（01_白酒/02_红酒/...）
   - 打包为 ZIP 文件，直接拖入 IMA 客户端即可导入

2. API 模式（需配置 ClientID + APIKey）：
   - 通过 IMA OpenAPI 自动上传到指定知识库
   - 三步流程：create_media → COS PUT → add_knowledge

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

IMA_API_BASE = "https://ima.qq.com/openapi/wiki/v1"


def clean_markdown_for_ima(md_content: str) -> str:
    """将 Hermes 渲染的 Markdown 优化为 IMA 知识库友好格式。

    主要处理：
    1. 移除 YAML front matter（IMA 会自己解析，保留元数据为正文开头）
    2. 移除图片参考链接章节（WikiMedia/Unsplash/Google 图片搜索链接在 IMA 中无效）
    3. 将评分信息保留为表格格式
    4. 移除合规提示（IMA 自带合规提示）
    5. 移除参考资料中的图片搜索链接
    """
    lines = md_content.split("\n")
    result_lines = []
    in_front_matter = False
    fm_passed = False
    skip_section = False
    in_image_refs = False
    in_compliance = False

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

        # 清理并写入
        cleaned = clean_markdown_for_ima(content)
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


def ima_api_request(endpoint: str, data: dict, client_id: str, api_key: str) -> dict:
    """调用 IMA OpenAPI。"""
    url = f"{IMA_API_BASE}/{endpoint}"
    body = json.dumps(data).encode("utf-8")
    req = Request(url, data=body, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("ima-openapi-clientid", client_id)
    req.add_header("ima-openapi-apikey", api_key)
    try:
        with urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except HTTPError as e:
        error_body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"IMA API 错误 {e.code}: {error_body}") from e


def upload_to_ima(
    kb_dir: Path,
    client_id: str,
    api_key: str,
    kb_id: str,
    subcat_filter: set[str] | None = None,
    confidence_filter: set[str] | None = None,
    folder_id: str = "",
    dry_run: bool = False,
) -> dict:
    """通过 IMA OpenAPI 上传 Markdown 文件到知识库。

    三步流程：
    1. create_media: 创建媒体，获取 COS 上传凭证
    2. PUT to COS: 上传文件到腾讯云 COS
    3. add_knowledge: 将媒体添加到知识库
    """
    # 验证凭证
    print("验证 IMA API 凭证...")
    try:
        kb_list = ima_api_request("get_addable_knowledge_base_list", {
            "cursor": "", "limit": 50
        }, client_id, api_key)
        if kb_list.get("code") != 0:
            print(f"凭证验证失败: {kb_list}")
            return {"success": 0, "failed": 0, "errors": [str(kb_list)]}
        print(f"✓ API 连接成功，可访问 {len(kb_list.get('data', {}).get('list', []))} 个知识库")
    except Exception as e:
        print(f"✗ API 连接失败: {e}")
        return {"success": 0, "failed": 0, "errors": [str(e)]}

    if dry_run:
        print("\n[DRY RUN] 仅验证连接，实际上传跳过")
        return {"success": 0, "failed": 0, "errors": []}

    # 上传文件
    md_files = sorted(kb_dir.glob("*.md"))
    success = 0
    failed = 0
    errors = []

    for i, md_path in enumerate(md_files, 1):
        content = md_path.read_text(encoding="utf-8")
        meta = parse_markdown_meta(content)

        subcat = meta.get("subcategory", "unknown")
        confidence = meta.get("data_confidence", "simulated")
        title = meta.get("title", md_path.stem)

        if subcat_filter and subcat not in subcat_filter:
            continue
        if confidence_filter and confidence not in confidence_filter:
            continue

        cleaned = clean_markdown_for_ima(content)
        file_name = md_path.name
        file_bytes = cleaned.encode("utf-8")
        file_size = len(file_bytes)

        print(f"[{i}/{len(md_files)}] 上传 {file_name} ({title}) ...", end=" ", flush=True)

        try:
            # Step 1: create_media
            create_resp = ima_api_request("create_media", {
                "file_name": file_name,
                "file_size": file_size,
                "knowledge_base_id": kb_id,
            }, client_id, api_key)

            if create_resp.get("code") != 0:
                print(f"失败: create_media 返回 {create_resp.get('msg', 'unknown error')}")
                failed += 1
                errors.append(f"{file_name}: create_media failed - {create_resp}")
                continue

            media_data = create_resp.get("data", {})
            cos_url = media_data.get("url", "")
            media_id = media_data.get("media_id", "")
            cos_headers = media_data.get("headers", {})

            if not cos_url or not media_id:
                print(f"失败: COS 凭证不完整")
                failed += 1
                errors.append(f"{file_name}: incomplete COS credentials")
                continue

            # Step 2: PUT to COS
            cos_req = Request(cos_url, data=file_bytes, method="PUT")
            for k, v in cos_headers.items():
                cos_req.add_header(k, v)
            cos_req.add_header("Content-Type", "text/markdown; charset=utf-8")
            with urlopen(cos_req, timeout=60) as cos_resp:
                if cos_resp.status not in (200, 204):
                    print(f"失败: COS 上传返回 {cos_resp.status}")
                    failed += 1
                    errors.append(f"{file_name}: COS upload failed - {cos_resp.status}")
                    continue

            # Step 3: add_knowledge
            add_resp = ima_api_request("add_knowledge", {
                "knowledge_base_id": kb_id,
                "media_id": media_id,
                "folder_id": folder_id,
            }, client_id, api_key)

            if add_resp.get("code") != 0:
                print(f"失败: add_knowledge 返回 {add_resp.get('msg', 'unknown error')}")
                failed += 1
                errors.append(f"{file_name}: add_knowledge failed - {add_resp}")
                continue

            print("✓")
            success += 1

        except Exception as e:
            print(f"失败: {e}")
            failed += 1
            errors.append(f"{file_name}: {e}")

    print(f"\n{'='*60}")
    print(f"IMA API 上传完成")
    print(f"{'='*60}")
    print(f"成功: {success}")
    print(f"失败: {failed}")
    if errors:
        print(f"错误详情:")
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
        )


if __name__ == "__main__":
    main()
