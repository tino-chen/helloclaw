"""身份更新工具 - 从对话中提取并更新身份信息"""

from typing import List, Dict, Any

from hello_agents.tools import Tool, ToolParameter, ToolResponse, tool_action


class IdentityTool(Tool):
    """身份更新工具

    用于更新 Agent 身份信息和用户信息
    可展开为多个子工具：
    - identity_update_agent: 更新 Agent 身份信息
    - identity_update_user: 更新用户信息
    """

    def __init__(self, workspace_manager):
        """初始化身份工具

        Args:
            workspace_manager: 工作空间管理器实例
        """
        super().__init__(
            name="identity",
            description="身份信息更新工具，用于更新 Agent 或用户的信息",
            expandable=True
        )
        self.workspace = workspace_manager

    def run(self, parameters: Dict[str, Any]) -> ToolResponse:
        """默认执行"""
        return ToolResponse.success(
            text="请使用 identity_update_agent 或 identity_update_user 子工具"
        )

    def get_parameters(self) -> List[ToolParameter]:
        return []

    @tool_action("identity_update_agent", "更新 Agent 的身份信息")
    def _update_agent(self, info_type: str, content: str) -> str:
        """更新 Agent 身份信息

        Args:
            info_type: 信息类型（如：name, personality, ability 等）
            content: 信息内容
        """
        current = self.workspace.load_config("IDENTITY") or ""

        # 添加新信息
        update = f"\n\n## 更新 - {info_type}\n\n{content}\n"
        updated = current + update

        self.workspace.save_config("IDENTITY", updated)
        return f"已更新 Agent 身份信息 ({info_type})"

    @tool_action("identity_update_user", "更新用户信息")
    def _update_user(self, info_type: str, content: str) -> str:
        """更新用户信息

        Args:
            info_type: 信息类型（如：name, preference, interest 等）
            content: 信息内容
        """
        current = self.workspace.load_config("USER") or ""

        # 添加新信息
        update = f"\n\n## 更新 - {info_type}\n\n{content}\n"
        updated = current + update

        self.workspace.save_config("USER", updated)
        return f"已更新用户信息 ({info_type})"
