/**
 * GEPA 周期性自我进化评估插件
 *
 * 借鉴 Hermes Agent (Nous Research) 的 GEPA 算法，每 N 次工具调用后
 * 自动向会话注入评估提醒，触发 self-improving-agent 的周期性评估流程。
 *
 * 机制：
 * 1. 监听 after_tool_call 钩子，每次工具调用后计数器 +1
 * 2. 达到阈值时，通过 enqueueSystemEvent 注入 GEPA 评估提醒
 * 3. 模型在下一轮看到提醒，按 self-improving-agent skill 执行评估
 *
 * 注意：after_tool_call 是 fire-and-forget void hook，不能阻断工具链。
 *       评估提醒通过 system event 队列注入，模型在下一轮处理。
 */

import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";

// 每个会话独立的工具调用计数器
const sessionCounters = new Map<string, number>();

// GEPA 评估提醒文本
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

const plugin = {
  id: "hermes-gepa",
  name: "Hermes GEPA",
  description: "GEPA 周期性自我进化评估插件",
  configSchema: {
    type: "object",
    additionalProperties: false,
    properties: {
      threshold: {
        type: "number",
        description: "触发评估的工具调用次数阈值",
        default: 15,
      },
      enabled: {
        type: "boolean",
        description: "是否启用 GEPA 周期性评估",
        default: true,
      },
    },
  },

  register(api: OpenClawPluginApi) {
    // 从插件配置读取参数
    const pluginConfig = (api.pluginConfig ?? {}) as {
      threshold?: number;
      enabled?: boolean;
    };
    const threshold = pluginConfig.threshold ?? 15;
    const enabled = pluginConfig.enabled ?? true;

    if (!enabled) {
      api.logger.info("[hermes-gepa] 插件已禁用");
      return;
    }

    api.logger.info(
      `[hermes-gepa] 插件已启用，阈值：每 ${threshold} 次工具调用触发评估`,
    );

    // 注册 after_tool_call 钩子
    api.on(
      "after_tool_call",
      (event, ctx) => {
        const sessionKey = ctx.sessionKey;
        if (!sessionKey) {
          return;
        }

        // 计数器 +1
        const current = (sessionCounters.get(sessionKey) ?? 0) + 1;
        sessionCounters.set(sessionKey, current);

        // 未达阈值，跳过
        if (current < threshold) {
          return;
        }

        // 达到阈值，重置计数器并注入 GEPA 评估提醒
        sessionCounters.set(sessionKey, 0);

        const message = buildGepaMessage(threshold);

        try {
          api.runtime.system.enqueueSystemEvent(message, { sessionKey });
          api.logger.info(
            `[hermes-gepa] 会话 ${sessionKey} 达到 ${threshold} 次工具调用，已注入 GEPA 评估提醒`,
          );
        } catch (err) {
          api.logger.warn(
            `[hermes-gepa] 注入系统事件失败: ${err instanceof Error ? err.message : String(err)}`,
          );
        }
      },
      { priority: 5 },
    );
  },
};

export default plugin;
