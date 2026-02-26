# HelloClaw 记忆系统

## 设计理念

遵循 OpenClaw 的设计哲学：**"文件 > 大脑"**

让 Agent 主动管理记忆，而非依赖复杂的后台系统。

## 架构

```
┌─────────────────────────────────────────────┐
│              MEMORY.md (长期记忆)            │
│         重要信息固化，永久保存                │
├─────────────────────────────────────────────┤
│         memory/YYYY-MM-DD.md (每日记忆)      │
│         日常对话记录，30天后可清理            │
├─────────────────────────────────────────────┤
│         memory/YYYY-MM-DD-slug.md (会话总结) │
│         会话摘要，90天后可清理               │
└─────────────────────────────────────────────┘
```

## 自动捕获

### 触发规则

```python
MEMORY_TRIGGERS = [
    (r"记住|记下|remember", "fact"),
    (r"我喜欢|我偏好|prefer|like|hate", "preference"),
    (r"决定了|decision|用这个|选定", "decision"),
    (r"\+\d{10,}|[\w.-]+@[\w.-]+\.\w+", "entity"),
    (r"我的\w+是|is my", "entity"),
]
```

### 分类说明

| 分类 | 标签 | 用途 | 示例 |
|------|------|------|------|
| preference | `[preference]` | 用户偏好 | 用户喜欢简洁的回复风格 |
| decision | `[decision]` | 决策记录 | 决定使用 Vue 3 作为前端框架 |
| entity | `[entity]` | 实体信息 | 用户的邮箱是 test@example.com |
| fact | `[fact]` | 事实信息 | 项目部署在北京的服务器上 |

## 去重机制

使用关键词重叠检测：

1. 提取内容关键词（过滤停用词）
2. 检查今日记忆、长期记忆、最近 2 天记忆
3. 重叠度 ≥ 70% 视为重复，跳过存储

## 记忆工具

### memory_search

搜索记忆，返回带行号的上下文。

```
参数:
  keyword: 搜索关键词
  context_lines: 上下文行数（默认 3）
```

### memory_get

读取指定记忆文件。

```
参数:
  filename: 文件名（默认今天）
  start_line: 起始行号
  end_line: 结束行号
  lines: 行范围字符串（如 "10-20"）
```

### memory_add

添加记忆到今日文件。

```
参数:
  content: 记忆内容
  category: 分类标签（可选）
```

### memory_list

列出所有记忆文件。

### memory_cleanup

清理过期记忆。

```
参数:
  days: 保留天数（默认 30）
```

## API 端点

| 方法 | 路径 | 功能 |
|------|------|------|
| GET | /api/memory/list | 列出记忆（支持分类过滤） |
| GET | /api/memory/stats | 记忆统计 |
| GET | /api/memory/{filename} | 读取指定记忆 |
| POST | /api/memory/capture | 手动添加记忆 |
| POST | /api/memory/cleanup | 清理过期记忆 |

## AGENTS.md 引导

Agent 在每次会话开始时会自动读取 AGENTS.md，其中包含记忆读取指引：

```markdown
## 每次会话开始前

1. 使用 memory_get 读取今天的每日记忆
2. 使用 memory_get 读取昨天的每日记忆
3. 如果用户提问涉及特定主题，使用 memory_search 搜索相关记忆
```

## 记忆文件示例

### 每日记忆 (2026-02-27.md)

```markdown
# 2026-02-27

## 10:30 - 自动捕获

- [preference] 用户喜欢简洁的回复风格

## 14:00 - 对话记录

- [decision] 决定使用 Vue 3 + TypeScript 作为前端技术栈

## 16:30 - 实体信息

- [entity] 用户的 GitHub 账号是 tino-chen
```

### 长期记忆 (MEMORY.md)

```markdown
# 长期记忆

## 用户偏好

- 用户喜欢简洁的回复风格
- 用户使用 macOS 系统

## 项目信息

- HelloClaw 项目位于 /Users/tino/Desktop/tasks/2026-02-24-hello-claw

## 重要实体

- GitHub: tino-chen
- Email: tino.ai.chen@gmail.com
```
