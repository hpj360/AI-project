#!/usr/bin/env python3
"""
GEPA v2.0 vs v3.0 能力对比测试

模拟场景：weather skill 的一个变异候选
- 变异类型：add_checkpoint（增加边界检查）
- 变异内容：在查询天气前增加"网络可用性检查"
- 评估得分：85.3 → 87.1（+1.8，看似改进）

测试 v2.0 和 v3.0 的处理差异：
- v2.0：约束门控通过 → 直接替换 SKILL.md
- v3.0：约束门控通过 → Judge 评判 → 可能否决 → 创建 PR（需人工审查）
"""

import json

# 模拟 Judge 判定结果（v3.0）
JUDGE_VERDICT = {
    "verdict": "reject",
    "confidence": 0.85,
    "reason": "变异声称增加了网络可用性检查，但执行轨迹显示所有查询都成功完成，不存在网络问题。这个 CHECKPOINT 是多余的，增加了不必要的步骤，反而降低了执行效率。变异还增加了'反例与黑名单'章节，这些内容与网络检查无关，是在堆砌关键词以提高评估器分数。",
    "evidence": [
        "执行轨迹中 100% 的天气查询都成功完成，无网络失败案例",
        "新增的 Step 0 网络检查会增加 ~500ms 延迟，降低用户体验",
        "'反例与黑名单'章节与变异理由（add_checkpoint）无关，疑似关键词堆砌",
    ],
    "goodhartRisk": "high",
    "suggestions": [
        "移除 Step 0 网络检查（执行轨迹未显示此问题）",
        "移除无关的'反例与黑名单'章节",
        "如果确实需要网络检查，应在失败时触发而非每次都检查",
    ],
}

JUDGE_APPROVE = {
    "verdict": "approve",
    "confidence": 0.92,
    "reason": "变异增加了 wttr.in 失败时的 Open-Meteo 降级逻辑，执行轨迹显示有 1 次 wttr.in 超时案例，这个改进针对实际问题且不引入无关内容。",
    "evidence": [
        "执行轨迹中有 1 次 wttr.in 超时（sess-003）",
        "新增的降级逻辑直接解决此问题",
        "未堆砌无关关键词",
    ],
    "goodhartRisk": "none",
    "suggestions": [],
}


