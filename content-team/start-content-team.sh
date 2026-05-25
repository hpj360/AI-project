#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "$SCRIPT_DIR/.." && pwd)"
CONFIG_PATH="$SCRIPT_DIR/content-team-config.json"

echo ""
echo "========================================"
echo "  启动 ContentTeam 内容智能体团队"
echo "========================================"
echo ""

if [ ! -f "$CONFIG_PATH" ]; then
    echo "[错误] 配置文件不存在: $CONFIG_PATH"
    exit 1
fi

if ! command -v node &>/dev/null; then
    echo "[错误] Node.js 未安装，请先运行 env-setup.sh 检查环境"
    exit 1
fi

if [ ! -d "$ROOT_DIR/node_modules/openclaw" ]; then
    echo "[提示] 正在安装 npm 依赖..."
    (cd "$ROOT_DIR" && npm install)
fi

env_file="$SCRIPT_DIR/.env"
if [ -f "$env_file" ]; then
    echo "[提示] 加载 .env 文件..."
    set -a
    while IFS='=' read -r key value; do
        key=$(echo "$key" | xargs)
        value=$(echo "$value" | xargs)
        case "$key" in
            ''|\#*) continue ;;
        esac
        export "$key=$value"
    done < "$env_file"
    set +a
fi

echo "[启动] ContentTeam (端口 18791)"
echo "[配置] $CONFIG_PATH"
echo ""

cd "$ROOT_DIR"
npx openclaw start --config "$CONFIG_PATH"
