@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo.
echo ================================================
echo   MC Skill V1.0.1 - GitHub 发布包生成脚本
echo ================================================
echo.

set "PROJECT_DIR=%~dp0"
cd /d "%PROJECT_DIR%"

set "RELEASE_DIR=release\github_package_v101"

echo [1/5] 清理旧发布包...
if exist "%RELEASE_DIR%" rmdir /s /q "%RELEASE_DIR%"
mkdir "%RELEASE_DIR%"

echo.
echo [2/5] 复制核心文件...
echo       复制主程序...
copy main.py "%RELEASE_DIR%\" >nul
copy config.py "%RELEASE_DIR%\" >nul
copy build.py "%RELEASE_DIR%\" >nul
copy requirements.txt "%RELEASE_DIR%\" >nul
copy start.bat "%RELEASE_DIR%\" >nul

echo       复制功能模块 (core/)...
xcopy core "%RELEASE_DIR%\core\" /e /i /q >nul

echo       复制工具模块 (utils/)...
xcopy utils "%RELEASE_DIR%\utils\" /e /i /q >nul

echo       复制数据文件 (data/)...
xcopy data "%RELEASE_DIR%\data\" /e /i /q >nul

echo       复制国际化文件 (locales/)...
xcopy locales "%RELEASE_DIR%\locales\" /e /i /q >nul

echo       复制发布资源 (release/)...
xcopy release "%RELEASE_DIR%\release\" /e /i /q >nul

echo       复制脚本 (scripts/)...
xcopy scripts "%RELEASE_DIR%\scripts\" /e /i /q >nul

echo       复制文档...
copy README.md "%RELEASE_DIR%\" >nul
copy SKILL.md "%RELEASE_DIR%\" >nul
copy SKILL.json "%RELEASE_DIR%\" >nul

echo.
echo [3/5] 复制图标资源...
if not exist "%RELEASE_DIR%\assets" mkdir "%RELEASE_DIR%\assets"
if exist "assets\icon-local.jpg" copy assets\icon-local.jpg "%RELEASE_DIR%\assets\" >nul
if exist "assets\icon-market.jpg" copy assets\icon-market.jpg "%RELEASE_DIR%\assets\" >nul

echo.
echo [4/5] 生成版本信息文件...
(
echo {
echo   "version": "1.0.1",
echo   "release_date": "%date%",
echo   "loader_support": ["NeoForge", "Forge", "Fabric", "Quilt"],
echo   "mc_version_range": "1.20.1 - 1.21.1",
echo   "features": [
echo     "F1_JAR解析",
echo     "F2_模组检索下载_增强版",
echo     "F3_环境引导搭建",
echo     "F4_版本推荐",
echo     "F5_资源级重打包",
echo     "F6_依赖冲突诊断",
echo     "F7_翻译汉化",
echo     "F8_报错修复",
echo     "F9_模组移植评估",
echo     "F10_授权与使用管理",
echo     "F11_付费引导页面"
echo   ]
echo }
) > "%RELEASE_DIR%\version.json"

echo.
echo [5/5] 压缩为 ZIP 发布包...
set "ZIP_NAME=mc-skill-v1.0.1.zip"
set "ZIP_PATH=%PROJECT_DIR%release\%ZIP_NAME%"

if exist "%ZIP_PATH%" del /q "%ZIP_PATH%"

powershell -Command "Compress-Archive -Path '%RELEASE_DIR%\*' -DestinationPath '%ZIP_PATH%' -Force"

if %errorlevel% equ 0 (
    echo.
    echo ================================================
    echo   发布包生成成功！
    echo ================================================
    echo.
    echo   ZIP 文件: release\%ZIP_NAME%
    echo   大小:
    for %%A in ("%ZIP_PATH%") do echo         %%~zA 字节
    echo.
    echo   内容结构:
    echo     ├── main.py
    echo     ├── config.py
    echo     ├── build.py
    echo     ├── requirements.txt
    echo     ├── start.bat
    echo     ├── core/        (14个功能模块)
    echo     ├── utils/       (4个工具模块)
    echo     ├── data/        (静态数据文件)
    echo     ├── locales/     (11种语言文件)
    echo     ├── release/     (发布资源)
    echo     ├── scripts/     (辅助脚本)
    echo     ├── assets/      (图标资源)
    echo     ├── SKILL.md
    echo     ├── SKILL.json
    echo     ├── README.md
    echo     └── version.json
    echo.
    echo   下一步：
    echo   1. 运行 _git_push_v101.bat 推送到 GitHub
    echo   2. 在 GitHub 创建 Release 并上传此 ZIP
    echo.
    
    REM 打开文件夹
    start "" "explorer /select,%ZIP_PATH%"
) else (
    echo.
    echo [错误] 压缩失败，请检查 PowerShell 是否可用
    echo       或者手动将 %RELEASE_DIR% 文件夹压缩为 ZIP
)

pause
