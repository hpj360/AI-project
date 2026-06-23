/**
 * 执行轨迹收集器
 *
 * 监听 after_tool_call 钩子，收集工具调用序列到 .gepa/traces/ 目录。
 * 这些轨迹供 GEPA 变异引擎分析，找出可改进的模式。
 */

import fs from "node:fs";
import path from "node:path";
import type { ToolCallTrace, SessionTrace } from "./types.js";

/** 截断字符串到指定长度 */
function truncate(s: string, max: number): string {
  if (s.length <= max) return s;
  return s.slice(0, max) + "...[truncated]";
}

/** 轨迹收集器 */
export class TraceCollector {
  private readonly dataDir: string;
  private readonly tracesDir: string;
  /** 每会话的工具调用缓冲 */
  private readonly sessionBuffer = new Map<string, ToolCallTrace[]>();
  /** 每会话的 prompt 缓冲 */
  private readonly sessionPrompt = new Map<string, string>();
  /** 每会话的开始时间 */
  private readonly sessionStart = new Map<string, string>();
  /** 最大缓冲大小（超过则 flush） */
  private readonly maxBufferSize = 50;

  constructor(dataDir: string) {
    this.dataDir = dataDir;
    this.tracesDir = path.join(dataDir, "traces");
    this.ensureDir(this.tracesDir);
  }

  private ensureDir(dir: string): void {
    try {
      fs.mkdirSync(dir, { recursive: true });
    } catch {
      // 目录已存在或创建失败，忽略
    }
  }

  /** 记录会话的 prompt（在 before_prompt_build 或会话开始时调用） */
  recordPrompt(sessionKey: string, prompt: string): void {
    this.sessionPrompt.set(sessionKey, truncate(prompt, 1000));
    if (!this.sessionStart.has(sessionKey)) {
      this.sessionStart.set(sessionKey, new Date().toISOString());
    }
  }

  /** 记录工具调用（在 after_tool_call 钩子中调用） */
  recordToolCall(
    sessionKey: string,
    tool: string,
    params: unknown,
    result: unknown,
    success: boolean,
    durationMs: number,
  ): void {
    const trace: ToolCallTrace = {
      tool,
      params: truncate(typeof params === "string" ? params : JSON.stringify(params), 500),
      result: truncate(typeof result === "string" ? result : JSON.stringify(result), 500),
      success,
      durationMs,
      ts: new Date().toISOString(),
    };

    let buffer = this.sessionBuffer.get(sessionKey);
    if (!buffer) {
      buffer = [];
      this.sessionBuffer.set(sessionKey, buffer);
    }
    buffer.push(trace);

    // 缓冲区满时 flush
    if (buffer.length >= this.maxBufferSize) {
      this.flushSession(sessionKey);
    }
  }

  /** 将会话轨迹写入文件 */
  flushSession(sessionKey: string): void {
    const buffer = this.sessionBuffer.get(sessionKey);
    if (!buffer || buffer.length === 0) return;

    const prompt = this.sessionPrompt.get(sessionKey) ?? "";
    const startTime = this.sessionStart.get(sessionKey) ?? new Date().toISOString();

    const trace: SessionTrace = {
      sessionKey,
      prompt,
      toolCalls: buffer,
      startTime,
      endTime: new Date().toISOString(),
    };

    // 写入 JSONL 文件（追加模式）
    const fileName = `trace-${Date.now()}-${sessionKey.replace(/[^a-zA-Z0-9]/g, "_")}.json`;
    const filePath = path.join(this.tracesDir, fileName);

    try {
      fs.writeFileSync(filePath, JSON.stringify(trace, null, 2), "utf-8");
    } catch {
      // 写入失败，忽略
    }

    // 清空缓冲
    this.sessionBuffer.delete(sessionKey);
    this.sessionPrompt.delete(sessionKey);
    this.sessionStart.delete(sessionKey);
  }

  /** 读取所有轨迹文件 */
  loadTraces(maxCount: number): SessionTrace[] {
    let files: string[] = [];
    try {
      files = fs
        .readdirSync(this.tracesDir)
        .filter((f) => f.endsWith(".json"))
        .sort()
        .reverse() // 最新的在前
        .slice(0, maxCount);
    } catch {
      return [];
    }

    const traces: SessionTrace[] = [];
    for (const file of files) {
      try {
        const content = fs.readFileSync(path.join(this.tracesDir, file), "utf-8");
        traces.push(JSON.parse(content) as SessionTrace);
      } catch {
        // 跳过损坏的文件
      }
    }
    return traces;
  }

  /** 获取轨迹数量 */
  getTraceCount(): number {
    try {
      return fs.readdirSync(this.tracesDir).filter((f) => f.endsWith(".json")).length;
    } catch {
      return 0;
    }
  }

  /** 清理旧轨迹（保留最近 N 个） */
  cleanupOldTraces(keepCount: number): number {
    let files: string[] = [];
    try {
      files = fs.readdirSync(this.tracesDir).filter((f) => f.endsWith(".json")).sort();
    } catch {
      return 0;
    }

    if (files.length <= keepCount) return 0;

    const toDelete = files.slice(0, files.length - keepCount);
    let deleted = 0;
    for (const file of toDelete) {
      try {
        fs.unlinkSync(path.join(this.tracesDir, file));
        deleted++;
      } catch {
        // 忽略删除失败
      }
    }
    return deleted;
  }
}
