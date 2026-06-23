/**
 * Hermes GEPA 插件 — 方案 C + D 合体
 *
 * 方案 C（指令层）：after_tool_call 钩子 + enqueueSystemEvent
 *   每 N 次工具调用后注入 GEPA 评估提醒，模型按 self-improving-agent skill 执行评估。
 *
 * 方案 D（代码层）：原生 TypeScript GEPA 引擎
 *   1. after_tool_call 钩子 → 收集执行轨迹到 .gepa/traces/
 *   2. 后台服务定期触发 → 变异引擎生成候选 → 帕累托选择 → 约束门控 → 应用改进
 *   3. 通过 registerService 注册后台进化服务
 *
 * 两层协同：
 *   - 方案 C 的提醒让模型在会话中即时学习（快速反馈）
 *   - 方案 D 的引擎在后台批量进化技能（深度优化）
 *
 * 参考：arXiv:2507.19457 (ICLR 2026 Oral)
 */

import path from "node:path";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";
import { TraceCollector } from "./src/trace-collector.js";
import { EvolveRunner } from "./src/evolve-runner.js";
import type { GepaPluginConfig, GepaStateSnapshot } from "./src/types.js";

// ─── 方案 C：会话级计数器 ──────────────────────────────────

const sessionCounters = new Map<string, number>();

function buildGepaMessage(threshold: number): string {
  return [
    `[GEPA] 已完成 ${threshold} 次工具调用，触发周期性自我进化评估。`,
    ``,
    `请执行以下 GEPA 评估流程（参考 self-improving-agent skill）：`,
    ``,
    `1. 模式识别：本次会话出现了什么重复模式？哪些步骤被重复执行？`,
    `2. 步骤提取：成功的步骤序列是什么？有没有更优的路径？`,
    `3. 可复用性判断：这个模式是否通用？是否跨项目可用？是否非显而易见？`,
    `4. 决策：满足条件（重复性+非显而易见+可验证+通用性，任意2条）时提取为 skill 文件`,
    ``,
    `评估完成后，将结果记录到 .learnings/LEARNINGS.md（格式：[GEPA-YYYYMMDD-XXX]）。`,
  ].join("\n");
}

// ─── 默认配置 ──────────────────────────────────────────────

const DEFAULT_CONFIG: GepaPluginConfig = {
  reminderEnabled: true,
  reminderThreshold: 15,
  engineEnabled: true,
  engineIntervalHours: 6,
  numCandidates: 3,
  numEvalSamples: 10,
  maxIterations: 3,
  llmModel: "deepseek/deepseek-chat",
  evaluatorPath: "",
  targetSkills: [],
  dataDir: ".gepa",
};

// ─── GEPA 引擎状态 ─────────────────────────────────────────

let gepaState: GepaStateSnapshot = {
  state: "idle",
  currentSkill: null,
  currentIteration: 0,
  traceCount: 0,
  lastEvolveTime: null,
  lastResult: null,
  history: [],
};

// ─── 插件定义 ──────────────────────────────────────────────

