# ClawHub Skill 发布操作指南 (V1.0.1)

本指南将一步步引导你将 **MC 全生态智能适配工程师** 发布到 ClawHub。

ClawHub 提供了三种发布方式，**强烈推荐方式一或方式二**。

---

## 🎯 第一步：准备发布素材

在发布前，请确保以下素材已准备好：

| 素材 | 位置 | 说明 |
|------|------|------|
| **Skill 文件夹** | `dist/mc-ecosystem-adapt-engine/` | 包含所有核心文件的干净文件夹，用于拖拽上传 |
| **Skill 压缩包** | `dist/mc-skill-market-<时间戳>.zip` | 文件夹的 zip 版本，备用 |
| **市场图标** | `assets/icon-market.jpg` | Skill 在市场上显示的图标 |
| **描述文档** | `release/clawhub_desc.md` | 平台介绍文案 |
| **版本日志** | `release/changelog_v1.md` | 更新日志 |

### 如何生成 Skill 文件夹？

在 CMD 中双击运行 `build_skill_package.bat`，它会自动在 `dist` 目录下生成干净的 `mc-ecosystem-adapt-engine` 文件夹。

---

## 🚀 第二步：选择发布方式

### ⭐ 方式一：从 GitHub 导入（最推荐，最适合你）

**适用场景**：你的 Skill 代码已经托管在 GitHub 上。

**操作步骤**：
1. 在 ClawHub 发布页面，点击右上角的 **“从 GitHub 导入”** 按钮。
2. 在弹出的窗口中，选择你的仓库 `Liang030214/mc-skill-v1`。
3. 选择正确的分支（通常是 `main` 或 `master`）。
4. 系统会自动拉取代码、解析 `SKILL.md`、读取所有元数据和图标。
5. 核对信息后，点击 **“导入”** 即可。

**优点**：
- 无需手动打包上传
- 后续更新 Skill 时，只需在 GitHub 上更新代码，然后在 ClawHub 点击 **“同步”** 即可
- 保持 GitHub 和 ClawHub 版本一致

---

### ⭐ 方式二：拖拽文件夹上传（最通用）

**适用场景**：代码还没有托管到 GitHub，或者想手动控制发布。

**操作步骤**：
1. 打开文件管理器，找到 `dist` 目录下的 `mc-ecosystem-adapt-engine` 文件夹。
2. **点击并拖拽** 这个文件夹，拖到 ClawHub 发布页面的上传区域（“Drop a skill folder here”）。
3. 或者点击 **“选择文件夹”** 按钮，手动选择该文件夹。
4. 系统会自动解析 `SKILL.md`，你只需核对信息并补充描述。

**文件夹结构要求**：
```
mc-ecosystem-adapt-engine/
├── SKILL.md          # 必须！元数据描述文件
├── main.py           # 主入口
├── config.py         # 配置
├── requirements.txt  # 依赖
├── core/             # 核心模块
├── data/             # 数据
├── utils/            # 工具
├── locales/          # 语言包
├── assets/           # 图标
├── scripts/          # 脚本
└── README.md         # 说明文档
```
*(不用担心，`build.py` 已经为你整理好了这个结构)*

---

### 方式三：上传 ZIP 文件（备选）

**适用场景**：某些情况下 ClawHub 只接受 zip。

**操作步骤**：
1. 在 ClawHub 发布页面，点击上传区域。
2. 选择 `dist` 目录下的 `mc-skill-market-<时间戳>.zip` 文件。
3. 系统会解压并解析 zip 内容。

---

## 📝 第三步：完善 Skill 信息

无论使用哪种方式，导入后都需要完善以下信息：

### 1. 基本信息（自动填充）

| 字段 | 值 | 状态 |
|------|-----|------|
| 技能名称 | MC全生态智能适配工程师 | 自动从 SKILL.md 读取 |
| 版本号 | 1.0.1 | 自动从 SKILL.md 读取 |
| 源代码地址 | https://github.com/Liang030214/mc-skill-v1 | 手动填写 |

### 2. 上传图标

- 上传 `assets/icon-market.jpg` 作为 Skill 的市场显示图标。
- 建议图标尺寸：512x512 像素。

### 3. 填写描述

- **简短描述**：
  > Minecraft 模组全生态智能适配工具，支持模组检索、环境搭建、Mixin冲突扫描、崩溃修复、汉化、移植评估等10大功能。

- **详细描述**：
  从 [release/clawhub_desc.md](file:///d:/Users/lele/Desktop/MC模组版本优化与拓展/mc-skill-v1/release/clawhub_desc.md) 复制完整内容。

### 4. 选择分类和标签

- **分类 (Category)**：选择 **“游戏” (Gaming)**。
- **标签 (Tags)**：`minecraft`, `modding`, `forge`, `fabric`, `neoforge`, `mixin`, `crash-fix`, `i18n`, `migration-assessment`。

### 5. 填写版本日志

- 从 [release/changelog_v1.md](file:///d:/Users/lele/Desktop/MC模组版本优化与拓展/mc-skill-v1/release/changelog_v1.md) 复制 V1.0.1 的内容。
- 这会告诉审核人员和用户本次更新了什么。

### 6. 设置权限

- **访问权限**：选择 **“公开” (Public)**。
- **许可协议**：选择 **MIT License**。

---

## ✅ 第四步：提交审核

1. **检查信息**：仔细核对以上所有信息，确保没有错误。
2. **点击“提交审核”**：点击 **“Submit for Review”** 按钮。
3. **等待审核**：
   - 审核周期通常为 **1-3 个工作日**。
   - 如果审核通过，你会收到一封恭喜邮件，你的 Skill 就正式上线了！
   - 如果被驳回，邮件中会告诉你具体原因，修改后可以重新提交。

---

## 🔄 第五步：未来更新 Skill

当你在后续版本（如 V1.0.2）中修复了 Bug 或增加了新功能时：

### 如果使用 GitHub 导入：
1. 在 GitHub 上更新代码。
2. 在 ClawHub 的“我的技能”页面，点击 **“同步”** 按钮即可。

### 如果使用文件夹上传：
1. 更新版本号：修改 `SKILL.md` 中的 `version` 字段。
2. 更新日志：在 `release/changelog_v1.md` 中添加新版本说明。
3. 重新运行 `build_skill_package.bat`。
4. 在 ClawHub 的“我的技能”页面，点击 **“发布新版本”**，上传新生成的文件夹。

---

**祝发布顺利！🎊**