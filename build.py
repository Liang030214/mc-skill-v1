# -*- coding: utf-8 -*-
"""打包脚本 - 将项目打包为可分发的 zip 文件或 exe"""

import sys
import os
import zipfile
import shutil
import subprocess
from pathlib import Path
from datetime import datetime

PROJECT_ROOT = Path(__file__).resolve().parent
OUTPUT_DIR = PROJECT_ROOT / "dist"

# 需要打包的文件/目录
INCLUDE_DIRS = ["core", "data", "utils"]
INCLUDE_FILES = ["main.py", "config.py", "requirements.txt", "README.md"]

# 排除的文件模式
EXCLUDE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    ".git",
    ".idea",
    ".vscode",
    "output",
    "dist",
    "temp",
    "verify_*.py",
    "_expand_db.py",
    "*.log",
    "*.tmp",
]


def should_exclude(file_path: Path) -> bool:
    """检查文件是否应该被排除"""
    file_name = file_path.name
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*"):
            # 通配符匹配扩展名
            ext = pattern[1:]  # 去掉 *
            if file_name.endswith(ext):
                return True
        elif file_name == pattern:
            return True
        elif pattern in str(file_path).replace("\\", "/"):
            return True
    return False


def create_zip():
    """创建 zip 分发包"""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"mc-skill-v1-{timestamp}.zip"
    zip_path = OUTPUT_DIR / zip_filename

    print(f"📦 开始打包: {zip_filename}", flush=True)

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        # 添加根目录文件
        for file_name in INCLUDE_FILES:
            file_path = PROJECT_ROOT / file_name
            if file_path.exists():
                arcname = f"mc-skill-v1/{file_name}"
                zf.write(file_path, arcname)
                print(f"  ✅ {file_name}", flush=True)
            else:
                print(f"  ⚠️  {file_name} 不存在，跳过", flush=True)

        # 添加目录
        for dir_name in INCLUDE_DIRS:
            dir_path = PROJECT_ROOT / dir_name
            if not dir_path.exists():
                print(f"  ⚠️  目录 {dir_name} 不存在，跳过", flush=True)
                continue

            for root, dirs, files in os.walk(dir_path):
                # 排除目录
                dirs_to_remove = []
                for d in dirs:
                    if should_exclude(Path(root) / d):
                        dirs_to_remove.append(d)
                for d in dirs_to_remove:
                    dirs.remove(d)

                # 添加文件
                for file in files:
                    file_path = Path(root) / file
                    if should_exclude(file_path):
                        continue
                    arcname = f"mc-skill-v1/{file_path.relative_to(PROJECT_ROOT)}"
                    zf.write(file_path, str(arcname))

    print(f"\n✅ 打包完成: {zip_path}", flush=True)
    print(f"📊 文件大小: {zip_path.stat().st_size / 1024:.1f} KB", flush=True)

    # 生成 Windows 一键运行脚本
    _create_run_scripts(OUTPUT_DIR)

    return zip_path


