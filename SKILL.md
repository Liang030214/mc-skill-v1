---
name: MC Ecosystem Adaptation Engineer
name_zh: MC全生态智能适配工程师
slug: mc-ecosystem-adapt-engineer
version: 1.0.2
description: One-stop Minecraft mod ecosystem intelligent management tool with 12 features including mod search, environment setup, Mixin conflict scanning, crash fix, translation, migration assessment, save sync, authorization management, and multi-language support (11 languages with auto-detection). V1.0.2: Enhanced API caching, offline mode, report rendering performance, and security compliance.
description_zh: Minecraft 模组全生态智能适配工具，支持模组检索、环境搭建、Mixin冲突扫描、崩溃修复、汉化、移植评估、存档同步、授权管理等12大功能，支持11种语言自动切换。V1.0.2：增强API缓存、离线模式、报告渲染性能和安全合规性。
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
  - chinese
  - i18n
  - multilingual
  - save-sync
  - authorization
  - payment-guide
category: games
license: MIT
language: en
languages_supported: ["en", "zh", "ja", "ko", "ru", "es", "it", "el", "th", "hi"]
min_agent_version: "1.0.0"
---

# MC Ecosystem Adaptation Engineer

One-stop Minecraft mod environment intelligent management tool.

# MC 全生态智能适配工程师

一站式 Minecraft 模组环境智能管理工具。

## Feature List

| # | Feature | Description |
|---|---------|-------------|
| F1 | JAR Structure Parser | Parse mod JAR metadata (mcmod.info, fabric.mod.json, mods.toml) |
| F2 | Mod Search & Download | Search and download mods from Modrinth with version and loader filters (supports batch search, category search, similar mod recommendations) |
| F3 | Environment Setup Guide | Intelligently recommend MC version and loader combinations |
| F4 | Mixin Conflict Scanner | Detect Mixin injection conflicts between multiple mods |
| F5 | Resource Repacker | Repack and optimize mod resource files |
| F6 | Save Sync | Backup and restore game saves via Baidu Netdisk sync (supports PC-to-mobile handoff, setup/backup/restore operations) |
| F7 | Multi-Language Translation | Translate mods to target languages (Chinese, English, Japanese, Korean, etc.) with 11-language auto-detection |
| F8 | Crash Fix | Intelligently analyze crash logs and provide fix suggestions |
| F8.1 | Auto Fix | One-click mod upgrade to resolve crash issues |
| F9 | Migration Feasibility Assessment | Assess feasibility of cross-version/cross-loader migration |
| F10 | Authorization & Usage Management | Local machine ID generation, daily usage counting, free period management (60 days), membership tier management (free/normal), and license activation |
| F11 | Payment Guide Page | Generate HTML payment guide page with QR codes for WeChat Official, Afdian, personal payment, and merchant payment when usage limits are reached |

## 功能列表

| # | 功能 | 说明 |
|---|------|------|
| F1 | JAR结构解析 | 解析模组 JAR 文件元数据（mcmod.info、fabric.mod.json、mods.toml） |
| F2 | 模组检索下载 | 从 Modrinth 搜索下载模组，支持版本和加载器筛选（支持批量搜索、分类搜索、同类推荐） |
| F3 | 环境引导搭建 | 智能推荐 MC 版本和加载器组合 |
| F4 | Mixin 冲突扫描 | 检测多个模组间的 Mixin 注入冲突 |
| F5 | 资源重打包 | 模组资源文件重打包优化 |
| F6 | 存档同步 | 通过百度网盘同步空间实现存档备份与恢复（支持PC与手机端接力，包含配置/备份/恢复操作） |
| F7 | 多语言翻译 | 模组目标语言翻译（中文、英文、日文、韩文等），支持11种语言自动检测 |
| F8 | 报错修复 | 智能分析崩溃日志，给出修复建议 |
| F8.1 | 自动修复 | 一键升级模组修复崩溃问题 |
| F9 | 移植可行性评估 | 评估模组跨版本/跨加载器迁移可行性 |
| F10 | 授权与使用管理 | 本地机器码生成、每日使用计数、免费期管理（60天）、会员等级管理（免费/普通）、授权码激活 |
| F11 | 付费引导页面 | 当使用次数达到限制时，生成HTML付费引导页面，展示微信公众号、爱发电、个人付款、商户付款等二维码 |

## Usage

### Method 1: Direct Command Line

```bash
# Parse mod JAR
python main.py --feature jar_parser --jar-path "create.jar"

# Search mods
python main.py --feature mod_searcher --query "Create" --mc-version "1.21.1" --loader "neoforge"

# Scan Mixin conflicts
python main.py --feature mixin_scanner --mods-dir "./mods"

# Analyze crash log
python main.py --feature crash_analyzer --crash-log "crash-2024-01-01.txt"

# Assess migration feasibility
python main.py --feature migration_assess --jar-path "create.jar" --from-mc-version "1.20.1" --to-mc-version "1.21.1" --from-loader "forge" --to-loader "neoforge"
```

