/**
 * 帕累托前沿选择器
 *
 * GEPA 核心组件之二：不保留全局平均分最高的候选，
 * 而是保留在任意单个评估样本上表现最好的候选。
 * 确保技能探索的多样性和鲁棒性。
 *
 * 参考：arXiv:2507.19457 (ICLR 2026 Oral)
 */

import type {
  MutationCandidate,
  CandidateEvaluation,
  EvalSampleScore,
  ConstraintGateResult,
} from "./types.js";

/** 帕累托选择器配置 */
export interface ParetoSelectorConfig {
  /** 最小改进幅度（候选必须比基线高出此值才被保留） */
  minImprovement: number;
}

/** 帕累托前沿选择结果 */
export interface ParetoSelectionResult {
  /** 被选中的候选 */
  selected: CandidateEvaluation[];
  /** 被淘汰的候选 */
  eliminated: CandidateEvaluation[];
  /** 基线得分 */
  baselineScore: number;
  /** 最佳候选（帕累托前沿中平均分最高的） */
  best: CandidateEvaluation | null;
}

export class ParetoSelector {
  constructor(private readonly config: ParetoSelectorConfig) {}

  /**
   * 执行帕累托前沿选择
   *
   * 算法：
   * 1. 过滤掉未通过约束门控的候选
   * 2. 过滤掉平均分低于基线 + minImprovement 的候选
   * 3. 计算帕累托前沿：候选 A 支配候选 B 当且仅当 A 在所有样本上 ≥ B，且至少一个样本上 > B
   * 4. 保留帕累托前沿中的候选
   * 5. 从前沿中选择平均分最高的作为最佳候选
   *
   * @param candidates 所有候选的评估结果
   * @param baselineScore 基线（当前 SKILL.md）的平均分
   */
  select(
    candidates: CandidateEvaluation[],
    baselineScore: number,
  ): ParetoSelectionResult {
    // Step 1: 过滤未通过约束门控的候选
    const gatePassed = candidates.filter((c) => c.gateResult.passed);

    // Step 2: 过滤得分低于基线 + minImprovement 的候选
    const threshold = baselineScore + this.config.minImprovement;
    const qualified = gatePassed.filter((c) => c.avgScore >= threshold);

    if (qualified.length === 0) {
      return {
        selected: [],
        eliminated: candidates,
        baselineScore,
        best: null,
      };
    }

    // Step 3: 计算帕累托前沿
    const paretoFront = this.computeParetoFront(qualified);

    // Step 4: 标记被淘汰的候选
    const paretoIds = new Set(paretoFront.map((c) => c.candidateId));
    const eliminated = candidates.filter((c) => !paretoIds.has(c.candidateId));

    // Step 5: 选择平均分最高的作为最佳候选
    const best = paretoFront.reduce(
      (best, current) => (current.avgScore > best.avgScore ? current : best),
      paretoFront[0],
    );

    return {
      selected: paretoFront,
      eliminated,
      baselineScore,
      best,
    };
  }

  /**
   * 计算帕累托前沿
   *
   * 候选 A 支配候选 B 当且仅当：
   * - A 在所有样本上得分 ≥ B
   * - A 至少在一个样本上得分 > B
   *
   * 帕累托前沿 = 不被任何其他候选支配的候选集合
   */
  private computeParetoFront(
    candidates: CandidateEvaluation[],
  ): CandidateEvaluation[] {
    const front: CandidateEvaluation[] = [];

    for (const candidate of candidates) {
      let isDominated = false;

      for (const other of candidates) {
        if (other.candidateId === candidate.candidateId) continue;

        if (this.dominates(other, candidate)) {
          isDominated = true;
          break;
        }
      }

      if (!isDominated) {
        front.push(candidate);
      }
    }

    return front;
  }

  /**
   * 判断 candidate A 是否支配 candidate B
   *
   * A 支配 B 当且仅当：
   * - A 在所有样本上得分 ≥ B
   * - A 至少在一个样本上得分 > B
   */
  private dominates(a: CandidateEvaluation, b: CandidateEvaluation): boolean {
    const aScores = this.getScoreMap(a);
    const bScores = this.getScoreMap(b);

    const sampleIds = new Set([...aScores.keys(), ...bScores.keys()]);

    let atLeastOneGreater = false;

    for (const sampleId of sampleIds) {
      const aScore = aScores.get(sampleId) ?? 0;
      const bScore = bScores.get(sampleId) ?? 0;

      if (aScore < bScore) {
        // A 在某个样本上比 B 差，A 不支配 B
        return false;
      }
      if (aScore > bScore) {
        atLeastOneGreater = true;
      }
    }

    return atLeastOneGreater;
  }

  /** 获取候选的样本得分映射 */
  private getScoreMap(candidate: CandidateEvaluation): Map<string, number> {
    const map = new Map<string, number>();
    for (const score of candidate.sampleScores) {
      map.set(score.sampleId, score.score);
    }
    return map;
  }

  /**
   * 从执行轨迹生成评估样本
   *
   * 将轨迹转换为评估样本，每个样本包含：
   * - 样本 ID
   * - 用户 prompt（作为评估输入）
   * - 期望的工具调用序列（作为评估标准）
   */
  static generateEvalSamples(
    traces: import("./types.js").SessionTrace[],
    maxSamples: number,
  ): { sampleId: string; prompt: string; expectedTools: string[] }[] {
    // 选择有代表性的轨迹（成功和失败各取一些）
    const successful = traces.filter((t) =>
      t.toolCalls.every((tc) => tc.success),
    );
    const failed = traces.filter((t) =>
      t.toolCalls.some((tc) => !tc.success),
    );

    // 各取一半，确保多样性
    const halfMax = Math.floor(maxSamples / 2);
    const selected = [
      ...successful.slice(0, halfMax),
      ...failed.slice(0, maxSamples - halfMax),
    ];

    // 如果不够，用剩余的补
    if (selected.length < maxSamples) {
      const remaining = traces.filter(
        (t) => !selected.includes(t),
      );
      selected.push(...remaining.slice(0, maxSamples - selected.length));
    }

    return selected.map((t, i) => ({
      sampleId: `sample-${i + 1}`,
      prompt: t.prompt,
      expectedTools: t.toolCalls.map((tc) => tc.tool),
    }));
  }
}
