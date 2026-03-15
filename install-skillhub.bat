@echo off

set "INSTALL_BASE=%USERPROFILE%\.skillhub"
set "BIN_DIR=%USERPROFILE%\.local\bin"
set "CLI_TARGET=%INSTALL_BASE%\skills_store_cli.py"
set "UPGRADE_MODULE_TARGET=%INSTALL_BASE%\skills_upgrade.py"
set "VERSION_TARGET=%INSTALL_BASE%\version.json"
set "METADATA_TARGET=%INSTALL_BASE%\metadata.json"
set "CONFIG_TARGET=%INSTALL_BASE%\config.json"
set "WRAPPER_TARGET=%BIN_DIR%\skillhub.bat"
set "LEGACY_WRAPPER_TARGET=%BIN_DIR%\oc-skills.bat"

set "PLUGIN_TARGET_DIR=%USERPROFILE%\.openclaw\extensions\skillhub"
set "FIND_SKILL_TARGET_DIR=%USERPROFILE%\.openclaw\workspace\skills\find-skills"
set "PREFERENCE_SKILL_TARGET_DIR=%USERPROFILE%\.openclaw\workspace\skills\skillhub-preference"

:: 创建必要的目录
mkdir "%INSTALL_BASE%" 2>nul
mkdir "%BIN_DIR%" 2>nul
mkdir "%PLUGIN_TARGET_DIR%" 2>nul
mkdir "%FIND_SKILL_TARGET_DIR%" 2>nul
mkdir "%PREFERENCE_SKILL_TARGET_DIR%" 2>nul

:: 复制文件
copy "d:\AI项目\skillhub\cli\skills_store_cli.py" "%CLI_TARGET%"
copy "d:\AI项目\skillhub\cli\skills_upgrade.py" "%UPGRADE_MODULE_TARGET%"
copy "d:\AI项目\skillhub\cli\version.json" "%VERSION_TARGET%"
copy "d:\AI项目\skillhub\cli\metadata.json" "%METADATA_TARGET%"

:: 创建配置文件
if not exist "%CONFIG_TARGET%" (
    echo {
    echo   "self_update_url": "https://skillhub-1388575217.cos.ap-guangzhou.myqcloud.com/version.json"
    echo } > "%CONFIG_TARGET%"
)

:: 创建包装脚本
echo @echo off > "%WRAPPER_TARGET%"
echo set "BASE=%USERPROFILE%\.skillhub" >> "%WRAPPER_TARGET%"
echo set "CLI=%%BASE%%\skills_store_cli.py" >> "%WRAPPER_TARGET%"
echo if not exist "%%CLI%%" ( >> "%WRAPPER_TARGET%"
echo   echo Error: CLI not found at %%CLI%% >> "%WRAPPER_TARGET%"
echo   exit /b 1 >> "%WRAPPER_TARGET%"
echo ) >> "%WRAPPER_TARGET%"
echo python "%%CLI%%" %%* >> "%WRAPPER_TARGET%"

:: 创建 legacy 包装脚本
echo @echo off > "%LEGACY_WRAPPER_TARGET%"
echo "%BIN_DIR%\skillhub.bat" %%* >> "%LEGACY_WRAPPER_TARGET%"

:: 复制插件文件
copy "d:\AI项目\skillhub\cli\plugin\index.ts" "%PLUGIN_TARGET_DIR%\index.ts"
copy "d:\AI项目\skillhub\cli\plugin\openclaw.plugin.json" "%PLUGIN_TARGET_DIR%\openclaw.plugin.json"

:: 复制技能文件
copy "d:\AI项目\skillhub\cli\skill\SKILL.md" "%FIND_SKILL_TARGET_DIR%\SKILL.md"
copy "d:\AI项目\skillhub\cli\skill\SKILL.skillhub-preference.md" "%PREFERENCE_SKILL_TARGET_DIR%\SKILL.md"

echo 安装完成。
echo 模式: all
echo CLI: %WRAPPER_TARGET%
echo 技能: %FIND_SKILL_TARGET_DIR%\SKILL.md
echo 技能: %PREFERENCE_SKILL_TARGET_DIR%\SKILL.md
echo 插件: %PLUGIN_TARGET_DIR%

echo 快速检查:
echo   skillhub search calendar
echo   if exist "%FIND_SKILL_TARGET_DIR%\SKILL.md" echo find-skills-installed
echo   if exist "%PREFERENCE_SKILL_TARGET_DIR%\SKILL.md" echo skillhub-preference-installed
echo   如果使用 OpenClaw: openclaw plugins list ^| findstr skillhub
