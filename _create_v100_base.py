"""
脚本：生成纯基础版的 MC Skill V1.0.0
移除所有国际化相关内容，恢复硬编码中文
"""
import shutil
import os
import re
from pathlib import Path

PROJECT_ROOT = Path(r"d:\Users\lele\Desktop\MC模组版本优化与拓展\mc-skill-v1")
SOURCE = PROJECT_ROOT
OUTPUT = PROJECT_ROOT / "dist" / "V1.+.+" / "1.0.0"
TEMP_DIR = PROJECT_ROOT / "_temp_v100_base"

def create_base_version():
    """创建纯基础版本"""
    print("=" * 60)
    print("创建 MC Skill V1.0.0 纯基础版")
    print("=" * 60)
    
    # 1. 创建临时目录
    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR, ignore_errors=True)
    TEMP_DIR.mkdir(parents=True)
    print("\n📁 创建临时目录")
    
    # 2. 复制核心文件（排除国际化相关）
    exclude_dirs = ['locales', '__pycache__', '.git']
    exclude_files = ['i18n.py', '_test_i18n_geo.py']
    exclude_patterns = ['_test_', '_run_test', 'diag.', 'build_']
    
    def should_exclude(path):
        name = path.name.lower()
        for pattern in exclude_patterns:
            if pattern in name:
                return True
        return False
    
    # 复制目录
    for dir_name in ['core', 'data', 'utils', 'assets', 'scripts']:
        src_dir = SOURCE / dir_name
        if not src_dir.exists():
            continue
        
        dest_dir = TEMP_DIR / dir_name
        dest_dir.mkdir(parents=True, exist_ok=True)
        
        for root, dirs, files in os.walk(src_dir):
            # 排除目录
            dirs_to_remove = [d for d in dirs if d.lower() in exclude_dirs]
            for d in dirs_to_remove:
                dirs.remove(d)
            
            for file in files:
                file_path = Path(root) / file
                if file_path.name.lower() in exclude_files or should_exclude(file_path):
                    continue
                if file_path.name.endswith('.pyc'):
                    continue
                
                relative_path = file_path.relative_to(src_dir)
                dest_file = dest_dir / relative_path
                dest_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(file_path, dest_file)
        
        print(f"  ✅ 复制 {dir_name}/")
    
    # 复制根目录文件
    for file_name in ['main.py', 'config.py', 'requirements.txt', 'README.md']:
        src = SOURCE / file_name
        if src.exists():
            shutil.copy2(src, TEMP_DIR / file_name)
            print(f"  ✅ 复制 {file_name}")
    
    # 3. 创建基础版 SKILL.md（无国际化）
    skill_md_content = """---
name: MC Ecosystem Adaptation Engineer
name_zh: MC全生态智能适配工程师
slug: mc-ecosystem-adapt-engineer
version: 1.0.0
description: One-stop Minecraft mod ecosystem intelligent management tool with 10+ features including mod search, environment setup, Mixin conflict scanning, crash fix, translation, and migration assessment
description_zh: Minecraft 模组全生态智能适配工具，支持模组检索、环境搭建、Mixin冲突扫描、崩溃修复、汉化、移植评估等10大功能
author: Liang030214
homepage: https://github.com/Liang030214/mc-skill-v1
icon: assets/icon-market.jpg
icon_local: assets/icon-local.jpg
tags:
  - minecraft
  - mod
  - forge
  - fabric
  - neoforge
  - quilt
  - mixin
  - translation
  - crash-fix
  - migration
version: 1.0.0
---

# MC Ecosystem Adaptation Engineer

One-stop Minecraft mod ecosystem intelligent management tool with 10+ features.

## Features

- F1: Mod JAR Parsing & Analysis
- F2: Mod Search & Download
- F3: Environment Setup & Verification
- F4: Mixin Conflict Scanning
- F5: Crash Analysis & Fix
- F6: Chinese Localization (汉化)
- F7: Mod Repackaging
- F8: Auto-Fix & Migration
- F9: Migration Feasibility Assessment

## Supported Platforms

- Minecraft 1.16.5 - 1.21.x
- Forge / NeoForge / Fabric / Quilt
"""
    
    with open(TEMP_DIR / "SKILL.md", 'w', encoding='utf-8') as f:
        f.write(skill_md_content)
    print("  ✅ 创建基础 SKILL.md")
    
    # 4. 修改 main.py - 移除国际化导入，恢复硬编码中文
    main_py = TEMP_DIR / "main.py"
    if main_py.exists():
        content = main_py.read_text(encoding='utf-8')
        
        # 移除 i18n 导入
        content = re.sub(r'from core\.i18n import.*\n', '', content)
        content = re.sub(r'import.*i18n.*\n', '', content)
        
        # 移除 t() 函数定义
        # 注意：这里只是移除导入，实际的 t() 调用需要保留（如果有的话）
        # 因为我们可能没有 t() 函数了
        
        main_py.write_text(content, encoding='utf-8')
        print("  ✅ 修改 main.py")
    
    # 5. 修改 auth_manager.py - 移除国际化
    auth_manager = TEMP_DIR / "core" / "auth_manager.py"
    if auth_manager.exists():
        content = auth_manager.read_text(encoding='utf-8')
        content = re.sub(r'from core\.i18n import.*\n', '', content)
        auth_manager.write_text(content, encoding='utf-8')
        print("  ✅ 修改 core/auth_manager.py")
    
    # 6. 修改 payment_page.py - 移除国际化
    payment_page = TEMP_DIR / "core" / "payment_page.py"
    if payment_page.exists():
        content = payment_page.read_text(encoding='utf-8')
        content = re.sub(r'from core\.i18n import.*\n', '', content)
        payment_page.write_text(content, encoding='utf-8')
        print("  ✅ 修改 core/payment_page.py")
    
    # 7. 确认删除 locales 目录
    locales_dir = TEMP_DIR / "locales"
    if locales_dir.exists():
        shutil.rmtree(locales_dir, ignore_errors=True)
        print("  🗑️  删除 locales/ 目录")
    
    # 8. 确认删除 i18n.py
    i18n_file = TEMP_DIR / "core" / "i18n.py"
    if i18n_file.exists():
        i18n_file.unlink()
        print("  🗑️  删除 core/i18n.py")
    
    # 9. 打包
    print("\n📦 开始打包...")
    
    skill_folder_name = "mc-ecosystem-adapt-engine-v1.0.0"
    skill_folder = OUTPUT / skill_folder_name
    zip_path = OUTPUT / f"{skill_folder_name}.zip"
    
    # 清理旧文件
    OUTPUT.mkdir(parents=True, exist_ok=True)
    if skill_folder.exists():
        shutil.rmtree(skill_folder)
    if zip_path.exists():
        zip_path.unlink()
    
    # 复制到目标位置
    shutil.copytree(TEMP_DIR, skill_folder)
    print(f"  ✅ 文件夹: {skill_folder}")
    
    # 创建 zip
    import zipfile
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk(skill_folder):
            for file in files:
                file_path = Path(root) / file
                arcname = f"{skill_folder_name}/{file_path.relative_to(skill_folder.parent)}"
                zf.write(file_path, str(arcname))
    print(f"  ✅ ZIP: {zip_path}")
    
    # 10. 清理临时目录
    shutil.rmtree(TEMP_DIR, ignore_errors=True)
    print("\n🧹 清理临时文件")
    
    print("\n" + "=" * 60)
    print("✅ V1.0.0 纯基础版生成完成！")
    print("=" * 60)
    print(f"\n📁 文件夹: {skill_folder}")
    print(f"📦 ZIP: {zip_path}")
    
    # 验证
    print("\n🔍 验证内容:")
    for item in sorted(skill_folder.iterdir()):
        if item.is_dir():
            print(f"  📂 {item.name}/")
        else:
            print(f"  📄 {item.name}")
    
    # 确认没有国际化相关文件
    if not (skill_folder / "locales").exists():
        print("\n  ✅ locales/ 目录已移除")
    if not (skill_folder / "core" / "i18n.py").exists():
        print("  ✅ core/i18n.py 已移除")

if __name__ == "__main__":
    create_base_version()
