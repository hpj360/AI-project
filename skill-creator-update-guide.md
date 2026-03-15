# skill-creator 最新版更新指南

## 概述
skill-creator 是 OpenClaw/skillhub 项目中的一个技能，用于创建和打包技能。本文档介绍如何更新 skill-creator 到最新版本。

## 当前状态

- **当前 skillhub 版本**: 2026.3.13
- **skill-creator**: 是 OpenClaw 项目的内置技能之一

## 更新方法

### 方法 1: 使用 skillhub self-upgrade（推荐）

在命令行中运行：
```bash
# Windows
skillhub self-upgrade

# 或者使用完整路径
python d:\AI项目\skillhub-local\skills_store_cli.py self-upgrade
```

### 方法 2: 手动更新

如果自动更新失败，可以手动更新：

1. 访问 https://github.com/anthropics/skills 查看最新的 skill-creator
2. 或者访问 skillhub 的更新源获取最新版本
3. 下载最新的 skillhub 包
4. 替换旧的文件

### 方法 3: 在 OpenClaw 中更新

如果你在使用 OpenClaw：

1. 确保 OpenClaw 是最新版本
2. skill-creator 通常随 OpenClaw 一起更新
3. 检查 OpenClaw 的 CHANGELOG.md 查看 skill-creator 的更新记录

## skill-creator 功能

根据 OpenClaw 的 CHANGELOG.md，skill-creator 提供以下功能：

- 指导创建和打包技能
- 安全加固：跳过符号链接条目，拒绝路径逃出技能根目录的文件
- 帮助你创建符合标准的技能格式

## 验证更新

更新完成后，你可以：

1. 检查 version.json 文件的版本号
2. 尝试创建一个新技能来验证功能
3. 查看是否有新的安全特性或功能改进

## 注意事项

- 更新前备份当前的技能文件
- 确保有足够的权限写入文件
- 如果在更新过程中遇到问题，可以回滚到备份版本

## 获取帮助

如果遇到更新问题，可以：
- 查看 skillhub 的错误日志
- 访问 OpenClaw 的 GitHub 仓库提交 issue
- 查看相关文档
