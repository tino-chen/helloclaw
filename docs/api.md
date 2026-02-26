# HelloClaw API 文档

Base URL: `http://localhost:8000/api`

## 聊天

### POST /chat/send

发送消息，SSE 流式返回。

**Request:**
```json
{
  "session_id": "xxx",
  "message": "你好"
}
```

**Response:** SSE 流

## 会话管理

### GET /session/list

列出所有会话。

**Response:**
```json
{
  "sessions": [
    {
      "id": "xxx",
      "created_at": "2026-02-27T10:00:00",
      "message_count": 10
    }
  ]
}
```

### POST /session/create

创建新会话。

**Request:**
```json
{
  "summarize_old": true
}
```

### GET /session/{id}

获取会话详情。

### DELETE /session/{id}

删除会话。

## 配置管理

### GET /config/list

列出所有配置文件。

**Response:**
```json
{
  "configs": ["IDENTITY", "USER", "MEMORY", "AGENTS"]
}
```

### GET /config/{name}

读取配置文件内容。

### PUT /config/{name}

更新配置文件。

**Request:**
```json
{
  "content": "# IDENTITY\n..."
}
```

## 记忆管理

### GET /memory/list

列出记忆文件。

**Query:**
- `category`: 按分类过滤（preference/decision/entity/fact）

**Response:**
```json
{
  "memories": [
    {
      "date": "2026-02-27",
      "filename": "2026-02-27.md",
      "preview": "- [preference] 用户喜欢...",
      "category": null
    }
  ],
  "total": 1
}
```

### GET /memory/stats

获取记忆统计。

**Response:**
```json
{
  "total_files": 5,
  "daily_files": 4,
  "total_size": 2048,
  "categories": {
    "preference": 3,
    "decision": 2,
    "entity": 1,
    "fact": 0
  }
}
```

### GET /memory/{filename}

读取指定记忆文件。

**Response:**
```json
{
  "filename": "2026-02-27.md",
  "date": "2026-02-27",
  "content": "# 2026-02-27\n..."
}
```

### POST /memory/capture

手动添加记忆。

**Request:**
```json
{
  "content": "用户喜欢深色主题",
  "category": "preference"
}
```

**Response:**
```json
{
  "status": "ok",
  "message": "已添加 [preference] 记忆",
  "category": "preference"
}
```

### POST /memory/cleanup

清理过期记忆。

**Query:**
- `days`: 保留天数（默认 30）

**Response:**
```json
{
  "status": "ok",
  "deleted": ["2026-01-15.md"],
  "message": "已清理 1 个过期记忆文件"
}
```

## 健康检查

### GET /health

**Response:**
```json
{
  "status": "ok",
  "service": "helloclaw-backend"
}
```
