/**
 * 反思式变异引擎
 *
 * GEPA 核心组件之一：读取执行轨迹和当前 SKILL.md，
 * 通过 LLM 反思"为什么做对了/做错了"，生成改进后的候选变体。
 *
 * 参考：arXiv:2507.19457 (ICLR 2026 Oral)
 */

import fs from "node:fs";
import path from "node:path";
import type {
  SessionTrace,
  MutationCandidate,
  MutationType,
} from "./types.js";

/** 变异引擎配置 */
export interface MutationEngineConfig {
  /** LLM 模型名称（OpenAI 兼容） */
  model: string;
  /** API Key */
  apiKey: string;
  /** API Base URL */
  apiBaseUrl: string;
  /** 生成候选数量 */
  numCandidates: number;
}

/** LLM 消息 */
interface ChatMessage {
  role: "system" | "user" | "assistant";
  content: string;
}

/**
 * 调用 OpenAI 兼容的 Chat Completions API
 */
async function callLLM(
  config: MutationEngineConfig,
  messages: ChatMessage[],
  temperature: number,
): Promise<string> {
  const response = await fetch(`${config.apiBaseUrl}/chat/completions`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${config.apiKey}`,
    },
    body: JSON.stringify({
      model: config.model,
      messages,
      temperature,
      max_tokens: 4096,
    }),
  });

  if (!response.ok) {
    const errorText = await response.text().catch(() => "unknown error");
    throw new Error(`LLM API error ${response.status}: ${errorText}`);
  }

  const data = (await response.json()) as {
    choices: { message: { content: string } }[];
  };

  if (!data.choices?.[0]?.message?.content) {
    throw new Error("LLM API returned empty response");
  }

  return data.choices[0].message.content;
}

/** 将轨迹格式化为可读文本 */
function formatTraces(traces: SessionTrace[]): string {
  return traces
    .map((t, i) => {
      const toolSummary = t.toolCalls
        .map(
          (tc) =>
            `  - ${tc.tool}(${tc.params.slice(0, 100)}) → ${tc.success ? "✓" : "✗"} ${tc.result.slice(0, 100)}`,
        )
        .join("\n");
      return `Trace #${i + 1}: "${t.prompt.slice(0, 200)}"\n${toolSummary}`;
    })
    .join("\n\n");
}

/** 解析 LLM 返回的候选变体 */
function parseCandidates(
  response: string,
  count: number,
): MutationCandidate[] {
  const candidates: MutationCandidate[] = [];

  // 尝试解析 JSON 格式的响应
  try {
    const parsed = JSON.parse(response);
    if (Array.isArray(parsed)) {
      for (const item of parsed) {
        if (item.content && typeof item.content === "string") {
          candidates.push({
            id: `mut-${Date.now()}-${candidates.length}`,
            content: item.content,
            rationale: item.rationale ?? "无说明",
            mutationType: (item.type as MutationType) ?? "other",
            createdAt: new Date().toISOString(),
          });
        }
      }
      return candidates;
    }
  } catch {
    // 不是 JSON，尝试其他解析方式
  }

  // 尝试按分隔符分割
  const blocks = response.split(/---CANDIDATE\s*\d*---/).filter((s) => s.trim());
  if (blocks.length > 0) {
    for (let i = 0; i < Math.min(blocks.length, count); i++) {
      const block = blocks[i].trim();
      // 提取 rationale（第一行如果是注释）
      const lines = block.split("\n");
      const rationaleLine = lines.find((l) => l.startsWith("RATIONALE:"));
      const rationale = rationaleLine
        ? rationaleLine.replace("RATIONALE:", "").trim()
        : "LLM 生成变体";
      const content = block
        .replace(/^RATIONALE:.*$/m, "")
        .trim();

      candidates.push({
        id: `mut-${Date.now()}-${i}`,
        content,
        rationale,
        mutationType: detectMutationType(content, rationale),
        createdAt: new Date().toISOString(),
      });
    }
  }

  return candidates;
}

