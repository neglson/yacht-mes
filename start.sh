#!/bin/bash

# Yacht MES 启动脚本
# 铝合金电动游艇建造管理系统

set -e

echo "========================================"
echo "  Yacht MES - 启动脚本"
echo "  铝合金电动游艇建造管理系统"
echo "========================================"
echo ""

# 检查 Docker
check_docker() {
    if ! command -v docker &> /dev/null; then
        echo "❌ Docker 未安装，请先安装 Docker"
        exit 1
    fi
    
    if ! command -v docker-compose &> /dev/null; then
        echo "❌ Docker Compose 未安装，请先安装 Docker Compose"
        exit 1
    fi
    
    echo "✅ Docker 环境检查通过"
}

# 创建必要目录
setup_directories() {
    echo "📁 创建必要目录..."
    mkdir -p uploads
    mkdir -p logs
    echo "✅ 目录创建完成"
}

# 启动服务
start_services() {
    echo ""
    echo "🚀 启动 Yacht MES 服务..."
    echo ""
    
    docker-compose up -d --build
    
    echo ""
    echo "⏳ 等待服务启动..."
    sleep 5
    
    # 检查服务状态
    echo ""
    echo "📊 服务状态："
    docker-compose ps
}

# 显示访问信息
show_info() {
    echo ""
    echo "========================================"
    echo "  ✅ Yacht MES 启动成功！"
    echo "========================================"
    echo ""
    echo "🌐 访问地址："
    echo "   Web 界面: http://localhost:8080"
    echo "   API 文档: http://localhost:8000/docs"
    echo "   MinIO 控制台: http://localhost:9001"
    echo ""
    echo "🔑 默认账号："
    echo "   用户名: admin"
    echo "   密码: admin"
    echo ""
    echo "📋 常用命令："
    echo "   查看日志: docker-compose logs -f"
    echo "   停止服务: docker-compose down"
    echo "   重启服务: docker-compose restart"
    echo ""
    echo "========================================"
}

# 主流程
main() {
    check_docker
    setup_directories
    start_services
    show_info
}

main "$@"
