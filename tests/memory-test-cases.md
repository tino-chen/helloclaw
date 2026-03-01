# HelloClaw 记忆系统测试用例

## 快速测试命令（复制粘贴即可）

### 1. 查看当前统计
```bash
curl -s http://localhost:8000/api/memory/stats | jq
```

### 2. 添加偏好类记忆
```bash
curl -s -X POST http://localhost:8000/api/memory/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "用户喜欢使用深色主题", "category": "preference"}' | jq
```

### 3. 添加决策类记忆
```bash
curl -s -X POST http://localhost:8000/api/memory/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "决定使用 glm-4.7-flash 作为默认模型", "category": "decision"}' | jq
```

### 4. 添加实体类记忆
```bash
curl -s -X POST http://localhost:8000/api/memory/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "用户的邮箱是 test@example.com", "category": "entity"}' | jq
```

### 5. 添加事实类记忆
```bash
curl -s -X POST http://localhost:8000/api/memory/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "项目部署在北京的服务器上", "category": "fact"}' | jq
```

### 6. 测试去重（应该返回 skipped）
```bash
curl -s -X POST http://localhost:8000/api/memory/capture \
  -H "Content-Type: application/json" \
  -d '{"content": "用户喜欢使用深色主题", "category": "preference"}' | jq
```

### 7. 列出所有记忆
```bash
curl -s http://localhost:8000/api/memory/list | jq
```

### 8. 按分类过滤（只看偏好）
```bash
curl -s "http://localhost:8000/api/memory/list?category=preference" | jq
```

### 9. 读取今日记忆
```bash
curl -s http://localhost:8000/api/memory/$(date +%Y-%m-%d)
```

### 10. 清理过期记忆（30天前的）
```bash
curl -s -X POST "http://localhost:8000/api/memory/cleanup?days=30" | jq
```

---

## 预期结果

| 测试 | 预期结果 |
|------|----------|
| 1. 统计 | 返回各分类数量 |
| 2-5. 添加 | `status: "ok"`, `message: "已添加 [category] 记忆"` |
| 6. 去重 | `status: "skipped"`, `message: "记忆已存在，跳过"` |
| 7. 列表 | 返回 `memories` 数组，包含今日记忆 |
| 8. 过滤 | 只返回包含 `[preference]` 标签的记忆 |
| 9. 读取 | 返回完整记忆文件内容 |
| 10. 清理 | `deleted: []`（今天的不被删除） |

---

## 分类说明

| 分类 | 标签 | 用途 | 触发关键词示例 |
|------|------|------|----------------|
| preference | `[preference]` | 用户偏好 | "我喜欢"、"我偏好"、"prefer" |
| decision | `[decision]` | 决策记录 | "决定了"、"用这个"、"选定" |
| entity | `[entity]` | 实体信息 | 电话、邮箱、地址、账号 |
| fact | `[fact]` | 事实信息 | "记住"、"事实上"、"实际上" |

---

## 自动运行所有测试

```bash
cd /Users/tino/Desktop/tasks/2026-02-24-hello-claw/helloclaw/tests
bash memory-api-test.sh
```
