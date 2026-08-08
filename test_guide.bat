@echo off
chcp 65001 >nul
setlocal

cd /d "%~dp0"

echo ============================================================
echo   MC Skill V1.0.1 功能测试 - 详细命令
echo ============================================================
echo.
echo   请按顺序逐个执行以下命令：
echo.
echo   ==============================================
echo   第1步: 查看所有测试（了解测试内容）
echo   ==============================================
echo     python tests\test_mod_searcher_v101.py --list
echo.
echo   ==============================================
echo   第2步: 测试 #1 - 批量搜索模式
echo   ==============================================
echo     python tests\test_mod_searcher_v101.py --test 1
echo.
echo   ==============================================
echo   第3步: 测试 #2 - 分类搜索（预定义分类）
echo   ==============================================
echo     python tests\test_mod_searcher_v101.py --test 2
echo.
echo   ==============================================
echo   第4步: 测试 #3 - 同类模组推荐
echo   ==============================================
echo     python tests\test_mod_searcher_v101.py --test 3
echo.
echo   ==============================================
echo   第5步: 测试 #4 - 兼容规则库数据完整性（离线测试）
echo   ==============================================
echo     python tests\test_mod_searcher_v101.py --test 4
echo.
echo   ==============================================
echo   第6步: 测试 #5 - 动态分类获取
echo   ==============================================
echo     python tests\test_mod_searcher_v101.py --test 5
echo.
echo   ==============================================
echo   第7步: 测试 #6 - 自动更新兼容规则库
echo   ==============================================
echo     python tests\test_mod_searcher_v101.py --test 6
echo.
echo   ==============================================
echo   附加命令（可选）:
echo   ==============================================
echo   # 运行所有测试
echo     python tests\test_mod_searcher_v101.py --run-all
echo.
echo   # 运行所有测试并保存结果
echo     python tests\test_mod_searcher_v101.py --run-all --output tests\results.json
echo.
echo   # 只运行离线测试
echo     python tests\test_mod_searcher_v101.py --run-all --skip-online
echo.
echo ============================================================
echo   当前执行: %1 %2 %3 %4 %5 %6 %7
echo ============================================================
echo.

if "%1"=="" (
    echo 请复制上面的命令到终端执行
    echo.
    echo 快速开始:
    echo   1. 先查看测试列表: python tests\test_mod_searcher_v101.py --list
    echo   2. 挨个测试: python tests\test_mod_searcher_v101.py --test 1
    echo   3. 查看结果: python tests\test_mod_searcher_v101.py --run-all
    goto :eof
)

python tests\test_mod_searcher_v101.py %*

echo.
echo ============================================================
echo   测试完成
echo ============================================================
pause
