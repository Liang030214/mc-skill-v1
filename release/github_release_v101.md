# MC Ecosystem Adaptation Engineer V1.0.1

> MC 全生态智能适配工程师 — 一站式 Minecraft 模组环境智能管理工具
>
> 📝 **版本说明**: 本地版本号为 V1.0.1，市场/平台版本号可能因发布规则略有差异

---

## 🎯 版本亮点 / Highlights

### 中文

- 🔍 **模组检索增强**: 新增16个模组分类索引，支持批量搜索、分类搜索、同类推荐
- 📚 **兼容规则库扩充**: 模组版本推荐数据库从35+扩充至65+，覆盖机械动力、乐事、科技能源、红石魔改等热门模组
- 🌐 **国际化支持**: 新增11种语言（英语、简体/繁体中文、日语、韩语、俄语、西班牙语、意大利语、希腊语、泰语、印地语），支持智能检测自动切换
- 🔐 **权限声明完善**: 新增 SKILL.json 元数据文件，完整声明12个功能的权限需求与数据收集策略
- 🐛 **Bug修复**: 修复 F2 模组检索、F3 环境搭建、F5 资源重打包、F8.1 自动修复等多处已知问题

### English

- 🔍 **Enhanced Mod Search**: New 16-category index with batch search, category search, and similar mod recommendations
- 📚 **Expanded Compatibility Library**: Mod recommendation database expanded from 35+ to 65+ mods, covering Create, Fun series, Tech & Energy, Redstone & Automation, and more
- 🌐 **Multi-language Support**: 11 languages (EN, ZH-CN, ZH-TW, JA, KO, RU, ES, IT, EL, TH, HI) with auto-detection via IP geolocation → system locale → English fallback
- 🔐 **Complete Permission Declaration**: New SKILL.json with full declaration of 12 features' permission requirements and data collection policies
- 🐛 **Bug Fixes**: Fixed issues in F2 mod search, F3 environment setup, F5 resource repacking, F8.1 auto-fix, and more

---

## ✨ 功能清单 / Feature List

| # | 功能 / Feature | 说明 / Description | 权限 / Permissions |
|---|---|---|---|
| F1 | JAR Structure Parser | Parse mod JAR metadata (mcmod.info, fabric.mod.json, mods.toml) | file_read |
| F2 | Mod Search & Download | Search and download mods from Modrinth with batch/category/similar search | network |
| F3 | Environment Setup Guide | Intelligently recommend MC version and loader combinations | — |
| F4 | Mixin Conflict Scanner | Detect Mixin injection conflicts between multiple mods | file_read |
| F5 | Resource Repacker | Repack and optimize mod resource files (textures, sounds, lang files) | file_read, file_write |
| F6 | Save Sync | Backup and restore game saves with multi-device sync | file_read, file_write |
| F7 | Multi-language Translation | Translate mod language files between 11 supported languages | file_read, file_write |
| F8 | Crash Fix | Analyze crash logs, identify 25+ error patterns, provide fix suggestions | file_read |
| F8.1 | Auto Fix | One-click mod version upgrade with automatic backup and rollback | file_read, file_write |
| F9 | Migration Feasibility Assessment | Cross-version/cross-loader migration report with API/dependency/Mixin analysis | file_read |
| F10 | Authorization & Usage Mgmt | Local machine ID, usage counting, 60-day free period, membership tiers | local_storage, system_info |
| F11 | Payment Guide Page | Generate HTML payment guide when limits reached (disabled in V1.0.1) | browser_open |

---

## 🔧 技术特性 / Technical Highlights

- **All-Loader Support**: Native support for Forge, NeoForge, Fabric, and Quilt
- **11 Languages**: Complete language packs with smart auto-detection
- **25+ Crash Patterns**: Comprehensive crash pattern database covering OOM, shader conflicts, Mixin conflicts, and more
- **Modrinth API Integration**: Real-time mod version queries with local database fallback
- **Smart Caching**: Avoid redundant API calls for improved response speed
- **Safety Backups**: Forced backup before auto-fix with one-click rollback
- **Mixin Analysis**: Deep scan of Mixin injection points with compatibility assessment
- **Cross-Platform**: Windows, macOS, and Linux support

