import os
import shutil
import json
import zipfile
from datetime import datetime

PROJECT_DIR = r"d:\Users\lele\Desktop\MC模组版本优化与拓展\mc-skill-v1"
RELEASE_DIR = os.path.join(PROJECT_DIR, "release", "github_package_v101")
ZIP_PATH = os.path.join(PROJECT_DIR, "release", "mc-skill-v1.0.1.zip")

if os.path.exists(RELEASE_DIR):
    shutil.rmtree(RELEASE_DIR)

items_to_copy = [
    "main.py", "config.py", "build.py", "requirements.txt", "start.bat",
    "README.md", "SKILL.md", "SKILL.json", "PROJECT_SUMMARY_EN.txt",
    "core", "utils", "data", "locales", "scripts", "tests", "assets"
]

for item in items_to_copy:
    src = os.path.join(PROJECT_DIR, item)
    if not os.path.exists(src):
        continue
    dst = os.path.join(RELEASE_DIR, item)
    if os.path.isdir(src):
        shutil.copytree(src, dst, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy2(src, dst)

release_src = os.path.join(PROJECT_DIR, "release")
release_dst = os.path.join(RELEASE_DIR, "release")
if os.path.exists(release_src):
    os.makedirs(release_dst, exist_ok=True)
    for f in os.listdir(release_src):
        fpath = os.path.join(release_src, f)
        if os.path.isfile(fpath) and f.endswith('.md'):
            shutil.copy2(fpath, os.path.join(release_dst, f))

version_info = {
    "version": "1.0.1",
    "release_date": datetime.now().strftime("%Y-%m-%d"),
    "loader_support": ["NeoForge", "Forge", "Fabric", "Quilt"],
    "mc_version_range": "1.20.1 - 1.21.1",
    "features": [
        "F1_JAR解析",
        "F2_模组检索下载_增强版",
        "F3_环境引导搭建",
        "F4_版本推荐",
        "F5_资源级重打包",
        "F6_依赖冲突诊断",
        "F7_翻译汉化",
        "F8_报错修复",
        "F9_模组移植评估",
        "F10_授权与使用管理",
        "F11_付费引导页面"
    ]
}
with open(os.path.join(RELEASE_DIR, "version.json"), "w", encoding="utf-8") as f:
    json.dump(version_info, f, ensure_ascii=False, indent=2)

if os.path.exists(ZIP_PATH):
    os.remove(ZIP_PATH)

with zipfile.ZipFile(ZIP_PATH, "w", zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk(RELEASE_DIR):
        for file in files:
            file_path = os.path.join(root, file)
            arcname = os.path.relpath(file_path, RELEASE_DIR)
            zf.write(file_path, arcname)

size_kb = os.path.getsize(ZIP_PATH) / 1024
print(f"✅ 发布包已生成: release/mc-skill-v1.0.1.zip")
print(f"   大小: {size_kb:.2f} KB")
print(f"   位置: {ZIP_PATH}")
