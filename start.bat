@echo off
chcp 65001 >nul 2>&1
title MC全生态智能适配工程师 V1

REM === MC全生态智能适配工程师 V1 启动脚本 ===
REM 双击运行此脚本即可启动工具

setlocal enabledelayedexpansion

REM === 切换到脚本所在目录 ===
cd /d "%~dp0"

echo.
echo ============================================
echo   MC全生态智能适配工程师 V1
echo ============================================
echo.

REM === 检查 Python 是否安装 ===
python --version >nul 2>&1
if errorlevel 1 (
    echo [错误] 未检测到 Python 环境
    echo.
    echo 请安装 Python 3.11 或更高版本:
    echo   下载地址: https://www.python.org/downloads/
    echo.
    echo 安装时请勾选 "Add Python to PATH" 选项
    echo.
    pause
    exit /b 1
)

REM === 显示 Python 版本 ===
echo [信息] 检测到 Python:
python --version
echo.

REM === 检查依赖是否已安装 ===
python -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo [警告] 缺少依赖库，正在尝试安装...
    echo.
    python -m pip install -r requirements.txt
    if errorlevel 1 (
        echo.
        echo [错误] 依赖安装失败，请手动执行:
        echo   pip install -r requirements.txt
        echo.
        pause
        exit /b 1
    )
    echo.
    echo [信息] 依赖安装完成
    echo.
)

REM === 显示功能菜单 ===
:menu
echo ============================================
echo  请选择功能:
echo ============================================
echo.
echo   [1] F1 JAR结构解析
echo   [2] F2 模组检索下载
echo   [3] F3 环境引导搭建
echo   [4] F4 Mixin冲突扫描
echo   [5] F5 资源级重打包
echo   [6] F6 存档同步
echo   [7] F7 基础汉化
echo   [8] F8 报错修复
echo   [h] 显示完整帮助
echo   [q] 退出
echo.
set /p choice=请输入选项 (1-8/h/q):

if "%choice%"=="1" goto feature_1
if "%choice%"=="2" goto feature_2
if "%choice%"=="3" goto feature_3
if "%choice%"=="4" goto feature_4
if "%choice%"=="5" goto feature_5
if "%choice%"=="6" goto feature_6
if "%choice%"=="7" goto feature_7
if "%choice%"=="8" goto feature_8
if /i "%choice%"=="h" goto show_help
if /i "%choice%"=="q" goto end
echo.
echo [错误] 无效的选项: %choice%
echo.
goto menu

:feature_1
echo.
echo --- F1 JAR结构解析 ---
echo.
set /p jar_path=请输入JAR文件路径:
python main.py --feature jar_parser --jar-path "%jar_path%"
echo.
pause
goto menu

:feature_2
echo.
echo --- F2 模组检索下载 ---
echo.
set /p query=请输入模组名称或关键词:
set /p mc_ver=请输入MC版本 (如 1.21.1):
set /p loader=请输入加载器 (forge/neoforge/fabric/quilt):
python main.py --feature mod_searcher --query "%query%" --mc-version "%mc_ver%" --loader "%loader%"
echo.
pause
goto menu

:feature_3
echo.
echo --- F3 环境引导搭建 ---
echo.
set /p launcher=请输入启动器类型 (pcl2/hmcl/xmcl/prism/bakaxl/fcl/pojav/ling_zalith/netease):
set /p mc_ver=请输入MC版本:
set /p loader=请输入加载器:
python main.py --feature env_builder --launcher "%launcher%" --mc-version "%mc_ver%" --loader "%loader%"
echo.
pause
goto menu

:feature_4
echo.
echo --- F4 Mixin冲突扫描 ---
echo.
set /p mods_dir=请输入mods文件夹路径:
python main.py --feature mixin_scanner --mods-dir "%mods_dir%"
echo.
pause
goto menu

:feature_5
echo.
echo --- F5 资源级重打包 ---
echo.
set /p jar_path=请输入原始JAR文件路径:
set /p res_dir=请输入修改后的资源目录:
python main.py --feature repacker --jar-path "%jar_path%" --resources-dir "%res_dir%"
echo.
pause
goto menu

:feature_6
echo.
echo --- F6 存档同步 ---
echo.
set /p launcher=请输入启动器类型:
set /p mc_ver=请输入MC版本:
set /p action=请输入操作类型 (setup/backup/restore):
python main.py --feature save_sync --launcher "%launcher%" --mc-version "%mc_ver%" --action "%action%"
echo.
pause
goto menu

:feature_7
echo.
echo --- F7 基础汉化 ---
echo.
set /p jar_path=请输入JAR文件路径:
python main.py --feature translator --jar-path "%jar_path%"
echo.
pause
goto menu

:feature_8
echo.
echo --- F8 报错修复 ---
echo.
set /p crash_log=请输入crash report或latest.log文件路径:
python main.py --feature crash_analyzer --crash-log "%crash_log%"
echo.
pause
goto menu

:show_help
echo.
python main.py --help
echo.
pause
goto menu

:end
echo.
echo 感谢使用 MC全生态智能适配工程师 V1
echo.
exit /b 0
