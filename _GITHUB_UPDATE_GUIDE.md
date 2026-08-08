# MC Skill V1.0.1 - GitHub 自动化更新流程

## 概述

本文档提供 MC Ecosystem Adapt Engine V1.0.1 版本更新到 GitHub 仓库的 **自动化操作流程**，无需手动逐步操作。

---

## 前置条件

1. ✅ Git 已安装 ([下载地址](https://git-scm.com/download/win))
2. ✅ 本地仓库已配置远程 origin
3. ✅ 有 GitHub 仓库的推送权限
4. ✅ 网络可访问 GitHub

### 检查环境

```bash
# 检查 Git 是否可用
git --version

# 检查远程仓库配置
cd "d:\Users\lele\Desktop\MC模组版本优化与拓展\mc-skill-v1"
git remote -v
# 预期输出: https://github.com/Liang030214/mc-skill-v1.git
```

---

## 流程一：一键推送脚本（推荐）

### 使用 `_git_push_v101.bat`

**位置**: `mc-skill-v1\_git_push_v101.bat`

**执行步骤**:
1. 双击运行 `_git_push_v101.bat`
2. 脚本自动执行以下 8 个步骤：

```
[1/8] 检查 Git 环境
[2/8] 检查远程仓库配置
[3/8] 显示当前变更摘要
[4/8] 暂存所有变更 (git add -A)
[5/8] 提交变更 (git commit -m "release: MC Skill V1.0.1 ...")
[6/8] 创建版本标签 v1.0.1
[7/8] 推送到 GitHub (git push origin main + git push origin v1.0.1)
[8/8] 验证推送结果
```

3. 脚本完成后会自动打开 GitHub Release 页面

---

## 流程二：发布包生成脚本

### 使用 `_build_release_package.bat`

**位置**: `mc-skill-v1\_build_release_package.bat`

**用途**: 生成可上传到 GitHub Release 的 ZIP 发布包

**执行步骤**:
1. 双击运行 `_build_release_package.bat`
2. 脚本自动：
   - 清理旧发布包
   - 复制核心文件到临时目录
   - 生成 `version.json` 版本信息
   - 压缩为 `release\mc-skill-v1.0.1.zip`
3. 输出发布包路径并打开文件位置

---

## 流程三：GitHub Release 创建（可选）

推送完成后，创建正式 Release：

### 方式 A：通过浏览器（脚本已自动打开）

1. 访问: `https://github.com/Liang030214/mc-skill-v1/releases/new?tag=v1.0.1`
2. **Tag version**: 选择 `v1.0.1`
3. **Release title**: `MC Ecosystem Adapt Engine V1.0.1`
4. **Description**:

```markdown
## 🎮 MC 全生态智能适配工程师 V1.0.1

### 版本亮点
- 🔍 **模组检索增强**: 新增16个模组分类索引，支持分类搜索和批量搜索
- 📚 **兼容规则库扩充**: 覆盖机械动力、乐事、科技能源、红石魔改等65+模组
- 🌐 **国际化支持**: 新增11种语言框架
- 🔐 **权限声明完善**: 新增SKILL.json元数据文件，完整声明功能与权限
- 🐛 **Bug修复**: 修复F2/F3/F5/F8.1等多处已知问题

### 系统要求
- Java 17+
- Python 3.8+
- Windows / macOS / Linux

### 支持的加载器
- NeoForge
- Forge
- Fabric
- Quilt

### 支持的MC版本
- 1.20.1 - 1.21.1

### 安装说明
1. 解压 ZIP 到任意目录
2. 运行 `start.bat` 启动
3. 或通过命令行: `python main.py --help`
```

5. 上传 `mc-skill-v1.0.1.zip` 二进制文件
6. 点击 **"Publish release"**

### 方式 B：通过 Git 命令（可选）

```bash
# 创建 Release（需要 GitHub CLI）
gh release create v1.0.1 ^
  --title "MC Ecosystem Adapt Engine V1.0.1" ^
  --notes "模组检索增强、兼容规则库扩充、国际化支持、权限声明完善" ^
  release/mc-skill-v1.0.1.zip
```

---

## 流程四：命令行手动操作（备选）

如果脚本无法使用，可手动执行以下命令：

### 步骤 1: 提交所有变更

```bash
cd "d:\Users\lele\Desktop\MC模组版本优化与拓展\mc-skill-v1"

# 查看变更
git status

# 添加所有文件
git add -A

# 提交
git commit -m "release: MC Skill V1.0.1 - 模组检索增强与兼容规则库扩充"
```

### 步骤 2: 创建版本标签

```bash
# 创建带注释的标签
git tag -a v1.0.1 -m "MC Ecosystem Adapt Engine V1.0.1"

# 验证标签
git tag -l
```

### 步骤 3: 推送到远程

```bash
# 推送主分支
git push origin main

# 推送标签
git push origin v1.0.1

# 如果标签已存在，强制推送
git push -f origin v1.0.1
```

### 步骤 4: 验证推送

```bash
# 查看远程状态
git log --oneline -5

# 查看标签
git tag -l
```

---

## 常见问题解决

### Q1: 推送认证失败

```bash
# 配置 Git 凭据管理器
git config --global credential.helper manager

# 或使用 Personal Access Token
git remote set-url origin https://<your-token>@github.com/Liang030214/mc-skill-v1.git
```

### Q2: 远程分支冲突

```bash
# 拉取远程更新
git pull origin main --rebase

# 解决冲突后重新推送
git push origin main
```

### Q3: 标签已存在

```bash
# 删除本地标签
git tag -d v1.0.1

# 删除远程标签
git push origin :refs/tags/v1.0.1

# 重新创建并推送
git tag -a v1.0.1 -m "MC Ecosystem Adapt Engine V1.0.1"
git push origin v1.0.1
```

### Q4: 大文件推送失败

```bash
# 检查 .gitignore 是否排除大文件
# 或使用 Git LFS
git lfs install
git lfs track "*.zip"
git add .gitattributes
```

---

## 文件清单

| 文件 | 用途 |
|------|------|
| `_git_push_v101.bat` | 一键推送脚本（提交+标签+推送） |
| `_build_release_package.bat` | 发布包生成脚本（ZIP打包） |
| `_GITHUB_UPDATE_GUIDE.md` | 本流程文档 |

---

## 快速执行顺序

```
1. 双击运行 _build_release_package.bat → 生成 ZIP
2. 双击运行 _git_push_v101.bat → 推送到 GitHub
3. 在浏览器中完成 Release 创建
4. 验证: https://github.com/Liang030214/mc-skill-v1/releases
```

---

## 版本历史

- **V1.0.1** (2026-08-08): 模组检索增强、兼容规则库扩充、国际化支持、权限声明完善
- **V1.0.0** (初始版本): 10个核心功能发布
