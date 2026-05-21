@echo off
chcp 65001 >nul
echo ========================================
echo   AI项目 同步工具
echo ========================================
echo.

if "%1"=="push" goto PUSH
if "%1"=="PUSH" goto PUSH
if "%1"=="pull" goto PULL
if "%1"=="PULL" goto PULL
if "%1"=="status" goto STATUS
if "%1"=="STATUS" goto STATUS
goto MENU

:MENU
echo 请选择操作：
echo   1. 拉取云端最新代码 (pull)
echo   2. 推送本地修改到云端 (push)
echo   3. 查看同步状态 (status)
echo   4. 退出
echo.
set /p choice=请输入选项 (1/2/3/4):

if "%choice%"=="1" goto PULL
if "%choice%"=="2" goto PUSH
if "%choice%"=="3" goto STATUS
if "%choice%"=="4" exit
echo 无效选项，请重试
echo.
goto MENU

:PULL
echo.
echo [1/2] 拉取主仓库...
cd /d "d:\AI项目"
git pull origin main
echo.
echo [2/2] 更新子模块...
git submodule update --init --recursive
echo.
echo ✅ 拉取完成！
pause
exit

:PUSH
echo.
echo [1/3] 检查子模块变更...
cd /d "d:\AI项目\pm-team"
git status --short
for /f %%i in ('git status --porcelain') do (
    echo 发现子模块变更，正在提交...
    git add -A
    git commit -m "sync: auto commit from sync tool %date% %time%"
    git push origin master
    goto PUSH_MAIN
)
echo 子模块无变更，跳过

:PUSH_MAIN
echo.
echo [2/3] 检查主仓库变更...
cd /d "d:\AI项目"
git status --short
for /f %%i in ('git status --porcelain') do (
    echo 发现主仓库变更，正在提交...
    git add -A
    git commit -m "sync: auto commit from sync tool %date% %time%"
    git push origin main
    goto DONE
)
echo 主仓库无变更，无需推送
goto DONE

:DONE
echo.
echo ✅ 推送完成！
pause
exit

:STATUS
echo.
echo === 主仓库状态 ===
cd /d "d:\AI项目"
git status -sb
echo.
echo === 最近提交 ===
git log --oneline -5
echo.
echo === pm-team 子模块状态 ===
cd pm-team
git status -sb
echo.
echo === 子模块最近提交 ===
git log --oneline -3
echo.
pause
exit
