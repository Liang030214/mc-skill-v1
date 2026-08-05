---
name: mc-ecosystem-adapt-engineer
version: 1.0.0
description: Minecraft 模组全生态智能适配工具，支持模组检索、环境搭建、Mixin冲突扫描、崩溃修复、汉化、移植评估等10大功能
author: Liang030214
homepage: https://github.com/Liang030214/mc-skill-v1
tags:
  - minecraft
  - mod
  - forge
  - fabric
  - neoforge
  - mixin
  - chinese
  - translation
  - crash-fix
  - migration
category: games
license: MIT
language: zh-CN
min_agent_version: "1.0.0"
---

# MC 全生态智能适配工程师

一站式 Minecraft 模组环境智能管理工具。

## 功能列表

| 功能 | 说明 |
|------|------|
| F1 JAR结构解析 | 解析模组 JAR 文件元数据（mcmod.info、fabric.mod.json、mods.toml） |
| F2 模组检索下载 | 从 Modrinth 搜索下载模组，支持版本和加载器筛选 |
| F3 环境引导搭建 | 智能推荐 MC 版本和加载器组合 |
| F4 Mixin 冲突扫描 | 检测多个模组间的 Mixin 注入冲突 |
| F5 资源重打包 | 模组资源文件重打包优化 |
| F6 存档同步 | 存档备份与恢复 |
| F7 基础汉化 | 模组中文翻译 |
| F8 报错修复 | 智能分析崩溃日志，给出修复建议 |
| F8.1 自动修复 | 一键升级模组修复崩溃问题 |
| F9 移植可行性评估 | 评估模组跨版本/跨加载器迁移可行性 |

## 使用方式

### 方式1：命令行直接运行

```bash
# 解析模组 JAR
python main.py --feature jar_parser --jar-path "create.jar"

# 搜索模组
python main.py --feature mod_searcher --query "Create" --mc-version "1.21.1" --loader "neoforge"

# 扫描 Mixin 冲突
python main.py --feature mixin_scanner --mods-dir "./mods"

# 分析崩溃日志
python main.py --feature crash_analyzer --crash-log "crash-2024-01-01.txt"

# 评估模组移植可行性
python main.py --feature migration_assess --jar-path "create.jar" --from-mc-version "1.20.1" --to-mc-version "1.21.1" --from-loader "forge" --to-loader "neoforge"
```

### 方式2：交互式菜单

```bash
python main.py
# 或
python mc-skill-start.bat
```

### 方式3：Agent AI 调用

Agent 可通过 scripts 目录下的封装脚本调用各功能，返回 JSON 格式结果。

## 支持的加载器

- Forge
- NeoForge
- Fabric
- Quilt

## 支持的 MC 版本

- 1.16.5 ~ 1.21.x

## 运行环境

- Python 3.10+
- Windows / macOS / Linux
- 网络连接（模组搜索功能需要）

## 许可证

MIT License
