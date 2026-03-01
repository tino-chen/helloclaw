#!/bin/bash
# HelloClaw 记忆系统 API 测试用例
# 使用方法: source memory-api-test.sh 或直接复制命令执行

BASE_URL="http://localhost:8000/api/memory"

echo "=========================================="
echo "HelloClaw 记忆系统 API 测试"
echo "=========================================="

# ==================== 测试 1: 查看统计 ====================
echo -e "\n📊 测试 1: 查看记忆统计"
echo "命令: curl -s $BASE_URL/stats | jq"
curl -s $BASE_URL/stats | jq

# ==================== 测试 2: 添加偏好类记忆 ====================
echo -e "\n🎭 测试 2: 添加偏好类记忆 (preference)"
echo '命令: curl -s -X POST $BASE_URL/capture -H "Content-Type: application/json" -d '\''{"content": "用户喜欢使用深色主题", "category": "preference"}'\'''
curl -s -X POST $BASE_URL/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "用户喜欢使用深色主题", "category": "preference"}' | jq

# ==================== 测试 3: 添加决策类记忆 ====================
echo -e "\n🎯 测试 3: 添加决策类记忆 (decision)"
echo '命令: curl -s -X POST $BASE_URL/capture -H "Content-Type: application/json" -d '\''{"content": "决定使用 glm-4.7-flash 作为默认模型", "category": "decision"}'\'''
curl -s -X POST $BASE_URL/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "决定使用 glm-4.7-flash 作为默认模型", "category": "decision"}' | jq

# ==================== 测试 4: 添加实体类记忆 ====================
echo -e "\n👤 测试 4: 添加实体类记忆 (entity)"
echo '命令: curl -s -X POST $BASE_URL/capture -H "Content-Type: application/json" -d '\''{"content": "用户的邮箱是 test@example.com", "category": "entity"}'\'''
curl -s -X POST $BASE_URL/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "用户的邮箱是 test@example.com", "category": "entity"}' | jq

# ==================== 测试 5: 添加事实类记忆 ====================
echo -e "\n📝 测试 5: 添加事实类记忆 (fact)"
echo '命令: curl -s -X POST $BASE_URL/capture -H "Content-Type: application/json" -d '\''{"content": "项目部署在北京的服务器上", "category": "fact"}'\'''
curl -s -X POST $BASE_URL/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "项目部署在北京的服务器上", "category": "fact"}' | jq

# ==================== 测试 6: 去重测试 ====================
echo -e "\n🔄 测试 6: 去重测试 - 尝试添加重复内容"
echo '命令: curl -s -X POST $BASE_URL/capture -H "Content-Type: application/json" -d '\''{"content": "用户喜欢使用深色主题", "category": "preference"}'\'''
curl -s -X POST $BASE_URL/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "用户喜欢使用深色主题", "category": "preference"}' | jq
echo "↑ 应该返回 status: \"skipped\""

# ==================== 测试 7: 查看更新后的统计 ====================
echo -e "\n📊 测试 7: 查看更新后的统计"
echo "命令: curl -s $BASE_URL/stats | jq"
curl -s $BASE_URL/stats | jq

# ==================== 测试 8: 列出所有记忆 ====================
echo -e "\n📋 测试 8: 列出所有记忆"
echo "命令: curl -s $BASE_URL/list | jq"
curl -s $BASE_URL/list | jq

# ==================== 测试 9: 按分类过滤 ====================
echo -e "\n🔍 测试 9: 只列出偏好类记忆"
echo "命令: curl -s \"$BASE_URL/list?category=preference\" | jq"
curl -s "$BASE_URL/list?category=preference" | jq

# ==================== 测试 10: 读取今日记忆 ====================
echo -e "\n📖 测试 10: 读取今日记忆文件"
TODAY=$(date +%Y-%m-%d)
echo "命令: curl -s $BASE_URL/$TODAY"
curl -s $BASE_URL/$TODAY

# ==================== 测试 11: 清理测试（不会真的删除）====================
echo -e "\n🧹 测试 11: 清理过期记忆（保留 30 天，不会删除今天的）"
echo "命令: curl -s -X POST \"$BASE_URL/cleanup?days=30\" | jq"
curl -s -X POST "$BASE_URL/cleanup?days=30" | jq

echo -e "\n=========================================="
echo "测试完成！"
echo "=========================================="
