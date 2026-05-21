# 技能安装指南

## 推荐的技能仓库

### 1. Anthropic Skills（官方仓库）
- **GitHub地址**: https://github.com/anthropics/skills
- **特点**:
  - Anthropic 官方出品的 Agent Skills 仓库
  - 包含 16+ 个官方示例技能
  - 涵盖办公套件（Word/PDF/PPT/Excel）、开发工具、创意工具等多个领域
  - Claude Code 和 Claude.ai 都可直接使用
  - 官方维护，质量保证

### 2. Superpowers
- **GitHub地址**: https://github.com/obra/superpowers
- **特点**:
  - 完整的软件开发工作流，基于一套可组合的技能
  - 覆盖脑暴、写需求文档、开发、测试全流程
  - 支持 TDD（测试驱动开发）、YAGNI、DRY 等最佳实践
  - 包含子代理驱动开发、代码审查等高级功能
  - 口碑极佳，适合专业开发者

---

## 各平台安装方法

### Claude Code（推荐）

#### 安装 Anthropic Skills
```
/plugin marketplace add anthropics/skills
/plugin install document-skills@anthropic-agent-skills
/plugin install example-skills@anthropic-agent-skills
```

#### 安装 Superpowers
```
/plugin install superpowers@claude-plugins-official
```

### OpenClaw

由于 OpenClaw 正在开发中，建议以下方法：

1. 将技能仓库克隆到本地目录
2. 在 OpenClaw 项目中创建 `skills/` 文件夹
3. 手动复制技能文件到该目录

### Cursor

#### 安装 Superpowers
```
/add-plugin superpowers
```
或者在插件市场搜索 "superpowers"

### Gemini CLI

#### 安装 Superpowers
```
gemini extensions install https://github.com/obra/superpowers
```

---

## 手动安装（无需 Git）

如果无法使用 Git 克隆，你可以：

1. 访问每个仓库的 GitHub 页面
2. 点击 "Code" 按钮
3. 选择 "Download ZIP"
4. 解压下载的文件
5. 将技能文件夹复制到你的项目中

---

## 使用建议

### 优先安装顺序：

1. **Anthropic Skills** - 官方技能，质量保证，适合日常使用
2. **Superpowers** - 专业开发技能，适合软件开发项目
3. **Planning-with-files** - 复杂任务规划，适合多步骤项目

### 验证安装：

安装完成后，尝试以下命令：
- 对于 Claude Code：让 AI 帮你做一个简单的任务，看看技能是否自动触发
- 对于 Cursor：在 Agent chat 中说 "help me plan this feature"

---

## 注意事项

- 确保你的 IDE/平台支持 Agent Skills
- 部分技能可能需要特定版本的平台
- 建议先阅读技能的 README 文档了解详细用法