/** 检测变异类型 */
function detectMutationType(content: string, rationale: string): MutationType {
  const text = (content + " " + rationale).toLowerCase();
  if (text.includes("checkpoint")) return "add_checkpoint";
  if (text.includes("reorder") || text.includes("顺序")) return "reorder_steps";
  if (text.includes("failure") || text.includes("失败")) return "add_failure_handling";
  if (text.includes("example") || text.includes("示例")) return "add_example";
  if (text.includes("trigger") || text.includes("触发")) return "refine_trigger";
  if (text.includes("compress") || text.includes("压缩") || text.includes("精简")) return "compress";
  return "other";
}

/** 变异引擎 */
export class MutationEngine {
  constructor(private readonly config: MutationEngineConfig) {}

  /**
   * 生成变异候选
   *
   * @param skillContent 当前 SKILL.md 内容
   * @param traces 执行轨迹
   * @returns 变异候选列表
   */
  async generateMutations(
    skillContent: string,
    traces: SessionTrace[],
  ): Promise<MutationCandidate[]> {
    const tracesText = formatTraces(traces);

    const systemPrompt = `你是一个 GEPA（遗传-帕累托提示进化）变异引擎。
你的任务是分析 AI Agent 的执行轨迹，反思"为什么做对了/做错了"，
然后生成改进后的 SKILL.md 变体。

变异原则：
1. 反思式变异：基于执行轨迹中的具体问题进行改进，而非随机修改
2. 多样性：生成不同类型的变异（增加检查点、调整步骤顺序、增加失败处理等）
3. 最小化改动：只修改需要改进的部分，保留有效内容
4. 保持格式：SKILL.md 的 YAML frontmatter 必须保留

变异类型：
- add_checkpoint: 增加 CHECKPOINT 验证步骤
- reorder_steps: 调整步骤顺序（如先检查再执行）
- add_failure_handling: 增加失败处理流程
- add_example: 增加示例或反例
- refine_trigger: 优化触发条件
- compress: 压缩冗余内容`;

    const userPrompt = `## 当前 SKILL.md

${skillContent}

## 执行轨迹（最近 ${traces.length} 个会话）

${tracesText}

## 任务

分析上述执行轨迹，找出 SKILL.md 中可以改进的地方。
生成 ${this.config.numCandidates} 个改进候选变体。

每个候选必须包含：
1. rationale: 改进理由（为什么这样改）
2. type: 变异类型（add_checkpoint/reorder_steps/add_failure_handling/add_example/refine_trigger/compress/other）
3. content: 完整的改进后 SKILL.md 内容

请以 JSON 数组格式返回：
\`\`\`json
[
  {
    "rationale": "执行轨迹显示步骤3后没有验证结果，增加了 CHECKPOINT",
    "type": "add_checkpoint",
    "content": "---\\nname: ...\\n---\\n# 完整的 SKILL.md 内容"
  }
]
\`\`\``;

    const response = await callLLM(
      this.config,
      [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
      0.8, // 较高温度促进多样性
    );

    const candidates = parseCandidates(response, this.config.numCandidates);

    if (candidates.length === 0) {
      // 如果解析失败，返回空数组
      return [];
    }

    return candidates;
  }

  /**
   * 检查语义保持（变异后的 SKILL.md 是否偏离原始目的）
   */
  async checkSemanticPreservation(
    original: string,
    mutated: string,
  ): Promise<boolean> {
    const systemPrompt = `你是一个语义保持检查器。判断变异后的 SKILL.md 是否偏离了原始目的。

判断标准：
- 核心功能是否改变？（如从"搜索"变成了"下载"）
- 触发条件是否偏离？（如从"用户要求搜索"变成了"用户要求删除"）
- 如果只是增加步骤、调整顺序、增加检查点，不算偏离

只返回 true 或 false。`;

    const userPrompt = `## 原始 SKILL.md（前 500 字符）

${original.slice(0, 500)}

## 变异后 SKILL.md（前 500 字符）

${mutated.slice(0, 500)}

## 变异是否偏离原始目的？只返回 true 或 false。`;

    const response = await callLLM(
      this.config,
      [
        { role: "system", content: systemPrompt },
        { role: "user", content: userPrompt },
      ],
      0.1, // 低温度确保确定性
    );

    return response.trim().toLowerCase().startsWith("true");
  }
}
