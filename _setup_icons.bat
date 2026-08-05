@echo off
chcp 65001 >nul

echo 正在整理 Skill 图标文件...

:: 创建 assets 目录
mkdir "%~dp0assets" 2>nul

:: 复制图2作为市场展示图标
copy "%~dp0data\payment\skill_icon_v2.jpg" "%~dp0assets\icon-market.jpg" >nul
echo ✅ 市场展示图标: assets\icon-market.jpg

:: 复制图1作为本地显示图标
copy "%~dp0data\payment\skill_icon.jpg" "%~dp0assets\icon-local.jpg" >nul
echo ✅ 本地显示图标: assets\icon-local.jpg

echo.
echo 图标整理完成！
pause
