# -*- coding: utf-8 -*-
"""多平台发布包生成器 - 为每个平台生成带对应描述文件的发布包"""

import shutil
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
DIST_DIR = PROJECT_ROOT / "dist"
RELEASE_DIR = PROJECT_ROOT / "release"

# 平台配置
PLATFORMS = {
    "skillhub": {
        "name": "SkillHub V1",
        "desc_file": "skillhub_desc.md",
        "folder_name": "mc-ecosystem-adapt-engine-skillhub-v1",
        "version": "SkillHub V1",
    },
    "github": {
        "name": "GitHub V1.0.2",
        "desc_file": "github_desc.md",
        "folder_name": "mc-ecosystem-adapt-engine-github-v1.0.2",
        "version": "v1.0.2",
    },
    "clawhub": {
        "name": "ClawHub V1.0.3",
        "desc_file": "clawhub_desc.md",
        "folder_name": "mc-ecosystem-adapt-engine-clawhub-v1.0.3",
        "version": "v1.0.3",
    },
}

# 要打包的目录和文件
INCLUDE_DIRS = ["core", "data", "utils", "locales", "assets", "scripts"]
INCLUDE_FILES = ["main.py", "config.py", "requirements.txt", "SKILL.md", "SKILL.json"]

# 排除模式
EXCLUDE_PATTERNS = ["__pycache__", "*.pyc", "*.pyo"]


def should_exclude(file_path: Path) -> bool:
    """检查文件是否需要排除"""
    name = file_path.name
    for pattern in EXCLUDE_PATTERNS:
        if pattern.startswith("*") and pattern.endswith("*"):
            if pattern[1:-1] in name:
                return True
        elif pattern.startswith("*"):
            if name.endswith(pattern[1:]):
                return True
        elif pattern.endswith("*"):
            if name.startswith(pattern[:-1]):
                return True
    return False


def build_platform_package(platform_key: str):
    """为指定平台构建发布包"""
    config = PLATFORMS[platform_key]
    print(f"\n{'='*60}")
    print(f"📦 构建 {config['name']} 发布包")
    print(f"{'='*60}")

    # 创建输出目录
    version_dir = DIST_DIR / "V1.+.+" / config["version"].replace("v", "")
    folder_path = version_dir / config["folder_name"]
    zip_path = version_dir / f"{config['folder_name']}.zip"

    # 清理旧文件
    if folder_path.exists():
        shutil.rmtree(folder_path)
    if zip_path.exists():
        zip_path.unlink()

    folder_path.mkdir(parents=True, exist_ok=True)

    # 1. 复制平台描述文件作为 README.md
    desc_src = RELEASE_DIR / config["desc_file"]
    if desc_src.exists():
        shutil.copy2(desc_src, folder_path / "README.md")
        print(f"  ✅ 使用 {config['desc_file']} 作为 README.md")
    else:
        print(f"  ⚠️  描述文件不存在: {desc_src}")

    # 2. 复制其他根目录文件
    for file_name in INCLUDE_FILES:
        src = PROJECT_ROOT / file_name
        if src.exists():
            shutil.copy2(src, folder_path / file_name)
            print(f"  ✅ {file_name}")

    # 3. 复制目录
    for dir_name in INCLUDE_DIRS:
        src_dir = PROJECT_ROOT / dir_name
        if not src_dir.exists():
            print(f"  ⚠️  目录不存在: {dir_name}")
            continue

        dest_dir = folder_path / dir_name
        for item in src_dir.rglob("*"):
            if should_exclude(item):
                continue
            rel_path = item.relative_to(src_dir)
            dest_path = dest_dir / rel_path
            if item.is_dir():
                dest_path.mkdir(parents=True, exist_ok=True)
            else:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)

        file_count = sum(1 for f in dest_dir.rglob("*") if f.is_file())
        print(f"  ✅ {dir_name}/ ({file_count} 个文件)")

    # 4. 创建 zip
    print(f"\n  📦 创建 zip 压缩包...")
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in folder_path.rglob("*"):
            arcname = f"{config['folder_name']}/{item.relative_to(folder_path)}"
            zf.write(item, str(arcname))

    zip_size = zip_path.stat().st_size / 1024
    print(f"  ✅ zip 创建完成: {zip_path.name} ({zip_size:.1f} KB)")

    return folder_path, zip_path


def main():
    import sys

    # 获取目标平台
    target = sys.argv[1] if len(sys.argv) > 1 else "all"

    if target == "all":
        # 构建所有平台
        for platform_key in PLATFORMS:
            build_platform_package(platform_key)
    elif target in PLATFORMS:
        build_platform_package(target)
    else:
        print(f"未知平台: {target}")
        print(f"可选平台: {', '.join(PLATFORMS.keys())}, all")
        sys.exit(1)

    # 打印汇总
    print(f"\n{'='*60}")
    print("📊 发布包构建完成汇总")
    print(f"{'='*60}")
    for key, config in PLATFORMS.items():
        version_dir = DIST_DIR / "V1.+.+" / config["version"].replace("v", "")
        zip_path = version_dir / f"{config['folder_name']}.zip"
        if zip_path.exists():
            size = zip_path.stat().st_size / 1024
            print(f"  ✅ {config['name']}: {zip_path.name} ({size:.1f} KB)")
        else:
            print(f"  ❌ {config['name']}: 未生成")

    print(f"\n📁 输出目录: {DIST_DIR}")


if __name__ == "__main__":
    main()
