---
name: github
description: |
  Interact with GitHub using the `gh` CLI. Use `gh issue`, `gh pr`, `gh run`, and `gh api` for issues, PRs, CI runs, and advanced queries.
  Triggers: "GitHub"、"PR状态"、"CI失败"、"issue管理"、"代码审查"
---

# GitHub Skill

Interact with GitHub using the `gh` CLI. Always specify `--repo owner/repo` when not in a git directory, or use URLs directly.

## 🔴 CHECKPOINT · Before Any Operation

Confirm with user: "要执行什么GitHub操作？[1]查看PR状态 [2]管理issues [3]CI/CD排查 [4]代码审查 [5]高级查询"

---

## Workflow 1: PR 状态检查

**Use when**: 用户需要查看PR状态、CI运行情况

### Phase 1: 获取PR信息

**Step 1.1 — 列出PR状态**
```bash
# 查看所有开放PR
gh pr list --repo owner/repo

# 查看指定PR详情
gh pr view <pr-number> --repo owner/repo
```

**Step 1.2 — 检查CI状态**
```bash
# 查看PR的CI检查
gh pr checks <pr-number> --repo owner/repo

# 查看最近工作流运行
gh run list --repo owner/repo --limit 10
```

**失败分支**:
| 场景 | 处理方式 |
|------|----------|
| PR不存在 | 提示用户检查PR编号是否正确 |
| 权限不足 | 提示用户需要登录或权限不够 |
| 网络失败 | 重试2次，仍失败则提示稍后重试 |

---

## Workflow 2: Issue 管理

**Use when**: 用户需要创建、查看或管理issues

### Phase 1: Issue操作

**Step 1.1 — 创建Issue**
```bash
gh issue create --repo owner/repo --title "<标题>" --body "<描述>"
```

**Step 1.2 — 🔴 CHECKPOINT · 确认创建**
展示标题和描述，询问用户："确认创建这个issue吗？"

**Step 1.3 — 查看Issues**
```bash
# 列出所有开放issues
gh issue list --repo owner/repo

# 查看指定issue详情
gh issue view <issue-number> --repo owner/repo
```

**Step 1.4 — 关闭Issue**
```bash
gh issue close <issue-number> --repo owner/repo --comment "<关闭原因>"
```

---

## Workflow 3: CI/CD 故障排查

**Use when**: 用户需要排查CI失败问题

### Phase 1: 定位失败

**Step 1.1 — 查看失败的工作流**
```bash
gh run list --repo owner/repo --status failure --limit 5
```

**Step 1.2 — 查看失败详情**
```bash
# 查看失败的工作流
gh run view <run-id> --repo owner/repo

# 只查看失败步骤的日志
gh run view <run-id> --repo owner/repo --log-failed
```

**Step 1.3 — 重新运行工作流**
```bash
gh run rerun <run-id> --repo owner/repo
```

**失败分支**:
| 场景 | 处理方式 |
|------|----------|
| run-id不存在 | 提示用户检查ID是否正确 |
| 无权限重跑 | 提示用户需要维护者权限 |

---

## Workflow 4: 代码审查

**Use when**: 用户需要审查PR代码

### Phase 1: 审查流程

**Step 1.1 — 查看PR变更**
```bash
gh pr diff <pr-number> --repo owner/repo
```

**Step 1.2 — 提交审查意见**
```bash
gh pr review <pr-number> --repo owner/repo --comment "<审查意见>"

# 批准PR
gh pr review <pr-number> --repo owner/repo --approve
```

**Step 1.3 — 🔴 CHECKPOINT · 确认审查**
"确认提交审查意见/批准这个PR吗？"

---

## Workflow 5: 高级查询

**Use when**: 用户需要自定义查询

### Phase 1: API查询

**Step 1.1 — 使用gh api**
```bash
# 获取PR特定字段
gh api repos/owner/repo/pulls/<pr-number> --jq '.title, .state, .user.login'

# 搜索PR
gh api search/issues --jq '.items[] | {number: .number, title: .title}' \
  -f q="repo:owner/repo type:pr is:open"
```

**Step 1.2 — JSON输出**
```bash
gh issue list --repo owner/repo --json number,title --jq '.[] | "\(.number): \(.title)"'
```

---

## 反例清单（What NOT to do）

1. **不要在未确认的情况下执行写操作** — 创建/关闭issue、批准PR前必须确认
2. **不要忽略权限问题** — 如果权限不足，告知用户需要提升权限
3. **不要长时间重试** — 网络失败重试2次即可，不要无限循环
4. **不要泄露敏感信息** — 日志中可能包含敏感数据，注意审查输出
5. **不要执行危险操作** — 删除仓库、强制推送等操作需要额外确认

---

## 失败处理

| 场景 | 处理方式 |
|------|----------|
| gh CLI未安装 | 提示用户安装：`brew install gh` 或 `sudo apt install gh` |
| 未登录 | 提示用户执行：`gh auth login` |
| 仓库不存在 | 提示用户检查owner/repo格式是否正确 |
| API限制 | 提示用户等待或使用API token |

---

## 输出格式规范

每次输出包含：
- [ ] 明确的命令说明
- [ ] 占位符用 `<angle-brackets>` 标记
- [ ] 失败情况说明
- [ ] 下一步操作建议