---

## 📋 更新详情 / Changelog

### V1.0.1 (2026-08-08)

#### 新增功能 / New Features

- **F9 Migration Feasibility Assessment**: Analyzes mod portability across environments with 5 dimensions (loader migration, MC version, dependency, Mixin injection, feasibility scoring 0-100). Outputs JSON and HTML reports.
- **F8.1 Auto Fix**: One-click mod version upgrade with automatic JAR backup and rollback. Real-time version recommendations via Modrinth API.

#### F2 模组检索增强 / F2 Mod Search Enhancement

- **Batch Search**: Search multiple keywords at once for bulk downloads
- **Category Search**: 17 preset categories (create/fun/tech/redstone/magic/storage/adventure/survival/decoration/mobs/equipment/food/worldgen/gameplay/performance/utility) + dynamic categories from Modrinth API
- **Similar Mod Recommendations**: Smart recommendations based on search queries
- **Auto-update Library**: Automatically sync new mod data after each search

#### 兼容规则库扩充 / Compatibility Library Expansion

Database expanded from 35+ to **65+ mods**:
- **Create Add-ons**: Create Factory, Create Enchantment Industry, Create Minecraft Industrial
- **Fun Series**: Kitchen's Delight, Cooking for Blockheads, Spice of Life
- **Tech & Energy**: Mekanism, Immersive Engineering, Tech Reborn, Big Reactors
- **Redstone & Automation**: Redstone Flux, BuildCraft, Refined Storage, Draconic Evolution
- **Magic & Adventure**: Ars Magica, Blood Magic, Psi
- **Performance**: Lithium, Phosphor, Starlight (Fabric optimizations)

#### 核心优化 / Core Enhancements

- **Code-level i18n**: All hardcoded strings replaced with `t()` translation calls (main.py, auth_manager.py, payment_page.py, migration_assessor.py, auto_fix.py)
- **11 Languages**: Added en_us, zh_cn, zh_tw, ja_jp, ko_kr, ru_ru, es_es, it_it, el_gr, th_th, hi_in
- **Smart Detection**: 3-tier fallback: IP geolocation → system locale → English
- **Auth Panel Refactored**: Membership, payment info, usage limits all multi-language
- **Payment Page i18n**: HTML payment guide supports multi-language QR codes
- **Skill Package Support**: `build.py` with `--skill-package` flag for market-compliant packages

#### 修复与改进 / Fixes & Improvements

- Optimized crash log regex matching precision
- Improved Modrinth API error handling and retry mechanisms
- Enhanced Mixin injection point analysis accuracy
- Optimized multi-language file loading performance
- Improved interactive menu user experience
- Enhanced auto-fix backup and rollback mechanisms

---

## 💻 系统要求 / System Requirements

- **Python**: 3.10+
- **操作系统 / OS**: Windows / macOS / Linux
- **网络 / Network**: Required for mod search and version queries
- **存储 / Storage**: ~50MB for installation

### 支持的加载器 / Supported Loaders

| Loader | Version |
|--------|---------|
| Forge | 47.x+ (1.20.x) |
| NeoForge | 21.1+ (1.21.x) |
| Fabric | 0.15+ |
| Quilt | 0.23+ |

### 支持的MC版本 / Supported MC Versions

- 1.16.5 ~ 1.21.x

---

## 🚀 安装与使用 / Installation & Usage

### 快速开始 / Quick Start

```bash
# 1. 安装依赖 / Install dependencies
pip install -r requirements.txt

# 2. 运行 / Run interactively
python main.py

# 或使用启动脚本 / Or use startup script
# Windows: start.bat
```

### 命令行使用 / Command Line Usage

