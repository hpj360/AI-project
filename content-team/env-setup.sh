#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"

echo ""
echo "========================================"
echo "  ContentTeam 环境配置脚本 (Linux/Mac)"
echo "========================================"
echo ""

check_command() {
    if command -v "$1" &>/dev/null; then
        return 0
    else
        return 1
    fi
}

check_env_var() {
    local name="$1"
    local desc="$2"
    local required="${3:-true}"
    local val="${!name:-}"
    if [ -n "$val" ]; then
        echo "  [OK] $desc ($name) 已设置"
        return 0
    else
        local tag="可选"
        [ "$required" = true ] && tag="必须"
        echo "  [--] $desc ($name) 未设置 [$tag]"
        return 1
    fi
}

echo "--- 1. 检查运行时依赖 ---"
echo ""

node_ok=false
if check_command node; then
    node_ver=$(node --version 2>/dev/null)
    major=$(echo "$node_ver" | sed 's/v\([0-9]*\).*/\1/')
    if [ "$major" -ge 22 ]; then
        echo "  [OK] Node.js $node_ver (>= 22.16.0)"
        node_ok=true
    else
        echo "  [!!] Node.js $node_ver 版本过低，需要 >= 22.16.0"
    fi
else
    echo "  [!!] Node.js 未安装，请前往 https://nodejs.org 安装 v22+"
fi

if check_command npm; then
    npm_ver=$(npm --version 2>/dev/null)
    echo "  [OK] npm $npm_ver"
else
    echo "  [!!] npm 未安装"
fi

if check_command pnpm; then
    pnpm_ver=$(pnpm --version 2>/dev/null)
    echo "  [OK] pnpm $pnpm_ver"
else
    echo "  [--] pnpm 未安装 (OpenClaw 源码构建需要)"
fi

if check_command python3 || check_command python; then
    py_ver=$(python3 --version 2>/dev/null || python --version 2>/dev/null)
    echo "  [OK] Python $py_ver"
else
    echo "  [--] Python 未安装 (Skillhub CLI 需要)"
fi

echo ""
echo "--- 2. 检查 Skill 工具依赖 ---"
echo ""

if check_command jq; then
    echo "  [OK] jq 已安装 (Trello skill 依赖)"
else
    echo "  [--] jq 未安装 (Trello skill 依赖)"
    echo "      安装: sudo apt install jq / brew install jq"
fi

if check_command gh; then
    echo "  [OK] GitHub CLI 已安装 (github skill 依赖)"
else
    echo "  [--] GitHub CLI 未安装 (github skill 依赖)"
    echo "      安装: https://cli.github.com/"
fi

if check_command blogwatcher; then
    echo "  [OK] blogwatcher 已安装 (调研 skill)"
else
    echo "  [--] blogwatcher 未安装 (调研 skill, 可选)"
    echo "      安装: go install github.com/Hyaxia/blogwatcher/cmd/blogwatcher@latest"
fi

if check_command summarize; then
    echo "  [OK] summarize 已安装 (摘要 skill)"
else
    echo "  [--] summarize 未安装 (摘要 skill, 可选)"
fi

echo ""
echo "--- 3. 检查环境变量 ---"
echo ""

check_env_var FEISHU_BOT_TOKEN "飞书 Bot Token" true
check_env_var NOTION_API_KEY "Notion API Key" true
check_env_var TRELLO_API_KEY "Trello API Key" true
check_env_var TRELLO_TOKEN "Trello Token" true
check_env_var OPENAI_API_KEY "OpenAI API Key (designer/图片生成)" false
check_env_var ANTHROPIC_API_KEY "Anthropic API Key (主模型)" false

echo ""
echo "--- 4. 检查 npm 依赖 ---"
echo ""

if [ -d "$ROOT_DIR/node_modules/openclaw" ]; then
    echo "  [OK] openclaw npm 包已安装"
else
    echo "  [!!] openclaw npm 包未安装"
    echo "      运行: cd $ROOT_DIR && npm install"
fi

echo ""
echo "--- 5. 检查 ContentTeam 配置 ---"
echo ""

config_path="$SCRIPT_DIR/content-team-config.json"
if [ -f "$config_path" ]; then
    if python3 -c "import json; json.load(open('$config_path'))" 2>/dev/null || python -c "import json; json.load(open('$config_path'))" 2>/dev/null || jq empty "$config_path" 2>/dev/null; then
        echo "  [OK] content-team-config.json 格式正确"
    else
        echo "  [!!] content-team-config.json JSON 格式错误"
    fi
else
    echo "  [!!] content-team-config.json 不存在"
fi

agent_count=$(find "$SCRIPT_DIR/agents" -mindepth 1 -maxdepth 1 -type d 2>/dev/null | wc -l)
if [ "$agent_count" -eq 8 ]; then
    echo "  [OK] 8 个 Agent 目录完整"
else
    echo "  [!!] Agent 目录数量: $agent_count (应为 8)"
fi

soul_count=$(find "$SCRIPT_DIR/agents" -name "SOUL.md" 2>/dev/null | wc -l)
if [ "$soul_count" -eq 8 ]; then
    echo "  [OK] 8 个 SOUL.md 文件完整"
else
    echo "  [!!] SOUL.md 文件数量: $soul_count (应为 8)"
fi

echo ""
echo "========================================"
echo "  检查完成"
echo "========================================"
echo ""
echo "下一步操作:"
echo "  1. 安装缺失的运行时依赖 (Node.js 22+, npm, pnpm)"
echo "  2. 设置环境变量 (FEISHU_BOT_TOKEN, NOTION_API_KEY 等)"
echo "  3. 安装 npm 依赖: cd $ROOT_DIR && npm install"
echo "  4. 启动团队: bash $SCRIPT_DIR/start-content-team.sh"
echo ""
