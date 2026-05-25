# AI 内容智能体团队 — 设计文档

> 日期：2026-05-26
> 状态：已确认
> 方案：职能型（Functional）

---

## 1. 背景与目标

### 1.1 背景

现有 DevTeam 是面向软件开发的多智能体团队（6 角色），基于 OpenClaw 框架运行。现需新建一个面向**全栈内容创作**的智能体团队，覆盖国内社媒平台（公众号、小红书、微博、抖音）的内容策划、创作、运营和分析全链路。

### 1.2 目标

- 搭建 8 角色的内容智能体团队，覆盖内容生产全流程
- 与现有 DevTeam 独立运行但可互通协作
- 支持多角色方案评审机制，确保内容质量
- 复用 DevTeam 的架构模式（SOUL.md + AGENTS.md + config），降低学习成本

### 1.3 核心能力优先级

1. 智能写作（最高优先级）
2. 运营管理
3. 内容调研

---

## 2. 架构设计

### 2.1 方案选型

采用**职能型（Functional）架构**，按专业职能分三层：

| 层级 | 角色 | 说明 |
|------|------|------|
| 核心层 | director, writer, editor | 内容生产核心链路 |
| 专业层 | researcher, seo, operator | 专业支撑 |
| 支撑层 | analyst, designer | 数据与视觉支撑 |

选择理由：
- 与 DevTeam 架构模式一致，降低学习成本
- 核心层+专业层+支撑层结构既有分工又有协作弹性
- 策划总监作为调度中心，可灵活应对不同内容类型
- 复杂度适中，不过度工程化

### 2.2 角色定义

#### 核心层

| 角色 ID | 名称 | 职责 | 交付物 |
|---------|------|------|--------|
| `director` | 策划总监 | 内容策略制定、选题规划、团队调度、质量把控 | 内容日历、选题方案、任务分配 |
| `writer` | 内容写手 | 文章撰写、多风格改写、标题优化 | 文章初稿、社媒文案、视频脚本 |
| `editor` | 资深编辑 | 内容审核、润色、风格统一、事实核查 | 终稿、审核意见、风格指南 |

#### 专业层

| 角色 ID | 名称 | 职责 | 交付物 |
|---------|------|------|--------|
| `researcher` | 调研分析师 | 热点追踪、竞品分析、行业趋势、用户画像 | 调研报告、趋势分析、竞品动态 |
| `seo` | SEO/增长专家 | 关键词研究、SEO 优化、标题/描述优化、增长策略 | 关键词库、SEO 方案、增长建议 |
| `operator` | 社媒运营 | 发布排期、多平台分发、互动管理、粉丝运营 | 发布计划、运营报告、互动数据 |

#### 支撑层

| 角色 ID | 名称 | 职责 | 交付物 |
|---------|------|------|--------|
| `analyst` | 数据分析师 | 内容效果分析、数据看板、策略优化建议 | 数据报告、效果评估、优化建议 |
| `designer` | 视觉设计师 | 封面图设计、配图、视觉规范、排版优化 | 设计稿、配图素材、视觉规范 |

---

## 3. 项目结构

```
AI项目/
├── dev-team/                          # 现有开发团队（不变）
├── content-team/                      # 内容智能体团队
│   ├── agents/                        # 各角色 Agent 定义
│   │   ├── director/
│   │   │   └── SOUL.md
│   │   ├── writer/
│   │   │   └── SOUL.md
│   │   ├── editor/
│   │   │   └── SOUL.md
│   │   ├── researcher/
│   │   │   └── SOUL.md
│   │   ├── seo/
│   │   │   └── SOUL.md
│   │   ├── operator/
│   │   │   └── SOUL.md
│   │   ├── analyst/
│   │   │   └── SOUL.md
│   │   └── designer/
│   │       └── SOUL.md
│   ├── shared/                        # 共享资源
│   │   ├── content-calendar/          #   内容日历
│   │   ├── drafts/                    #   内容草稿
│   │   ├── research/                  #   调研报告
│   │   ├── seo-data/                  #   SEO 数据
│   │   ├── analytics/                 #   数据分析
│   │   ├── designs/                   #   设计素材
│   │   └── templates/                 #   内容模板
│   ├── AGENTS.md                      # Agent 总览
│   ├── SOUL.md                        # 团队灵魂/价值观
│   └── content-team-config.json       # 团队配置
```

---

## 4. 配置设计

### 4.1 与 DevTeam 的配置差异

| 配置项 | DevTeam | ContentTeam |
|--------|---------|-------------|
| identity.name | DevTeam | ContentTeam |
| identity.emoji | 🚀 | ✍️ |
| identity.theme | software development | content creation & operations |
| gateway.port | 18790 | 18791 |
| gateway.basePath | /dev-team | /content-team |
| workspace | ~/.openclaw/workspace/dev-team | ~/.openclaw/workspace/content-team |
| sandbox.workspaceRoot | ~/.openclaw/sandboxes/dev-team | ~/.openclaw/sandboxes/content-team |
| skills | github, trello, notion | notion, trello |
| channels | Slack | 飞书 |

### 4.2 模型配置

