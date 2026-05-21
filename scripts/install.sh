#!/usr/bin/env bash
set -euo pipefail

KIT_URL="https://skillhub-1251783334.cos.ap-guangzhou.myqcloud.com/install/latest.tar.gz"

TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

# 下载安装包(带重试机制)
MAX_RETRIES=3
RETRY_INTERVAL=2
retry_count=0

echo "正在下载安装包..."
while [ $retry_count -lt $MAX_RETRIES ]; do
  if curl -fSL --progress-bar "$KIT_URL" -o "$TMP_DIR/latest.tar.gz"; then
    download_success=true
    break
  else
    retry_count=$((retry_count + 1))
    if [ $retry_count -lt $MAX_RETRIES ]; then
      echo "下载失败,${RETRY_INTERVAL}秒后重试 ($retry_count/$MAX_RETRIES)..." >&2
      sleep $RETRY_INTERVAL
    else
      download_success=false
    fi
  fi
done

if [ "$download_success" = false ]; then
  echo "错误: 下载安装包失败,已重试 $MAX_RETRIES 次" >&2
  echo "可能的原因:" >&2
  echo "  - 网络连接不稳定" >&2
  echo "  - 下载地址不可用,请联系管理员" >&2
  echo "  - 防火墙或代理阻止了下载" >&2
  exit 1
fi

# 解压安装包
echo "正在解压安装包..."
if ! tar -xzf "$TMP_DIR/latest.tar.gz" -C "$TMP_DIR"; then
  echo "错误: 解压安装包失败" >&2
  echo "可能的原因:" >&2
  echo "  - 下载的文件已损坏" >&2
  echo "  - 磁盘空间不足" >&2
  echo "  - 文件格式不正确" >&2
  exit 1
fi

echo "安装包准备完成"

INSTALLER="$TMP_DIR/cli/install.sh"
if [[ ! -f "$INSTALLER" ]]; then
  echo "Error: install.sh not found at $INSTALLER" >&2
  find "$TMP_DIR" -maxdepth 3 -print >&2
  exit 1
fi

bash "$INSTALLER" "$@"
