@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

echo ============================================================
echo   MC Skill V1.0.1 功能测试
echo ============================================================
echo.

if "%1"=="" (
    echo 用法:
    echo   run_test.bat              - 运行默认测试 (数据完整性)
    echo   run_test.bat --list       - 列出所有测试
    echo   run_test.bat --run-all    - 运行所有测试
    echo   run_test.bat --test N     - 运行指定测试 (1-6)
    echo   run_test.bat --skip-online - 跳过在线测试
    echo.
    echo 可用测试:
    echo   #1 批量搜索模式
    echo   #2 分类搜索 - 预定义分类
    echo   #3 同类模组推荐
    echo   #4 兼容规则库数据完整性 (离线)
    echo   #5 动态分类获取
    echo   #6 自动更新兼容规则库
    goto :eof
)

python "%~dp0tests\test_mod_searcher_v101.py" %*

echo.
pause
