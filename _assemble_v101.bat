@echo off
chcp 65001 >nul
echo ========================================
echo   MC Skill V1.0.2 发布包组装脚本
echo ========================================
echo.

set "SOURCE=d:\Users\lele\Desktop\MC模组版本优化与拓展\mc-skill-v1"
set "DEST=d:\Users\lele\Desktop\MC模组版本优化与拓展\mc-skill-v1\Dist\V1.+.+\1.0.1\mc-ecosystem-adapt-engine-v1.0.1"

echo [1/6] 复制核心模块 (core/)
xcopy "%SOURCE%\core" "%DEST%\core\" /E /I /Y /Q
echo   完成

echo [2/6] 复制工具模块 (utils/)
xcopy "%SOURCE%\utils" "%DEST%\utils\" /E /I /Y /Q
echo   完成

echo [3/6] 复制数据文件 (data/)
xcopy "%SOURCE%\data" "%DEST%\data\" /E /I /Y /Q
echo   完成

echo [4/6] 复制本地化文件 (locales/)
if exist "%SOURCE%\locales" (
    xcopy "%SOURCE%\locales" "%DEST%\locales\" /E /I /Y /Q
    echo   完成
) else (
    echo   跳过 (目录不存在)
)

echo [5/6] 复制资源文件 (assets/)
if exist "%SOURCE%\assets" (
    xcopy "%SOURCE%\assets" "%DEST%\assets\" /E /I /Y /Q
    echo   完成
) else (
    echo   跳过 (目录不存在)
)

echo [6/6] 复制脚本文件 (scripts/)
if exist "%SOURCE%\scripts" (
    xcopy "%SOURCE%\scripts" "%DEST%\scripts\" /E /I /Y /Q
    echo   完成
) else (
    echo   跳过 (目录不存在)
)

echo.
echo [额外] 复制根目录文件
copy "%SOURCE%\main.py" "%DEST%\" /Y >nul
copy "%SOURCE%\config.py" "%DEST%\" /Y >nul
copy "%SOURCE%\requirements.txt" "%DEST%\" /Y >nul
if exist "%SOURCE%\README.md" copy "%SOURCE%\README.md" "%DEST%\" /Y >nul
echo   完成

echo.
echo ========================================
echo   ✅ 发布包组装完成！
echo ========================================
echo.
echo   位置: %DEST%
echo.
echo   下一步:
echo   1. 检查文件是否完整
echo   2. 压缩为 zip 或直接上传文件夹
echo   3. 上传至 Skill 市场
echo.
pause
