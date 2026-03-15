---
name: skill-manager
description: 管理所有已安装的skill，包括列出、安装、更新、卸载、搜索和配置管理
---

# Skill Manager

这个技能用于全面管理已安装的skill，提供完整的生命周期管理功能。

## 功能

- **列出技能**：显示所有已安装的skill及其状态
- **安装技能**：从skillhub或其他源安装新的skill
- **更新技能**：检查并更新现有的skill到最新版本
- **卸载技能**：移除不需要的skill
- **搜索技能**：在skillhub中搜索新的skill
- **配置管理**：查看和修改skill的配置

## 工作流程

### 列出技能

运行以下命令查看所有已安装的skill：

```bash
skillhub list
```

### 安装技能

从skillhub安装新的skill：

```bash
skillhub install <skill-name>
```

### 更新技能

更新所有已安装的skill或特定skill：

```bash
# 更新所有skill
skillhub update

# 更新特定skill
skillhub update <skill-name>
```

### 卸载技能

移除不需要的skill：

```bash
skillhub uninstall <skill-name>
```

### 搜索技能

在skillhub中搜索新的skill：

```bash
skillhub search <query>
```

### 配置管理

查看和修改skill的配置：

```bash
# 查看配置
skillhub config <skill-name>

# 修改配置
skillhub config <skill-name> <key> <value>
```

## 使用示例

1. **列出所有技能**：
   - 输入："列出所有已安装的skill"
   - 操作：运行 `skillhub list` 并展示结果

2. **安装新技能**：
   - 输入："安装一个代码审查的skill"
   - 操作：运行 `skillhub search code review`，展示结果，然后安装用户选择的skill

3. **更新技能**：
   - 输入："更新所有skill"
   - 操作：运行 `skillhub update` 并展示更新结果

4. **卸载技能**：
   - 输入："卸载不需要的skill"
   - 操作：运行 `skillhub list`，用户选择要卸载的skill，然后运行 `skillhub uninstall <skill-name>`

5. **搜索技能**：
   - 输入："搜索与前端开发相关的skill"
   - 操作：运行 `skillhub search frontend` 并展示结果

6. **管理配置**：
   - 输入："查看skill的配置"
   - 操作：运行 `skillhub config <skill-name>` 并展示配置信息

## 注意事项

- 确保skillhub命令可用且已正确安装
- 对于网络问题，会自动尝试使用clawhub作为备选
- 安装前会检查技能的安全性和兼容性
- 配置修改时会备份原始配置，以便恢复