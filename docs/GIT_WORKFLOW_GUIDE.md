# Git 工作流程指南

## 🚀 项目Git工作流程概述

本项目使用标准的 **Fork + Pull Request** 工作流程，确保代码质量和协作效率。

### 📋 远程仓库配置

```bash
# 查看当前远程仓库配置
git remote -v

# 应该看到：
# origin    git@github.com:your-username/deer-flow.git (fetch)
# origin    git@github.com:your-username/deer-flow.git (push)  
# upstream  git@github.com:bytedance/deer-flow.git (fetch)
# upstream  git@github.com:bytedance/deer-flow.git (push)
```

### 🔧 初始设置

如果还没有配置远程仓库，执行以下命令：

```bash
# 1. Fork 原仓库到你的GitHub账户
# 2. 添加upstream远程仓库
git remote add upstream git@github.com:bytedance/deer-flow.git

# 3. 设置origin为你的fork
git remote set-url origin git@github.com:your-username/deer-flow.git
```

## 🌟 功能分支同步Main分支流程

### ⭐ 方法1: 使用Rebase（推荐）

**完整流程：**

```bash
# 1️⃣ 获取上游最新代码
git fetch upstream

# 2️⃣ 切换到main分支并更新
git checkout main
git merge upstream/main

# 3️⃣ 推送更新后的main到你的fork
git push origin main

# 4️⃣ 回到功能分支
git checkout feature/your-feature

# 5️⃣ 使用rebase同步main的更改
git rebase main

# 6️⃣ 推送更新后的功能分支（需要强制推送）
git push origin feature/your-feature -f
```

### 🔄 方法2: 使用Merge

```bash
# 前面步骤相同
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# 不同之处：使用merge而不是rebase
git checkout feature/your-feature
git merge main

# 正常推送（不需要强制推送）
git push origin feature/your-feature
```

### 📊 两种方法对比

| 特性 | Rebase | Merge |
|------|--------|-------|
| 提交历史 | 线性、干净 | 包含合并提交 |
| 强制推送 | 需要 `-f` | 不需要 |
| 冲突解决 | 逐个提交解决 | 一次性解决 |
| 推荐场景 | 功能分支同步 | 紧急修复 |

## 🎯 标准开发工作流程

### 1. 开始新功能开发

```bash
# 确保main分支是最新的
git checkout main
git fetch upstream
git merge upstream/main
git push origin main

# 创建新功能分支
git checkout -b feature/new-feature-name

# 开始开发...
```

### 2. 提交代码

```bash
# 添加修改
git add .

# 提交修改（使用规范的提交信息）
git commit -m "feat: 添加新功能描述"

# 推送到你的fork
git push origin feature/new-feature-name
```

### 3. 定期同步（避免冲突）

```bash
# 每周或主要更新时同步
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

git checkout feature/your-feature
git rebase main
git push origin feature/your-feature -f
```

### 4. 准备Pull Request

```bash
# 最终同步确保没有冲突
git fetch upstream
git checkout main
git merge upstream/main
git checkout feature/your-feature
git rebase main

# 推送最终版本
git push origin feature/your-feature -f

# 在GitHub上创建Pull Request
```

## 🚨 冲突处理

### Rebase过程中的冲突

```bash
# 当rebase出现冲突时：
# 1. 手动解决冲突文件
# 2. 添加解决后的文件
git add .

# 3. 继续rebase
git rebase --continue

# 如果想放弃rebase：
git rebase --abort
```

### Merge冲突

```bash
# 解决冲突后
git add .
git commit -m "resolve merge conflicts"
```

## 📝 提交信息规范

使用以下前缀：
- `feat:` 新功能
- `fix:` 修复bug
- `docs:` 文档更新
- `style:` 代码格式调整
- `refactor:` 重构
- `test:` 测试相关
- `chore:` 构建/工具相关

## ⚠️ 重要注意事项

### 1. 分支保护规则
- ❌ **绝不在功能分支上执行** `git merge upstream/main`
- ✅ **始终在main分支上合并upstream**
- ✅ **功能分支使用rebase同步main**

### 2. 强制推送注意事项
- ⚠️ 使用 `git push -f` 前确保没有其他人在同一分支工作
- ✅ 个人功能分支可以安全使用强制推送
- ❌ 不要对共享分支使用强制推送

### 3. 同步时机
- **开发新功能前** - 确保基于最新代码
- **长期开发中** - 定期保持同步（建议每周）
- **提交PR前** - 确保没有冲突
- **main分支有重要更新时** - 及时同步

## 🔍 常用命令速查

```bash
# 查看分支状态
git status
git branch
git branch -a

# 查看提交历史
git log --oneline -10
git log --graph --oneline

# 查看远程仓库
git remote -v

# 查看分支差异
git diff main...feature/your-feature

# 撤销操作
git reset --hard HEAD~1  # 撤销最后一次提交
git checkout .           # 撤销工作区修改
```

## 🎯 最佳实践

1. **小步快走** - 频繁提交小的更改
2. **定期同步** - 避免长期分支分叉
3. **清晰提交信息** - 便于代码审查和历史追踪
4. **测试后提交** - 确保代码质量
5. **及时清理** - 合并后删除功能分支

## 🆘 常见问题解决

### Q: 推送时提示"Permission denied"？
A: 检查SSH key配置或使用HTTPS认证

### Q: Rebase时出现大量冲突？
A: 考虑使用merge，或者小批量同步

### Q: 误操作如何恢复？
A: 使用 `git reflog` 查看操作历史，然后 `git reset` 恢复

### Q: 如何删除已合并的分支？
```bash
# 删除本地分支
git branch -d feature/merged-feature

# 删除远程分支
git push origin --delete feature/merged-feature
```

---

**记住：保持简单，保持同步，保持沟通！** 🚀 