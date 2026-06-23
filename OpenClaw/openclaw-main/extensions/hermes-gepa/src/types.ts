/**
 * GEPA 引擎类型定义
 *
 * 基于 GEPA 算法（arXiv:2507.19457, ICLR 2026 Oral），
 * 在 OpenClaw 内部实现反思式变异 + 帕累托前沿选择 + 约束门控。
 */

// ─── 执行轨迹 ────────────────────────────────────────────

/** 单次工具调用记录 */
export interface ToolCallTrace {
  /** 工具名称 */
  tool: string;
  /** 调用参数摘要（截断到 500 字符） */
  params: string;
  /** 返回结果摘要（截断到 500 字符） */
  result: string;
  /** 是否成功 */
  success: boolean;
  /** 耗时（毫秒） */
  durationMs: number;
  /** 时间戳 */
  ts: string;
}

/** 会话轨迹 */
export interface SessionTrace {
  /** 会话键 */
  sessionKey: string;
  /** 用户 prompt 摘要 */
  prompt: string;
  /** 工具调用序列 */
  toolCalls: ToolCallTrace[];
  /** 会话开始时间 */
  startTime: string;
  /** 会话结束时间 */
  endTime: string;
}

// ─── 变异 ────────────────────────────────────────────────

/** 变异候选 */
export interface MutationCandidate {
  /** 候选 ID */
  id: string;
  /** 变异后的 SKILL.md 内容 */
  content: string;
  /** 变异说明（LLM 生成的反思） */
  rationale: string;
  /** 变异类型 */
  mutationType: MutationType;
  /** 生成时间 */
  createdAt: string;
}

/** 变异类型 */
export type MutationType =
  | "add_checkpoint"      // 增加 CHECKPOINT
  | "reorder_steps"       // 调整步骤顺序
  | "add_failure_handling" // 增加失败处理
  | "add_example"         // 增加示例
  | "refine_trigger"      // 优化触发条件
  | "compress"            // 压缩冗余内容
  | "other";              // 其他

// ─── 评估 ────────────────────────────────────────────────

/** 单个评估样本的得分 */
export interface EvalSampleScore {
  /** 样本 ID */
  sampleId: string;
  /** 得分（0-100） */
  score: number;
  /** 评估说明 */
  notes: string;
}

/** 候选的评估结果 */
export interface CandidateEvaluation {
  /** 候选 ID */
  candidateId: string;
  /** 各样本得分 */
  sampleScores: EvalSampleScore[];
  /** 平均分 */
  avgScore: number;
  /** 约束门控结果 */
  gateResult: ConstraintGateResult;
}

// ─── 约束门控 ────────────────────────────────────────────

/** 约束门控结果 */
export interface ConstraintGateResult {
  /** 是否通过 */
  passed: boolean;
  /** 测试得分（skill_evaluator.py 输出，0-100） */
  testScore: number;
  /** 文件大小（字节） */
  sizeBytes: number;
  /** 是否大小合规（≤ 15KB） */
  sizeOk: boolean;
  /** 语义是否保持（LLM 判断） */
  semanticPreserved: boolean;
  /** 失败原因（如果未通过） */
  failureReason?: string;
}

// ─── 进化运行 ────────────────────────────────────────────

/** GEPA 进化运行配置 */
export interface EvolveConfig {
  /** 要进化的技能名称 */
  skillName: string;
  /** SKILL.md 文件路径 */
  skillPath: string;
  /** 变异候选数量 */
  numCandidates: number;
  /** 评估样本数量 */
  numEvalSamples: number;
  /** 最大迭代轮次 */
  maxIterations: number;
  /** LLM 模型（用于变异） */
  llmModel: string;
  /** skill_evaluator.py 路径 */
  evaluatorPath: string;
}

/** GEPA 进化运行结果 */
export interface EvolveResult {
  /** 技能名称 */
  skillName: string;
  /** 是否找到改进 */
  improved: boolean;
  /** 基线得分 */
  baselineScore: number;
  /** 最佳候选得分 */
  bestScore: number;
  /** 改进幅度 */
  improvement: number;
  /** 最佳候选 ID */
  bestCandidateId: string | null;
  /** 应用的变异类型 */
  appliedMutation: MutationType | null;
  /** 迭代轮次 */
  iterations: number;
  /** 时间戳 */
  timestamp: string;
  /** 失败原因（如果未改进） */
  failureReason?: string;
}

// ─── GEPA 引擎状态 ───────────────────────────────────────

/** GEPA 引擎运行状态 */
export type GepaState = "idle" | "collecting" | "evolving" | "applying";

/** GEPA 引擎状态快照 */
export interface GepaStateSnapshot {
  state: GepaState;
  /** 当前进化的技能 */
  currentSkill: string | null;
  /** 当前迭代轮次 */
  currentIteration: number;
  /** 已收集的轨迹数 */
  traceCount: number;
  /** 上次进化时间 */
  lastEvolveTime: string | null;
  /** 上次进化结果 */
  lastResult: EvolveResult | null;
  /** 进化历史 */
  history: EvolveResult[];
}

// ─── 插件配置 ────────────────────────────────────────────

/** hermes-gepa 插件配置 */
export interface GepaPluginConfig {
  /** 是否启用 GEPA 周期性评估提醒（方案 C） */
  reminderEnabled: boolean;
  /** 触发评估提醒的工具调用次数阈值 */
  reminderThreshold: number;
  /** 是否启用 GEPA 引擎（方案 D） */
  engineEnabled: boolean;
  /** GEPA 引擎触发间隔（小时） */
  engineIntervalHours: number;
  /** 每次进化生成的候选数量 */
  numCandidates: number;
  /** 每次评估的样本数量 */
  numEvalSamples: number;
  /** 最大迭代轮次 */
  maxIterations: number;
  /** 变异用的 LLM 模型 */
  llmModel: string;
  /** skill_evaluator.py 路径 */
  evaluatorPath: string;
  /** 要进化的技能列表（空 = 自动发现所有技能） */
  targetSkills: string[];
  /** .gepa 数据目录（相对于 workspace） */
  dataDir: string;
}
