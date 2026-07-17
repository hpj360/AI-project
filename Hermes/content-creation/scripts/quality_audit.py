#!/usr/bin/env python3
"""Hermes 知识库质量分析器。

检测维度：
1. 文件级问题：极短、空白、错误信息
2. 内容问题：占位符、未完成模板、硬编码错误
3. 数据问题：simulated 数据比例、缺失关键字段
4. 重复问题：高度相似/完全相同内容
5. 命名问题：英文文件名/乱码/无效字符
"""
import re
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

KB_DIR = Path("content-creation/knowledge")

# 问题关键词（精确匹配，避免误报 Markdown 链接方括号）
PLACEHOLDER_PATTERNS = [
    r"待补充[^。，\n]{0,10}",  # 待补充...
    r"待完善[^。，\n]{0,10}",
    r"暂无(数据|内容|信息|资料)",
    r"\bTODO\b",
    r"\bTBD\b",
    r"占位符",
    r"\bplaceholder\b",
    r"暂无数据",
    r"数据缺失",
    r"未填写",
    r"未补充",
    r"以后补充",
    r"^\s*\[此处[^]]*\]\s*$",  # 整行 [此处添加...]
]

ERROR_PATTERNS = [
    r"^#+\s*Error", r"^#+\s*404", r"^#+\s*未找到",
    r"页面不存在", r"内容不存在", r"无法找到",
    r"^#+\s*Hello", r"^#+\s*World", r"^#+\s*Test",
    r"^#+\s*Sample", r"^#+\s*Demo",
]

# 低质内容特征
LOW_QUALITY_INDICATORS = [
    r"lorem ipsum",
    r"example\.com",
    r"foo\s*bar",
    r"^\s*test\s*$",
]

def parse_front_matter(content):
    """解析 YAML front matter。"""
    if not content.startswith("---"):
        return {}, "", [], 0
    end_idx = content.find("---", 3)
    if end_idx == -1:
        return {}, "", [], 0
    fm = content[3:end_idx]
    meta = {}
    tags = []
    title = ""
    for line in fm.split("\n"):
        line = line.rstrip()
        if line.startswith("#"):
            continue
        if ":" not in line:
            continue
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
    return meta, title, tags, end_idx + 3

def has_placeholder(content):
    """检查占位符。"""
    issues = []
    for pat in PLACEHOLDER_PATTERNS:
        for m in re.finditer(pat, content, re.IGNORECASE):
            issues.append(pat)
    return issues

def has_error_indicator(content):
    """检查错误/测试指示。"""
    for pat in ERROR_PATTERNS:
        if re.search(pat, content, re.IGNORECASE | re.MULTILINE):
            return pat
    return None

