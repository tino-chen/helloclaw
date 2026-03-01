# 维护规范


# 项目概述

**HelloClaw** 是 Hello-Agents 框架的毕业设计项目，实现 OpenClaw 核心功能。

**技术栈**: Python + uv + HelloAgents + FastAPI (后端) | Vue3 + TypeScript + Ant Design Vue (前端)


## 架构

**核心**: HelloClawAgent 封装 ReActAgent，所有功能通过 Tool 实现（非 Service 层）

```
backend/
├── agent/helloclaw_agent.py   # 封装 ReActAgent
├── tools/builtin/             # MemoryTool, IdentityTool 等
├── workspace/manager.py       # 工作空间管理
├── channels/                  # Web/CLI 渠道
└── api/                       # FastAPI 路由
```

## 运行

```bash
# 后端
cd helloclaw/backend && uv run uvicorn main:app --reload --port 8000

# 前端
cd helloclaw/frontend && npm run dev
```



---



# 经验教训

## UI 主题颜色（2026-02-25）

**项目整体主题是龙虾红（Lobster Red），不是蓝色或绿色。**

CSS 变量（定义在 `frontend/src/assets/base.css`）：
- 主色：`--color-primary: #ff5c5c`
- Hover：`--color-primary-hover: #ff7070`
- 浅色背景：`--color-primary-light: rgba(255, 92, 92, 0.15)`

Ant Design Vue 组件使用：
- Tag 颜色：`color="error"` 或 `color="red"`
- 选中状态背景：`#fff1f0`
- 选中状态边框：`#ff4d4f`

**教训**：用户说"改主题"时，应先确认项目整体主题色，而不是假设默认颜色。

## UI 布局一致性（2026-02-25）

**新增视图页面时必须保持与现有视图的布局一致性。**

当前约定：
- 左侧列表宽度：`280px`
- 页面内边距：`24px`
- 卡片间距：`24px`

**教训**：新增 MemoryView 时使用了 300px 列表宽度，与 ConfigView 的 280px 不一致。应先查看现有类似页面的样式再开发。

