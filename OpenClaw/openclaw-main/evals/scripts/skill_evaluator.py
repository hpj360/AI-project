#!/usr/bin/env python3
"""
Skill 质量评估器

基于三层评分体系对 skill 进行系统化评估：
- 确定性评分（20%）：结构合规性、执行效率、稳定性
- 模型评分（60%）：内容质量、工作流清晰度、失败处理、反例覆盖
- 人工审核（20%）：复杂场景、边界情况

用法：
  python3 skill_evaluator.py <skill-path> [--baseline <baseline-path>] [--json]
"""

import argparse
import json
import os
import re
import sys
import yaml
from pathlib import Path


class SkillEvaluator:
    """Skill 质量评估器"""
    
    def __init__(self, skill_path, baseline_path=None):
        self.skill_path = Path(skill_path)
        self.baseline_path = Path(baseline_path) if baseline_path else None
        self.skill_name = self.skill_path.name
        self.skill_md = self.skill_path / "SKILL.md"
        self.scores = {}
        self.issues = []
        
    def evaluate(self):
        """执行完整评估"""
        if not self.skill_md.exists():
            return {"error": f"SKILL.md not found in {self.skill_path}"}
        
        self._deterministic_eval()
        self._model_eval()
        self._human_audit_prep()
        
        total = sum(self.scores.get(k, 0) for k in ["deterministic", "model", "human"])
        max_total = sum(self.scores.get(f"{k}_max", 0) for k in ["deterministic", "model", "human"])
        
        return {
            "skill": self.skill_name,
            "path": str(self.skill_path),
            "total_score": round(total, 2),
            "max_score": max_total,
            "percentage": round(total / max_total * 100, 1) if max_total > 0 else 0,
            "grade": self._grade(total / max_total * 100) if max_total > 0 else "N/A",
            "scores": self.scores,
            "issues": self.issues,
            "recommendations": self._generate_recommendations()
        }
    
    def _deterministic_eval(self):
        """确定性评分（结构合规 + 执行效率 + 稳定性指标）"""
        score = 0
        max_score = 20
        
        # 1. 结构合规性检查（10分）
        structure_score = 0
        
        # 1.1 YAML frontmatter 存在且格式正确（3分）
        content = self.skill_md.read_text(encoding='utf-8')
        if content.startswith('---'):
            try:
                # 提取 frontmatter
                parts = content.split('---', 2)
                if len(parts) >= 3:
                    frontmatter = yaml.safe_load(parts[1])
                    if frontmatter and 'name' in frontmatter and 'description' in frontmatter:
                        structure_score += 3
                    else:
                        self.issues.append("Frontmatter 缺少 name 或 description 字段")
                        structure_score += 1
                else:
                    self.issues.append("Frontmatter 格式不正确")
            except Exception as e:
                self.issues.append(f"Frontmatter YAML 解析失败: {e}")
        else:
            self.issues.append("缺少 YAML frontmatter")
        
        # 1.2 目录结构合规（2分）
        has_scripts = (self.skill_path / "scripts").exists()
        has_references = (self.skill_path / "references").exists()
        if has_scripts or has_references:
            structure_score += 2
        else:
            # 纯 SKILL.md 也可以，不扣分
            structure_score += 2
        
        # 1.3 SKILL.md 内容长度适中（2分）
        lines = content.count('\n')
        if 50 <= lines <= 500:
            structure_score += 2
        elif lines > 500:
            self.issues.append(f"SKILL.md 过长 ({lines} 行)，建议拆分为 references/")
            structure_score += 1
        else:
            self.issues.append(f"SKILL.md 过短 ({lines} 行)，内容可能不完整")
            structure_score += 1
        
        # 1.4 命名规范（1分）
        if re.match(r'^[a-z][a-z0-9-]*$', self.skill_name):
            structure_score += 1
        else:
            self.issues.append("Skill 名称不符合 kebab-case 规范")
        
        # 1.5 描述长度检查（2分）
        desc_match = re.search(r'description:\s*(.+?)(?:\n\w+:|\n---|$)', content, re.DOTALL)
        if desc_match:
            desc = desc_match.group(1).strip()
            desc_len = len(desc)
            if 50 <= desc_len <= 1024:
                structure_score += 2
            elif desc_len > 1024:
                self.issues.append(f"描述过长 ({desc_len} 字符)，建议精简")
                structure_score += 1
            else:
                self.issues.append(f"描述过短 ({desc_len} 字符)，建议增加触发场景")
                structure_score += 1
        
        score += min(structure_score, 10)
        
        # 2. 执行效率指标（5分）— 基于内容推断
        efficiency_score = 0
        
        # 2.1 是否有明确的步骤/流程（2分）
        has_steps = bool(re.search(r'##\s*(?:Step|步骤|流程|Workflow)', content, re.IGNORECASE))
        has_checkpoints = bool(re.search(r'(?:CHECKPOINT|检查点|验证)', content, re.IGNORECASE))
        if has_steps:
            efficiency_score += 2
        else:
            self.issues.append("缺少明确的步骤/流程说明")
        
        if has_checkpoints:
            efficiency_score += 1
        else:
            self.issues.append("缺少 CHECKPOINT 设计，建议增加关键节点验证")
        
        # 2.2 是否有失败处理（2分）
        has_failure = bool(re.search(r'(?:失败|错误|异常|fallback|降级|error|fail)', content, re.IGNORECASE))
        if has_failure:
            efficiency_score += 2
        else:
            self.issues.append("缺少失败处理说明")
        
        score += min(efficiency_score, 5)
        
        # 3. 稳定性指标（5分）
        stability_score = 0
        
        # 3.1 是否有反例/黑名单（2分）
        has_antipatterns = bool(re.search(r'(?:反例|黑名单|禁止|不要|避免|antipattern|blacklist)', content, re.IGNORECASE))
        if has_antipatterns:
            stability_score += 2
        else:
            self.issues.append("缺少反例/黑名单，Agent 容易犯错")
        
        # 3.2 是否有边界情况处理（2分）
        has_edge_cases = bool(re.search(r'(?:边界|edge case|特殊情况|异常输入|空值|超时)', content, re.IGNORECASE))
        if has_edge_cases:
            stability_score += 2
        else:
            self.issues.append("缺少边界情况处理")
        
        # 3.3 是否有版本/兼容性说明（1分）
        has_compat = bool(re.search(r'(?:兼容|compatibility|版本|version|依赖)', content, re.IGNORECASE))
        if has_compat:
            stability_score += 1
        
        score += min(stability_score, 5)
        
        self.scores["deterministic"] = round(score, 2)
        self.scores["deterministic_max"] = max_score
    
    def _model_eval(self):
        """模型评分（内容质量 + 工作流 + 失败处理 + 反例覆盖）"""
        score = 0
        max_score = 60
        content = self.skill_md.read_text(encoding='utf-8')
        
        # 1. 内容质量（20分）
        quality_score = 0
        
        # 1.1 是否有清晰的输入/输出定义（5分）
        has_input = bool(re.search(r'(?:输入|input|参数|argument)', content, re.IGNORECASE))
        has_output = bool(re.search(r'(?:输出|output|返回|result|格式)', content, re.IGNORECASE))
        if has_input and has_output:
            quality_score += 5
        elif has_input or has_output:
            quality_score += 2
            self.issues.append("缺少输入或输出的明确定义")
        else:
            self.issues.append("缺少输入和输出的定义")
        
        # 1.2 是否有示例（5分）
        has_examples = bool(re.search(r'(?:示例|example|Example|```)', content, re.IGNORECASE))
        if has_examples:
            quality_score += 5
        else:
            self.issues.append("缺少使用示例")
        
        # 1.3 是否有 FAQ 或常见问题（5分）
        has_faq = bool(re.search(r'(?:FAQ|常见问题|Q:|问题)', content, re.IGNORECASE))
        if has_faq:
            quality_score += 5
        else:
            self.issues.append("缺少 FAQ 部分")
        
        # 1.4 内容是否具体而非泛泛（5分）
        # 检查是否有具体的命令、路径、参数
        has_commands = bool(re.search(r'`[^`]+`', content))
        has_paths = bool(re.search(r'(?:/\w+|\.py|\.js|\.md)', content))
        if has_commands and has_paths:
            quality_score += 5
        elif has_commands or has_paths:
            quality_score += 3
            self.issues.append("内容可以更具体，增加具体命令和路径")
        else:
            self.issues.append("内容过于泛泛，缺少具体命令和路径")
        
        score += min(quality_score, 20)
        
        # 2. 工作流清晰度（15分）
        workflow_score = 0
        
        # 2.1 是否有分层的执行策略（5分）
        has_layers = bool(re.search(r'(?:Layer|层|降级|fallback|优先级|首选|备用)', content, re.IGNORECASE))
        if has_layers:
            workflow_score += 5
        else:
            self.issues.append("缺少分层执行策略（如 Layer 1/2/3）")
        
        # 2.2 步骤是否有序号或流程图（5分）
        has_numbered_steps = bool(re.search(r'(?:Step \d|步骤\d|###? \d+\.)', content, re.IGNORECASE))
        if has_numbered_steps:
            workflow_score += 5
        else:
            self.issues.append("步骤缺少序号，建议用 Step 1/2/3 或 ①②③ 标注")
        
        # 2.3 是否有明确的判断/分支逻辑（5分）
        has_branching = bool(re.search(r'(?:如果|if|是否|判断|成功|失败|通过|拒绝)', content, re.IGNORECASE))
        if has_branching:
            workflow_score += 5
        else:
            self.issues.append("缺少判断/分支逻辑说明")
        
        score += min(workflow_score, 15)
        
        # 3. 失败处理覆盖度（15分）
        failure_score = 0
        
        # 3.1 是否有明确的失败处理流程（5分）
        has_failure_flow = bool(re.search(r'(?:失败处理|错误处理|异常处理|降级策略|fallback)', content, re.IGNORECASE))
        if has_failure_flow:
            failure_score += 5
        else:
            self.issues.append("缺少失败处理流程")
        
        # 3.2 是否有具体的错误类型和对应处理（5分）
        error_types = ['超时', '超时', '验证码', '限流', '429', '404', '403', '500', '网络', '连接']
        found_errors = sum(1 for e in error_types if e in content)
        if found_errors >= 3:
            failure_score += 5
        elif found_errors >= 1:
            failure_score += 2
            self.issues.append("错误类型覆盖不足，建议增加更多具体错误场景")
        else:
            self.issues.append("缺少具体错误类型说明")
        
        # 3.3 是否有用户通知/回退方案（5分）
        has_notify = bool(re.search(r'(?:告知用户|通知用户|提示用户|替代方案|手动|复制粘贴)', content, re.IGNORECASE))
        if has_notify:
            failure_score += 5
        else:
            self.issues.append("失败时缺少用户通知或替代方案")
        
        score += min(failure_score, 15)
        
        # 4. 反例与黑名单覆盖（10分）
        antipattern_score = 0
        
        # 4.1 是否有明确的禁止行为（5分）
        has_prohibited = bool(re.search(r'(?:禁止|不要|避免|严禁|不得|never|avoid|don\'t)', content, re.IGNORECASE))
        if has_prohibited:
            antipattern_score += 5
        else:
            self.issues.append("缺少禁止行为说明")
        
        # 4.2 是否有错误示例（5分）
        has_bad_example = bool(re.search(r'(?:错误示例|反例|bad example|❌|错误做法)', content, re.IGNORECASE))
        if has_bad_example:
            antipattern_score += 5
        else:
            self.issues.append("缺少错误示例（反例）")
        
        score += min(antipattern_score, 10)
        
        self.scores["model"] = round(score, 2)
        self.scores["model_max"] = max_score
    
    def _human_audit_prep(self):
        """人工审核准备（生成审核清单，实际评分由人工完成）"""
        score = 0
        max_score = 20
        content = self.skill_md.read_text(encoding='utf-8')
        
        # 自动生成人工审核检查清单
        checklist = []
        
        # 1. 复杂场景覆盖（10分）— 检查清单
        checklist.append({
            "item": "复杂输入处理",
            "check": "Skill 是否能处理复杂/异常的输入（如混合文本和 URL、多个链接等）",
            "evidence": "混合输入" in content or "多个" in content or "批量" in content
        })
        checklist.append({
            "item": "多轮交互支持",
            "check": "Skill 是否支持多轮对话中的上下文保持",
            "evidence": "上下文" in content or "多轮" in content or "session" in content.lower()
        })
        checklist.append({
            "item": "安全与隐私",
            "check": "Skill 是否考虑了数据安全和隐私保护",
            "evidence": "隐私" in content or "安全" in content or "PII" in content or "敏感" in content
        })
        
        # 2. 可维护性（5分）
        checklist.append({
            "item": "文档完整性",
            "check": "Skill 是否有足够的文档说明，新用户能否快速上手",
            "evidence": "README" in content or "用法" in content or "使用" in content
        })
        checklist.append({
            "item": "可扩展性",
            "check": "Skill 是否容易扩展新功能或适配新场景",
            "evidence": "扩展" in content or "适配" in content or "配置" in content
        })
        
        # 3. 用户体验（5分）
        checklist.append({
            "item": "输出可读性",
            "check": "Skill 的输出是否清晰、结构化、易于理解",
            "evidence": "表格" in content or "结构化" in content or "Markdown" in content
        })
        checklist.append({
            "item": "反馈机制",
            "check": "Skill 是否提供清晰的进度反馈和状态说明",
            "evidence": "进度" in content or "状态" in content or "反馈" in content
        })
        
        # 根据清单自动打分（保守估计）
        passed = sum(1 for c in checklist if c["evidence"])
        score = (passed / len(checklist)) * max_score if checklist else 0
        
        self.scores["human"] = round(score, 2)
        self.scores["human_max"] = max_score
        self.scores["human_checklist"] = checklist
    
    def _grade(self, percentage):
        """根据百分比给出等级"""
        if percentage >= 90:
            return "A+ (优秀)"
        elif percentage >= 80:
            return "A (良好)"
        elif percentage >= 70:
            return "B (合格)"
        elif percentage >= 60:
            return "C (需改进)"
        elif percentage >= 40:
            return "D (较差)"
        else:
            return "F (不合格)"
    
    def _generate_recommendations(self):
        """生成改进建议"""
        recommendations = []
        
        # 根据分数生成针对性建议
        if self.scores.get("deterministic", 0) < 15:
            recommendations.append("【结构合规】完善 YAML frontmatter，确保 name/description 完整；增加 CHECKPOINT 和失败处理")
        
        if self.scores.get("model", 0) < 40:
            recommendations.append("【内容质量】增加具体示例、FAQ、输入/输出定义；内容更具体化")
        
        if self.scores.get("model", 0) < 30:
            recommendations.append("【工作流】增加分层执行策略（Layer 1/2/3），明确步骤序号和判断分支")
        
        if not any("反例" in i or "黑名单" in i for i in self.issues):
            recommendations.append("【反例覆盖】增加禁止行为和错误示例，降低 Agent 犯错概率")
        
        if not recommendations:
            recommendations.append("Skill 质量良好，建议定期回归测试保持稳定性")
        
        return recommendations


