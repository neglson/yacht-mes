#!/bin/bash

# Yacht MES 部署验证脚本

echo "========================================"
echo "  Yacht MES 部署验证"
echo "========================================"
echo ""

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查 Docker
check_docker() {
    echo "🔍 检查 Docker..."
    if command -v docker &> /dev/null; then
        echo -e "${GREEN}✓ Docker 已安装${NC}"
        docker --version
    else
        echo -e "${RED}✗ Docker 未安装${NC}"
        return 1
    fi
    
    if command -v docker-compose &> /dev/null; then
        echo -e "${GREEN}✓ Docker Compose 已安装${NC}"
        docker-compose --version
    else
        echo -e "${RED}✗ Docker Compose 未安装${NC}"
        return 1
    fi
    echo ""
}

# 检查端口
check_ports() {
    echo "🔍 检查端口占用..."
    ports=(5432 6379 8000 8080 9000 9001)
    
    for port in "${ports[@]}"; do
        if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
            echo -e "${YELLOW}⚠ 端口 $port 已被占用${NC}"
        else
            echo -e "${GREEN}✓ 端口 $port 可用${NC}"
        fi
    done
    echo ""
}

# 检查文件结构
check_files() {
    echo "🔍 检查项目文件..."
    
    required_files=(
        "docker-compose.yml"
        "backend/app/main.py"
        "frontend/package.json"
        "database/schema.sql"
        "start.sh"
    )
    
    for file in "${required_files[@]}"; do
        if [ -f "$file" ]; then
            echo -e "${GREEN}✓ $file${NC}"
        else
            echo -e "${RED}✗ $file 缺失${NC}"
        fi
    done
    echo ""
}

# 检查服务状态
check_services() {
    echo "🔍 检查服务状态..."
    
    if docker-compose ps &> /dev/null; then
        services=$(docker-compose ps --services)
        if [ -n "$services" ]; then
            echo -e "${GREEN}✓ 服务正在运行${NC}"
            docker-compose ps
        else
            echo -e "${YELLOW}⚠ 服务未启动${NC}"
        fi
    else
        echo -e "${YELLOW}⚠ 无法检查服务状态${NC}"
    fi
    echo ""
}

# 测试 API
test_api() {
    echo "🔍 测试 API..."
    
    # 健康检查
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health 2>/dev/null)
    if [ "$response" = "200" ]; then
        echo -e "${GREEN}✓ API 健康检查通过${NC}"
    else
        echo -e "${RED}✗ API 健康检查失败 (HTTP $response)${NC}"
    fi
    
    # 测试登录
    login_response=$(curl -s -X POST \
        -H "Content-Type: application/x-www-form-urlencoded" \
        -d "username=admin&password=admin" \
        http://localhost:8000/api/auth/login 2>/dev/null)
    
    if echo "$login_response" | grep -q "access_token"; then
        echo -e "${GREEN}✓ API 登录测试通过${NC}"
    else
        echo -e "${RED}✗ API 登录测试失败${NC}"
    fi
    echo ""
}

# 测试前端
test_frontend() {
    echo "🔍 测试前端..."
    
    response=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8080 2>/dev/null)
    if [ "$response" = "200" ] || [ "$response" = "304" ]; then
        echo -e "${GREEN}✓ 前端可访问${NC}"
    else
        echo -e "${RED}✗ 前端访问失败 (HTTP $response)${NC}"
    fi
    echo ""
}

# 测试数据库
test_database() {
    echo "🔍 测试数据库..."
    
    if docker-compose exec -T postgres pg_isready -U yacht_mes &> /dev/null; then
        echo -e "${GREEN}✓ 数据库连接正常${NC}"
    else
        echo -e "${RED}✗ 数据库连接失败${NC}"
    fi
    echo ""
}

# 测试 Redis
test_redis() {
    echo "🔍 测试 Redis..."
    
    if docker-compose exec -T redis redis-cli ping | grep -q "PONG"; then
        echo -e "${GREEN}✓ Redis 连接正常${NC}"
    else
        echo -e "${RED}✗ Redis 连接失败${NC}"
    fi
    echo ""
}

# 显示访问信息
show_access_info() {
    echo "========================================"
    echo "  访问信息"
    echo "========================================"
    echo ""
    echo "🌐 Web 界面: http://localhost:8080"
    echo "📚 API 文档: http://localhost:8000/docs"
    echo "🔧 API 健康: http://localhost:8000/health"
    echo "📦 MinIO: http://localhost:9001"
    echo ""
    echo "🔑 默认账号:"
    echo "   用户名: admin"
    echo "   密码: admin"
    echo ""
}

# 主函数
main() {
    check_docker
    check_ports
    check_files
    check_services
    test_api
    test_frontend
    test_database
    test_redis
    show_access_info
    
    echo "========================================"
    echo "  验证完成"
    echo "========================================"
}

main "$@"
