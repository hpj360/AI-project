/**
 * 三层记忆模型插件 - L3 语义记忆注入
 *
 * 通过 before_prompt_build 钩子，在每次会话构建 system prompt 时
 * 自动读取并注入 USER.md 内容，实现用户偏好的永久记忆（L3 语义记忆层）。
 *
 * 三层记忆模型：
 *   L1 工作记忆 → 会话上下文 + compaction（OpenClaw 原生）
 *   L2 情节记忆 → memory/YYYY-MM-DD.md + 向量搜索（OpenClaw 原生）
 *   L3 语义记忆 → USER.md + MEMORY.md（本插件注入 USER.md）
 *
 * USER.md 文件位于 workspace 根目录，包含用户偏好、工作习惯、项目约定等
 * 永久性语义信息。每次会话启动时自动注入到 system prompt 中。
 */

import fs from "node:fs";
import path from "node:path";
import type { OpenClawPluginApi } from "openclaw/plugin-sdk/core";

// 缓存 USER.md 内容和修改时间，避免每次 prompt build 都读磁盘
let cachedContent: string | null = null;
let cachedMtime = 0;

async function readUserProfile(
  workspaceDir: string,
  relativePath: string,
  logger: { warn: (msg: string) => void; info: (msg: string) => void },
): Promise<string | null> {
  const fullPath = path.join(workspaceDir, relativePath);

  try {
    const stat = await fs.promises.stat(fullPath);

    // 文件未修改，使用缓存
    if (cachedContent !== null && stat.mtimeMs === cachedMtime) {
      return cachedContent;
    }

    const content = await fs.promises.readFile(fullPath, "utf-8");
    cachedContent = content;
    cachedMtime = stat.mtimeMs;
    return content;
  } catch {
    // 文件不存在是正常情况（用户尚未创建 USER.md）
    if (cachedContent !== null) {
      cachedContent = null;
      cachedMtime = 0;
    }
    return null;
  }
}

const plugin = {
  id: "memory-layer",
  name: "Memory Layer",
  description: "三层记忆模型 - L3 语义记忆（USER.md）注入",
  configSchema: {
    type: "object",
    additionalProperties: false,
    properties: {
      userProfilePath: {
        type: "string",
        description: "USER.md 文件路径（相对于 workspace）",
        default: "USER.md",
      },
      enabled: {
        type: "boolean",
        description: "是否启用 USER.md 注入",
        default: true,
      },
    },
  },

  register(api: OpenClawPluginApi) {
    const pluginConfig = (api.pluginConfig ?? {}) as {
      userProfilePath?: string;
      enabled?: boolean;
    };
    const userProfilePath = pluginConfig.userProfilePath ?? "USER.md";
    const enabled = pluginConfig.enabled ?? true;

    if (!enabled) {
      api.logger.info("[memory-layer] 插件已禁用");
      return;
    }

    api.logger.info(
      `[memory-layer] 插件已启用，USER.md 路径：${userProfilePath}`,
    );

    // 注册 before_prompt_build 钩子
    // 使用 prependSystemContext 而非 prependContext，因为：
    // 1. USER.md 是静态内容，利于 provider 缓存
    // 2. 放在 system prompt 空间，与 MEMORY.md 等同级
    api.on(
      "before_prompt_build",
      async (_event, ctx) => {
        const workspaceDir = ctx.workspaceDir;
        if (!workspaceDir) {
          return;
        }

        const content = await readUserProfile(
          workspaceDir,
          userProfilePath,
          api.logger,
        );

        if (!content || content.trim().length === 0) {
          return;
        }

        // 将 USER.md 内容包装为语义记忆段，注入到 system prompt 前部
        return {
          prependSystemContext: `## User Profile (L3 Semantic Memory)\n\n${content}`,
        };
      },
      { priority: 10 },
    );
  },
};

export default plugin;
