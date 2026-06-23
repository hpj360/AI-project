/**
 * 自动 PR 发布器
 *
 * Hermes 的自动 PR 机制：GEPA 进化通过 Judge 审批后，
 * 不直接替换 SKILL.md，而是创建 Git 分支 → 提交 → 推送 → 创建 PR。
 *
 * 优势：
 * 1. 人工审查：所有自动进化都通过 PR 审查，防止低质量改进合入
 * 2. 可回溯：每个 PR 对应一次进化，可追溯变异过程和 Judge 判定
 * 3. 可回滚：如果改进有问题，revert PR 即可
 * 4. 团队协作：团队成员可以审查、讨论、修改自动生成的改进
 *
 * 降级策略：
 * - gh CLI 可用 → 创建 PR
 * - gh CLI 不可用但 git 可用 → 创建分支 + 提交（不创建 PR）
 * - git 不可用 → 直接写入文件（原始行为）+ 日志警告
 */

import fs from "node:fs";
import path from "node:path";
import { execFile } from "node:child_process";
import { promisify } from "node:util";
import type { JudgeVerdict, MutationCandidate, EvolveResult } from "./types.js";

const execFileAsync = promisify(execFile);

/** PR 发布器配置 */
export interface PrPublisherConfig {
  /** 工作区目录（git 仓库根目录） */
  workspaceDir: string;
  /** 技能目录（相对于 workspace） */
  skillsDir: string;
  /** 是否启用自动 PR */
  enabled: boolean;
  /** PR 目标分支 */
  baseBranch: string;
  /** PR 标签 */
  labels: string[];
  /** 是否自动合并（仅当 Judge confidence ≥ autoMergeThreshold 时） */
  autoMerge: boolean;
  /** 自动合并的 confidence 阈值 */
  autoMergeThreshold: number;
  /** 日志函数 */
  log: (msg: string) => void;
}

/** PR 发布结果 */
export interface PrPublishResult {
  /** 发布方式 */
  method: "pr" | "branch" | "direct";
  /** PR URL（如果创建了 PR） */
  prUrl: string | null;
  /** 分支名称 */
  branchName: string | null;
  /** 提交哈希 */
  commitHash: string | null;
  /** 是否自动合并 */
  autoMerged: boolean;
}

/** 检查命令是否可用 */
async function isCommandAvailable(cmd: string): Promise<boolean> {
  try {
    await execFileAsync("which", [cmd], { timeout: 5000 });
    return true;
  } catch {
    return false;
  }
}

/** 执行 git 命令 */
async function git(
  cwd: string,
  args: string[],
): Promise<string> {
  const { stdout } = await execFileAsync("git", args, {
    cwd,
    timeout: 30000,
    maxBuffer: 1024 * 1024,
  });
  return stdout.trim();
}

/** 执行 gh 命令 */
async function gh(
  cwd: string,
  args: string[],
): Promise<string> {
  const { stdout } = await execFileAsync("gh", args, {
    cwd,
    timeout: 30000,
    maxBuffer: 1024 * 1024,
  });
  return stdout.trim();
}

/** 生成分支名称 */
function generateBranchName(skillName: string): string {
  const timestamp = Date.now();
  return `gepa/evolve-${skillName}-${timestamp}`;
}

/** 生成 PR 标题 */
function generatePrTitle(
  skillName: string,
  baselineScore: number,
  bestScore: number,
): string {
  const delta = (bestScore - baselineScore).toFixed(1);
  const sign = bestScore > baselineScore ? "+" : "";
  return `[GEPA] 进化 ${skillName}: ${baselineScore.toFixed(1)} → ${bestScore.toFixed(1)} (${sign}${delta})`;
}

/** 生成 PR 正文 */
function generatePrBody(
  skillName: string,
  candidate: MutationCandidate,
  judgeVerdict: JudgeVerdict,
  baselineScore: number,
  bestScore: number,
  tracesCount: number,
): string {
  const lines = [
    `## GEPA 自动进化报告`,
    ``,
    `| 维度 | 值 |`,
    `|------|-----|`,
    `| 技能 | ${skillName} |`,
    `| 变异类型 | ${candidate.mutationType} |`,
    `| 基线得分 | ${baselineScore.toFixed(1)} |`,
    `| 改进后得分 | ${bestScore.toFixed(1)} |`,
    `| 提升幅度 | +${(bestScore - baselineScore).toFixed(1)} |`,
    `| 轨迹样本数 | ${tracesCount} |`,
    ``,
    `## 变异说明`,
    ``,
    candidate.rationale,
    ``,
    `## Judge 判定`,
    ``,
    `| 维度 | 值 |`,
    `|------|-----|`,
    `| 判定 | ${judgeVerdict.verdict} |`,
    `| 置信度 | ${(judgeVerdict.confidence * 100).toFixed(0)}% |`,
    `| 古德哈特风险 | ${judgeVerdict.goodhartRisk} |`,
    ``,
    `### 判定理由`,
    ``,
    judgeVerdict.reason,
    ``,
  ];

  if (judgeVerdict.evidence.length > 0) {
    lines.push(`### 证据`, ``);
    for (const evidence of judgeVerdict.evidence) {
      lines.push(`- ${evidence}`);
    }
    lines.push(``);
  }

  if (judgeVerdict.suggestions.length > 0) {
    lines.push(`### 改进建议`, ``);
    for (const suggestion of judgeVerdict.suggestions) {
      lines.push(`- ${suggestion}`);
    }
    lines.push(``);
  }

  lines.push(
    `## 审查指南`,
    ``,
    `1. 检查变异是否真正解决了执行轨迹中的问题`,
    `2. 确认变异没有引入新的风险`,
    `3. 如果 Judge 判定为 needs_revision，请根据建议修改后再合并`,
    `4. 合并前可运行 \`python3 evals/scripts/skill_evaluator.py --skill <path>\` 验证评分`,
    ``,
    `---`,
    `*此 PR 由 GEPA 引擎自动生成 | 时间: ${new Date().toISOString()}*`,
  );

  return lines.join("\n");
}