def _create_run_scripts(output_dir: Path):
    """创建 Windows 一键运行脚本"""
    run_bat = output_dir / "mc-skill-start.bat"

    content = r"""@echo off
chcp 65001 >nul
title MC 全生态智能适配工程师 V1

echo ========================================
echo   MC 全生态智能适配工程师 V1
echo   MC Ecosystem Adaptation Engineer
echo ========================================
echo.

REM 检查 Python 环境
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [错误] 未检测到 Python，请先安装 Python 3.10+
    echo 下载地址: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM 检查并安装依赖
if not exist "mc-skill-v1\requirements_installed" (
    echo [信息] 首次运行，正在安装依赖...
    pip install -r "mc-skill-v1\requirements.txt"
    if %errorlevel% neq 0 (
        echo [错误] 依赖安装失败
        pause
        exit /b 1
    )
    echo ok > "mc-skill-v1\requirements_installed"
)

REM 进入项目目录
cd /d "%~dp0mc-skill-v1"

:menu
cls
echo.
echo  功能菜单:
echo  ────────────────────────────────────────
echo  1. F1  JAR结构解析
echo  2. F2  模组检索下载
echo  3. F3  环境引导搭建
echo  4. F4  Mixin 冲突扫描
echo  5. F5  资源重打包
echo  6. F6  存档同步
echo  7. F7  基础汉化
echo  8. F8  报错修复
echo  9. F8.1 自动修复（一键升级模组）
echo  10. F9 模组移植可行性评估
echo  11. 查看授权状态
echo  0. 退出
echo  ────────────────────────────────────────
echo.

set /p choice=请选择功能 (0-11): 

if "%choice%"=="1" goto jar_parse
if "%choice%"=="2" goto mod_search
if "%choice%"=="3" goto env_build
if "%choice%"=="4" goto mixin_scan
if "%choice%"=="5" goto repack
if "%choice%"=="6" goto save_sync
if "%choice%"=="7" goto translate
if "%choice%"=="8" goto crash_analyze
if "%choice%"=="9" goto auto_fix
if "%choice%"=="10" goto migration
if "%choice%"=="11" goto auth_status
if "%choice%"=="0" goto end
goto menu

:jar_parse
echo.
echo [F1] JAR结构解析
set /p jar_path=JAR文件路径: 
python main.py --feature jar_parser --jar-path "%jar_path%"
pause
goto menu

:mod_search
echo.
echo [F2] 模组检索下载
set /p query=搜索关键词 (如 Create): 
set /p mc_ver=Minecraft 版本 (如 1.21.1): 
set /p loader=加载器 (neoforge/forge/fabric): 
python main.py --feature mod_searcher --query "%query%" --mc-version "%mc_ver%" --loader "%loader%"
pause
goto menu

:env_build
echo.
echo [F3] 环境引导搭建
set /p mc_ver=Minecraft 版本 (如 1.21.1): 
set /p loader=加载器 (neoforge/forge/fabric): 
python main.py --feature env_builder --mc-version "%mc_ver%" --loader "%loader%"
pause
goto menu

:mixin_scan
echo.
echo [F4] Mixin 冲突扫描
set /p mods_dir=mods 目录路径: 
python main.py --feature mixin_scanner --mods-dir "%mods_dir%"
pause
goto menu

:repack
echo.
echo [F5] 资源重打包
set /p jar_path=JAR文件路径: 
python main.py --feature repacker --jar-path "%jar_path%"
pause
goto menu

:save_sync
echo.
echo [F6] 存档同步
set /p action=操作 (sync/backup/restore): 
set /p save_dir=存档目录: 
python main.py --feature save_sync --action %action% --save-dir "%save_dir%"
pause
goto menu

:translate
echo.
echo [F7] 基础汉化
set /p mods_dir=mods 目录路径: 
python main.py --feature translator --mods-dir "%mods_dir%"
pause
goto menu

:crash_analyze
echo.
echo [F8] 报错修复
set /p crash_log=崩溃日志文件路径: 
set /p offline=离线模式? (y/n): 
if "%offline%"=="y" (
    python main.py --feature crash_analyzer --crash-log "%crash_log%" --offline
) else (
    python main.py --feature crash_analyzer --crash-log "%crash_log%"
)
pause
goto menu

:auto_fix
echo.
echo [F8.1] 自动修复（一键升级模组）
echo 警告: 此功能会自动下载并替换模组文件！
echo.
set /p crash_log=崩溃日志文件路径: 
set /p mods_dir=Minecraft mods 目录路径: 
python main.py --feature auto_fix --crash-log "%crash_log%" --fix-mods-dir "%mods_dir%"
pause
goto menu

:migration
echo.
echo [F9] 模组移植可行性评估
set /p jar_path=模组JAR文件路径: 
set /p from_mc=源MC版本 (如 1.20.1): 
set /p to_mc=目标MC版本 (如 1.21.1): 
set /p from_loader=源加载器 (forge/neoforge/fabric/quilt): 
set /p to_loader=目标加载器 (forge/neoforge/fabric/quilt): 
python main.py --feature migration_assess --jar-path "%jar_path%" --from-mc-version "%from_mc%" --to-mc-version "%to_mc%" --from-loader "%from_loader%" --to-loader "%to_loader%"
pause
goto menu

:auth_status
echo.
python main.py --auth-status
pause
goto menu

:end
echo.
echo 再见！
exit /b 0
"""

    with open(run_bat, "w", encoding="utf-8") as f:
        f.write(content)

    print(f"🖥️  已创建启动脚本: {run_bat.name}", flush=True)


def create_standalone_package():
    """创建独立运行包（含 Python 嵌入版）"""
    print("\n📦 创建独立运行包...", flush=True)

    # 检查是否有 Python 嵌入版
    python_embed_path = PROJECT_ROOT / "python_embed"
    if not python_embed_path.exists():
        print("  ⚠️  未找到 Python 嵌入版，跳过独立包创建", flush=True)
        print("  💡 如需独立运行包，请下载 Python embed 版本:")
        print("     https://www.python.org/downloads/windows/", flush=True)
        print("     选择 'Windows embeddable package (ZIP)'")
        return None

    standalone_dir = OUTPUT_DIR / f"mc-skill-v1-standalone-{datetime.now().strftime('%Y%m%d')}"
    standalone_dir.mkdir(parents=True, exist_ok=True)

    # 复制 Python 嵌入版
    shutil.copytree(python_embed_path, standalone_dir / "python", dirs_exist_ok=True)

    # 复制项目文件
    shutil.copytree(PROJECT_ROOT, standalone_dir / "mc-skill-v1", dirs_exist_ok=True,
                    ignore=shutil.ignore_patterns(
                        "__pycache__", "*.pyc", "output", "dist", ".git",
                        "verify_*.py", "_expand_db.py"
                    ))

    # 创建启动脚本
    bat_content = r"""@echo off
chcp 65001 >nul
title MC 全生态智能适配工程师 V1 (独立版)

set PYTHON_HOME=%~dp0python
set PATH=%PYTHON_HOME%;%PATH%

cd /d "%~dp0mc-skill-v1"
python main.py %*
"""

    with open(standalone_dir / "start.bat", "w", encoding="utf-8") as f:
        f.write(bat_content)

    print(f"  ✅ 独立运行包: {standalone_dir}", flush=True)
    return standalone_dir