```bash
# 模组检索 / Mod search
python main.py --feature mod_searcher --query "Create" --mc-version "1.21.1" --loader "neoforge"

# 模组移植评估 / Migration assessment
python main.py --feature migration_assess --jar-path "mod.jar" --from-mc-version "1.20.1" --to-mc-version "1.21.1" --from-loader "forge" --to-loader "neoforge"

# 报错修复 / Crash fix
python main.py --feature crash_analyzer --crash-log "crash-report.txt"

# 自动修复 / Auto fix
python main.py --feature auto_fix --crash-log "crash.txt" --fix-mods-dir "~/mods"

# 汉化翻译 / Translation
python main.py --feature translator --mods-dir "~/mods" --lang zh_cn

# Mixin扫描 / Mixin scan
python main.py --feature mixin_scanner --mods-dir "~/mods"
```

---

## 🔒 权限声明 / Permission Declaration

| 权限 / Permission | 用途 / Purpose |
|---|---|
| `file_read` | 读取模组JAR、崩溃日志、配置文件 / Read mod JARs, crash logs, config files |
| `file_write` | 写入重打包模组、备份存档、升级模组 / Write repacked mods, backup saves, upgrade mods |
| `network` | 从Modrinth下载模组 / Download mods from Modrinth |
| `browser_open` | 打开付费引导页面（V1.0.1已禁用）/ Open payment guide page (disabled in V1.0.1) |
| `local_storage` | 存储授权状态、使用计数 / Store auth state, usage counts |
| `system_info` | 生成机器码 / Generate machine ID |

### 数据收集 / Data Collection

- **本地存储**: 机器码、使用次数、会员等级、首次使用日期
- **外部传输**: 默认不传输到外部服务器
- **免费期**: 首次使用起60天，存储在本地

---

## 📁 项目结构 / Project Structure

```
mc-skill-v1/
├── main.py                    # 主程序入口 / Main entry
├── config.py                  # 全局配置 / Global config
├── build.py                   # 构建脚本 / Build script
├── SKILL.json                 # 功能元数据 / Feature metadata
├── SKILL.md                   # 功能说明 / Feature documentation
├── requirements.txt           # 依赖清单 / Dependencies
├── start.bat                  # Windows启动脚本 / Windows startup
├── core/                      # 核心功能 / Core features
│   ├── jar_parser.py         # F1 JAR结构解析
│   ├── mod_searcher.py       # F2 模组检索下载
│   ├── env_builder.py        # F3 环境引导搭建
│   ├── mixin_scanner.py      # F4 Mixin冲突扫描
│   ├── repacker.py           # F5 资源重打包
│   ├── save_sync.py          # F6 存档同步
│   ├── translator.py         # F7 多语言翻译
│   ├── crash_analyzer.py     # F8 报错修复
│   ├── auto_fix.py           # F8.1 自动修复
│   ├── migration_assessor.py # F9 移植可行性评估
│   ├── auth_manager.py       # F10 授权与使用管理
│   ├── payment_page.py       # F11 付费引导页面
│   ├── i18n.py               # 国际化框架
│   └── modrinth_client.py    # Modrinth API客户端
├── data/                      # 数据文件 / Data files
│   ├── crash_patterns.json
│   ├── java_version_map.json
│   ├── launcher_paths.json
│   └── mod_version_recommendations.json
├── locales/                   # 语言文件 / Language files (11 languages)
├── utils/                     # 工具模块 / Utilities
└── tests/                     # 测试脚本 / Tests
```

---

## 📄 版本信息 / Version Info

- **版本 / Version**: 1.0.1
- **发布日期 / Release Date**: 2026-08-08
- **许可证 / License**: MIT
- **作者 / Author**: Liang030214
- **首页 / Homepage**: [https://github.com/Liang030214/mc-skill-v1](https://github.com/Liang030214/mc-skill-v1)
- **标签 / Tags**: minecraft, mod, forge, fabric, neoforge, quilt, mixin, translation, crash-fix, migration, i18n

---

## 🙏 致谢 / Credits

- [Modrinth API](https://modrinth.com/) for providing mod search and version data
- Minecraft community for feedback and testing
- All contributors to the open-source Minecraft ecosystem

---

**MC Ecosystem Adaptation Engineer V1.0.1** | 让 Minecraft 模组管理更简单