/** PR 发布器 */
export class PrPublisher {
  constructor(private readonly config: PrPublisherConfig) {}

  /**
   * 发布进化结果
   *
   * 降级策略：
   * 1. gh + git 可用 → 创建 PR
   * 2. 仅 git 可用 → 创建分支 + 提交
   * 3. 都不可用 → 直接写入文件
   */
  async publish(
    skillName: string,
    skillPath: string,
    improvedContent: string,
    candidate: MutationCandidate,
    judgeVerdict: JudgeVerdict,
    baselineScore: number,
    bestScore: number,
    tracesCount: number,
  ): Promise<PrPublishResult> {
    if (!this.config.enabled) {
      return this.directWrite(
        skillPath,
        improvedContent,
      );
    }

    const gitAvailable = await isCommandAvailable("git");
    if (!gitAvailable) {
      this.config.log("[GEPA-PR] git 不可用，降级为直接写入文件");
      return this.directWrite(skillPath, improvedContent);
    }

    // 检查是否在 git 仓库中
    try {
      await git(this.config.workspaceDir, ["rev-parse", "--git-dir"]);
    } catch {
      this.config.log("[GEPA-PR] 不在 git 仓库中，降级为直接写入文件");
      return this.directWrite(skillPath, improvedContent);
    }

    const ghAvailable = await isCommandAvailable("gh");

    if (ghAvailable) {
      return this.createPullRequest(
        skillName,
        skillPath,
        improvedContent,
        candidate,
        judgeVerdict,
        baselineScore,
        bestScore,
        tracesCount,
      );
    }

    // gh 不可用，只创建分支
    return this.createBranchOnly(
      skillName,
      skillPath,
      improvedContent,
      candidate,
    );
  }

