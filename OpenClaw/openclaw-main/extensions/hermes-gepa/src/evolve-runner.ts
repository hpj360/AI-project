/**
 * GEPA 进化主循环
 *
 * 将轨迹收集 → 变异引擎 → 帕累托选择 → 约束门控串联为完整进化流程。
 *
 * 完整流程：
 * 1. 读取现有 SKILL.md（基线）
 * 2. 从轨迹采样构建评估集
 * 3. GEPA 变异：分析执行轨迹 → 反思 → 生成候选变体
 * 4. 约束门控：对每个候选运行测试 + 大小检查 + 语义检查
 * 5. 帕累托选择：保留在任意单样本上表现最好的候选
 * 6. 应用改进：备份原 SKILL.md → 替换为改进版
 *
 * 参考：arXiv:2507.19457 (ICLR 2026 Oral)
 */

import fs from "node:fs";
import path from "node:path";
import type {
  EvolveConfig,
  EvolveResult,
  MutationCandidate,
  CandidateEvaluation,
  EvalSampleScore,
  ConstraintGateResult,
  SessionTrace,
} from "./types.js";
import { TraceCollector } from "./trace-collector.js";
import { MutationEngine } from "./mutation-engine.js";
import { ParetoSelector } from "./pareto-selector.js";
import { ConstraintGate } from "./constraint-gate.js";

/** 进化运行器配置 */
export interface EvolveRunnerConfig {
  /** 工作区目录 */
  workspaceDir: string;
  /** .gepa 数据目录 */
  dataDir: string;
  /** 技能目录 */
  skillsDir: string;
  /** skill_evaluator.py 路径 */
  evaluatorPath: string;
  /** LLM 模型 */
  llmModel: string;
  /** API Key */
  apiKey: string;
  /** API Base URL */
  apiBaseUrl: string;
  /** 每次生成的候选数量 */
  numCandidates: number;
  /** 每次评估的样本数量 */
  numEvalSamples: number;
  /** 最大迭代轮次 */
  maxIterations: number;
  /** 日志函数 */
  log: (msg: string) => void;
}

/** 进化运行器 */
export class EvolveRunner {
  private readonly traceCollector: TraceCollector;
  private readonly paretoSelector: ParetoSelector;

  constructor(private readonly config: EvolveRunnerConfig) {
    this.traceCollector = new TraceCollector(config.dataDir);
    this.paretoSelector = new ParetoSelector({ minImprovement: 1.0 });
  }

  /**
   * 发现可进化的技能
   *
   * 扫描技能目录，返回所有包含 SKILL.md 的子目录
   */
  discoverSkills(): string[] {
    try {
      return fs
        .readdirSync(this.config.skillsDir, { withFileTypes: true })
        .filter((entry) => entry.isDirectory())
        .map((entry) => entry.name)
        .filter((name) => {
          const skillPath = path.join(this.config.skillsDir, name, "SKILL.md");
          return fs.existsSync(skillPath);
        });
    } catch {
      return [];
    }
  }

