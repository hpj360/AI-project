# AGENTS.md - 模型自律规则（认知层护栏）

> 本文件定义 AI 模型在本项目工作时必须遵守的硬性规则。
> 违反任何一条都可能导致工作丢失，是之前多次"幻觉丢失"事件的根因。

## 一、环境认知（必须铭记）

### 1.1 沙箱临时性
- 本项目运行在 **TRAE 远程沙箱**，文件系统是临时性的
- **会话结束后沙箱销毁，所有本地文件丢失**
- 唯一能跨会话保留的：**已 push 到远程仓库的内容**

### 1.2 持久化层级
```
本地文件（沙箱临时） → 本地 git commit（沙箱临时） → git push（远程持久） ✓
```
只有到达最后一层才算真正持久化。

### 1.3 历史教训
- **第 1 次丢失**：声称 1072 条目，实际从未 commit
- **第 2 次丢失**：声称 1550 条目 + 3 次 push，实际远程只有 1 个无关 commit
- **共同点**：模型口头声称"已持久化"，但验证逻辑闭环在本地沙箱内

---

## 二、三道关卡强制流程（必须执行）

### 关卡 1：会话启动
**每次新会话开始，第一步必须运行：**
```bash
python3 Hermes/content-creation/scripts/session_check.py start
```

**根据输出判断：**
- 若显示"全新沙箱"：**之前的临时工作已丢失**，不得声称"之前的工作还在"
- 若本地与远程不一致：**不得假装一致**，必须如实告知用户
- 若远程不可达：**告知用户网络问题**，无法保证持久化

### 关卡 2：工作中阶段性
**每完成一个独立任务后运行：**
```bash
python3 Hermes/content-creation/scripts/session_check.py working
```

显示未提交文件和未 push commit 数量，提醒及时持久化。

### 关卡 3：会话结束
**会话结束前必须运行：**
```bash
python3 Hermes/content-creation/scripts/session_check.py exit
```

- **退出码 0**：可安全结束会话
- **退出码 1**：**禁止结束会话**，必须先修复未持久化内容

修复方法：
```bash
python3 Hermes/content-creation/scripts/git_guard.py save "提交说明"
python3 Hermes/content-creation/scripts/session_check.py exit  # 重新检查
```

---

## 三、模型自律红线（禁止行为）

### 3.1 禁止编造 commit hash
- **禁止**口头声称"已 commit (3a30c4d)"等 hash
- **必须**从 `git rev-parse HEAD` 实际输出获取 hash
- **必须**展示 `git log` 实际输出作为证据

### 3.2 禁止虚假声称"已 push"
- **禁止**在未运行 `git_guard.py save` 的情况下声称"已持久化"
- **禁止**在 `git_guard.py save` 返回失败时声称"已保存"
- **必须**展示 `git_guard.py save` 的完整输出（含三重验证结果）

### 3.3 禁止在空环境上假装工作存在
- **禁止**在全新沙箱上声称"之前的 1500 条目还在"
- **必须**先运行 `session_check.py start` 验证远程实际状态
- **必须**如实告知用户：之前未 push 的工作已丢失

### 3.4 禁止跳过护栏
- **禁止**用 `git commit` + `git push` 手动操作代替 `git_guard.py save`
- **禁止**在 `session_check.py exit` 返回 1 时继续后续任务
- **禁止**删除或绕过 `.session_state` 状态文件

---

## 四、正确工作流模板

```
[会话开始]
1. python3 Hermes/content-creation/scripts/session_check.py start
   → 识别沙箱状态，建立基线

[任务执行]
2. 创建/修改文件
3. python3 Hermes/content-creation/scripts/git_guard.py save "feat: xxx"
   → commit + push + 三重验证
4. (每个独立任务后) python3 Hermes/content-creation/scripts/session_check.py working
   → 确认本地状态

[会话结束]
5. python3 Hermes/content-creation/scripts/session_check.py exit
   → 必须退出码 0 才可结束
```

---

## 五、用户监督建议

为防止模型违反自律规则，建议用户：
1. **会话开始时**：要求模型先运行 `session_check.py start` 并展示输出
2. **模型声称"已保存"时**：要求展示 `git_guard.py save` 的完整输出
3. **会话结束前**：要求模型运行 `session_check.py exit` 并展示退出码
4. **看到 commit hash 时**：要求模型运行 `git log` 验证 hash 真实存在

---

## 六、护栏工具清单

| 工具 | 路径 | 用途 |
|------|------|------|
| git_guard.py | Hermes/content-creation/scripts/ | 持久化（commit+push+验证） |
| session_check.py | Hermes/content-creation/scripts/ | 三道关卡流程检查 |
| validate_kb.py | Hermes/content-creation/scripts/ | 知识库数据校验 |

---

## 七、违规后果

违反上述规则将导致：
1. 工作随沙箱销毁丢失，无法恢复
2. 模型声称的成果是幻觉，误导用户决策
3. 用户需要重新检查所有"已完成"的工作

**这是不可接受的失败模式，必须严格避免。**
