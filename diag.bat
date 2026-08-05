@echo off
chcp 65001 >nul 2>&1
echo ========================================
echo  MC-Skill-V1 环境诊断
echo ========================================
echo.

echo [1] 检查 Python 是否可用...
python --version 2>&1
if errorlevel 1 (
    echo     [失败] python 命令不可用
    echo     尝试 py 启动器...
    py --version 2>&1
    if errorlevel 1 (
        echo     [失败] py 启动器也不可用
        echo     请安装 Python 3.11+ 并勾选 "Add to PATH"
        echo     下载: https://www.python.org/downloads/
        pause
        exit /b 1
    )
    set PYTHON_CMD=py
) else (
    set PYTHON_CMD=python
)
echo     [成功] Python 可用

echo.
echo [2] 检查 Python 版本...
%PYTHON_CMD% -c "import sys; print(f'    Python {sys.version}'); print(f'    路径: {sys.executable}')" 2>&1

echo.
echo [3] 检查必要目录...
if exist "data\java_version_map.json" (
    echo     [成功] data\java_version_map.json 存在
) else (
    echo     [失败] data\java_version_map.json 不存在
)
if exist "utils\__init__.py" (
    echo     [成功] utils\__init__.py 存在
) else (
    echo     [失败] utils\__init__.py 不存在
)

echo.
echo [4] 测试 config 模块导入...
%PYTHON_CMD% -c "import sys; sys.path.insert(0,'.'); import config; print('    [成功] config 导入成功'); print('    版本映射示例:', config.get_java_version('1.21.1'))" 2>&1
if errorlevel 1 echo     [失败] config 模块导入失败

echo.
echo [5] 测试 logger 模块导入...
%PYTHON_CMD% -c "import sys; sys.path.insert(0,'.'); from utils.logger import get_logger; print('    [成功] logger 导入成功')" 2>&1
if errorlevel 1 echo     [失败] logger 模块导入失败

echo.
echo [6] 测试 jar_utils 模块导入...
%PYTHON_CMD% -c "import sys; sys.path.insert(0,'.'); from utils.jar_utils import get_file_type; print('    [成功] jar_utils 导入成功'); print('    文件类型测试:', get_file_type('META-INF/mods.toml'))" 2>&1
if errorlevel 1 echo     [失败] jar_utils 模块导入失败

echo.
echo [7] 测试 api_client 模块导入...
%PYTHON_CMD% -c "import sys; sys.path.insert(0,'.'); from utils.api_client import ModrinthClient; print('    [成功] api_client 导入成功')" 2>&1
if errorlevel 1 echo     [失败] api_client 模块导入失败

echo.
echo [8] 测试 report_gen 模块导入...
%PYTHON_CMD% -c "import sys; sys.path.insert(0,'.'); from utils.report_gen import ReportGenerator; print('    [成功] report_gen 导入成功')" 2>&1
if errorlevel 1 echo     [失败] report_gen 模块导入失败

echo.
echo [9] 测试 main 模块导入...
%PYTHON_CMD% -c "import sys; sys.path.insert(0,'.'); import main; print('    [成功] main 导入成功'); print('    功能数量:', len(main.FEATURES))" 2>&1
if errorlevel 1 echo     [失败] main 模块导入失败

echo.
echo [10] 完整运行验证脚本...
echo.
%PYTHON_CMD% verify_p1.py 2>&1

echo.
echo ========================================
echo  诊断完成
echo ========================================
pause