const plugin = {
  id: "hermes-gepa",
  name: "Hermes GEPA",
  description:
    "GEPA 自我进化引擎：方案 C（会话级评估提醒）+ 方案 D（后台 GEPA 引擎自动进化技能）",
  configSchema: {
    type: "object",
    additionalProperties: false,
    properties: {
      reminderEnabled: {
        type: "boolean",
        description: "是否启用会话级 GEPA 评估提醒（方案 C）",
        default: true,
      },
      reminderThreshold: {
        type: "number",
        description: "触发评估提醒的工具调用次数阈值",
        default: 15,
      },
      engineEnabled: {
        type: "boolean",
        description: "是否启用后台 GEPA 引擎（方案 D）",
        default: true,
      },
      engineIntervalHours: {
        type: "number",
        description: "GEPA 引擎触发间隔（小时）",
        default: 6,
      },
      numCandidates: {
        type: "number",
        description: "每次进化生成的候选数量",
        default: 3,
      },
      numEvalSamples: {
        type: "number",
        description: "每次评估的样本数量",
        default: 10,
      },
      maxIterations: {
        type: "number",
        description: "最大迭代轮次",
        default: 3,
      },
      llmModel: {
        type: "string",
        description: "变异用的 LLM 模型（OpenAI 兼容）",
        default: "deepseek/deepseek-chat",
      },
      evaluatorPath: {
        type: "string",
        description: "skill_evaluator.py 路径",
        default: "",
      },
      targetSkills: {
        type: "array",
        items: { type: "string" },
        description: "要进化的技能列表（空 = 自动发现）",
        default: [],
      },
      dataDir: {
        type: "string",
        description: ".gepa 数据目录（相对于 workspace）",
        default: ".gepa",
      },
    },
  },

  register(api: OpenClawPluginApi) {
    // 合并配置
    const raw = (api.pluginConfig ?? {}) as Partial<GepaPluginConfig>;
    const config: GepaPluginConfig = { ...DEFAULT_CONFIG, ...raw };

    if (!config.reminderEnabled && !config.engineEnabled) {
      api.logger.info("[hermes-gepa] 方案 C 和 D 均已禁用，插件不活跃");
      return;
    }

    // 解析路径
    const workspaceDir = api.config?.loadConfig
      ? process.cwd()
      : process.cwd();
    const dataDir = path.resolve(workspaceDir, config.dataDir);
    const skillsDir = path.resolve(workspaceDir, ".trae", "skills");
    const evaluatorPath =
      config.evaluatorPath ||
      path.resolve(
        workspaceDir,
        "OpenClaw",
        "openclaw-main",
        "evals",
        "scripts",
        "skill_evaluator.py",
      );

    api.logger.info(
      `[hermes-gepa] 插件已启用 | 方案C(提醒): ${config.reminderEnabled ? "ON" : "OFF"} | 方案D(引擎): ${config.engineEnabled ? "ON" : "OFF"}`,
    );

    // ─── 方案 C：会话级评估提醒 ───────────────────────────

    const traceCollector = new TraceCollector(dataDir);

    if (config.reminderEnabled) {
      api.logger.info(
        `[hermes-gepa] 方案 C 已启用，阈值：每 ${config.reminderThreshold} 次工具调用触发评估`,
      );

      api.on(
        "after_tool_call",
        (event, ctx) => {
          const sessionKey = ctx.sessionKey;
          if (!sessionKey) return;

          // 方案 C：计数 + 提醒
          const current = (sessionCounters.get(sessionKey) ?? 0) + 1;
          sessionCounters.set(sessionKey, current);

          // 方案 D：收集轨迹
          const toolName = (event as { toolName?: string }).toolName ?? "unknown";
          const toolResult = (event as { result?: unknown }).result;
          const params = (event as { params?: unknown }).params;
          traceCollector.recordToolCall(
            sessionKey,
            toolName,
            params,
            toolResult,
            true,
            0,
          );

          // 更新状态
          gepaState.traceCount = traceCollector.getTraceCount();

          // 达到阈值，注入提醒
          if (current >= config.reminderThreshold) {
            sessionCounters.set(sessionKey, 0);
            const message = buildGepaMessage(config.reminderThreshold);
            try {
              api.runtime.system.enqueueSystemEvent(message, { sessionKey });
              api.logger.info(
                `[hermes-gepa] 会话 ${sessionKey} 达到 ${config.reminderThreshold} 次调用，已注入 GEPA 评估提醒`,
              );
            } catch (err) {
              api.logger.warn(
                `[hermes-gepa] 注入系统事件失败: ${err instanceof Error ? err.message : String(err)}`,
              );
            }
          }
        },
        { priority: 5 },
      );

      // 会话结束时 flush 轨迹
      api.on("session_end", (event, ctx) => {
        const sessionKey = ctx.sessionKey;
        if (sessionKey) {
          traceCollector.flushSession(sessionKey);
        }
      });
    }

    // ─── 方案 D：后台 GEPA 引擎 ───────────────────────────

    if (config.engineEnabled) {
      api.logger.info(
        `[hermes-gepa] 方案 D 已启用，进化间隔：每 ${config.engineIntervalHours} 小时`,
      );

      // 注册后台服务
      api.registerService({
        id: "hermes-gepa-engine",
        start: async () => {
          api.logger.info("[hermes-gepa] 后台进化服务已启动");

          // 获取 API Key
          let apiKey = "";
          let apiBaseUrl = "https://openrouter.ai/api/v1";

          try {
            const auth = await api.runtime.modelAuth.resolveApiKeyForProvider({
              provider: "openrouter",
            });
            apiKey = auth.apiKey ?? "";
          } catch {
            // 尝试从环境变量获取
            apiKey = process.env.OPENROUTER_API_KEY ?? "";
          }

          if (!apiKey) {
            api.logger.warn(
              "[hermes-gepa] 未找到 API Key，后台引擎将使用空 Key（LLM 调用会失败）",
            );
          }

          // 创建进化运行器
          const evolveRunner = new EvolveRunner({
            workspaceDir,
            dataDir,
            skillsDir,
            evaluatorPath,
            llmModel: config.llmModel,
            apiKey,
            apiBaseUrl,
            numCandidates: config.numCandidates,
            numEvalSamples: config.numEvalSamples,
            maxIterations: config.maxIterations,
            log: (msg) => api.logger.info(msg),
          });

          // 定时触发进化
          const intervalMs = config.engineIntervalHours * 60 * 60 * 1000;

          const runEvolution = async () => {
            if (gepaState.state === "evolving") {
              api.logger.info("[hermes-gepa] 进化正在进行中，跳过本次触发");
              return;
            }

            gepaState.state = "evolving";
            api.logger.info("[hermes-gepa] 开始 GEPA 进化周期");

            try {
              const results = await evolveRunner.runEvolution(
                config.targetSkills,
              );

              gepaState.state = "idle";
              gepaState.lastEvolveTime = new Date().toISOString();
              gepaState.history.push(...results);

              // 保留最近 50 条历史
              if (gepaState.history.length > 50) {
                gepaState.history = gepaState.history.slice(-50);
              }

              const improved = results.filter((r) => r.improved).length;
              api.logger.info(
                `[hermes-gepa] 进化周期完成: ${improved}/${results.length} 个技能已改进`,
              );

              // 通知活跃会话
              if (improved > 0) {
                const improvedSkills = results
                  .filter((r) => r.improved)
                  .map(
                    (r) =>
                      `${r.skillName} (${r.baselineScore.toFixed(0)}→${r.bestScore.toFixed(0)})`,
                  )
                  .join(", ");
                try {
                  api.runtime.system.enqueueSystemEvent(
                    `[GEPA] 引擎已自动改进 ${improved} 个技能: ${improvedSkills}。详见 .gepa/GEPA_LOG.md`,
                    { sessionKey: "gepa-engine" },
                  );
                } catch {
                  // 忽略
                }
              }
            } catch (err) {
              gepaState.state = "idle";
              api.logger.error(
                `[hermes-gepa] 进化周期失败: ${err instanceof Error ? err.message : String(err)}`,
              );
            }
          };

          // 首次启动延迟 60 秒（等系统稳定）
          const initialDelay = 60 * 1000;
          const timer = setTimeout(runEvolution, initialDelay);

          // 定时器
          const interval = setInterval(runEvolution, intervalMs);

          // 保存清理函数
          (api as unknown as { _gepaCleanup?: () => void })._gepaCleanup =
            () => {
              clearTimeout(timer);
              clearInterval(interval);
            };
        },
        stop: async () => {
          const cleanup = (api as unknown as { _gepaCleanup?: () => void })
            ._gepaCleanup;
          if (cleanup) {
            cleanup();
          }
          api.logger.info("[hermes-gepa] 后台进化服务已停止");
        },
      });

      // 注册 CLI 命令（手动触发进化）
      api.registerCli(
        ({ program }) => {
          program
            .command("gepa:evolve")
            .description("手动触发 GEPA 技能进化")
            .option("-s, --skill <name>", "指定技能名称")
            .option("--dry-run", "只生成候选，不应用改进")
            .action(async (options: { skill?: string; dryRun?: boolean }) => {
              console.log("[GEPA] 手动触发进化...");

              let apiKey = process.env.OPENROUTER_API_KEY ?? "";
              try {
                const auth =
                  await api.runtime.modelAuth.resolveApiKeyForProvider({
                    provider: "openrouter",
                  });
                apiKey = auth.apiKey ?? apiKey;
              } catch {
                // 使用环境变量
              }

              const evolveRunner = new EvolveRunner({
                workspaceDir,
                dataDir,
                skillsDir,
                evaluatorPath,
                llmModel: config.llmModel,
                apiKey,
                apiBaseUrl: "https://openrouter.ai/api/v1",
                numCandidates: config.numCandidates,
                numEvalSamples: config.numEvalSamples,
                maxIterations: config.maxIterations,
                log: (msg) => console.log(msg),
              });

              const targetSkills = options.skill ? [options.skill] : [];
              const results = await evolveRunner.runEvolution(targetSkills);

              console.log("\n=== GEPA 进化结果 ===");
              for (const r of results) {
                const status = r.improved ? "✅" : "❌";
                const delta =
                  r.improvement > 0 ? `(+${r.improvement.toFixed(1)})` : "";
                console.log(
                  `${status} ${r.skillName}: ${r.baselineScore.toFixed(1)} → ${r.bestScore.toFixed(1)} ${delta}`,
                );
                if (r.failureReason) {
                  console.log(`   原因: ${r.failureReason}`);
                }
              }
              console.log(`\n详见: ${path.join(dataDir, "GEPA_LOG.md")}`);
            });
        },
        { commands: ["gepa:evolve"] },
      );
    }
  },
};

export default plugin;
