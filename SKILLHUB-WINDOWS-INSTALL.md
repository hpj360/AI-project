# Skillhub Windows 安装指南

## 前提条件

在安装skillhub之前，您需要确保系统上安装了以下软件：

1. **Python 3.7+** - skillhub需要Python 3来运行
2. **Git** - 用于克隆和管理代码

## 安装步骤

### 步骤 1: 安装Python 3

1. 访问 [Python官方网站](https://www.python.org/downloads/windows/)
2. 下载最新的Python 3安装包（64位）
3. 运行安装程序，确保勾选"Add Python to PATH"选项
4. 完成安装后，打开命令提示符并运行 `python --version` 来验证安装

### 步骤 2: 安装Git（可选）

1. 访问 [Git for Windows](https://git-scm.com/download/win)
2. 下载并安装Git，使用默认选项
3. 完成安装后，打开Git Bash并运行 `git --version` 来验证安装

### 步骤 3: 安装Skillhub

1. 打开命令提示符或Git Bash
2. 导航到您想要安装skillhub的目录
3. 运行以下命令：

```bash
# 克隆skillhub仓库
git clone https://github.com/your-repo/skillhub.git

# 进入skillhub目录
cd skillhub

# 运行安装脚本
bash install.sh
```

### 步骤 4: 手动安装（如果自动安装失败）

如果自动安装脚本在Windows上失败，您可以手动安装skillhub：

1. 创建必要的目录：
   - `%USERPROFILE%\.skillhub`
   - `%USERPROFILE%\.local\bin`

2. 复制以下文件到 `%USERPROFILE%\.skillhub` 目录：
   - `skills_store_cli.py`
   - `skills_upgrade.py`
   - `version.json`
   - `metadata.json`

3. 创建配置文件 `%USERPROFILE%\.skillhub\config.json`：

```json
{
  "self_update_url": "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/version.json"
}
```

4. 创建批处理文件 `%USERPROFILE%\.local\bin\skillhub.bat`：

```batch
@echo off
set "BASE=%USERPROFILE%\.skillhub"
set "CLI=%BASE%\skills_store_cli.py"
if not exist "%CLI%" (
  echo Error: CLI not found at %CLI%
  exit /b 1
)
python "%CLI%" %*
```

5. 将 `%USERPROFILE%\.local\bin` 添加到系统PATH环境变量中

## 验证安装

1. 打开命令提示符
2. 运行 `skillhub --help` 来验证skillhub是否安装成功
3. 运行 `skillhub search calendar` 来测试基本功能

## 故障排除

### 问题：`skillhub` 命令未找到

**解决方案**：
- 确保 `%USERPROFILE%\.local\bin` 已添加到系统PATH环境变量中
- 重新启动命令提示符以应用环境变量更改
- 尝试使用完整路径运行：`%USERPROFILE%\.local\bin\skillhub.bat`

### 问题：Python 命令未找到

**解决方案**：
- 确保Python已安装并添加到PATH中
- 尝试使用完整路径运行Python：`C:\Python39\python.exe`（根据您的Python安装路径调整）

### 问题：权限错误

**解决方案**：
- 以管理员身份运行命令提示符
- 检查目录权限，确保您有读写权限

## 联系方式

如果您在安装过程中遇到任何问题，请联系：
- 电子邮件：support@skillhub.com
- GitHub：https://github.com/your-repo/skillhub/issues