def main():
    parser = argparse.ArgumentParser(description="Skill 质量评估器")
    parser.add_argument("skill_path", help="Skill 目录路径")
    parser.add_argument("--baseline", help="基线数据路径（可选）")
    parser.add_argument("--json", action="store_true", help="输出 JSON 格式")
    args = parser.parse_args()
    
    evaluator = SkillEvaluator(args.skill_path, args.baseline)
    result = evaluator.evaluate()
    
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"\n{'='*60}")
        print(f"Skill 质量评估报告: {result['skill']}")
        print(f"{'='*60}")
        print(f"总分: {result['total_score']}/{result['max_score']} ({result['percentage']}%)")
        print(f"等级: {result['grade']}")
        print(f"\n--- 评分详情 ---")
        print(f"确定性评分: {result['scores']['deterministic']}/{result['scores']['deterministic_max']}")
        print(f"模型评分:   {result['scores']['model']}/{result['scores']['model_max']}")
        print(f"人工审核:   {result['scores']['human']}/{result['scores']['human_max']}")
        
        if result['issues']:
            print(f"\n--- 发现的问题 ({len(result['issues'])} 个) ---")
            for i, issue in enumerate(result['issues'][:10], 1):
                print(f"  {i}. {issue}")
            if len(result['issues']) > 10:
                print(f"  ... 还有 {len(result['issues']) - 10} 个问题")
        
        print(f"\n--- 改进建议 ---")
        for rec in result['recommendations']:
            print(f"  • {rec}")
        
        # 人工审核清单
        if 'human_checklist' in result['scores']:
            print(f"\n--- 人工审核清单（需人工确认）---")
            for item in result['scores']['human_checklist']:
                status = "✅" if item['evidence'] else "❌"
                print(f"  {status} {item['item']}: {item['check']}")
        
        print(f"\n{'='*60}")


if __name__ == "__main__":
    main()
