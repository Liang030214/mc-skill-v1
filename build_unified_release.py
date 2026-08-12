# -*- coding: utf-8 -*-
"""生成统一的多平台发布包目录结构"""

import shutil
import zipfile
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
RELEASE_DIR = PROJECT_ROOT / "release"
OUTPUT_DIR = PROJECT_ROOT / "dist" / "release-packages"

# 平台配置
PLATFORMS = [
    {
        "key": "skillhub",
        "folder": "SkillHub_V1",
        "package_name": "mc-ecosystem-adapt-engine-skillhub-v1",
        "desc_file": "skillhub_desc.md",
        "version": "SkillHub V1",
    },
    {
        "key": "github",
        "folder": "GitHub_V1.0.2",
        "package_name": "mc-ecosystem-adapt-engine-github-v1.0.2",
        "desc_file": "github_desc.md",
        "version": "v1.0.2",
    },
    {
        "key": "clawhub",
        "folder": "ClawHub_V1.0.3",
        "package_name": "mc-ecosystem-adapt-engine-clawhub-v1.0.3",
        "desc_file": "clawhub_desc.md",
        "version": "v1.0.3",
    },
]

# 要打包的目录和文件
INCLUDE_DIRS = ["core", "data", "utils", "locales", "assets", "scripts"]
INCLUDE_ROOT_FILES = ["main.py", "config.py", "requirements.txt", "SKILL.md", "SKILL.json"]
EXCLUDE_PATTERNS = ["__pycache__", "*.pyc", "*.pyo"]


def should_exclude(file_path: Path) -> bool:
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


def build_package(platform: dict):
    """为指定平台构建发布包"""
    output_platform_dir = OUTPUT_DIR / platform["folder"]
    package_dir = output_platform_dir / platform["package_name"]
    zip_path = output_platform_dir / f"{platform['package_name']}.zip"

    print(f"\n📁 构建 {platform['version']} 发布包")

    # 清理旧文件
    if output_platform_dir.exists():
        shutil.rmtree(output_platform_dir)
    package_dir.mkdir(parents=True, exist_ok=True)

    # 1. 复制平台描述文件作为 README.md
    desc_src = RELEASE_DIR / platform["desc_file"]
    if desc_src.exists():
        shutil.copy2(desc_src, package_dir / "README.md")
        print(f"  ✅ README.md ← {platform['desc_file']}")

    # 2. 复制根目录文件
    for file_name in INCLUDE_ROOT_FILES:
        src = PROJECT_ROOT / file_name
        if src.exists():
            shutil.copy2(src, package_dir / file_name)

    # 3. 复制目录
    for dir_name in INCLUDE_DIRS:
        src_dir = PROJECT_ROOT / dir_name
        if not src_dir.exists():
            continue

        for item in src_dir.rglob("*"):
            if should_exclude(item):
                continue
            rel_path = item.relative_to(src_dir)
            dest_path = package_dir / dir_name / rel_path
            if item.is_dir():
                dest_path.mkdir(parents=True, exist_ok=True)
            else:
                dest_path.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(item, dest_path)

    # 统计文件
    file_count = sum(1 for f in package_dir.rglob("*") if f.is_file())
    print(f"  ✅ 文件夹: {platform['package_name']}/ ({file_count} 个文件)")

    # 4. 创建 zip
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for item in package_dir.rglob("*"):
            arcname = f"{platform['package_name']}/{item.relative_to(package_dir)}"
            zf.write(item, str(arcname))

    zip_size = zip_path.stat().st_size / 1024
    print(f"  ✅ 压缩包: {zip_path.name} ({zip_size:.1f} KB)")


def main():
    print("=" * 60)
    print("📦 多平台发布包统一生成器")
    print("=" * 60)
    print(f"\n📂 输出目录: {OUTPUT_DIR}")

    # 生成所有平台包
    for platform in PLATFORMS:
        build_package(platform)

    # 生成目录结构说明
    print(f"\n📝 生成目录结构说明文件")
    readme_content = """# MC Ecosystem Adaptation Engineer - 发布包

## 版本对应关系

| 平台 | 版本号 | 目录名 |
|------|--------|--------|
| SkillHub | V1 | SkillHub_V1/ |
| GitHub | v1.0.2 | GitHub_V1.0.2/ |
| ClawHub | v1.0.3 | ClawHub_V1.0.3/ |

## 目录结构

```
release-packages/
├── SkillHub_V1/
│   ├── mc-ecosystem-adapt-engine-skillhub-v1/     ← 文件夹（拖拽上传）
│   └── mc-ecosystem-adapt-engine-skillhub-v1.zip  ← 压缩包
├── GitHub_V1.0.2/
│   ├── mc-ecosystem-adapt-engine-github-v1.0.2/
│   └── mc-ecosystem-adapt-engine-github-v1.0.2.zip
└── ClawHub_V1.0.3/
    ├── mc-ecosystem-adapt-engine-clawhub-v1.0.3/
    └── mc-ecosystem-adapt-engine-clawhub-v1.0.3.zip
```

## 使用方法

### SkillHub 上传
1. 进入 `SkillHub_V1/` 目录
2. 将 `mc-ecosystem-adapt-engine-skillhub-v1/` 文件夹拖拽到 SkillHub 上传
3. 或使用 `mc-ecosystem-adapt-engine-skillhub-v1.zip` 压缩包

### GitHub 推送
1. 推送代码到 GitHub 仓库
2. 使用 `GitHub_V1.0.2/` 中的内容作为 Release 附件

### ClawHub 发布
1. 进入 `ClawHub_V1.0.3/` 目录
2. 上传 `mc-ecosystem-adapt-engine-clawhub-v1.0.3.zip` 到 ClawHub

## 版本说明

### V1.0.2 / V1.0.3 更新内容

**安全合规修复**：
- 移除所有付费相关敏感内容（二维码、定价表、支付引导）
- 付费功能改为"敬请期待"占位页面
- 功能声明同步更新

**性能优化**：
- API 请求缓存系统重构：TTL 过期机制 + 磁盘持久化 + 命中统计
- 新增离线数据库模块：50+ 热门模组索引 + 模糊匹配
- 报告生成器性能优化：模板预编译 + 静态资源缓存 + 批量生成
- 11 种语言翻译校对与补全，所有文件 368 键完全同步

## 作者

- **作者**: Liang030214
- **许可证**: MIT License
- **项目主页**: https://github.com/Liang030214/mc-skill-v1
"""

    readme_path = OUTPUT_DIR / "README.md"
    readme_path.write_text(readme_content, encoding="utf-8")
    print(f"  ✅ README.md 说明文件已生成")

    # 打印汇总
    print(f"\n{'='*60}")
    print("✅ 所有发布包生成完成")
    print(f"{'='*60}")
    print(f"\n📁 输出目录结构:")
    print(f"  release-packages/")
    for platform in PLATFORMS:
        size = (OUTPUT_DIR / platform["folder"] / f"{platform['package_name']}.zip").stat().st_size / 1024
        print(f"  ├── {platform['folder']}/  ({size:.0f} KB)")
    print(f"  └── README.md")

    print(f"\n💡 使用提示:")
    print(f"  • 直接将各平台文件夹拖拽到对应平台上传")
    print(f"  • 或使用 zip 压缩包上传")


if __name__ == "__main__":
    main()
