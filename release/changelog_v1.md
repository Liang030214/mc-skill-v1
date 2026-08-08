# 版本日志 / Changelog

> **Note / 版本说明**: Local version numbers are for development tracking only. The version number on the market/platform may differ from the local version due to platform publishing rules.
> **注意 / 版本说明**: 本地版本号仅用于开发追踪，网站/市场上发布的版本号可能因平台发布规则而不同。

## V1.0.1 (2026-08-06)

### 🔧 首个迭代优化版 / First Iterative Enhancement

---

### 中文说明

#### 新增功能

- **F9 模组移植可行性评估**：分析模组从一个环境（MC 版本 + 加载器）移植到另一个环境的可行性，包含加载器迁移兼容性、MC 版本兼容性、依赖兼容性、Mixin 注入分析、可行性评分（0-100）五大维度。支持 JSON 和 HTML 报告输出。
- **F8.1 自动修复**：一键将模组升级到推荐版本，自动备份旧版本 JAR 文件，支持回滚恢复。基于 Modrinth API 实时获取版本推荐数据。

#### F2 模组检索增强（V1.0.1 新增）

- **批量搜索模式**：支持一次性输入多个关键词进行批量搜索，可批量下载模组，大幅提升检索效率
- **分类搜索模式**：支持预定义分类和动态分类两种搜索方式：
  - 预定义分类：17 大模组分类索引（create/fun/tech/redstone/magic/storage/adventure/survival/decoration/mobs/equipment/food/worldgen/gameplay/performance/utility）
  - **动态分类**：从 Modrinth API 自动获取所有可用分类，支持世界上所有模组类型的搜索
- **同类模组推荐**：根据已搜索的模组智能推荐同分类的相关模组，发现更多优质模组
- **自动更新兼容规则库**：每次联网搜索后自动将新模组和版本信息更新到本地兼容规则库，保持数据实时性

#### 兼容规则库扩充（V1.0.1 新增）

模组版本推荐数据库 `mod_version_recommendations.json` 从原来的 35+ 模组扩充至 **65+ 模组**，重点补充：

- **机械动力周边**：Create Factory、Create Enchantment Industry、Create Minecraft Industrial 等
- **乐事系列**：Kitchen's Delight（厨房乐事）、Cooking for Blockheads（方块料理）、Spice of Life（生活调味料）等
- **科技能源类**：Mekanism（机械动力）、Immersive Engineering（沉浸工程）、Tech Reborn（科技重生）、Big Reactors（大型反应堆）等
- **红石魔改类**：Redstone Flux（红石通量）、BuildCraft（建筑工艺）、Refined Storage（精炼存储）、Draconic Evolution（龙之进化）等
- **魔法冒险类**：Ars Magica（神秘魔法）、Blood Magic（血魔法）、Psi 等
- **性能优化类**：Lithium（锂）、Phosphor（磷）、Starlight（星光）等 Fabric 优化模组

#### 核心优化

- **代码级国际化改造（i18n）**：将 `main.py`、`auth_manager.py`、`payment_page.py`、`migration_assessor.py`、`auto_fix.py` 中所有硬编码的中文用户可见字符串，全部替换为 `t()` 翻译函数调用。支持 **11 种语言**无缝切换。
- **11 种语言支持**：新增 `en_us`（英语）、`zh_cn`（简体中文）、`zh_tw`（繁体中文）、`ja_jp`（日语）、`ko_kr`（韩语）、`ru_ru`（俄语）、`es_es`（西班牙语）、`it_it`（意大利语）、`el_gr`（希腊语）、`th_th`（泰语）、`hi_in`（印地语）的完整翻译文件。
- **智能语言检测**：实现 **IP 地理定位 → 系统 Locale → 英文** 的三级降级策略，自动识别用户设备所在地区并切换语言，无网络时自动降级。
- **授权状态面板重构**：会员等级名称、付费说明、使用次数限制提示等全部支持多语言显示。
- **付费页面国际化**：`payment_page.py` 生成的 HTML 付费引导页面已支持多语言，可根据用户偏好展示对应语言的二维码和定价信息。
- **Skill 市场发布包支持**：`build.py` 新增 `create_skill_package()` 函数，通过 `--skill-package` 参数可一键生成符合国内外 Skill 市场要求的发布包，自动排除临时文件。

#### 修复与改进

- 优化崩溃日志解析的正则表达式匹配精度
- 改进 Modrinth API 的错误处理与重试机制
- 增强 Mixin 注入点分析的准确性
- 优化多语言文件的加载性能
- 改进交互式菜单的用户体验
- 增强自动修复的备份与回滚机制

---

### English Description

#### New Features

- **F9 Migration Feasibility Assessment**: Analyzes mod portability across environments (MC version + loader) with 5 dimensions: loader migration compatibility, MC version compatibility, dependency compatibility, Mixin injection analysis, and feasibility scoring (0-100). Outputs both JSON and HTML reports.
- **F8.1 Auto Fix**: One-click mod version upgrade to recommended versions with automatic JAR backup and rollback support. Fetches real-time version recommendations via Modrinth API.

#### F2 Mod Search Enhancement (V1.0.1 New)

- **Batch Search Mode**: Supports batch searching with multiple keywords at once, enabling bulk mod downloads for improved efficiency
- **Category Search Mode**: Supports both preset and dynamic categories:
  - Preset categories: 17 mod categories (create/fun/tech/redstone/magic/storage/adventure/survival/decoration/mobs/equipment/food/worldgen/gameplay/performance/utility)
  - **Dynamic categories**: Automatically fetches all available categories from Modrinth API, supporting all mod types worldwide