  /**
   * 进化单个技能
   */
  async evolveSkill(skillName: string): Promise<EvolveResult> {
    const skillPath = path.join(this.config.skillsDir, skillName, "SKILL.md");
    const timestamp = new Date().toISOString();

    this.config.log(`[GEPA] 开始进化技能: ${skillName}`);

    // Step 1: 读取现有 SKILL.md
    let baselineContent: string;
    try {
      baselineContent = fs.readFileSync(skillPath, "utf-8");
    } catch {
      return {
        skillName,
        improved: false,
        baselineScore: 0,
        bestScore: 0,
        improvement: 0,
        bestCandidateId: null,
        appliedMutation: null,
        iterations: 0,
        timestamp,
        failureReason: `无法读取 SKILL.md: ${skillPath}`,
      };
    }

    // Step 2: 加载执行轨迹
    const traces = this.traceCollector.loadTraces(this.config.numEvalSamples);

    if (traces.length < 3) {
      this.config.log(`[GEPA] 轨迹不足（${traces.length} < 3），跳过进化`);
      return {
        skillName,
        improved: false,
        baselineScore: 0,
        bestScore: 0,
        improvement: 0,
        bestCandidateId: null,
        appliedMutation: null,
        iterations: 0,
        timestamp,
        failureReason: `执行轨迹不足（${traces.length} < 3）`,
      };
    }

    // Step 3: 评估基线
    const baselineScore = await this.evaluateBaseline(baselineContent);
    this.config.log(`[GEPA] 基线得分: ${baselineScore.toFixed(1)}`);

    // Step 4: 创建变异引擎和约束门控
    const mutationEngine = new MutationEngine({
      model: this.config.llmModel,
      apiKey: this.config.apiKey,
      apiBaseUrl: this.config.apiBaseUrl,
      numCandidates: this.config.numCandidates,
    });

    const constraintGate = new ConstraintGate(
      {
        maxSizeBytes: 15360, // 15KB
        evaluatorPath: this.config.evaluatorPath,
        workspaceDir: this.config.workspaceDir,
      },
      mutationEngine,
    );

    // Step 5: 生成变异候选
    this.config.log(`[GEPA] 生成 ${this.config.numCandidates} 个变异候选...`);
    let candidates: MutationCandidate[];
    try {
      candidates = await mutationEngine.generateMutations(
        baselineContent,
        traces,
      );
    } catch (err) {
      return {
        skillName,
        improved: false,
        baselineScore,
        bestScore: baselineScore,
        improvement: 0,
        bestCandidateId: null,
        appliedMutation: null,
        iterations: 0,
        timestamp,
        failureReason: `变异生成失败: ${err instanceof Error ? err.message : String(err)}`,
      };
    }

    if (candidates.length === 0) {
      return {
        skillName,
        improved: false,
        baselineScore,
        bestScore: baselineScore,
        improvement: 0,
        bestCandidateId: null,
        appliedMutation: null,
        iterations: 0,
        timestamp,
        failureReason: "LLM 未生成有效候选",
      };
    }

    this.config.log(`[GEPA] 生成了 ${candidates.length} 个候选`);

    // Step 6: 评估每个候选
    const evalSamples = ParetoSelector.generateEvalSamples(
      traces,
      this.config.numEvalSamples,
    );

    const evaluations: CandidateEvaluation[] = [];

    for (const candidate of candidates) {
      this.config.log(`[GEPA] 评估候选 ${candidate.id} (${candidate.mutationType})...`);

      // 约束门控
      const gateResult: ConstraintGateResult = await constraintGate.check(
        candidate,
        baselineContent,
        baselineScore,
      );

      if (!gateResult.passed) {
        this.config.log(`[GEPA] 候选 ${candidate.id} 未通过门控: ${gateResult.failureReason}`);
        evaluations.push({
          candidateId: candidate.id,
          sampleScores: [],
          avgScore: gateResult.testScore,
          gateResult,
        });
        continue;
      }

      // 生成样本得分（基于评估样本）
      const sampleScores: EvalSampleScore[] = evalSamples.map((sample) => ({
        sampleId: sample.sampleId,
        score: gateResult.testScore, // 简化：用整体得分作为每个样本的得分
        notes: `评估基于 skill_evaluator.py`,
      }));

      evaluations.push({
        candidateId: candidate.id,
        sampleScores,
        avgScore: gateResult.testScore,
        gateResult,
      });

      this.config.log(
        `[GEPA] 候选 ${candidate.id} 得分: ${gateResult.testScore.toFixed(1)}`,
      );
    }

    // Step 7: 帕累托选择
    const selection = this.paretoSelector.select(evaluations, baselineScore);

    if (!selection.best) {
      this.config.log(`[GEPA] 没有候选优于基线，保留原版`);
      return {
        skillName,
        improved: false,
        baselineScore,
        bestScore: baselineScore,
        improvement: 0,
        bestCandidateId: null,
        appliedMutation: null,
        iterations: 1,
        timestamp,
        failureReason: "没有候选通过帕累托选择",
      };
    }

    // Step 8: 应用改进
    const bestCandidate = candidates.find(
      (c) => c.id === selection.best!.candidateId,
    );

    if (!bestCandidate) {
      return {
        skillName,
        improved: false,
        baselineScore,
        bestScore: selection.best.avgScore,
        improvement: selection.best.avgScore - baselineScore,
        bestCandidateId: selection.best.candidateId,
        appliedMutation: null,
        iterations: 1,
        timestamp,
        failureReason: "找不到最佳候选的原始内容",
      };
    }

    // 备份原 SKILL.md
    const backupDir = path.join(this.config.dataDir, "backups");
    fs.mkdirSync(backupDir, { recursive: true });
    const backupPath = path.join(
      backupDir,
      `${skillName}-${Date.now()}.md`,
    );
    fs.writeFileSync(backupPath, baselineContent, "utf-8");

    // 写入改进版
    fs.writeFileSync(skillPath, bestCandidate.content, "utf-8");

    this.config.log(
      `[GEPA] 技能 ${skillName} 已改进: ${baselineScore.toFixed(1)} → ${selection.best.avgScore.toFixed(1)}`,
    );

    return {
      skillName,
      improved: true,
      baselineScore,
      bestScore: selection.best.avgScore,
      improvement: selection.best.avgScore - baselineScore,
      bestCandidateId: selection.best.candidateId,
      appliedMutation: bestCandidate.mutationType,
      iterations: 1,
      timestamp,
    };
  }

