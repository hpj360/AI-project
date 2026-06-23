/**
 * 独立评判器（Judge）
 *
 * Hermes 的 Judge 机制核心：用一个独立的 LLM 调用判定结果是否真正达标，
 * 避免执行模型"自评总是通过"的自我偏见。
 *
 * 两种模式：
 * 1. GEPA Judge — 判定 GEPA 变异是否是真正的改进（古德哈特定律防护）
 * 2. Goal Judge  — 判定 /goal 循环是否达到验收标准
 *
 * 关键设计：
 * - Judge 使用与变异引擎不同的 prompt（角色分离）
 * - Judge 看到的是"原始版 + 变异版 + 执行轨迹 + 评估分数"，而非只看分数
 * - Judge 可以否决通过约束门控的变异（防止钻空子）
 */

import type {
  SessionTrace,
  MutationCandidate,
  ConstraintGateResult,
  JudgeVerdict,
  GoalJudgeResult,
} from "./types.js";

/** Judge 配置 */
export interface JudgeConfig {
  /** LLM 模型名称（OpenAI 兼容） */
  model: string;
  /** API Key */
  apiKey: string;
  /** API Base URL */
  apiBaseUrl: string;
  /** Judge 模型（建议用不同于变异引擎的模型，避免同源偏见） */
  judgeModel?: string;
}

/** LLM 消息 */
interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

/** 调用 OpenAI 兼容的 Chat Completions API */
async function callLLM(
  config: JudgeConfig,
  messages: ChatMessage[],
  temperature: number,
): Promise<string> {
  const model = config.judgeModel ?? config.model;
  const response = await fetch(`${config.apiBaseUrl}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${config.apiKey}`,
    },
    body: JSON.stringify({
      model,
      messages,
      temperature,
      max_tokens: 2048,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => "unknown error");
    throw new Error(`Judge LLM API error ${response.status}: ${errorText}`);
  }

  const data = (await response.json()) as {
    choices: { message: { content: string } }[];
  };

  if (!data.choices?.[0]?.message?.content) {
    throw new Error("Judge LLM API returned empty response");
  }

  return data.choices[0].message.content;
}

/** 将轨迹格式化为可读文本 */
function formatTraces(traces: SessionTrace[]): string {
  return traces
    .slice(0, 5)
    .map((t, i) => {
      const toolSummary = t.toolCalls
        .slice(0, 10)
        .map(
          (tc) =>
            `  - ${tc.tool}(${tc.params.slice(0, 80)}) → ${tc.success ? "✓" : "✗"} ${tc.result.slice(0, 80)}`,
        )
        .join("\n");
      return `Trace #${i + 1}: "${t.prompt.slice(0, 150)}"\n${toolSummary}`;
    })
    .join("\n\n");
}

/** 独立评判器 */
export class Judge {
  constructor(private readonly config: JudgeConfig) {}

