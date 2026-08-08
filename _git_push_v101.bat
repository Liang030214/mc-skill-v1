@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

REM ============================================================
REM  MC Ecosystem Adapt Engine - GitHub 自动化推送脚本
REM  版本: V1.0.1
REM  作者: Liang030214
REM  仓库: https://github.com/Liang030214/mc-skill-v1
REM ============================================================

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

echo.
echo ================================================
echo   MC Skill V1.0.1 - GitHub 自动化推送脚本
echo ================================================
echo.
echo [1/8] 检查 Git 环境...
where git >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Git，请先安装 Git: https://git-scm.com/download
    pause
    exit /b 1
)
echo       Git 已就绪

echo.
echo [2/8] 检查远程仓库配置...
git remote get-url origin >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未配置远程仓库 origin
    echo       请运行: git remote add origin https://github.com/Liang030214/mc-skill-v1.git
    pause
    exit /b 1
)
for /f "delims=" %%i in ('git remote get-url origin') do set "REMOTE_URL=%%i"
echo       远程仓库: !REMOTE_URL!

echo.
echo [3/8] 显示当前变更摘要...
echo ------------------------------------------------
echo       [已修改文件]
git diff --name-status | findstr /R "^M"
echo.
echo       [新增文件]
git ls-files --others --exclude-standard
echo.
echo       [待暂存变更统计]
for /f "tokens=1 delims= " %%a in ('git status --porcelain') do set /a COUNT+=1
echo       共 !COUNT! 个文件待处理
echo ------------------------------------------------

echo.
echo [4/8] 暂存所有变更...
git add -A
if %errorlevel% neq 0 (
    echo [错误] git add 失败
    pause
    exit /b 1
)
echo       所有文件已暂存

echo.
echo [5/8] 提交变更（V1.0.1）...
git commit -m "release: MC Skill V1.0.1 - 模组检索增强与兼容规则库扩充" -m "- 新增模组分类索引（16个分类），支持分类搜索和批量搜索" -m "- 扩大模组兼容规则库，覆盖机械动力/乐事/科技能源/红石魔改等65+模组" -m "- 新增国际化框架（11种语言支持）" -m "- 完善授权管理和付费引导页面声明" -m "- 新增 SKILL.json 元数据文件，完整声明功能与权限" -m "- 修复多处已知 bug（F2/F3/F5/F8.1）"
if %errorlevel% neq 0 (
    echo [警告] 提交可能失败，检查是否有重复提交
    git log --oneline -1
) else (
    echo       提交成功
)

echo.
echo [6/8] 创建版本标签 v1.0.1...
git tag -d v1.0.1 2>nul
git tag -a v1.0.1 -m "MC Ecosystem Adapt Engine V1.0.1" -m "模组检索范围增强、兼容规则库扩充、国际化支持、权限声明完善"
if %errorlevel% neq 0 (
    echo [警告] 标签创建失败，可能已存在，尝试继续...
) else (
    echo       标签 v1.0.1 创建成功
)

echo.
echo [7/8] 推送到 GitHub...
echo       正在推送主分支...
git push origin main
if %errorlevel% neq 0 (
    echo.
    echo [错误] 推送失败！可能原因：
    echo       1. 网络连接问题
    echo       2. GitHub 认证已过期
    echo       3. 远程仓库权限不足
    echo.
    echo       请尝试以下操作：
    echo       - 检查网络连接
    echo       - 运行: git config credential.helper manager 然后重试
    echo       - 使用 Personal Access Token 替代密码认证
    pause
    exit /b 1
)

echo.
echo       正在推送标签...
git push origin v1.0.1
if %errorlevel% neq 0 (
    echo [警告] 标签推送失败，可能标签已存在
) else (
    echo       标签 v1.0.1 已推送
)

echo.
echo [8/8] 验证推送结果...
echo ------------------------------------------------
echo       远程仓库最新提交:
git log --oneline -3
echo.
echo       标签列表:
git tag -l
echo ------------------------------------------------

echo.
echo ================================================
echo   推送完成！
echo ================================================
echo.
echo   仓库地址: https://github.com/Liang030214/mc-skill-v1
echo   标签页:   https://github.com/Liang030214/mc-skill-v1/tags
echo   Release页: https://github.com/Liang030214/mc-skill-v1/releases
echo.
echo   下一步操作：
echo   1. 打开 GitHub Release 页面
echo   2. 点击 "Draft a new release"
echo   3. 选择 v1.0.1 标签
echo   4. 填写 Release 标题和说明
echo   5. 上传发布包（如有）
echo   6. 点击 "Publish release"
echo.

REM 自动打开 GitHub Release 页面
start "" "https://github.com/Liang030214/mc-skill-v1/releases/new?tag=v1.0.1"

pause
