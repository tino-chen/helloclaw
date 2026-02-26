# HelloClaw

> 基于 HelloAgents 框架的个性化 AI Agent 平台，复刻 OpenClaw 核心功能

## 截图

![HelloClaw Screenshot](docs/image/helloclaw.png)

## 简介

HelloClaw 是一个基于 HelloAgents 框架的 AI Agent 平台，通过 Markdown 配置文件定义 Agent 的"个性"，结合工具系统和记忆管理，实现个性化 AI 助手。

### 核心特性

- 🎭 **可定制的 Agent 身份** - 通过 Markdown 配置文件定义 Agent 的身份、性格和行为规则
- 🧠 **多层次记忆系统** - 支持会话记忆、每日记忆、长期记忆，具备自动捕获、分类、去重、清理功能
- 🛠️ **丰富的工具系统** - 内置文件操作、计算器等工具，支持扩展
- 🔌 **多渠道支持** - Web UI 和 CLI 双渠道交互
- 🤖 **子 Agent 支持** - 支持创建子 Agent 处理复杂任务，实现上下文隔离
- ⚡ **配置热加载** - 修改配置后无需重启，下次对话自动生效

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python 3.10+ + uv + FastAPI + HelloAgents |
| 前端 | Vue 3 + TypeScript + Vite + Ant Design Vue |
| LLM | 支持所有 OpenAI 兼容接口（GLM、DeepSeek、Qwen 等） |

## 快速开始

### 环境要求

- Python 3.10+
- Node.js 18+
- pnpm 8+

### 后端启动

```bash
cd backend

# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env 填入你的 API Key

# 启动服务
uv run uvicorn main:app --reload --port 8000
```

### 前端启动

```bash
cd frontend

# 安装依赖
pnpm install

# 启动开发服务器
pnpm dev
```

访问 http://localhost:5173 即可使用。

## 项目结构

```
helloclaw/
├── backend/                 # 后端 Python 项目
│   ├── agent/               # Agent 核心
│   │   └── helloclaw_agent.py   # HelloClawAgent 实现
│   ├── tools/               # 工具系统
│   │   └── builtin/         # 内置工具
│   │       ├── memory.py    # 记忆工具
│   │       ├── identity.py  # 身份工具
│   │       └── ...
│   ├── memory/              # 记忆管理
│   │   ├── capture.py       # 自动捕获管理器
│   │   ├── session_summarizer.py  # 会话总结
│   │   └── memory_flush.py  # 记忆刷新
│   ├── workspace/           # 工作空间管理
│   │   ├── manager.py       # WorkspaceManager
│   │   └── templates/       # 配置文件模板
│   └── api/                 # FastAPI 路由
│       ├── chat.py          # 聊天接口
│       ├── config.py        # 配置管理
│       ├── memory.py        # 记忆接口
│       └── session.py       # 会话管理
│
├── frontend/                # 前端 Vue 项目
│   ├── src/views/           # 页面
│   │   ├── ChatView.vue     # 聊天界面
│   │   ├── ConfigView.vue   # 配置管理
│   │   └── MemoryView.vue   # 记忆查看
│   ├── src/components/      # 组件
│   └── src/stores/          # 状态管理
│
└── ~/.helloclaw/            # HelloClaw 工作空间
    ├── config.json          # 全局配置（LLM 设置等）
    └── workspace/           # Agent 配置文件
        ├── IDENTITY.md      # 身份定义
        ├── SOUL.md          # 人格模板
        ├── USER.md          # 用户信息
        ├── MEMORY.md        # 长期记忆
        └── memory/          # 每日记忆
            └── YYYY-MM-DD.md
```

## 配置文件

HelloClaw 使用 Markdown 文件配置 Agent，遵循 OpenClaw 的设计理念：**"文件 > 大脑"**

