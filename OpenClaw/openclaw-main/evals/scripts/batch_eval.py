#!/usr/bin/env python3
"""
批量 Skill 评估器

遍历所有 skill，生成评估报告和排名。

用法：
  python3 batch_eval.py [--skills-dir DIR] [--output DIR] [--json]
"""

import argparse
import json
import os
import sys
from pathlib import Path
from datetime import datetime

# 导入单个评估器
sys.path.insert(0, str(Path(__file__).parent))
from skill_evaluator import SkillEvaluator


def batch_evaluate(skills_dir, output_dir=None, json_output=False):
    """批量评估所有 skill"""
    skills_dir = Path(skills_dir)
    output_dir = Path(output_dir) if output_dir else Path(".")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    results = []
    skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and (d / "SKILL.md").exists()]
    
    print(f"发现 {len(skill_dirs)} 个 skill，开始评估...\n")
    
    for skill_path in sorted(skill_dirs):
        skill_name = skill_path.name
        print(f"评估: {skill_name} ...", end=" ", flush=True)
        
        try:
            evaluator = SkillEvaluator(skill_path)
            result = evaluator.evaluate()
            results.append(result)
            print(f"{result['percentage']}% ({result['grade']})")
        except Exception as e:
            print(f"失败: {e}")
            results.append({
                "skill": skill_name,
                "path": str(skill_path),
                "error": str(e),
                "percentage": 0,
                "grade": "ERROR"
            })
    
    # 排序
    results.sort(key=lambda x: x.get("percentage", 0), reverse=True)
    
    # 生成汇总
    summary = {
        "evaluated_at": datetime.now().isoformat(),
        "total_skills": len(skill_dirs),
        "successful": sum(1 for r in results if "error" not in r),
        "failed": sum(1 for r in results if "error" in r),
        "grade_distribution": {
            "A+": sum(1 for r in results if r.get("grade", "").startswith("A+")),
            "A": sum(1 for r in results if r.get("grade", "").startswith("A ")),
            "B": sum(1 for r in results if r.get("grade", "").startswith("B")),
            "C": sum(1 for r in results if r.get("grade", "").startswith("C")),
            "D": sum(1 for r in results if r.get("grade", "").startswith("D")),
            "F": sum(1 for r in results if r.get("grade", "").startswith("F")),
        },
        "average_score": round(sum(r.get("percentage", 0) for r in results) / len(results), 1) if results else 0,
        "results": results
    }
    
    # 保存报告
    report_path = output_dir / f"skill_evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    # 生成 Markdown 报告
    md_path = output_dir / f"skill_evaluation_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    generate_markdown_report(summary, md_path)
    
    if json_output:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*70}")
        print(f"批量评估完成")
        print(f"{'='*70}")
        print(f"评估时间: {summary['evaluated_at']}")
        print(f"总 skill 数: {summary['total_skills']}")
        print(f"成功: {summary['successful']} | 失败: {summary['failed']}")
        print(f"平均分: {summary['average_score']}%")
        print(f"\n等级分布:")
        for grade, count in summary['grade_distribution'].items():
            bar = "█" * count + "░" * (summary['total_skills'] - count)
            print(f"  {grade}: {bar} ({count})")
        
        print(f"\n--- Top 10 ---")
        for i, r in enumerate(results[:10], 1):
            status = "✅" if "error" not in r else "❌"
            print(f"  {status} #{i} {r['skill']}: {r.get('percentage', 0)}% {r.get('grade', 'N/A')}")
        
        if len(results) > 10:
            print(f"\n--- Bottom 5 ---")
            for i, r in enumerate(results[-5:], len(results) - 4):
                status = "✅" if "error" not in r else "❌"
                print(f"  {status} #{i} {r['skill']}: {r.get('percentage', 0)}% {r.get('grade', 'N/A')}")
        
        print(f"\n报告已保存:")
        print(f"  JSON: {report_path}")
        print(f"  Markdown: {md_path}")
        print(f"{'='*70}")
    
    return summary


def generate_markdown_report(summary, path):
    """生成 Markdown 格式的评估报告"""
    lines = [
        "# Skill 质量评估报告",
        "",
        f"**评估时间**: {summary['evaluated_at']}",
        f"**总 Skill 数**: {summary['total_skills']}",
        f"**成功评估**: {summary['successful']} | **失败**: {summary['failed']}",
        f"**平均分**: {summary['average_score']}%",
        "",
        "## 等级分布",
        "",
        "| 等级 | 数量 | 占比 |",
        "|------|------|------|",
    ]
    
    for grade, count in summary['grade_distribution'].items():
        pct = round(count / summary['total_skills'] * 100, 1) if summary['total_skills'] > 0 else 0
        lines.append(f"| {grade} | {count} | {pct}% |")
    
    lines.extend([
        "",
        "## 详细排名",
        "",
        "| 排名 | Skill | 分数 | 等级 | 确定性 | 模型 | 人工 |",
        "|------|-------|------|------|--------|------|------|",
    ])
    
    for i, r in enumerate(summary['results'], 1):
        if "error" in r:
            lines.append(f"| {i} | {r['skill']} | ERROR | ERROR | - | - | - |")
        else:
            scores = r.get('scores', {})
            det = scores.get('deterministic', 0)
            mod = scores.get('model', 0)
            hum = scores.get('human', 0)
            lines.append(f"| {i} | {r['skill']} | {r['percentage']}% | {r['grade']} | {det} | {mod} | {hum} |")
    
    lines.extend([
        "",
        "## 需要重点改进的 Skill",
        "",
    ])
    
    low_scores = [r for r in summary['results'] if r.get('percentage', 100) < 60 and "error" not in r]
    if low_scores:
        for r in low_scores:
            lines.append(f"### {r['skill']} ({r['percentage']}%)")
            lines.append("")
            for rec in r.get('recommendations', []):
                lines.append(f"- {rec}")
            lines.append("")
    else:
        lines.append("所有 Skill 评分均在 60% 以上，质量良好。")
        lines.append("")
    
    with open(path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


def main():
    parser = argparse.ArgumentParser(description="批量 Skill 评估器")
    parser.add_argument("--skills-dir", default="/workspace/.trae/skills", help="Skill 目录")
    parser.add_argument("--output", default="/workspace/OpenClaw/openclaw-main/evals/reports", help="输出目录")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()
    
    batch_evaluate(args.skills_dir, args.output, args.json)


if __name__ == "__main__":
    main()
