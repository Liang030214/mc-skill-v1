# MC 全生态智能适配工程师 V1

> MC Ecosystem Adaptation Engineer - 一站式 Minecraft 模组环境智能管理工具
> 
> **V1.0.2 增强**：API缓存优化、离线模式增强、报告渲染性能提升、安全合规修复
> 
> **V1.0.1 增强**：批量搜索、分类搜索（16+类别）、同类推荐、动态分类、自动更新兼容库

## 📖 项目简介

本工具是一个面向 Minecraft 模组玩家的智能辅助系统，核心能力包括：模组环境诊断、版本推荐、报错修复和自动修复。支持主流模组加载器（NeoForge、Forge、Fabric、Quilt），覆盖机械动力、乐事、工业时代、应用能源等热门模组生态。

**V1.0.1 新增功能**：
- 📦 **批量搜索模式**：一次性搜索多个关键词，效率翻倍
- 🗂️ **分类搜索**：16+ 预定义模组分类（机械动力、乐事、科技、魔法等）
- 🔍 **同类推荐**：智能发现相关模组
- 🌐 **动态分类**：从 Modrinth API 获取全球模组分类
- 🔄 **自动更新**：每次搜索自动同步版本数据

## ⚠️ 免费与付费说明

### 免费期（首次使用起 60 天）

从您首次使用本 Skill 当天算起 **60 天内**，所有功能**完全免费、不限次数**（模组移植可行性评估除外，首次免费后每天 1 次）。

### 付费机制（敬请期待）

付费订阅功能正在开发中，即将上线！付费机制上线后：

- **免费用户**：每日免费额度，可满足轻度使用需求
- **普通会员**：解锁更高次数限制和进阶服务
- **高级会员**：后续开放，敬请期待

> **说明**：即使付费机制上线后，免费额度每日重置，无需付费也能长期使用基础功能。付费只是为了解锁更高次数限制和进阶服务。

## ✨ 功能特性

| 功能 | 命令参数 | 说明 |
|------|----------|------|
| **F1 JAR解析** | `--feature jar_parser` | 解析模组JAR文件结构、生成中文功能说明书 |
| **F2 模组检索** | `--feature mod_searcher` | 从 Modrinth/CurseForge 搜索下载模组 |
| **F3 环境搭建** | `--feature env_builder` | 自动检测 Java 版本、启动器路径、生成 JVM 参数 |
| **F4 Mixin扫描** | `--feature mixin_scanner` | 分析模组间 Mixin 冲突风险 |
| **F5 资源重打包** | `--feature repacker` | 资源级重打包（图片、音效等处理） |
| **F6 存档同步** | `--feature save_sync` | 百度网盘存档多端同步 |
| **F7 基础汉化** | `--feature translator` | 提取模组语言文件、生成汉化补丁 |
| **F8 报错修复** | `--feature crash_analyzer` | 分析崩溃日志、智能推荐模组版本 |
| **F8.1 自动修复** | `--feature auto_fix` | 一键下载升级模组版本、自动备份替换 |
| **F9 移植评估** | `--feature migration_assess` | 模组移植可行性评估报告，分析API/依赖/Mixin兼容性 |

**V1.0.2 新增/优化**：
- 🚀 **API缓存优化**：带 TTL 的智能缓存（内存+磁盘双级），避免重复 API 请求
- 📦 **离线模式增强**：新增本地模组索引数据库，支持离线模糊搜索和版本查询
- ⚡ **报告渲染优化**：CSS/JS 静态缓存、模板预编译、批量生成支持
- 🔒 **安全合规**：移除付费相关敏感内容（二维码、定价表），改为占位页面
- 🌐 **翻译完善**：11 种语言翻译条目全部对齐（368 个键）

## 🔄 版本更新日志

### V1.0.2 (2026-08-10)

**主要目标修复**：
- ✅ 移除付费页面中的二维码、定价表等敏感内容
- ✅ 将付费页面改为"敬请期待"占位页面
- ✅ 更新 SKILL.json 功能声明，F11 设为禁用状态
- ✅ 同步更新 11 种语言的翻译条目

**次要目标优化**：
- ✅ API 请求缓存系统重构：TTL 过期机制 + 磁盘持久化 + 命中统计
- ✅ 新增离线数据库模块（offline_db.py）：50+ 热门模组索引 + 模糊匹配
- ✅ 报告生成器性能优化：模板预编译 + 静态资源缓存 + 批量生成
- ✅ 11 种语言翻译校对与补全，所有文件 368 键完全同步

## 🚀 快速开始

### 环境要求

- **Python**: 3.10+
- **操作系统**: Windows / macOS / Linux
- **网络**: 首次使用需要联网（下载模组、查询版本）