| 文件 | 用途 |
|------|------|
| BOOTSTRAP.md | 首次运行引导（完成后自动删除） |
| IDENTITY.md | Agent 身份定义（名字、角色、头像） |
| SOUL.md | Agent 人格模板（性格、边界、风格） |
| USER.md | 用户信息（名字、时区、偏好） |
| MEMORY.md | 长期记忆（重要信息固化） |
| AGENTS.md | 工作空间规则（每次会话自动加载） |
| HEARTBEAT.md | 定时任务检查清单 |

## 记忆系统

### 多层次记忆架构

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

### 记忆分类

每条记忆自动分类并打上标签：

| 分类 | 标签 | 示例 |
|------|------|------|
| 偏好 | `[preference]` | 用户喜欢简洁的回复风格 |
| 决策 | `[decision]` | 决定使用 Vue 3 + TypeScript |
| 实体 | `[entity]` | 用户的 GitHub 账号是 tino-chen |
| 事实 | `[fact]` | 项目位于 /Users/tino/Desktop/tasks |

### 自动捕获

对话结束后，系统自动识别值得记忆的信息：

- **触发规则**：检测"记住"、"我喜欢"、"决定了"等关键词
- **智能去重**：关键词重叠 > 70% 视为重复，不重复存储
- **自动分类**：根据内容自动判断分类

### 记忆工具

Agent 可使用以下记忆工具：

| 工具 | 功能 |
|------|------|
| `memory_add` | 添加新记忆（支持分类） |
| `memory_search` | 搜索记忆（返回行号和上下文） |
| `memory_get` | 读取指定记忆文件 |
| `memory_list` | 列出所有记忆文件 |
| `memory_update_longterm` | 固化到长期记忆 |
| `memory_cleanup` | 清理过期记忆 |

## API 文档

### 聊天

```
POST /api/chat/send
Body: { "session_id": "xxx", "message": "你好" }
Response: SSE 流式输出
```

### 会话管理

```
GET    /api/session/list           # 列出所有会话
POST   /api/session/create         # 创建新会话
GET    /api/session/{id}           # 获取会话详情
DELETE /api/session/{id}           # 删除会话
```

### 配置管理

```
GET    /api/config/list            # 列出所有配置文件
GET    /api/config/{name}          # 读取配置文件
PUT    /api/config/{name}          # 更新配置文件
```

### 记忆管理

```
GET    /api/memory/list            # 列出记忆文件
GET    /api/memory/{filename}      # 读取记忆文件
GET    /api/memory/search?q=xxx    # 搜索记忆
GET    /api/memory/stats           # 记忆统计
POST   /api/memory/capture         # 手动添加记忆
POST   /api/memory/cleanup         # 清理过期记忆
```

## 里程碑

| 里程碑 | 功能 | 状态 |
|--------|------|------|
| M1 | 项目骨架 | ✅ 已完成 |
| M2 | Agent 配置系统 | ✅ 已完成 |
| M3 | 记忆系统 | ✅ 已完成 |
| M4 | 工具系统 | 🚧 进行中 |
| M5 | 子 Agent 系统 | ⏳ 待开始 |
| M6 | Web 渠道 | ⏳ 待开始 |
| M7 | CLI 渠道 | ⏳ 待开始 |
| M8 | 完善 | ⏳ 待开始 |

## 开发路线

- [x] 项目骨架（FastAPI + Vue 3）
- [x] 配置文件系统（Markdown 模板）
- [x] LLM 配置热加载
- [x] 多层次记忆系统
- [x] 记忆自动捕获与分类
- [ ] 命令执行工具（安全控制）
- [ ] Web 搜索工具
- [ ] 子 Agent 任务委托
- [ ] CLI 交互模式
- [ ] 前端记忆分类过滤

## 致谢

- [HelloAgents](https://github.com/helloagents/helloagents) - Agent 框架基础
- [OpenClaw](https://github.com/openclaw/openclaw) - 设计理念和灵感来源

## License

[MIT](LICENSE)