  /**
   * 评估基线 SKILL.md 的得分
   */
  private async evaluateBaseline(skillContent: string): Promise<number> {
    const tmpDir = path.join(this.config.dataDir, "tmp");
    fs.mkdirSync(tmpDir, { recursive: true });

    const tmpFile = path.join(tmpDir, `baseline-${Date.now()}.md`);
    fs.writeFileSync(tmpFile, skillContent, "utf-8");

    try {
      const { spawn } = await import("node:child_process");

      return new Promise<number>((resolve) => {
        const proc = spawn(
          "python3",
          [this.config.evaluatorPath, "--skill", tmpFile, "--format", "json"],
          {
            cwd: this.config.workspaceDir,
            timeout: 30000,
          },
        );

        let stdout = "";
        proc.stdout.on("data", (data: Buffer) => {
          stdout += data.toString();
        });

        proc.on("close", () => {
          try {
            const result = JSON.parse(stdout) as {
              total_score?: number;
              score?: number;
            };
            resolve(result.total_score ?? result.score ?? 50);
          } catch {
            const match = stdout.match(/(\d+(?:\.\d+)?)\s*%/);
            resolve(match ? parseFloat(match[1]) : 50);
          }
        });

        proc.on("error", () => resolve(50));
      });
    } finally {
      try {
        fs.unlinkSync(tmpFile);
      } catch {
        // 忽略
      }
    }
  }

  /**
   * 运行完整进化流程（多个技能）
   */
  async runEvolution(targetSkills: string[]): Promise<EvolveResult[]> {
    const skills =
      targetSkills.length > 0
        ? targetSkills
        : this.discoverSkills();

    this.config.log(`[GEPA] 发现 ${skills.length} 个技能待进化`);

    const results: EvolveResult[] = [];

    for (const skillName of skills) {
      try {
        const result = await this.evolveSkill(skillName);
        results.push(result);
      } catch (err) {
        this.config.log(
          `[GEPA] 进化技能 ${skillName} 时出错: ${err instanceof Error ? err.message : String(err)}`,
        );
        results.push({
          skillName,
          improved: false,
          baselineScore: 0,
          bestScore: 0,
          improvement: 0,
          bestCandidateId: null,
          appliedMutation: null,
          iterations: 0,
          timestamp: new Date().toISOString(),
          failureReason: err instanceof Error ? err.message : String(err),
        });
      }
    }

    // 写入进化日志
    this.writeEvolveLog(results);

    // 清理旧轨迹
    this.traceCollector.cleanupOldTraces(100);

    return results;
  }

  /** 写入进化日志 */
  private writeEvolveLog(results: EvolveResult[]): void {
    const logDir = path.join(this.config.dataDir, "logs");
    fs.mkdirSync(logDir, { recursive: true });

    const logFile = path.join(logDir, `evolve-${Date.now()}.json`);
    fs.writeFileSync(
      logFile,
      JSON.stringify({ timestamp: new Date().toISOString(), results }, null, 2),
      "utf-8",
    );

    // 同时写入 Markdown 格式的可读日志
    const mdFile = path.join(this.config.dataDir, "GEPA_LOG.md");
    const mdContent = [
      `# GEPA 进化日志`,
      ``,
      `> 最后更新: ${new Date().toISOString()}`,
      ``,
      `## 本次进化结果`,
      ``,
      `| 技能 | 基线 | 改进后 | 提升 | 变异类型 | 状态 |`,
      `|------|------|--------|------|---------|------|`,
      ...results.map(
        (r) =>
          `| ${r.skillName} | ${r.baselineScore.toFixed(1)} | ${r.bestScore.toFixed(1)} | ${r.improvement > 0 ? "+" : ""}${r.improvement.toFixed(1)} | ${r.appliedMutation ?? "-"} | ${r.improved ? "✅ 改进" : "❌ 未改进"} |`,
      ),
      ``,
      `## 详细结果`,
      ``,
      ...results.map((r) => {
        const lines = [
          `### ${r.skillName}`,
          ``,
          `- **状态**: ${r.improved ? "✅ 已改进" : "❌ 未改进"}`,
          `- **基线得分**: ${r.baselineScore.toFixed(1)}`,
          `- **改进后得分**: ${r.bestScore.toFixed(1)}`,
          `- **提升幅度**: ${r.improvement > 0 ? "+" : ""}${r.improvement.toFixed(1)}`,
          `- **变异类型**: ${r.appliedMutation ?? "无"}`,
          `- **时间**: ${r.timestamp}`,
        ];
        if (r.failureReason) {
          lines.push(`- **失败原因**: ${r.failureReason}`);
        }
        lines.push("");
        return lines.join("\n");
      }),
    ].join("\n");

    fs.writeFileSync(mdFile, mdContent, "utf-8");
  }
}
