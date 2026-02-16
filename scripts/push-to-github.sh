#!/bin/bash

# Yacht MES - GitHub 推送脚本
# 用户名: neglson

REPO_NAME="yacht-mes"
GITHUB_USER="neglson"

echo "========================================"
echo "  Yacht MES - GitHub 推送脚本"
echo "  用户: $GITHUB_USER"
echo "========================================"
echo ""

# 检查 git
check_git() {
    if ! command -v git &> /dev/null; then
        echo "❌ Git 未安装"
        echo "   安装: sudo apt-get install git"
        exit 1
    fi
    echo "✅ Git 已安装"
}

# 配置 git
check_git_config() {
    if [ -z "$(git config --global user.name)" ] || [ -z "$(git config --global user.email)" ]; then
        echo "⚠️  Git 未配置用户信息"
        echo ""
        echo "请运行以下命令配置:"
        echo "  git config --global user.name \"你的名字\""
        echo "  git config --global user.email \"你的邮箱@example.com\""
        echo ""
        exit 1
    fi
    echo "✅ Git 用户: $(git config --global user.name)"
}

# 初始化仓库
init_repo() {
    if [ ! -d ".git" ]; then
        echo "📦 初始化 Git 仓库..."
        git init
        git add .
        git commit -m "Initial commit: Yacht MES 游艇建造管理系统"
        echo "✅ 仓库初始化完成"
    else
        echo "✅ Git 仓库已存在"
    fi
}

# 添加远程仓库
add_remote() {
    echo ""
    echo "🔗 配置远程仓库..."
    
    # 删除旧远程（如果存在）
    git remote remove origin 2> /dev/null
    
    # 添加新远程
    git remote add origin "https://github.com/$GITHUB_USER/$REPO_NAME.git"
    echo "✅ 远程仓库: https://github.com/$GITHUB_USER/$REPO_NAME.git"
}

# 推送代码
push_code() {
    echo ""
    echo "📤 推送代码到 GitHub..."
    
    # 检查是否有更改
    if [ -n "$(git status --porcelain)" ]; then
        echo "📝 检测到未提交的更改..."
        git add .
        git commit -m "Update: $(date '+%Y-%m-%d %H:%M:%S')"
    fi
    
    # 推送
    if git push -u origin main 2>&1 || git push -u origin master 2>&1; then
        echo "✅ 代码推送成功！"
    else
        echo ""
        echo "❌ 推送失败"
        echo ""
        echo "可能原因:"
        echo "  1. 仓库不存在 - 需要先在 GitHub 创建"
        echo "  2. 未登录 - 需要配置 GitHub 认证"
        echo ""
        echo "解决方案:"
        echo "  1. 访问 https://github.com/new 创建仓库 '$REPO_NAME'"
        echo "  2. 或使用 GitHub CLI 登录: gh auth login"
        return 1
    fi
}

# 显示后续步骤
show_next_steps() {
    echo ""
    echo "========================================"
    echo "  🎉 完成！后续步骤"
    echo "========================================"
    echo ""
    echo "1. 访问 GitHub 仓库:"
    echo "   https://github.com/$GITHUB_USER/$REPO_NAME"
    echo ""
    echo "2. 部署到 Railway（推荐）:"
    echo "   a. 访问 https://railway.app"
    echo "   b. 用 GitHub 登录"
    echo "   c. 点击 'New Project' → 'Deploy from GitHub repo'"
    echo "   d. 选择 '$REPO_NAME'"
    echo "   e. 自动部署完成！"
    echo ""
    echo "3. 部署后访问地址:"
    echo "   https://backend-$REPO_NAME.up.railway.app"
    echo ""
    echo "========================================"
}

# 主流程
main() {
    cd "$(dirname "$0")/.."
    
    check_git
    check_git_config
    init_repo
    add_remote
    push_code && show_next_steps
}

main "$@"