### 安装步骤

```bash
# 1. 克隆或下载项目
cd mc-skill-v1

# 2. 安装依赖
pip install -r requirements.txt

# 3. 运行主程序
python main.py
```

### 使用示例

#### 示例1: 分析崩溃日志 + 自动修复

```bash
# 分析崩溃日志
python main.py --feature crash_analyzer --crash-log "crash-report.txt"

# 一键自动修复（下载推荐版本并替换）
python main.py --feature auto_fix \
  --fix-mods-dir "C:\Users\xxx\AppData\Roaming\.minecraft\mods" \
  --crash-log "crash-report.txt" \
  --auto-confirm
```

#### 示例2: 搜索并下载模组

```bash
# 搜索机械动力
python main.py --feature mod_searcher \
  --query "Create" \
  --mc-version "1.21.1" \
  --loader "neoforge"

# 下载指定模组
python main.py --feature mod_searcher \
  --mod-id "create" \
  --mc-version "1.21.1" \
  --loader "neoforge"
```

#### 示例3: 环境诊断

```bash
python main.py --feature env_builder \
  --mc-version "1.21.1" \
  --loader "neoforge" \
  --device pc
```

#### 示例4: Mixin 冲突扫描

```bash
python main.py --feature mixin_scanner \
  --mods-dir "C:\Users\xxx\.minecraft\mods" \
  --loader neoforge
```

#### 示例5: 基础汉化

```bash
python main.py --feature translator \
  --mods-dir "C:\Users\xxx\.minecraft\mods" \
  --lang zh_cn
```

#### 示例6: 模组移植可行性评估

```bash
# 评估模组从 Forge 1.20.1 迁移到 NeoForge 1.21.1 的可行性
python main.py --feature migration_assess \
  --jar-path "C:\mods\create-1.20.1.jar" \
  --from-mc-version "1.20.1" \
  --to-mc-version "1.21.1" \
  --from-loader "forge" \
  --to-loader "neoforge"

# 评估 Fabric 版本升级
python main.py --feature migration_assess \
  --jar-path "C:\mods\mod.jar" \
  --from-mc-version "1.20.4" \
  --to-mc-version "1.21.1" \
  --from-loader "fabric" \
  --to-loader "fabric"
```

#### 示例7: 存档同步

```bash
python main.py --feature save_sync \
  --action sync \
  --save-dir "C:\Users\xxx\.minecraft\saves" \
  --netdisk-dir "/mc-saves"
```

## 📋 功能详解

### F9 模组移植可行性评估

分析模组从一个环境（MC版本+加载器）移植到另一个环境的可行性，生成包含以下维度的完整评估报告：

- **加载器迁移兼容性**：Forge→NeoForge、Forge→Fabric 等迁移路径的兼容性分析
- **MC版本兼容性**：API稳定性、关键变更点、常见问题
- **依赖兼容性**：自动检查所有依赖模组在目标环境下的支持情况
- **Mixin注入分析**：扫描模组使用的所有Mixin注入点，评估目标类兼容性
- **可行性评分**：0-100分，结合风险等级和预估工作量

**使用场景**:
- 计划将模组从 Forge 1.20.1 升级到 NeoForge 1.21.1
- 评估跨加载器迁移的工作量
- 检查依赖模组的版本兼容性
- 了解迁移过程中的关键技术变更

### F8 报错修复

分析 Minecraft 崩溃日志，识别错误模式，推荐最佳模组版本。

**支持的崩溃模式（25+种）**:
- 内存溢出 (OOM)
- 光影冲突
- 加载器版本不匹配
- 模组缺失/冲突
- 渲染错误
- Mixin 冲突
- 类加载失败
- 数据序列化错误
- ...等

**版本推荐策略**:
1. **优先本地数据库** - 快速响应，离线可用
2. **联网查询 Modrinth API** - 全生态模组覆盖
3. **智能缓存** - 避免重复 API 调用

### F8.1 自动修复

一键将模组升级到推荐版本。

**工作流程**:
```
崩溃日志 → 分析 → 提取需升级模组 → 下载推荐版本 → 备份旧版本 → 替换 → 生成报告
```

**安全机制**:
- ✅ 强制备份旧版本 JAR（`backup_mods_<时间戳>/`）
- ✅ 回滚支持（将备份文件复制回 mods 目录即可恢复）
- ✅ 操作前确认提示（可通过 `--auto-confirm` 跳过）
- ✅ 详细日志记录

## 📁 项目结构