### Method 2: Interactive Menu

```bash
python main.py
# or
python mc-skill-start.bat
```

### Method 3: Agent AI Invocation

Agents can invoke each feature through the wrapper scripts in the scripts directory, returning JSON-format results.

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

## Supported Loaders

- Forge
- NeoForge
- Fabric
- Quilt

## 支持的加载器

- Forge
- NeoForge
- Fabric
- Quilt

## Supported MC Versions

- 1.16.5 ~ 1.21.x

## 支持的 MC 版本

- 1.16.5 ~ 1.21.x

## Language Support

This skill supports 11 languages with automatic detection:

| Code | Language | Auto-Detect |
|------|----------|-------------|
| en | English | ✅ |
| zh | 中文 (Chinese) | ✅ |
| ja | 日本語 (Japanese) | ✅ |
| ko | 한국어 (Korean) | ✅ |
| ru | Русский (Russian) | ✅ |
| es | Español (Spanish) | ✅ |
| it | Italiano (Italian) | ✅ |
| el | Ελληνικά (Greek) | ✅ |
| th | ไทย (Thai) | ✅ |
| hi | हिन्दी (Hindi) | ✅ |

**Auto-Detection Strategy:**
- The skill automatically detects the user's language from the conversation context and responds in the preferred language.
- Users can also manually specify the language via the `--lang` parameter when calling commands.
- Translation (F7) supports bidirectional conversion between any two supported languages.

## 语言支持

本 Skill 支持 11 种语言，并具备自动检测能力：

| 代码 | 语言 | 自动检测 |
|------|------|----------|
| en | English (英语) | ✅ |
| zh | 中文 | ✅ |
| ja | 日本語 | ✅ |
| ko | 한국어 | ✅ |
| ru | Русский (俄语) | ✅ |
| es | Español (西班牙语) | ✅ |
| it | Italiano (意大利语) | ✅ |
| el | Ελληνικά (希腊语) | ✅ |
| th | ไทย (泰语) | ✅ |
| hi | हिन्दी (印地语) | ✅ |

**自动检测策略：**
- Skill 会根据对话上下文自动检测用户语言，并以用户偏好的语言回复。
- 用户也可在调用命令时通过 `--lang` 参数手动指定语言。
- 翻译功能（F7）支持任意两种语言之间的双向互译。

## Runtime Environment

- Python 3.10+
- Windows / macOS / Linux
- Network connection (required for mod search feature)
- UTF-8 compatible terminal for multilingual support
- For full i18n functionality, ensure the system locale supports Unicode (UTF-8)

## 运行环境

- Python 3.10+
- Windows / macOS / Linux
- 网络连接（模组搜索功能需要）
- 兼容 UTF-8 的终端以支持多语言显示
- 完整国际化功能需要系统区域设置支持 Unicode（UTF-8）

## Data Collection & Privacy / 数据收集与隐私声明

### Local Data Storage / 本地数据存储

This skill stores the following data **locally only** (in `data/auth_state.json`):

| Data | Description | Purpose |
|------|-------------|---------|
| Machine ID | Hash of device MAC address, hostname, and OS info | Unique device identification |
| First Use Date | Date of first skill usage | Calculate 60-day free period |
| Free Period End Date | First use date + 60 days | Determine free/paid status |
| Daily Usage Count | Count of each feature used per day | Enforce daily usage limits |
| Total Usage Count | Lifetime count of each feature used | Usage statistics |
| Membership Tier | free / normal | Apply appropriate usage limits |
| License Key | User's license activation key | Premium feature access |
| License Expiry | Subscription expiration date | License validity check |

**No data is transmitted to external servers by default.** The optional online verification server (`AUTH_SERVER_URL`) is currently **disabled** (empty string).

### 本地数据存储声明

本 Skill 仅在本地存储以下数据（存储于 `data/auth_state.json`）：

| 数据项 | 说明 | 用途 |
|--------|------|------|
| 机器码 | 设备MAC地址、主机名、操作系统信息的哈希值 | 唯一识别设备 |
| 首次使用日期 | 首次使用Skill的日期 | 计算60天免费期 |
| 免费期结束日期 | 首次使用日期+60天 | 判断免费/付费状态 |
| 每日使用计数 | 每日各功能的使用次数 | 执行每日使用限制 |
| 总使用计数 | 各功能的终身使用次数 | 使用统计 |
| 会员等级 | 免费/普通 | 应用对应的使用限制 |
| 授权码 | 用户的授权激活码 | 高级功能访问 |
| 授权过期时间 | 订阅过期日期 | 授权有效性检查 |