  /**
   * GEPA Judge：判定变异是否是真正的改进
   *
   * 这是约束门控之后的第二道防线：
   * - 约束门控检查：大小 + 语义 + 评分（可能被钻空子）
   * - Judge 检查：变异是否真正解决了执行轨迹中的问题
   *
   * 古德哈特定律防护：
   * "当一个指标成为目标时，它就不再是一个好指标"
   * skill_evaluator.py 的评分可能被变异引擎钻空子（如堆砌关键词），
   * Judge 通过语义理解来判断改进是否真实。
   */
  async judgeMutation(
    original: string,
    candidate: MutationCandidate,
    gateResult: ConstraintGateResult,
    traces: SessionTrace[],
    baselineScore: number,
  ): Promise<JudgeVerdict> {
    const systemPrompt = `你是一个独立的 GEPA 评判器（Judge）。
你的职责是判定一个 SKILL.md 变异是否是真正的改进，还是在钻评估器的空子。

判定维度：
1. **问题相关性**：变异是否针对执行轨迹中暴露的实际问题？
2. **改进实质性**：变异是否带来了实质性的改进，而非堆砌关键词或格式？
3. **无副作用**：变异是否引入了新的风险或问题？
4. **古德哈特防护**：变异是否只是在优化评估器分数而非真正提升技能质量？

判定标准：
- approve: 变异是真正的改进，可以应用
- reject: 变异在钻空子或无实质改进
- needs_revision: 变异方向正确但需要调整

你必须返回 JSON 格式：
{
  "verdict": "approve" | "reject" | "needs_revision",
  "confidence": 0.0-1.0,
  "reason": "判定理由",
  "evidence": ["具体证据1", "具体证据2"],
  "goodhart_risk": "none" | "low" | "medium" | "high",
  "suggestions": ["改进建议（如果 needs_revision）"]
}`;

    const userPrompt = `## 原始 SKILL.md（前 800 字符）

${original.slice(0, 800)}

## 变异后 SKILL.md（前 800 字符）

${candidate.content.slice(0, 800)}

## 变异说明

- 类型: ${candidate.mutationType}
- 理由: ${candidate.rationale}

## 约束门控结果

- 通过: ${gateResult.passed}
- 评分: ${gateResult.testScore.toFixed(1)}（基线: ${baselineScore.toFixed(1)}）
- 大小: ${gateResult.sizeBytes} 字节
- 语义保持: ${gateResult.semanticPreserved}

## 执行轨迹（最近 ${traces.length} 个会话）

${formatTraces(traces)}

## 请判定

这个变异是否是真正的改进？还是在钻评估器的空子？
请返回 JSON。`;

    try {
      const response = await callLLM(
        this.config,
        [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt },
        ],
        0.2, // 低温度确保判定确定性
      );

      return this.parseVerdict(response);
    } catch (err) {
      // Judge 调用失败时，保守处理：不否决（让约束门控结果生效）
      return {
        verdict: "approve",
        confidence: 0.0,
        reason: `Judge 调用失败，降级为约束门控结果: ${err instanceof Error ? err.message : String(err)}`,
        evidence: [],
        goodhartRisk: "unknown",
        suggestions: [],
      };
    }
  }

  /**
   * Goal Judge：判定 /goal 循环是否达到验收标准
   *
   * 用于 loop-engineering skill 的 /goal 命令：
   * - 每轮执行后，Judge 独立判定目标是否达成
   * - 避免执行模型"自评总是通过"
   * - Judge 看到的是：目标定义 + 验收标准 + 执行结果
   */
  async judgeGoal(
    goal: string,
    acceptanceCriteria: string[],
    executionLog: string,
    round: number,
    maxRounds: number,
  ): Promise<GoalJudgeResult> {
    const systemPrompt = `你是一个独立的目标验收评判器（Goal Judge）。
你的职责是判定一个 /goal 循环的目标是否已经达成。

判定原则：
1. **严格标准**：必须所有验收标准都满足才能判定 "done"
2. **证据导向**：判定必须基于执行日志中的具体证据，而非模型的自评
3. **防止自评偏见**：执行模型可能声称"已完成"，但你需要验证证据
4. **防止过早停止**：如果证据不足，应该判定 "continue"

返回 JSON 格式：
{
  "verdict": "done" | "continue",
  "confidence": 0.0-1.0,
  "reason": "判定理由",
  "criteria_met": [true, false, ...],
  "evidence": ["证据1", "证据2"],
  "next_action": "如果 continue，下一步建议做什么"
}`;

    const userPrompt = `## 目标

${goal}

## 验收标准

${acceptanceCriteria.map((c, i) => `${i + 1}. ${c}`).join("\n")}

## 第 ${round}/${maxRounds} 轮执行日志

${executionLog.slice(0, 3000)}

## 请判定

目标是否已达成？请逐条检查验收标准，返回 JSON。`;

    try {
      const response = await callLLM(
        this.config,
        [
          { role: "system", content: systemPrompt },
          { role: "user", content: userPrompt },
        ],
        0.2,
      );

      return this.parseGoalVerdict(response, acceptanceCriteria.length);
    } catch (err) {
      // Judge 调用失败时，保守处理：继续执行
      return {
        verdict: "continue",
        confidence: 0.0,
        reason: `Judge 调用失败，保守继续: ${err instanceof Error ? err.message : String(err)}`,
        criteriaMet: acceptanceCriteria.map(() => false),
        evidence: [],
        nextAction: "重试或手动检查目标是否达成",
      };
    }
  }

  /** 解析 GEPA Judge 的判定结果 */
  private parseVerdict(response: string): JudgeVerdict {
    try {
      const parsed = JSON.parse(response) as {
        verdict?: string;
        confidence?: number;
        reason?: string;
        evidence?: string[];
        goodhart_risk?: string;
        suggestions?: string[];
      };

      return {
        verdict: (parsed.verdict as JudgeVerdict["verdict"]) ?? "approve",
        confidence: parsed.confidence ?? 0.5,
        reason: parsed.reason ?? "无理由",
        evidence: parsed.evidence ?? [],
        goodhartRisk:
          (parsed.goodhart_risk as JudgeVerdict["goodhartRisk"]) ?? "unknown",
        suggestions: parsed.suggestions ?? [],
      };
    } catch {
      // JSON 解析失败，尝试从文本提取
      const text = response.toLowerCase();
      if (text.includes("reject")) {
        return {
          verdict: "reject",
          confidence: 0.5,
          reason: response.slice(0, 500),
          evidence: [],
          goodhartRisk: "unknown",
          suggestions: [],
        };
      }
      if (text.includes("needs_revision") || text.includes("needs revision")) {
        return {
          verdict: "needs_revision",
          confidence: 0.5,
          reason: response.slice(0, 500),
          evidence: [],
          goodhartRisk: "unknown",
          suggestions: [],
        };
      }
      return {
        verdict: "approve",
        confidence: 0.5,
        reason: response.slice(0, 500),
        evidence: [],
        goodhartRisk: "unknown",
        suggestions: [],
      };
    }
  }

  /** 解析 Goal Judge 的判定结果 */
  private parseGoalVerdict(
    response: string,
    criteriaCount: number,
  ): GoalJudgeResult {
    try {
      const parsed = JSON.parse(response) as {
        verdict?: string;
        confidence?: number;
        reason?: string;
        criteria_met?: boolean[];
        evidence?: string[];
        next_action?: string;
      };

      return {
        verdict:
          (parsed.verdict as GoalJudgeResult["verdict"]) ?? "continue",
        confidence: parsed.confidence ?? 0.5,
        reason: parsed.reason ?? "无理由",
        criteriaMet:
          parsed.criteria_met ?? new Array(criteriaCount).fill(false),
        evidence: parsed.evidence ?? [],
        nextAction: parsed.next_action ?? "继续执行",
      };
    } catch {
      const text = response.toLowerCase();
      return {
        verdict: text.includes("done") ? "done" : "continue",
        confidence: 0.5,
        reason: response.slice(0, 500),
        criteriaMet: new Array(criteriaCount).fill(false),
        evidence: [],
        nextAction: "继续执行",
      };
    }
  }
}
