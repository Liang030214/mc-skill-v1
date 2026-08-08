@echo off
chcp 65001 >nul
title MC Skill V1 - Multi-Version Package Generator

echo ================================================
echo   MC Skill V1 Multi-Version Builder
echo   Generates packages for different versions
echo ================================================
echo.

cd /d "%~dp0"

where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python not found. Please install Python 3.10+
    echo Download: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [INFO] This script will generate packages for v1.0.0 and v1.0.1
echo [INFO] ============================================================
echo.

echo [1/2] Generating package for version 1.0.0...
echo.
python build.py --skill-package --set-version 1.0.0

if %errorlevel% neq 0 (
    echo [ERROR] Failed to build version 1.0.0
    pause
    exit /b 1
)

echo.
echo [2/2] Generating package for version 1.0.1...
echo.
python build.py --skill-package --set-version 1.0.1

if %errorlevel% neq 0 (
    echo [ERROR] Failed to build version 1.0.1
    pause
    exit /b 1
)

echo.
echo ================================================
echo   SUCCESS! All versions built.
echo   Check the "dist" folder structure:
echo   dist/
echo   └── V1.+.+/          (Major Version Folder)
echo       ├── 1.0.0/       (First release)
echo       │   ├── folder for upload
echo       │   └── .zip backup
echo       └── 1.0.1/       (Updated version)
echo           ├── folder for upload
echo           └── .zip backup
echo ================================================
echo.

tree /F dist

echo.
pause