def main():
    md_files = sorted(KB_DIR.glob("*.md"))
    print(f"扫描 {len(md_files)} 个文件...\n")

    # 收集统计
    results = {
        "too_short": [],          # 极短内容
        "no_title": [],           # 无标题
        "placeholder": [],        # 占位符
        "error_indicator": [],    # 错误指示
        "low_quality": [],        # 低质量指示
        "duplicate": [],          # 重复内容
        "low_confidence_simulated": [],  # 高比例 simulated
        "english_only": [],       # 鸡尾酒英文文件名
        "suspicious_filename": [], # 可疑文件名
        "empty_content": [],      # 空内容
        "few_sections": [],       # 章节过少
        "no_real_ingredients": [],  # 鸡尾酒缺配方
        "abnormal_recipe": [],    # 配方异常
        "no_recipe_at_all": [],   # 鸡尾酒完全无配方
        "no_provenance": [],      # 无数据来源
        "filler_only": [],        # 只含引导语无实质内容
    }

    # 1. 基础分析
    content_hashes = defaultdict(list)
    name_stats = Counter()

    for f in md_files:
        content = f.read_text(encoding="utf-8")
        meta, title, tags, fm_end = parse_front_matter(content)

        # 1.1 文件名统计
        name_stats[f.name] += 1

        # 1.2 内容长度（去除 front matter 和图片参考）
        body = content[fm_end:].strip() if fm_end else content.strip()
        body_no_images = re.sub(r"##\s*图片参考.*?(?=^##\s|\Z)", "", body, flags=re.MULTILINE | re.DOTALL)
        body_clean = re.sub(r"^#+\s.*$", "", body_no_images, flags=re.MULTILINE).strip()
        body_length = len(body_clean)

        # 1.3 极短内容
        if body_length < 100:
            results["too_short"].append((f.name, body_length, title))

        # 1.4 空内容
        if body_length == 0:
            results["empty_content"].append(f.name)

        # 1.5 占位符
        placeholders = has_placeholder(content)
        if placeholders:
            results["placeholder"].append((f.name, len(placeholders), title))

        # 1.6 错误指示
        err = has_error_indicator(content)
        if err:
            results["error_indicator"].append((f.name, err, title))

        # 1.7 低质量指示
        for pat in LOW_QUALITY_INDICATORS:
            if re.search(pat, content, re.IGNORECASE):
                results["low_quality"].append((f.name, pat, title))
                break

        # 1.8 simulated 数据比例
        subcat = meta.get("subcategory", "")
        confidence = meta.get("data_confidence", "")
        if confidence == "simulated":
            results["low_confidence_simulated"].append(f.name)

        # 1.9 英文文件名（无中文，但只在鸡尾酒/酒类子类检查）
        if not re.search(r'[\u4e00-\u9fff]', f.name):
            if subcat in ("cocktail",) or "cocktail" in f.name.lower():
                # 鸡尾酒应该用中文名
                results["english_only"].append(f.name)

        # 1.10 重复检测（基于内容 hash）
        body_for_hash = re.sub(r"\s+", " ", body_clean)
        h = hashlib.md5(body_for_hash.encode("utf-8")).hexdigest()
        content_hashes[h].append(f.name)

        # 1.11 章节数统计（H2 标题）
        h2_count = len(re.findall(r"^##\s", body, re.MULTILINE))
        if h2_count < 3 and body_length > 100:
            results["few_sections"].append((f.name, h2_count, title))

        # 1.12 鸡尾酒应该有配方
        if subcat == "cocktail" or "cocktail" in f.name.lower():
            if not re.search(r"配方|调制方法|recipe|ingredients", body, re.IGNORECASE):
                results["no_recipe_at_all"].append(f.name)
            elif body_length < 300:
                results["no_real_ingredients"].append((f.name, body_length, title))

        # 1.13 数据来源检查（任何有内容文件应至少有 provenance 字段或参考章节）
        has_provenance = bool(meta.get("provenance") or meta.get("data_source") or meta.get("data_provenance"))
        has_ref_section = "参考资料" in body or "数据来源" in body or "参考来源" in body
        if not has_provenance and not has_ref_section and body_length > 200:
            results["no_provenance"].append(f.name)

        # 1.14 只含引导语（章节标题 + 极少正文）
        # 检测类似 "## 概述\n\n本节介绍 xxx" 的模板化内容
        if h2_count >= 2 and body_length < 300:
            # 检查是否章节标题下都是占位文本
            filler_pattern = re.findall(
                r"^##\s.+\n\n[^\n#]{0,50}$", body, re.MULTILINE
            )
            if len(filler_pattern) >= 2:
                results["filler_only"].append((f.name, body_length, title))

    # 处理重复
    for h, files in content_hashes.items():
        if len(files) > 1:
            results["duplicate"].append((files, len(files)))

    # 2. 输出报告
    print("="*70)
    print("Hermes 知识库质量分析报告")
    print("="*70)
    print(f"\n总文件数: {len(md_files)}")

    # 各问题统计
    issues_count = {
        "重复内容": len(results["duplicate"]),
        "极短内容 (<100字)": len(results["too_short"]),
        "空内容": len(results["empty_content"]),
        "占位符/未完成": len(results["placeholder"]),
        "错误指示": len(results["error_indicator"]),
        "低质量指示": len(results["low_quality"]),
        "simulated 数据": len(results["low_confidence_simulated"]),
        "鸡尾酒英文文件名": len(results["english_only"]),
        "章节过少 (<3个H2)": len(results["few_sections"]),
        "鸡尾酒无配方": len(results["no_recipe_at_all"]),
        "鸡尾酒配方过简": len(results["no_real_ingredients"]),
        "无数据来源": len(results["no_provenance"]),
        "仅占位文本": len(results["filler_only"]),
    }

    print("\n问题统计：")
    for k, v in issues_count.items():
        pct = v / len(md_files) * 100 if md_files else 0
        print(f"  {k}: {v} ({pct:.1f}%)")

    total_issues = sum(issues_count.values())
    print(f"\n问题总数: {total_issues}")

    # 详细列出
    print("\n" + "="*70)
    print("详细问题清单")
    print("="*70)

    if results["duplicate"]:
        print(f"\n【重复内容】 {len(results['duplicate'])} 组:")
        for files, cnt in results["duplicate"][:30]:
            print(f"  ×{cnt}:")
            for fn in files[:5]:
                print(f"    - {fn}")
            if len(files) > 5:
                print(f"    ... 等{len(files)}个")
        if len(results["duplicate"]) > 30:
            print(f"  ... 等{len(results['duplicate'])}组")

    if results["too_short"]:
        print(f"\n【极短内容】 {len(results['too_short'])} 条 (前20条):")
        for fn, length, title in results["too_short"][:20]:
            print(f"  {length}字 | {fn}: {title}")
        if len(results["too_short"]) > 20:
            print(f"  ... 等{len(results['too_short'])}条")

    if results["empty_content"]:
        print(f"\n【空内容】 {len(results['empty_content'])} 条:")
        for fn in results["empty_content"][:10]:
            print(f"  {fn}")

    if results["placeholder"]:
        print(f"\n【占位符/未完成】 {len(results['placeholder'])} 条 (前20条):")
        for fn, count, title in results["placeholder"][:20]:
            print(f"  {count}处 | {fn}: {title}")
        if len(results["placeholder"]) > 20:
            print(f"  ... 等{len(results['placeholder'])}条")

    if results["error_indicator"]:
        print(f"\n【错误指示】 {len(results['error_indicator'])} 条:")
        for fn, err, title in results["error_indicator"][:20]:
            print(f"  [{err}] {fn}: {title}")

    if results["low_quality"]:
        print(f"\n【低质量指示】 {len(results['low_quality'])} 条:")
        for fn, pat, title in results["low_quality"][:20]:
            print(f"  [{pat}] {fn}: {title}")

    # 命名统计
    print(f"\n【鸡尾酒英文文件名】 {len(results['english_only'])} 条 (前10条):")
    for fn in results["english_only"][:10]:
        print(f"  {fn}")
    if len(results["english_only"]) > 10:
        print(f"  ... 等{len(results['english_only'])}条")

    # 章节过少
    if results["few_sections"]:
        print(f"\n【章节过少 (<3个H2)】 {len(results['few_sections'])} 条 (前15条):")
        for fn, cnt, title in results["few_sections"][:15]:
            print(f"  {cnt}节 | {fn}: {title}")

    # 鸡尾酒无配方
    if results["no_recipe_at_all"]:
        print(f"\n【鸡尾酒完全无配方】 {len(results['no_recipe_at_all'])} 条 (前15条):")
        for fn in results["no_recipe_at_all"][:15]:
            print(f"  {fn}")

    # 鸡尾酒配方过简
    if results["no_real_ingredients"]:
        print(f"\n【鸡尾酒配方过简】 {len(results['no_real_ingredients'])} 条 (前15条):")
        for fn, length, title in results["no_real_ingredients"][:15]:
            print(f"  {length}字 | {fn}: {title}")

    # 无数据来源
    if results["no_provenance"]:
        print(f"\n【无数据来源】 {len(results['no_provenance'])} 条 (前20条):")
        for fn in results["no_provenance"][:20]:
            print(f"  {fn}")
        if len(results["no_provenance"]) > 20:
            print(f"  ... 等{len(results['no_provenance'])}条")

    # 仅占位文本
    if results["filler_only"]:
        print(f"\n【仅占位文本】 {len(results['filler_only'])} 条 (前15条):")
        for fn, length, title in results["filler_only"][:15]:
            print(f"  {length}字 | {fn}: {title}")

    # 2.3 simulated 数据按子类统计
    if results["low_confidence_simulated"]:
        # 按 subcategory 统计 simulated 比例
        subcat_total = Counter()
        subcat_simulated = Counter()
        for f in md_files:
            content = f.read_text(encoding="utf-8")
            meta, _, _, _ = parse_front_matter(content)
            subcat = meta.get("subcategory", "unknown")
            confidence = meta.get("data_confidence", "")
            subcat_total[subcat] += 1
            if confidence == "simulated":
                subcat_simulated[subcat] += 1

        print(f"\n【simulated 数据按子类统计】:")
        print(f"  {'子类':<25} {'simulated数':<12} {'总数':<8} {'占比':<8}")
        for subcat, total in subcat_total.most_common():
            sim_n = subcat_simulated.get(subcat, 0)
            if sim_n > 0:
                pct = sim_n / total * 100
                if pct > 50:  # 超过 50% 才列出
                    print(f"  {subcat:<25} {sim_n:<12} {total:<8} {pct:.1f}%")

    # 保存详细报告
    report_path = Path("content-creation/quality_report.json")
    json_report = {
        "total_files": len(md_files),
        "issues_count": issues_count,
        "details": {
            k: [list(map(str, x)) if isinstance(x, tuple) else str(x) for x in v]
            for k, v in results.items()
        }
    }
    report_path.write_text(json.dumps(json_report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n详细报告已保存: {report_path}")

if __name__ == "__main__":
    main()