```
mc-skill-v1/
├── main.py                 # 主程序入口
├── config.py               # 全局配置
├── requirements.txt        # 依赖清单
├── core/                   # 核心功能模块
│   ├── auth_manager.py    # 授权管理与付费体系
│   ├── auto_fix.py        # F8.1 自动修复
│   ├── crash_analyzer.py  # F8 报错修复
│   ├── env_builder.py     # F3 环境搭建
│   ├── jar_parser.py      # F1 JAR 解析
│   ├── migration_assessor.py # F9 移植可行性评估
│   ├── mixin_scanner.py   # F4 Mixin 扫描
│   ├── mod_searcher.py    # F2 模组检索
│   ├── modrinth_client.py # Modrinth API 客户端（V1.0.2 增强缓存）
│   ├── offline_db.py     # V1.0.2 离线数据库模块
│   ├── repacker.py        # F5 资源重打包
│   ├── save_sync.py       # F6 存档同步
│   └── translator.py      # F7 基础汉化
├── data/                   # 数据文件
│   ├── crash_patterns.json      # 崩溃模式库
│   ├── java_version_map.json    # Java 版本映射
│   ├── launcher_paths.json      # 启动器路径
│   └── mod_version_recommendations.json  # 模组版本推荐数据库
├── utils/                  # 工具模块
│   ├── api_client.py      # API 请求封装
│   ├── jar_utils.py       # JAR 工具函数
│   ├── logger.py          # 日志工具
│   └── report_gen.py      # 报告生成（V1.0.2 性能优化版）
├── verify_p1~p6.py        # 各阶段验证脚本
└── _expand_db.py          # 数据库扩充脚本
```

## 🔧 命令行参数

### 全局参数

| 参数 | 说明 |
|------|------|
| `--feature` | 指定功能模块（必填） |
| `--output` | 输出目录路径 |
| `--help` | 显示帮助信息 |

### F8 / F8.1 参数

| 参数 | 说明 |
|------|------|
| `--crash-log` | crash report 或 latest.log 文件路径 |
| `--offline` | 禁用联网查询，仅使用本地数据库 |
| `--fix-mods-dir` | Minecraft 的 mods 目录路径（F8.1 专用） |
| `--auto-confirm` | 自动修复时跳过确认提示 |

### F2 模组检索参数

| 参数 | 说明 |
|------|------|
| `--query` | 模组名称搜索关键词 |
| `--mod-id` | 指定模组 ID（直接查询） |
| `--mc-version` | Minecraft 版本 |
| `--loader` | 模组加载器 (neoforge/forge/fabric/quilt) |

### F9 模组移植评估参数

| 参数 | 说明 |
|------|------|
| `--jar-path` | 源模组 JAR 文件路径 |
| `--from-mc-version` | 源 MC 版本（如 1.20.1） |
| `--to-mc-version` | 目标 MC 版本（如 1.21.1） |
| `--from-loader` | 源加载器 (forge/neoforge/fabric/quilt) |
| `--to-loader` | 目标加载器 (forge/neoforge/fabric/quilt) |

## 💡 常见问题

### Q1: 如何处理下载超时？

```bash
# 增加超时时间或使用本地数据库
python main.py --feature crash_analyzer --crash-log "log.txt" --offline
```

### Q2: 如何扩充本地模组数据库？

```bash
python _expand_db.py
```

### Q3: 自动修复后游戏无法启动怎么办？

```bash
# 从备份目录恢复旧版本
# 备份路径格式: output/temp/backup_mods_<时间戳>/
# 将备份中的 JAR 文件复制回 mods 目录即可
```

### Q4: 支持哪些模组加载器？

| 加载器 | 支持版本 |
|--------|----------|
| NeoForge | 21.1+ (1.21.x) |
| Forge | 47.x+ (1.20.x) |
| Fabric | 0.15+ |
| Quilt | 0.23+ |

### Q5: 如何获取帮助？

```bash
python main.py --help
python main.py --feature crash_analyzer --help
```

## 📝 版本推荐数据库

本工具内置了热门模组的版本推荐规则：

**机械动力系列**:
- Create (机械动力)
- Create: Steam 'n' Rails (蒸汽与铁轨)
- Create: Aerodynamics (航空学)
- Create: Calculation (运算)
- Create: Recycling (创造招牌)
- Create Addition (创造拓展)

**乐事系列**:
- Industrial Foregoing (工业时代2)
- Thermal Series (热力系列)

**能源机械系列**:
- Applied Energistics 2 (应用能源2)
- IndustrialCraft 2 (工业时代)

**耕种生存系列**:
- Pam's HarvestCraft (潘氏丰收)

运行 `python _expand_db.py` 可扩充更多模组数据。

## 📄 许可证

本项目仅供学习交流使用。

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**MC 全生态智能适配工程师 V1** | 让 Minecraft 模组管理更简单
