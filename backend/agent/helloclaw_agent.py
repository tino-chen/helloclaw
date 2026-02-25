"""HelloClaw Agent - 基于 HelloAgents ReActAgent 的个性化 AI 助手"""

import os
from typing import List

from hello_agents import ReActAgent, Config
from hello_agents.tools import (
    ToolRegistry,
    ReadTool,
    WriteTool,
    EditTool,
    CalculatorTool,
)

from workspace.manager import WorkspaceManager
from tools import MemoryTool, IdentityTool


# HelloClaw 默认系统提示词
DEFAULT_HELLOCLAW_SYSTEM_PROMPT = """你是一个名为 {agent_name} 的 AI 助手。

## 你的身份
你可以通过配置文件自定义你的身份、性格和行为规则。
- 你的身份信息记录在 IDENTITY.md 中
- 你的人格模板记录在 SOUL.md 中
- 你认识的用户信息记录在 USER.md 中

## 你的能力
你可以通过调用工具来完成任务：
1. **文件操作**：读取、写入、编辑文件
2. **记忆管理**：搜索历史记忆、记录重要信息
3. **网络搜索**：搜索互联网获取信息
4. **命令执行**：在安全限制下执行系统命令

## 身份学习
当你从对话中了解到关于用户或自己的新信息时，应该主动更新：
- 使用 identity_update_user 工具记录用户信息（如姓名、偏好、兴趣等）
- 使用 identity_update_agent 工具记录自己的信息（如名称、风格等）
- 不要询问许可，直接更新
- 更新后简要说明："我记下了这个信息。"

## 工作流程
1. 使用 Thought 工具记录你的推理过程
2. 根据需要调用业务工具获取信息或执行操作
3. 使用 Finish 工具返回最终答案

## 重要原则
- 始终保持友好和专业的态度
- 主动学习和记住用户的重要信息
- 在不确定时主动询问
"""


