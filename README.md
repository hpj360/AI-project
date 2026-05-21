# AI 项目

AI 驱动的多智能体协作平台，集成 OpenClaw、Skillhub、开发团队和项目管理工具。

## 项目结构

```
AI项目/
├── dev-team/                    # 开发团队智能体配置
│   ├── agents/                  # 各角色 Agent 定义
│   │   ├── ba/                  #   业务分析师
│   │   ├── architect/           #   产品架构师
│   │   ├── backend/             #   后端开发工程师
│   │   ├── frontend/            #   前端开发工程师
│   │   ├── qa/                  #   测试工程师
│   │   └── ui/                  #   UI 设计师
│   ├── shared/                  # 共享资源
│   │   ├── api-specs/           #   API 规范 (YAML)
│   │   ├── architecture/        #   架构文档
│   │   └── requirements/        #   需求文档
│   ├── AGENTS.md                # Agent 总览
│   ├── SOUL.md                  # 团队灵魂/价值观
│   └── dev-team-config.json     # 团队配置
│
├── pm-team/                     # 项目管理团队 (独立 Git 仓库)
│   ├── openclaw.json            # OpenClaw 飞书 Bot 配置
│   ├── package.json             # Node.js 依赖
│   ├── env-check.ps1            # 环境检查脚本 (Windows)
│   ├── env-check.sh             # 环境检查脚本 (Linux/Mac)
│   └── README.md
│
├── skillhub-local/              # Skillhub 本地 CLI
│   ├── skills_store_cli.py      # 技能商店 CLI 主程序
│   ├── skills_upgrade.py        # 自升级模块
│   ├── skillhub.bat             # Windows 启动脚本
│   ├── metadata.json            # 元数据
│   └── version.json             # 版本信息
│
├── skillhub/                    # Skillhub 完整发行版
│   └── cli/                     # CLI + 插件 + 技能
│       ├── plugin/              #   OpenClaw 插件
│       ├── skill/               #   技能定义
│       ├── install.sh           #   安装脚本
│       └── SKILL.md             #   技能说明
│
├── OpenClaw/                    # OpenClaw 主项目源码
│   └── openclaw-main/           #   主程序 (TypeScript)
│
├── scripts/                     # 工具脚本
│   ├── sync.ps1                 # Git 同步工具 (pull/push/status)
│   ├── install-skillhub.bat     # Skillhub 完整安装
│   ├── install-skillhub-simple.bat  # Skillhub 简易安装
│   ├── install-self-improving-agent.ps1  # 自改进 Agent 安装
│   ├── install_skills.py        # 批量安装技能
│   ├── install.sh               # Linux/Mac 安装
│   ├── run-skillhub.ps1         # 运行 Skillhub
│   ├── test-skillhub.ps1/py     # 测试 Skillhub
│   ├── upgrade-skillhub.py      # 升级 Skillhub
│   ├── skillhub.bat             # Skillhub 包装脚本
│   └── skillhub-install.sh      # Skillhub 远程安装
│
├── docs/                        # 文档
│   ├── SKILLHUB-WINDOWS-INSTALL.md  # Skillhub Windows 安装指南
│   ├── skill-creator-update-guide.md # Skill Creator 更新指南
│   └── skills-install-guide.md      # 技能安装指南
│
├── agile-team-agent.json        # DevTeam 敏捷团队 Agent 配置
├── package.json                 # Node.js 依赖 (openclaw)
├── .gitignore
└── README.md
```

## 核心模块说明

### 1. DevTeam - 开发团队智能体

基于 OpenClaw 的多智能体协作系统，包含 6 个角色：

| 角色 | 职责 | 技能 |
|------|------|------|
| BA (业务分析师) | 需求分析、用户故事 | Notion, Trello |
| Architect (架构师) | 系统架构、技术选型 | GitHub, Notion |
| Frontend (前端) | UI 实现、组件开发 | GitHub, Notion |
| Backend (后端) | API 开发、数据库 | GitHub, Notion |
| QA (测试) | 测试计划、自动化 | GitHub, Trello |
| UI Designer (设计师) | 界面设计、交互规范 | Notion, Trello |

- **模型**: Claude Sonnet 4.5 (主) / GPT-4o (备)
- **协作**: 支持 Agent-to-Agent (A2A) 通信
- **配置**: `agile-team-agent.json` / `dev-team/dev-team-config.json`

### 2. PM Team - 项目管理

基于 OpenClaw 的飞书 Bot 集成，用于项目管理和团队协作。

- **仓库**: [hpj360/pm-team](https://github.com/hpj360/pm-team)
- **功能**: 飞书消息处理、环境检查

### 3. Skillhub - 技能管理平台

本地技能商店 CLI，支持搜索、安装、升级 Agent 技能。

```bash
# 搜索技能
python skillhub-local/skills_store_cli.py search <keyword>

# 自升级
python skillhub-local/skills_store_cli.py self-upgrade
```

**已安装技能**: product-manager, product-manager-skills, aipm-news-digest, self-improving-agent

### 4. OpenClaw - AI Agent 框架

开源 AI Agent 框架，支持多渠道（WhatsApp、Telegram、Slack 等）。

- **依赖**: `openclaw` (npm)
- **源码**: `OpenClaw/openclaw-main/` (TypeScript)

## 快速开始

### 环境要求

- Node.js 18+
- Python 3.7+
- Git

### 安装

```bash
# 克隆项目
git clone git@github.com:hpj360/AI-project.git
cd AI项目

# 安装 Node.js 依赖
npm install

# 安装 Skillhub
scripts/install-skillhub-simple.bat    # Windows
scripts/install.sh                     # Linux/Mac
```

### 同步

```powershell
# 拉取云端最新
.\scripts\sync.ps1 pull

# 推送本地变更
.\scripts\sync.ps1 push

# 查看同步状态
.\scripts\sync.ps1 status
```

## Git 仓库

| 仓库 | 地址 | 说明 |
|------|------|------|
| AI项目 (主仓库) | `git@github.com:hpj360/AI-project.git` | 主项目 |
| PM Team | `https://github.com/hpj360/pm-team.git` | 项目管理 (嵌套) |
