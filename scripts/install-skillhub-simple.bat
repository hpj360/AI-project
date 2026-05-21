@echo off

set "INSTALL_BASE=%USERPROFILE%\.skillhub"
set "BIN_DIR=%USERPROFILE%\.local\bin"

:: 创建必要的目录
mkdir "%INSTALL_BASE%" 2>nul
mkdir "%BIN_DIR%" 2>nul

:: 复制文件
copy "skills_store_cli.py" "%INSTALL_BASE%\skills_store_cli.py"
copy "skills_upgrade.py" "%INSTALL_BASE%\skills_upgrade.py"
copy "version.json" "%INSTALL_BASE%\version.json"
copy "metadata.json" "%INSTALL_BASE%\metadata.json"

:: 创建配置文件
if not exist "%INSTALL_BASE%\config.json" (
    echo {
    echo   "self_update_url": "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/version.json"
    echo } > "%INSTALL_BASE%\config.json"
)

:: 创建包装脚本
echo @echo off > "%BIN_DIR%\skillhub.bat"
echo set "BASE=%USERPROFILE%\.skillhub" >> "%BIN_DIR%\skillhub.bat"
echo set "CLI=%%BASE%%\skills_store_cli.py" >> "%BIN_DIR%\skillhub.bat"
echo if not exist "%%CLI%%" ( >> "%BIN_DIR%\skillhub.bat"
echo   echo Error: CLI not found at %%CLI%% >> "%BIN_DIR%\skillhub.bat"
echo   exit /b 1 >> "%BIN_DIR%\skillhub.bat"
echo ) >> "%BIN_DIR%\skillhub.bat"
echo python "%%CLI%%" %%* >> "%BIN_DIR%\skillhub.bat"

echo 安装完成。
echo CLI: %BIN_DIR%\skillhub.bat