  /** 创建完整 PR */
  private async createPullRequest(
    skillName: string,
    skillPath: string,
    improvedContent: string,
    candidate: MutationCandidate,
    judgeVerdict: JudgeVerdict,
    baselineScore: number,
    bestScore: number,
    tracesCount: number,
  ): Promise<PrPublishResult> {
    const branchName = generateBranchName(skillName);
    const cwd = this.config.workspaceDir;

    try {
      // 1. 获取当前分支（用于 PR base）
      const currentBranch = await git(cwd, [
        "rev-parse",
        "--abbrev-ref",
        "HEAD",
      ]);

      // 2. 创建并切换到新分支
      await git(cwd, ["checkout", "-b", branchName]);

      // 3. 写入改进后的 SKILL.md
      fs.writeFileSync(skillPath, improvedContent, "utf-8");

      // 4. 暂存 + 提交
      const relativePath = path.relative(cwd, skillPath);
      await git(cwd, ["add", relativePath]);

      const commitMessage = [
        generatePrTitle(skillName, baselineScore, bestScore),
        "",
        `变异类型: ${candidate.mutationType}`,
        `变异理由: ${candidate.rationale}`,
        `Judge 判定: ${judgeVerdict.verdict} (confidence: ${(judgeVerdict.confidence * 100).toFixed(0)}%)`,
        `古德哈特风险: ${judgeVerdict.goodhartRisk}`,
        "",
        "Generated by GEPA engine",
      ].join("\n");

      await git(cwd, ["commit", "-m", commitMessage]);

      // 5. 推送
      await git(cwd, ["push", "-u", "origin", branchName]);

      // 6. 创建 PR
      const prTitle = generatePrTitle(skillName, baselineScore, bestScore);
      const prBody = generatePrBody(
        skillName,
        candidate,
        judgeVerdict,
        baselineScore,
        bestScore,
        tracesCount,
      );

      const prArgs = [
        "pr",
        "create",
        "--title",
        prTitle,
        "--body",
        prBody,
        "--base",
        this.config.baseBranch || currentBranch,
        "--head",
        branchName,
      ];

      // 添加标签
      for (const label of this.config.labels) {
        prArgs.push("--label", label);
      }

      const prUrl = await gh(cwd, prArgs);

      this.config.log(`[GEPA-PR] PR 已创建: ${prUrl}`);

      // 7. 判断是否自动合并
      let autoMerged = false;
      if (
        this.config.autoMerge &&
        judgeVerdict.verdict === "approve" &&
        judgeVerdict.confidence >= this.config.autoMergeThreshold &&
        judgeVerdict.goodhartRisk === "none"
      ) {
        try {
          await gh(cwd, ["pr", "merge", prUrl, "--squash", "--delete-branch"]);
          autoMerged = true;
          this.config.log(`[GEPA-PR] PR 已自动合并（confidence ≥ ${this.config.autoMergeThreshold}）`);

          // 切回原分支
          await git(cwd, ["checkout", currentBranch]);
        } catch (err) {
          this.config.log(
            `[GEPA-PR] 自动合并失败: ${err instanceof Error ? err.message : String(err)}`,
          );
        }
      } else {
        // 切回原分支
        await git(cwd, ["checkout", currentBranch]);
      }

      // 获取 commit hash
      const commitHash = await git(cwd, ["rev-parse", "HEAD"]);

      return {
        method: "pr",
        prUrl,
        branchName,
        commitHash,
        autoMerged,
      };
    } catch (err) {
      this.config.log(
        `[GEPA-PR] 创建 PR 失败: ${err instanceof Error ? err.message : String(err)}`,
      );

      // 尝试切回原分支
      try {
        const branches = await git(cwd, ["branch", "--list"]);
        if (branches.includes("main") || branches.includes("master")) {
          const mainBranch = branches.includes("main") ? "main" : "master";
          await git(cwd, ["checkout", mainBranch]);
        }
      } catch {
        // 忽略
      }

      // 降级为直接写入
      this.config.log("[GEPA-PR] 降级为直接写入文件");
      return this.directWrite(skillPath, improvedContent);
    }
  }

  /** 仅创建分支（gh 不可用时） */
  private async createBranchOnly(
    skillName: string,
    skillPath: string,
    improvedContent: string,
    candidate: MutationCandidate,
  ): Promise<PrPublishResult> {
    const branchName = generateBranchName(skillName);
    const cwd = this.config.workspaceDir;

    try {
      const currentBranch = await git(cwd, [
        "rev-parse",
        "--abbrev-ref",
        "HEAD",
      ]);

      await git(cwd, ["checkout", "-b", branchName]);

      fs.writeFileSync(skillPath, improvedContent, "utf-8");

      const relativePath = path.relative(cwd, skillPath);
      await git(cwd, ["add", relativePath]);

      const commitMessage = [
        generatePrTitle(skillName, 0, 0),
        "",
        `变异类型: ${candidate.mutationType}`,
        `变异理由: ${candidate.rationale}`,
        "",
        "Generated by GEPA engine (branch-only mode)",
      ].join("\n");

      await git(cwd, ["commit", "-m", commitMessage]);

      // 尝试推送
      try {
        await git(cwd, ["push", "-u", "origin", branchName]);
        this.config.log(`[GEPA-PR] 分支已推送: ${branchName}`);
      } catch {
        this.config.log(`[GEPA-PR] 分支已创建但未推送: ${branchName}`);
      }

      // 切回原分支
      await git(cwd, ["checkout", currentBranch]);

      const commitHash = await git(cwd, ["rev-parse", "HEAD"]);

      this.config.log(
        `[GEPA-PR] 分支已创建: ${branchName}（gh CLI 不可用，未创建 PR）`,
      );

      return {
        method: "branch",
        prUrl: null,
        branchName,
        commitHash,
        autoMerged: false,
      };
    } catch (err) {
      this.config.log(
        `[GEPA-PR] 创建分支失败: ${err instanceof Error ? err.message : String(err)}`,
      );
      return this.directWrite(skillPath, improvedContent);
    }
  }

  /** 直接写入文件（降级模式） */
  private async directWrite(
    skillPath: string,
    content: string,
  ): Promise<PrPublishResult> {
    // 先备份
    const backupDir = path.join(
      this.config.workspaceDir,
      ".gepa",
      "backups",
    );
    fs.mkdirSync(backupDir, { recursive: true });

    try {
      const original = fs.readFileSync(skillPath, "utf-8");
      const backupPath = path.join(
        backupDir,
        `${path.basename(skillPath, ".md")}-${Date.now()}.md`,
      );
      fs.writeFileSync(backupPath, original, "utf-8");
    } catch {
      // 忽略备份失败
    }

    fs.writeFileSync(skillPath, content, "utf-8");

    return {
      method: "direct",
      prUrl: null,
      branchName: null,
      commitHash: null,
      autoMerged: false,
    };
  }
}
