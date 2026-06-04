---
name: skill-manager
description: |
  管理所有已安装的skill，包括列出、安装、更新、卸载、搜索和配置管理。
  触发词：安装skill、更新skill、列出skill、搜索skill、卸载skill、skill管理、列出已安装skill
---

# Skill Manager

全面管理已安装的skill，提供完整的生命周期管理功能。

## 🔴 CHECKPOINT · Before Any Write Operation

Confirm the target skill name with user before installing, updating, or uninstalling. Unintended operations can break other skills.

## 工作流程

### 列出技能

**Step 1 — 执行 list 命令**
```
skillhub list
```
Output: 已安装skill列表（名称、版本、安装时间）

**Step 2 — 展示结果**
展示给用户，包含：skill名称、版本号、安装来源

**如果 skillhub 不可用 → fallback:**
```
# 检查本地 skills 目录
ls ~/.trae/skills/ 或 ls ~/.openclaw/skills/
```

---

### 安装技能

**Step 1 — 确认skill名称**
```
Input: 用户提供的skill名称
Output: 确认要安装的skill名
```
**🔴 CHECKPOINT · 展示安装计划给用户确认后再执行:**
- 安装来源：skillhub
- 目标路径：`~/.trae/skills/<skill-name>`
- 如已存在：会覆盖现有版本

**Step 2 — 搜索确认skill存在**
```
skillhub search <skill-name>
```
**如果搜索返回空 → 尝试模糊搜索:**
```
skillhub search <关键字>
```

**Step 3 — 执行安装**
```
skillhub install <skill-name>
```
Output: 安装结果（成功/失败）

**失败分支:**
| 触发条件 | 一线修复 | 仍失败→兜底 |
|----------|----------|------------|
| HTTP 404（skill不存在）| 拼写检查，搜索正确的slug | 告知用户skill不存在 |
| HTTP 403/网络超时 | 重试2次（间隔3秒）| 告知网络问题，提示手动安装 |
| 目标目录已存在 | 提示使用 `--force` 覆盖 | 先 `rm -rf <目标目录>` 再重试 |
| 磁盘空间不足 | — | 告知用户清理磁盘空间 |

**Step 4 — 验证安装**
```
skillhub list | grep <skill-name>
```
确认skill出现在列表中。

---

### 更新技能

**Step 1 — 确定更新范围**
```
# 检查所有skill更新
skillhub check

# 或检查特定skill
skillhub check <skill-name>
```

**Step 2 — 🔴 CHECKPOINT · 展示更新内容给用户确认**
列出：哪些skill有新版本 → 用户确认后再执行

**Step 3 — 执行更新**
```
skillhub update <skill-name>
# 或全部更新
skillhub update --all
```

**失败分支:**
| 触发条件 | 处理方式 |
|----------|----------|
| skill目录非git仓库 | 更新失败，告知用户无法自动更新，需要手动git pull |
| git push需要认证 | 告知用户认证问题，需要手动处理 |
| 网络失败 | 重试2次，仍失败则告知用户稍后重试 |

---

### 卸载技能

**Step 1 — 🔴 CHECKPOINT · 双重确认**
```
展示：
- 要卸载的skill：<name>
- 目标路径：~/.trae/skills/<name>
- 风险：删除后不可恢复

等待用户明确说"确认删除"后再执行
```

**Step 2 — 执行卸载**
```
skillhub uninstall <skill-name>
```

**失败分支:**
| 触发条件 | 处理方式 |
|----------|----------|
| 目录不存在 | 告知用户skill未安装，无需卸载 |
| 权限不足 | 告知用户需要sudo或手动删除 |
| 仍在使用中 | 告知用户当前session正在使用，建议关闭session后卸载 |

**Step 3 — 确认删除**
```
ls ~/.trae/skills/<skill-name> 2>/dev/null && echo "仍存在" || echo "已删除"
```

---

### 搜索技能

**Step 1 — 执行搜索**
```
skillhub search <query>
```
Output: skill列表（含名称、描述、版本）

**Step 2 — 展示结果**
按相关性排序，展示前10个结果

**失败分支:**
| 触发条件 | 处理方式 |
|----------|----------|
| 返回空结果 | 提示用户尝试不同关键词，或搜索更宽泛的术语 |
| 网络失败 | fallback到本地缓存搜索（如果有）|

---

### 配置管理

**Step 1 — 查看配置**
```
skillhub config <skill-name>
```

**Step 2 — 🔴 CHECKPOINT · 修改前确认**
展示当前配置 → 用户确认后再修改

**Step 3 — 修改配置**
```
skillhub config <skill-name> <key> <value>
```

**失败分支:**
| 触发条件 | 处理方式 |
|----------|----------|
| skill无配置文件 | 告知用户该skill无配置选项 |
| key不存在 | 告知用户有效key列表 |

---

## 注意事项

- 确保 skillhub 命令可用：`which skillhub` 或 `python3 skills_store_cli.py`
- **网络问题 → 自动尝试 clawhub 备选源**
- 安装前会备份原始配置
- 配置修改前自动备份，变更前告知用户

## Anti-Patterns (What NOT to do)

- Do NOT install skills without explicit user confirmation on the skill name
- Do NOT uninstall skills without double-confirmation — deletion is irreversible
- Do NOT update all skills at once without showing what will change
- Do NOT assume skillhub is always available — always check fallback path first
- Do NOT modify skill files directly — always use the skill manager commands

## 常见问题处理

| 场景 | 命令 |
|------|------|
| skill安装后不生效 | 检查skill目录是否有SKILL.md；重启session |
| skill冲突 | 列出同名skill，确认使用哪个版本 |
| 手动安装的skill | 使用 `ls ~/.trae/skills/` 手动管理，不走skillhub |
