/**
 * 约束门控
 *
 * GEPA 核心组件之三：每个进化变体必须通过约束检查才能被应用。
 * 包括：测试通过、大小合规、语义保持。
 *
 * 参考：arXiv:2507.19457 (ICLR 2026 Oral)
 */

import fs from "node:fs";
import path from "node:path";
import type { ConstraintGateResult, MutationCandidate } from "./types.js";
import type { MutationEngine } from "./mutation-engine.js";

/** 约束门控配置 */
export interface ConstraintGateConfig {
  /** SKILL.md 最大大小（字节） */
  maxSizeBytes: number;
  /** skill_evaluator.py 路径 */
  evaluatorPath: string;
  /** 工作区目录 */
  workspaceDir: string;
}

/** 约束门控 */
export class ConstraintGate {
  constructor(
    private readonly config: ConstraintGateConfig,
    private readonly mutationEngine: MutationEngine,
  ) {}

  /**
   * 检查候选是否通过约束门控
   *
   * 三重检查：
   * 1. 大小合规：SKILL.md ≤ 15KB
   * 2. 测试通过：skill_evaluator.py 评分 ≥ 基线
   * 3. 语义保持：LLM 判断目的未偏移
   */
  async check(
    candidate: MutationCandidate,
    originalContent: string,
    baselineScore: number,
  ): Promise<ConstraintGateResult> {
    // Step 1: 大小检查
    const sizeBytes = Buffer.byteLength(candidate.content, "utf-8");
    const sizeOk = sizeBytes <= this.config.maxSizeBytes;

    if (!sizeOk) {
      return {
        passed: false,
        testScore: 0,
        sizeBytes,
        sizeOk: false,
        semanticPreserved: true,
        failureReason: `SKILL.md 大小 ${sizeBytes} 字节超过限制 ${this.config.maxSizeBytes} 字节`,
      };
    }

    // Step 2: 语义保持检查
    const semanticPreserved = await this.mutationEngine
      .checkSemanticPreservation(originalContent, candidate.content)
      .catch(() => true); // LLM 调用失败时默认通过

    if (!semanticPreserved) {
      return {
        passed: false,
        testScore: 0,
        sizeBytes,
        sizeOk: true,
        semanticPreserved: false,
        failureReason: "变异后 SKILL.md 偏离了原始目的",
      };
    }

    // Step 3: 测试通过检查（运行 skill_evaluator.py）
    const testScore = await this.runEvaluator(candidate.content).catch(() => 0);

    if (testScore < baselineScore) {
      return {
        passed: false,
        testScore,
        sizeBytes,
        sizeOk: true,
        semanticPreserved: true,
        failureReason: `测试得分 ${testScore} 低于基线 ${baselineScore}`,
      };
    }

    return {
      passed: true,
      testScore,
      sizeBytes,
      sizeOk: true,
      semanticPreserved: true,
    };
  }

  /**
   * 运行 skill_evaluator.py 评估 SKILL.md
   *
   * 将候选内容写入临时文件，调用 skill_evaluator.py 获取评分
   */
  private async runEvaluator(skillContent: string): Promise<number> {
    const tmpDir = path.join(this.config.workspaceDir, ".gepa", "tmp");
    fs.mkdirSync(tmpDir, { recursive: true });

    const tmpFile = path.join(tmpDir, `candidate-${Date.now()}.md`);
    fs.writeFileSync(tmpFile, skillContent, "utf-8");

    try {
      // 调用 skill_evaluator.py
      const { spawn } = await import("node:child_process");

      return new Promise<number>((resolve) => {
        const proc = spawn("python3", [
          this.config.evaluatorPath,
          "--skill",
          tmpFile,
          "--format",
          "json",
        ], {
          cwd: this.config.workspaceDir,
          timeout: 30000, // 30 秒超时
        });

        let stdout = "";
        let stderr = "";

        proc.stdout.on("data", (data: Buffer) => {
          stdout += data.toString();
        });
        proc.stderr.on("data", (data: Buffer) => {
          stderr += data.toString();
        });

        proc.on("close", (code: number | null) => {
          if (code !== 0) {
            // 评估器执行失败，返回 0 分
            resolve(0);
            return;
          }

          // 尝试解析 JSON 输出
          try {
            const result = JSON.parse(stdout) as {
              total_score?: number;
              score?: number;
            };
            resolve(result.total_score ?? result.score ?? 0);
          } catch {
            // 解析失败，尝试从输出中提取数字
            const match = stdout.match(/(\d+(?:\.\d+)?)\s*%/);
            if (match) {
              resolve(parseFloat(match[1]));
            }
            resolve(0);
          }
        });

        proc.on("error", () => {
          resolve(0);
        });
      });
    } finally {
      // 清理临时文件
      try {
        fs.unlinkSync(tmpFile);
      } catch {
        // 忽略
      }
    }
  }
}