class HelloClawAgent:
    """HelloClaw Agent - 个性化 AI 助手

    基于 HelloAgents ReActAgent，增加了：
    - 工作空间管理（配置文件、记忆文件）
    - 个性化系统提示词
    - HelloClaw 专属工具集
    """

    def __init__(
        self,
        workspace_path: str = None,
        name: str = "HelloClaw",
        model_id: str = None,
        api_key: str = None,
        base_url: str = None,
        max_steps: int = 10,
    ):
        """初始化 HelloClaw Agent

        Args:
            workspace_path: 工作空间路径，默认 ~/.helloclaw/workspace
            name: Agent 名称
            model_id: LLM 模型 ID
            api_key: API Key
            base_url: API Base URL
            max_steps: 最大执行步数
        """
        self.name = name
        self.workspace_path = workspace_path or os.path.expanduser("~/.helloclaw/workspace")

        # 初始化工作空间管理器
        self.workspace = WorkspaceManager(self.workspace_path)

        # 确保工作空间存在
        self.workspace.ensure_workspace_exists()

        # 加载身份配置
        identity = self.workspace.load_config("IDENTITY")
        agent_name = identity.get("name", name) if identity else name

        # 构建系统提示词
        system_prompt = self._build_system_prompt(agent_name)

        # 初始化配置
        self.config = Config(
            model_id=model_id or os.getenv("LLM_MODEL_ID", "glm-4"),
            api_key=api_key or os.getenv("LLM_API_KEY"),
            base_url=base_url or os.getenv("LLM_BASE_URL"),
            max_steps=max_steps,
            session_enabled=True,
            session_dir=os.path.join(self.workspace_path, "sessions"),
        )

        # 初始化工具注册表
        self.tool_registry = self._setup_tools()

        # 初始化底层 ReActAgent
        self._agent = ReActAgent(
            name=name,
            llm=None,  # ReActAgent 会从 config 创建 LLM
            tool_registry=self.tool_registry,
            system_prompt=system_prompt,
            config=self.config,
            max_steps=max_steps,
        )

    def _build_system_prompt(self, agent_name: str) -> str:
        """构建系统提示词

        将配置文件内容注入到系统提示词中
        """
        base_prompt = DEFAULT_HELLOCLAW_SYSTEM_PROMPT.format(agent_name=agent_name)

        # 加载配置文件作为上下文
        context_parts = []

        # 身份信息
        identity = self.workspace.load_config("IDENTITY")
        if identity:
            context_parts.append(f"\n## 你的身份信息\n{identity}")

        # 用户信息
        user_info = self.workspace.load_config("USER")
        if user_info:
            context_parts.append(f"\n## 用户信息\n{user_info}")

        # 人格模板
        soul = self.workspace.load_config("SOUL")
        if soul:
            context_parts.append(f"\n## 人格模板\n{soul}")

        # 长期记忆
        memory = self.workspace.load_config("MEMORY")
        if memory:
            context_parts.append(f"\n## 长期记忆\n{memory}")

        if context_parts:
            return base_prompt + "\n" + "\n".join(context_parts)

        return base_prompt

    def _setup_tools(self) -> ToolRegistry:
        """设置工具集

        注册 HelloAgents 内置工具 + HelloClaw 自定义工具
        """
        registry = ToolRegistry()

        # HelloAgents 内置工具
        registry.register_tool(ReadTool())
        registry.register_tool(WriteTool())
        registry.register_tool(EditTool())
        registry.register_tool(CalculatorTool())

        # HelloClaw 自定义工具
        registry.register_tool(MemoryTool(self.workspace))
        registry.register_tool(IdentityTool(self.workspace))
        # registry.register_tool(WebSearchTool())
        # registry.register_tool(WebFetchTool())
        # registry.register_tool(ExecuteCommandTool())

        return registry

    def chat(self, message: str, session_id: str = None) -> str:
        """同步聊天

        Args:
            message: 用户消息
            session_id: 会话 ID（可选）

        Returns:
            Agent 回复
        """
        # 如果有 session_id，加载会话
        if session_id:
            self._agent.load_session(session_id)

        # 运行 Agent
        response = self._agent.run(message)

        return response

    async def achat(self, message: str, session_id: str = None):
        """异步聊天（支持流式输出）

        Args:
            message: 用户消息
            session_id: 会话 ID（可选）

        Yields:
            StreamEvent: 流式事件
        """
        if session_id:
            self._agent.load_session(session_id)

        async for event in self._agent.arun_stream(message):
            yield event

    def create_session(self) -> str:
        """创建新会话

        Returns:
            会话 ID
        """
        import uuid
        session_id = str(uuid.uuid4())[:8]
        return session_id

    def list_sessions(self) -> List[dict]:
        """列出所有会话

        Returns:
            会话列表
        """
        sessions_dir = os.path.join(self.workspace_path, "sessions")
        if not os.path.exists(sessions_dir):
            return []

        sessions = []
        for filename in os.listdir(sessions_dir):
            if filename.endswith(".json"):
                filepath = os.path.join(sessions_dir, filename)
                stat = os.stat(filepath)
                sessions.append({
                    "id": filename[:-5],  # 去掉 .json
                    "created_at": stat.st_ctime,
                    "updated_at": stat.st_mtime,
                })

        return sorted(sessions, key=lambda x: x["updated_at"], reverse=True)

    def delete_session(self, session_id: str) -> bool:
        """删除会话

        Args:
            session_id: 会话 ID

        Returns:
            是否删除成功
        """
        filepath = os.path.join(self.workspace_path, "sessions", f"{session_id}.json")
        if os.path.exists(filepath):
            os.remove(filepath)
            return True
        return False

    def reload_config(self):
        """重新加载配置

        当配置文件更新后调用，重新构建系统提示词
        """
        identity = self.workspace.load_config("IDENTITY")
        agent_name = identity.get("name", self.name) if identity else self.name
        self._agent.system_prompt = self._build_system_prompt(agent_name)