| 角色 | 主模型 | 备选模型 | 说明 |
|------|--------|----------|------|
| director | claude-sonnet-4-5 | gpt-4o | 强推理和调度能力 |
| writer | claude-sonnet-4-5 | gpt-4o | 强创作能力 |
| editor | claude-sonnet-4-5 | gpt-4o | 强审核和润色能力 |
| researcher | claude-sonnet-4-5 | gpt-4o | 强分析和总结能力 |
| seo | claude-sonnet-4-5 | gpt-4o | 关键词理解和优化 |
| operator | claude-sonnet-4-5 | gpt-4o | 平台规则理解 |
| analyst | claude-sonnet-4-5 | gpt-4o | 数据分析和推理 |
| designer | gpt-4o | claude-sonnet-4-5 | 视觉生成能力更强 |

### 4.3 A2A 互通配置

content-team 的 director 可与 dev-team 的 architect 和 ba 互通：

```json
"a2a": {
  "enabled": true,
  "allowFrom": ["writer", "editor", "researcher", "seo", "operator", "analyst", "designer"],
  "crossTeam": {
    "enabled": true,
    "allowTo": ["dev-team:architect", "dev-team:ba"]
  }
}
```

---

## 5. 协作工作流

### 5.1 日常内容生产

```
用户/系统 → director（选题立项）
  → researcher（调研）→ writer（撰写）→ seo（优化）
  → 【方案评审会】director + editor + seo + operator 集体评审
  → editor（终审润色）→ designer（配图）→ operator（发布）
  → analyst（效果追踪）→ director（复盘优化）
```

### 5.2 热点快速响应

```
analyst/researcher（发现热点）→ director（快速决策）
  → writer（紧急撰稿）
  → 【快速评审】director + editor 简审
  → operator（立即发布）
```

### 5.3 深度内容（报告/白皮书）

```
director（立项）→ researcher（深度调研，多轮）
  → writer（分章节撰写）→ seo（优化）
  → 【深度评审会】director + editor + researcher + seo + analyst 集体评审
  → writer（根据评审意见修改）→ editor（终审）
  → designer（排版设计）→ operator（发布）
  → analyst（长期效果追踪）
```

### 5.4 方案评审机制

| 评审模式 | 参与者 | 触发条件 | 产出 |
|----------|--------|----------|------|
| 快速评审 | director + editor | 热点/紧急内容 | 通过/修改意见 |
| 标准评审 | director + editor + seo + operator | 日常内容 | 评审记录 + 修改清单 |
| 深度评审 | director + editor + researcher + seo + analyst | 深度报告/白皮书 | 评审报告 + 优化方案 |

评审流程：

1. director 发起评审，将草稿放入共享区 `shared/drafts/`
2. 各角色在限定时间内阅读并提交评审意见：
   - editor：内容质量、逻辑、事实核查
   - seo：关键词覆盖、标题优化、可读性
   - operator：平台适配性、发布时机
   - researcher：数据准确性、论据支撑
   - analyst：预期效果、目标受众匹配度
3. director 汇总意见，决策：通过 / 修改后通过 / 打回重写
4. 评审记录存入 `shared/drafts/REVIEW-<编号>-<标题>.md`

### 5.5 内容状态流转

```
idea → drafted → reviewed → revised → approved → published → analyzed
  ↑                                           │
  └──────────── 复盘优化 ←────────────────────┘
```

| 状态 | 负责人 | 说明 |
|------|--------|------|
| idea | director | 选题立项 |
| drafted | writer | 初稿完成 |
| reviewed | 多角色 | 方案评审完成 |
| revised | writer | 根据评审意见修改完成 |
| approved | director | 终审批准 |
| published | operator | 已发布 |
| analyzed | analyst | 效果分析完成 |

---

## 6. 文件命名规范

| 类型 | 格式 | 示例 |
|------|------|------|
| 选题方案 | `PLAN-<编号>-<标题>.md` | `PLAN-001-618大促内容方案.md` |
| 调研报告 | `RPT-<编号>-<标题>.md` | `RPT-001-竞品小红书运营分析.md` |
| 内容草稿 | `DRAFT-<编号>-<标题>.md` | `DRAFT-001-AI工具推荐指南.md` |
| 数据报告 | `DATA-<编号>-<标题>.md` | `DATA-001-5月内容效果分析.md` |
| 设计素材 | `DESIGN-<编号>-<描述>.md` | `DESIGN-001-618封面图.md` |
| 评审记录 | `REVIEW-<编号>-<标题>.md` | `REVIEW-001-AI工具指南评审.md` |

---

## 7. 跨团队互通

### 7.1 ContentTeam ↔ DevTeam

| 场景 | 方向 | 说明 |
|------|------|------|
| 内容团队需要技术支持 | content→dev | director 向 architect 委派技术需求 |
| 开发团队需要内容支持 | dev→content | architect 向 director 委派内容需求 |
| 共享知识库 | 双向 | `~/.openclaw/shared/` 跨团队共享 |

### 7.2 共享文件区

```
~/.openclaw/shared/
├── dev-team/          # DevTeam 共享文件（现有）
├── content-team/      # ContentTeam 共享文件
└── cross-team/        # 跨团队共享文件
```

---

## 8. 核心价值观（SOUL.md）

1. **内容为王** — 每篇内容都要有价值，拒绝水文和低质填充
2. **数据说话** — 用数据驱动内容决策，不凭感觉选题
3. **用户视角** — 始终从读者角度思考，内容要解决真实问题
4. **快速迭代** — 先发布再优化，不追求一次完美
5. **团队共创** — 评审不是挑刺，是让好内容变得更好