def build_exe():
    """使用 PyInstaller 打包成单文件 exe"""
    print("\n📦 PyInstaller 打包 exe...", flush=True)

    # 检查 PyInstaller 是否已安装
    try:
        import PyInstaller
        print(f"  ✅ PyInstaller {PyInstaller.__version__} 已安装", flush=True)
    except ImportError:
        print("  ⚠️  PyInstaller 未安装，正在安装...", flush=True)
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", "pyinstaller"
        ])
        print("  ✅ PyInstaller 安装完成", flush=True)

    # 创建入口脚本
    entry_script = PROJECT_ROOT / "_exe_entry.py"
    entry_content = '''# -*- coding: utf-8 -*-
import sys
import os

# 确保项目根目录在路径中
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from main import main

if __name__ == "__main__":
    main()
'''
    entry_script.write_text(entry_content, encoding="utf-8")

    # PyInstaller 命令
    exe_name = f"MC-Skill-V1-{datetime.now().strftime('%Y%m%d')}"
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",           # 单文件模式
        "--console",           # 控制台模式
        "--name", exe_name,
        "--distpath", str(OUTPUT_DIR),
        "--workpath", str(PROJECT_ROOT / "build_temp"),
        "--specpath", str(PROJECT_ROOT),
        "--add-data", f"data{os.pathsep}data",  # 包含 data 目录
        str(entry_script)
    ]

    print(f"  📋 执行: {' '.join(cmd)}", flush=True)
    print("  ⏳ 正在打包，请稍候...", flush=True)

    try:
        result = subprocess.run(
            cmd,
            cwd=str(PROJECT_ROOT),
            capture_output=False
        )
        if result.returncode == 0:
            exe_path = OUTPUT_DIR / f"{exe_name}.exe"
            if exe_path.exists():
                size_mb = exe_path.stat().st_size / (1024 * 1024)
                print(f"\n  ✅ exe 打包成功: {exe_path}", flush=True)
                print(f"  📊 文件大小: {size_mb:.1f} MB", flush=True)
                return exe_path
        else:
            print("  ❌ PyInstaller 打包失败", flush=True)
            print("  💡 将回退到 zip 打包模式", flush=True)
            return None
    except Exception as e:
        print(f"  ❌ 打包异常: {e}", flush=True)
        return None
    finally:
        # 清理入口脚本
        if entry_script.exists():
            entry_script.unlink()
        # 清理临时文件
        for temp_dir in ["build_temp", "__pycache__"]:
            temp_path = PROJECT_ROOT / temp_dir
            if temp_path.exists():
                shutil.rmtree(temp_path, ignore_errors=True)
        # 删除 .spec 文件
        spec_file = PROJECT_ROOT / f"{exe_name}.spec"
        if spec_file.exists():
            spec_file.unlink()


def main():
    print("=" * 50, flush=True)
    print("MC Skill V1 打包工具", flush=True)
    print("=" * 50, flush=True)

    # 检查命令行参数
    build_exe_flag = "--exe" in sys.argv

    if build_exe_flag:
        # PyInstaller 打包（生成 exe）
        exe_path = build_exe()
        if exe_path:
            print("\n🎉 发布给用户的文件:", flush=True)
            print(f"   {exe_path.name} ({exe_path.stat().st_size / (1024*1024):.1f} MB)", flush=True)
            print("\n📖 用户使用方式:", flush=True)
            print("   1. 下载 exe 文件", flush=True)
            print("   2. 双击运行（无需安装 Python）", flush=True)
            print("   3. 功能菜单会自动显示", flush=True)
            return 0
        else:
            print("\n⚠️  exe 打包失败，回退到 zip 模式", flush=True)

    # 创建标准 zip 包
    zip_path = create_zip()

    # 计算文件统计
    print("\n📊 打包统计:", flush=True)

    # 统计源代码行数
    total_lines = 0
    total_files = 0
    for py_file in PROJECT_ROOT.rglob("*.py"):
        if should_exclude(py_file):
            continue
        try:
            lines = len(py_file.read_text(encoding="utf-8").splitlines())
            total_lines += lines
            total_files += 1
        except Exception:
            pass

    print(f"  源代码文件: {total_files} 个", flush=True)
    print(f"  代码行数: {total_lines:,} 行", flush=True)

    # 统计核心模块
    core_modules = list((PROJECT_ROOT / "core").glob("*.py"))
    print(f"  核心功能模块: {len(core_modules)} 个", flush=True)
    for mod in core_modules:
        print(f"    - {mod.stem}.py", flush=True)

    # 打印使用说明
    print("\n📖 使用说明:", flush=True)
    print("  1. 解压 zip 文件", flush=True)
    print("  2. 安装依赖: pip install -r requirements.txt", flush=True)
    print("  3. 运行: python main.py --help", flush=True)
    print("\n  或使用启动脚本: mc-skill-start.bat", flush=True)

    print("\n💡 提示: 运行 'python build.py --exe' 可打包成免安装 exe", flush=True)
    print("\n✅ 打包完成!", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