- **Similar Mod Recommendations**: Intelligently recommends related mods in the same category based on your search queries
- **Auto-update compatibility library**: Automatically updates local compatibility library with new mods and version info after each online search

#### Compatibility Library Expansion (V1.0.1 New)

The mod version recommendation database `mod_version_recommendations.json` has been expanded from 35+ to **65+ mods**, with focus on:

- **Create Add-ons**: Create Factory, Create Enchantment Industry, Create Minecraft Industrial, etc.
- **Fun Series**: Kitchen's Delight, Cooking for Blockheads, Spice of Life, etc.
- **Tech & Energy**: Mekanism, Immersive Engineering, Tech Reborn, Big Reactors, etc.
- **Redstone & Automation**: Redstone Flux, BuildCraft, Refined Storage, Draconic Evolution, etc.
- **Magic & Adventure**: Ars Magica, Blood Magic, Psi, etc.
- **Performance**: Lithium, Phosphor, Starlight and other Fabric optimizations

#### Core Enhancements

- **Code-level Internationalization (i18n)**: All hardcoded Chinese user-visible strings in `main.py`, `auth_manager.py`, `payment_page.py`, `migration_assessor.py`, and `auto_fix.py` have been replaced with `t()` translation function calls. Supports **11 languages** seamlessly.
- **11 Languages Supported**: Complete translation files added for `en_us`, `zh_cn`, `zh_tw`, `ja_jp`, `ko_kr`, `ru_ru`, `es_es`, `it_it`, `el_gr`, `th_th`, and `hi_in`.
- **Smart Language Detection**: Implemented a 3-tier fallback strategy: **IP Geolocation → System Locale → English**. Automatically detects the user's device region and switches language, with graceful degradation when offline.
- **Auth Status Panel Refactored**: Membership tier names, payment descriptions, and usage limit prompts now support multi-language display.
- **Payment Page i18n**: The HTML payment guide generated by `payment_page.py` now supports multiple languages, displaying QR codes and pricing information in the user's preferred language.
- **Skill Market Publishing Support**: `build.py` now includes a `create_skill_package()` function. Use the `--skill-package` flag to generate a release package compliant with domestic and international Skill market requirements, automatically excluding temporary files.

#### Fixes & Improvements

- Optimized regex matching precision for crash log parsing
- Improved error handling and retry mechanisms for the Modrinth API client
- Enhanced accuracy of Mixin injection point analysis
- Optimized loading performance for multi-language files
- Improved user experience of the interactive menu
- Enhanced backup and rollback mechanisms for auto-fix

---

### 致谢 / Credits

- Modrinth API (https://modrinth.com/) for providing mod search and version data
- Minecraft community for feedback and testing
- All contributors to the open-source Minecraft ecosystem

---

**MC 全生态智能适配工程师 V1.0.1** | 让 Minecraft 模组管理更简单

---
---

## V1.0.0 (2026-08-06)

### 🚀 基础版本首发 / Initial Base Release

---

### 中文说明

#### 新增功能

- **F1 JAR 结构解析**：支持解析 Forge（mcmod.info）、Fabric（fabric.mod.json）、NeoForge/Forge（mods.toml）三种主流模组元数据格式
- **F2 模组检索下载**：集成 Modrinth API，支持按 MC 版本、加载器类型、分类筛选模组
- **F3 环境引导搭建**：智能推荐 MC 版本与加载器最佳组合方案
- **F4 Mixin 冲突扫描**：扫描 mods 目录下所有模组的 Mixin 配置，分析注入点冲突风险
- **F5 资源重打包**：模组资源文件重打包优化
- **F6 存档同步**：游戏存档备份与恢复
- **F7 汉化翻译**：支持中文、英文双向翻译
- **F8 报错修复**：内置 25+ 崩溃错误模式数据库

#### 技术特性

- 支持 4 大模组加载器：Forge、NeoForge、Fabric、Quilt
- 覆盖 MC 版本：1.16.5 ~ 1.21.x
- 内置 Modrinth API 客户端
- 双运行模式：交互式菜单 + 命令行直接调用
- 跨平台支持：Windows / macOS / Linux

---

### English Description

#### New Features

- **F1 JAR Structure Parser**: Supports parsing Forge (mcmod.info), Fabric (fabric.mod.json), NeoForge/Forge (mods.toml) mod metadata formats
- **F2 Mod Search & Download**: Integrated Modrinth API with MC version, loader type, and category filtering
- **F3 Environment Setup Guide**: Intelligently recommends optimal MC version and loader combinations
- **F4 Mixin Conflict Scanner**: Scans Mixin configurations across all mods, analyzes injection point conflicts
- **F5 Resource Repacker**: Mod resource file repacking and optimization
- **F6 Save Sync**: Game save backup and restore
- **F7 Translation**: Bidirectional translation between Chinese and English
- **F8 Crash Fix**: Built-in 25+ crash error pattern database

#### Technical Highlights

- 4 mod loaders supported: Forge, NeoForge, Fabric, Quilt
- MC version coverage: 1.16.5 ~ 1.21.x
- Built-in Modrinth API client
- Dual runtime: Interactive menu + command line
- Cross-platform: Windows / macOS / Linux

---

**MC 全生态智能适配工程师 V1.0.0** | 基础版本发布