def print_comparison():
    """打印 v2.0 vs v3.0 对比"""
    
    print("=" * 80)
    print("GEPA v2.0 vs v3.0 能力对比测试")
    print("=" * 80)
    print()
    
    # 场景描述
    print("## 测试场景")
    print()
    print("| 维度 | 值 |")
    print("|------|-----|")
    print("| 技能 | weather |")
    print("| 变异类型 | add_checkpoint |")
    print("| 变异理由 | 增加 Step 0 网络可用性检查 |")
    print("| 基线得分 | 85.3 |")
    print("| 变异得分 | 87.1 (+1.8) |")
    print("| 约束门控 | 通过 |")
    print()
    
    print("### 变异内容摘要")
    print()
    print("+ ### Step 0: 网络可用性检查（新增）")
    print("+ **CHECKPOINT**: 在查询天气前，先检查网络是否可用")
    print("+ ping -c 1 wttr.in")
    print("+")
    print("+ ## 反例与黑名单")
    print("+ - 不要在用户只问天气时自动猜测地点")
    print("+ - 不要使用付费 API")
    print()
    
    # v2.0 处理流程
    print("## v2.0 处理流程（方案 C+D）")
    print()
    print("Step 1: 轨迹收集 -> 2 个会话轨迹")
    print("Step 2: 反思式变异 -> 生成 1 个候选（add_checkpoint）")
    print("Step 3: 约束门控")
    print("        - 大小：2048 字节 <= 15KB [OK]")
    print("        - 语义保持：LLM 判断 [OK]")
    print("        - 评分：87.1 >= 85.3 [OK]")
    print("        -> 通过")
    print("Step 4: 帕累托选择 -> 保留此候选（唯一候选）")
    print("Step 5: 应用改进")
    print("        - 备份原 SKILL.md -> .gepa/backups/weather-xxx.md")
    print("        - 替换为变异版 SKILL.md")
    print("        -> 完成")
    print()
    
    print("### v2.0 结果")
    print()
    print("| 维度 | 值 |")
    print("|------|-----|")
    print("| 最终状态 | 变异已应用 |")
    print("| SKILL.md | 已替换为变异版 |")
    print("| 人工审查 | 无 |")
    print("| 可回滚 | 仅通过备份文件 |")
    print("| 古德哈特风险 | 未检测 |")
    print()
    
    # v3.0 处理流程
    print("## v3.0 处理流程（方案 C+D+Judge+PR）")
    print()
    print("Step 1: 轨迹收集 -> 2 个会话轨迹")
    print("Step 2: 反思式变异 -> 生成 1 个候选（add_checkpoint）")
    print("Step 3: 约束门控")
    print("        - 大小：2048 字节 <= 15KB [OK]")
    print("        - 语义保持：LLM 判断 [OK]")
    print("        - 评分：87.1 >= 85.3 [OK]")
    print("        -> 通过")
    print("Step 4: 帕累托选择 -> 保留此候选（唯一候选）")
    print("Step 5: Judge 评判 <- 新增")
    print("        - 判定：reject")
    print("        - 置信度：85%")
    print("        - 古德哈特风险：high")
    print("        - 理由：变异在钻空子（堆砌关键词、增加无关步骤）")
    print("        -> 否决")
    print("Step 6: 记录建议 -> .gepa/suggestions/weather-xxx.md")
    print("        - 移除 Step 0 网络检查")
    print("        - 移除无关的反例与黑名单章节")
    print("        -> 未应用变异")
    print()
    
    print("### v3.0 结果")
    print()
    print("| 维度 | 值 |")
    print("|------|-----|")
    print("| 最终状态 | 变异未应用（Judge 否决） |")
    print("| SKILL.md | 保持原版 |")
    print("| 人工审查 | Judge 建议已记录 |")
    print("| 可回滚 | 未修改，无需回滚 |")
    print("| 古德哈特风险 | 已检测并拦截 |")
    print()
    
    # Judge 判定详情
    print("### Judge 判定详情")
    print()
    print("| 维度 | 值 |")
    print("|------|-----|")
    print(f"| 判定 | **{JUDGE_VERDICT['verdict']}** |")
    print(f"| 置信度 | {JUDGE_VERDICT['confidence'] * 100:.0f}% |")
    print(f"| 古德哈特风险 | **{JUDGE_VERDICT['goodhartRisk']}** |")
    print()
    
    print("**理由**：")
    print(JUDGE_VERDICT['reason'])
    print()
    
    print("**证据**：")
    for evidence in JUDGE_VERDICT['evidence']:
        print(f"- {evidence}")
    print()
    
    print("**建议**：")
    for suggestion in JUDGE_VERDICT['suggestions']:
        print(f"- {suggestion}")
    print()
    
    # 对比总结
    print("## 对比总结")
    print()
    print("| 维度 | v2.0 | v3.0 | 差异 |")
    print("|------|------|------|------|")
    print("| 变异是否应用 | 是 | 否（Judge 否决） | v3.0 拦截了低质量变异 |")
    print("| 古德哈特检测 | 无 | 有 | v3.0 发现变异在钻空子 |")
    print("| 人工审查 | 无 | 建议记录 | v3.0 提供改进方向 |")
    print("| 可回滚性 | 备份文件 | 未修改 | v3.0 更安全 |")
    print("| 执行效率影响 | 降低（+500ms） | 保持 | v2.0 引入了不必要的检查 |")
    print()
    
    print("### 关键洞察")
    print()
    print("v2.0 的变异虽然通过了约束门控（评分从 85.3 -> 87.1），但实际上是在钻评估器的空子：")
    print()
    print("1. **堆砌关键词**：新增的反例与黑名单章节与变异理由无关，但评估器会给有反例加分")
    print("2. **增加无关步骤**：执行轨迹显示 100% 成功，网络检查是多余的")
    print("3. **降低用户体验**：每次查询前 ping 会增加 ~500ms 延迟")
    print()
    print("v3.0 的 Judge 通过语义理解发现了这些问题，并否决了变异。")
    print()
    
    # 如果 Judge 通过的场景
    print("## 场景 B：Judge 通过的变异")
    print()
    print("假设变异是真正有价值的改进（如增加错误重试机制）：")
    print()
    
    print("### Judge 判定")
    print()
    print("| 维度 | 值 |")
    print("|------|-----|")
    print(f"| 判定 | **{JUDGE_APPROVE['verdict']}** |")
    print(f"| 置信度 | {JUDGE_APPROVE['confidence'] * 100:.0f}% |")
    print(f"| 古德哈特风险 | **{JUDGE_APPROVE['goodhartRisk']}** |")
    print()
    
    print("### v3.0 处理")
    print()
    print("Step 5: Judge 评判 -> approve（置信度 92%）")
    print("Step 6: 自动 PR")
    print("        - 创建分支：gepa/evolve-weather-xxx")
    print("        - 提交变异 + Judge 报告")
    print("        - 推送到 origin")
    print("        - 创建 PR（含变异报告 + 审查指南）")
    print("        -> PR URL: https://github.com/xxx/pull/123")
    print()
    
    print("### 如果启用自动合并")
    print()
    print("autoMerge: true")
    print("confidence >= 0.9 [OK]")
    print("goodhartRisk = none [OK]")
    print("-> 自动合并 PR（squash + delete-branch）")
    print()
    
    print("=" * 80)
    print("测试完成")
    print("=" * 80)


if __name__ == "__main__":
    print_comparison()