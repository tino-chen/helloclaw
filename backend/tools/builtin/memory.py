"""记忆工具 - 支持记忆检索和更新"""

from typing import List, Dict, Any

from hello_agents.tools import Tool, ToolParameter, ToolResponse, tool_action


class MemoryTool(Tool):
    """记忆管理工具

    可展开为多个子工具：
    - memory_search: 搜索记忆
    - memory_add: 添加每日记忆
    - memory_update_longterm: 更新长期记忆
    """

    def __init__(self, workspace_manager):
        """初始化记忆工具

        Args:
            workspace_manager: 工作空间管理器实例
        """
        super().__init__(
            name="memory",
            description="记忆管理工具，支持搜索、添加和更新记忆",
            expandable=True
        )
        self.workspace = workspace_manager

    def run(self, parameters: Dict[str, Any]) -> ToolResponse:
        """默认执行：搜索记忆"""
        keyword = parameters.get("keyword", "")
        return self._search_memory(keyword)

    def get_parameters(self) -> List[ToolParameter]:
        return [
            ToolParameter(
                name="keyword",
                type="string",
                description="搜索关键词",
                required=True
            )
        ]

    def _search_memory(self, keyword: str) -> ToolResponse:
        """搜索记忆"""
        if not keyword:
            return ToolResponse.error(
                code="INVALID_INPUT",
                message="请提供搜索关键词"
            )

        results = self.workspace.search_memory(keyword)

        if not results:
            return ToolResponse.success(
                text=f"未找到与 '{keyword}' 相关的记忆",
                data={"results": []}
            )

        # 格式化结果
        formatted = []
        for r in results:
            formatted.append(f"**{r['source']}**:\n{r['content'][:500]}...")

        return ToolResponse.success(
            text=f"找到 {len(results)} 条相关记忆:\n\n" + "\n\n".join(formatted),
            data={"results": results, "count": len(results)}
        )

    @tool_action("memory_search", "搜索历史记忆")
    def _search(self, keyword: str) -> str:
        """搜索记忆

        Args:
            keyword: 搜索关键词
        """
        response = self._search_memory(keyword)
        return response.text

    @tool_action("memory_add", "添加内容到今日记忆")
    def _add_daily(self, content: str) -> str:
        """添加每日记忆

        Args:
            content: 记忆内容
        """
        self.workspace.append_to_daily_memory(content)
        return f"已添加到今日记忆: {content[:50]}..."

    @tool_action("memory_update_longterm", "更新长期记忆")
    def _update_longterm(self, content: str) -> str:
        """更新长期记忆

        Args:
            content: 要添加到长期记忆的内容
        """
        current = self.workspace.load_config("MEMORY") or ""
        updated = current + f"\n\n## 新增\n\n{content}\n"
        self.workspace.save_config("MEMORY", updated)
        return "已更新长期记忆"