**默认情况下，任何数据都不会传输到外部服务器。** 可选的在线验证服务器（`AUTH_SERVER_URL`）当前处于**禁用状态**（空字符串）。

---

## Authorization System (F10) / 授权管理系统

### Free Period / 免费期

- **Duration**: 60 days from first use
- **During free period**: All features unlimited except migration assessment (1 per day after first use)
- **After free period**: Daily usage limits apply (free users: 20 auto/day, 8 semi/day)

### Membership Tiers / 会员等级

| Tier | Auto Features | Semi Features | Migration Assessment |
|------|--------------|---------------|---------------------|
| Free | 20/day | 8/day | 1/day |
| Normal (¥8.88/month) | 100/day | 50/day | 5/day |
| Premium | Coming Soon | Coming Soon | Coming Soon |

### Pricing / 定价

- Monthly: ¥8.88/month
- Quarterly: ¥23.88/quarter
- Yearly: ¥88.88/year (continuous subscription)
- Per-use: ¥9.9-89.9 per feature

### 免费期与会员说明

- **免费期**：首次使用起60天内免费
- **免费期内**：除移植评估外所有功能不限次数（移植评估首次免费，之后每天1次）
- **免费期后**：自动应用基础限制

### 会员等级与定价

| 等级 | 全自动功能 | 半自动功能 | 移植评估 |
|------|-----------|-----------|---------|
| 免费 | 20次/日 | 8次/日 | 1次/日 |
| 普通会员 (¥8.88/月) | 100次/日 | 50次/日 | 5次/日 |
| 高级会员 | 敬请期待 | 敬请期待 | 敬请期待 |

---

## Payment Guide Page (F11) / 付费引导页面

When usage limits are reached, the skill generates an HTML payment page with:

- WeChat Official Account QR code
- Afdian platform QR code
- Personal payment QR code (WeChat Pay / Alipay)
- Merchant payment QR code

**Note**: Payment page is only displayed when `ENABLE_PAYMENT = True` and the user has reached their daily limit. Currently, `ENABLE_PAYMENT = False` in V1.0.1, so payment prompts are **not shown**.

### 付费引导说明

当使用次数达到限制时，Skill 会生成包含以下内容的HTML付费页面：

- 微信公众号二维码
- 爱发电平台二维码
- 个人付款二维码（微信/支付宝）
- 商户付款二维码

**注意**：付费页面仅在 `ENABLE_PAYMENT = True` 且用户达到每日限制时才显示。当前V1.0.1中 `ENABLE_PAYMENT = False`，因此**不会显示**付费提示。

---

## Save Sync (F6) / 存档同步

This feature supports **PC-to-mobile Minecraft save handoff** via Baidu Netdisk sync space:

- **Setup**: Configure sync directory and launcher
- **Backup**: Package and upload game saves to sync directory
- **Restore**: Download and extract latest backup to saves directory

**Data involved**: Only Minecraft save files (world data) are read and written. No game data is transmitted to external servers except through user-configured Baidu Netdisk sync.

### 存档同步说明

本功能通过百度网盘同步空间实现**PC与手机端MC存档接力**：

- **配置**：设置同步目录和启动器
- **备份**：打包游戏存档上传到同步目录
- **恢复**：从同步目录下载最新备份解压到存档目录

**涉及的数据**：仅读写Minecraft存档文件（世界数据）。除用户配置的百度网盘同步外，无游戏数据传输到外部服务器。

---

## Permissions / 权限声明

| Permission | Required By | Description |
|-----------|------------|-------------|
| File Read | F1, F2, F4, F5, F8, F9 | Read mod JARs, crash logs, config files |
| File Write | F5, F6, F8.1 | Write repacked mods, backup saves, upgrade mods |
| Network Access | F2, F10 (optional) | Download mods from Modrinth; optional auth verification |
| Browser Open | F11 | Open payment guide HTML page in browser |
| Local Storage | F10 | Store auth state, usage counts (auth_state.json) |
| System Info | F10 | Generate machine ID (MAC, hostname, OS) |

| 权限 | 功能 | 说明 |
|------|------|------|
| 文件读取 | F1, F2, F4, F5, F8, F9 | 读取模组JAR、崩溃日志、配置文件 |
| 文件写入 | F5, F6, F8.1 | 写入重打包模组、备份存档、升级模组 |
| 网络访问 | F2, F10（可选） | 从Modrinth下载模组；可选的授权验证 |
| 浏览器打开 | F11 | 在浏览器中打开付费引导HTML页面 |
| 本地存储 | F10 | 存储授权状态、使用计数（auth_state.json） |
| 系统信息 | F10 | 生成机器码（MAC、主机名、操作系统） |

---

## License

MIT License

## 许可证

MIT License