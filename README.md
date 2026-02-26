# HelloClaw

> Hello-Agents 框架的毕业设计项目，复刻 OpenClaw 核心功能

## 简介

HelloClaw 是一个基于 HelloAgents 框架的 AI Agent 平台，通过 Markdown 配置文件定义 Agent 的"个性"，结合工具系统和记忆管理，实现个性化 AI 助手。

### 核心特性

- 🎭 **可定制的 Agent 身份** - 通过 Markdown 配置文件定义 Agent 的身份、性格和行为规则
- 🧠 **多层次记忆系统** - 支持会话记忆、每日记忆、长期记忆和上下文压缩
- 🛠️ **丰富的工具系统** - 内置文件操作、网络搜索、命令执行等工具
- 🔌 **多渠道支持** - Web UI 和 CLI 双渠道交互
- 🤖 **子 Agent 支持** - 支持创建子 Agent 处理复杂任务，实现上下文隔离

## 技术栈

| 层级 | 技术 |
|------|------|
| 后端 | Python + uv + FastAPI + HelloAgents |
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
│   ├── tools/               # 工具系统
│   ├── channels/            # 通讯渠道
│   ├── workspace/           # 工作空间管理
│   └── api/                 # FastAPI 路由
│
├── frontend/                # 前端 Vue 项目
│   ├── src/views/           # 页面
│   ├── src/components/      # 组件
│   └── src/stores/          # 状态管理
│
└── ~/.helloclaw/            # HelloClaw 工作空间
    ├── config.json          # 全局配置
    └── workspace/           # Agent 配置文件
        ├── IDENTITY.md      # 身份定义
        ├── SOUL.md          # 人格模板
        ├── USER.md          # 用户信息
        ├── MEMORY.md        # 长期记忆
        └── memory/          # 每日记忆
```

## 配置文件

HelloClaw 使用 Markdown 文件配置 Agent：

| 文件 | 用途 |
|------|------|
| BOOTSTRAP.md | 首次运行引导（完成后自动删除） |
| IDENTITY.md | Agent 身份定义 |
| SOUL.md | Agent 人格模板 |
| USER.md | 用户信息 |
| MEMORY.md | 长期记忆 |
| AGENTS.md | 工作空间规则 |
| HEARTBEAT.md | 定时任务检查清单 |

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

## 致谢

- [HelloAgents](https://github.com/helloagents/helloagents) - Agent 框架
- [OpenClaw](https://github.com/openclaw/openclaw) - 灵感来源

## License

MIT
