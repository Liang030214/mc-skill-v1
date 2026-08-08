@echo off
chcp 65001 >nul

set SRC=%~dp0
set DST=%SRC%Dist\V1.+.+\1.0.1\mc-ecosystem-adapt-engine-v1.0.1

echo ========================================
echo   MC Skill V1.0.2 发布包组装
echo ========================================
echo.

if not exist "%DST%" mkdir "%DST%"

echo [1/6] Copying core/ ...
xcopy "%SRC%core" "%DST%\core\" /E /I /Y /Q >nul
echo      Done

echo [2/6] Copying utils/ ...
xcopy "%SRC%utils" "%DST%\utils\" /E /I /Y /Q >nul
echo      Done

echo [3/6] Copying data/ ...
xcopy "%SRC%data" "%DST%\data\" /E /I /Y /Q >nul
echo      Done

echo [4/6] Copying locales/ ...
if exist "%SRC%locales" (
    xcopy "%SRC%locales" "%DST%\locales\" /E /I /Y /Q >nul
    echo      Done
) else (
    echo      Skip (not found)
)

echo [5/6] Copying assets/ ...
if exist "%SRC%assets" (
    xcopy "%SRC%assets" "%DST%\assets\" /E /I /Y /Q >nul
    echo      Done
) else (
    echo      Skip (not found)
)

echo [6/6] Copying root files ...
copy "%SRC%main.py" "%DST%\" /Y >nul
copy "%SRC%config.py" "%DST%\" /Y >nul
copy "%SRC%requirements.txt" "%DST%\" /Y >nul
echo      Done

echo.
echo ========================================
echo   DONE! Package ready at:
echo   %DST%
echo ========================================
echo.
pause
