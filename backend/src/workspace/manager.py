"""工作空间管理器"""

import os
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


# 配置文件列表
CONFIG_FILES = [
    "BOOTSTRAP",
    "IDENTITY",
    "SOUL",
    "USER",
    "MEMORY",
    "AGENTS",
    "HEARTBEAT",
]

# 模板目录（相对于当前文件）
TEMPLATES_DIR = Path(__file__).parent / "templates"


class WorkspaceManager:
    """工作空间管理器

    负责：
    - 创建和管理工作空间目录结构
    - 加载和保存配置文件
    - 管理记忆文件（每日记忆、长期记忆）
    """

    def __init__(self, workspace_path: str):
        """初始化工作空间管理器

        Args:
            workspace_path: 工作空间根目录路径
        """
        self.workspace_path = os.path.expanduser(workspace_path)
        self.memory_path = os.path.join(self.workspace_path, "memory")
        self.sessions_path = os.path.join(self.workspace_path, "sessions")

    def ensure_workspace_exists(self):
        """确保工作空间存在

        如果工作空间不存在，创建默认目录和配置文件
        """
        # 创建目录
        os.makedirs(self.workspace_path, exist_ok=True)
        os.makedirs(self.memory_path, exist_ok=True)
        os.makedirs(self.sessions_path, exist_ok=True)

        # 创建默认配置文件
        for config_name in CONFIG_FILES:
            config_path = self.get_config_path(config_name)
            if not os.path.exists(config_path):
                self._create_default_config(config_name)

    def get_config_path(self, name: str) -> str:
        """获取配置文件路径

        Args:
            name: 配置文件名称（不含扩展名）

        Returns:
            配置文件完整路径
        """
        return os.path.join(self.workspace_path, f"{name}.md")

    def load_config(self, name: str) -> Optional[str]:
        """加载配置文件内容

        Args:
            name: 配置文件名称

        Returns:
            配置文件内容，如果不存在返回 None
        """
        config_path = self.get_config_path(name)
        if os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return f.read()
        return None

    def save_config(self, name: str, content: str):
        """保存配置文件

        Args:
            name: 配置文件名称
            content: 配置文件内容
        """
        config_path = self.get_config_path(name)
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(content)

    def list_configs(self) -> list:
        """列出所有配置文件

        Returns:
            配置文件名称列表
        """
        configs = []
        for name in CONFIG_FILES:
            config_path = self.get_config_path(name)
            if os.path.exists(config_path):
                configs.append(name)
        return configs

    def get_daily_memory_path(self, date: datetime = None) -> str:
        """获取每日记忆文件路径

        Args:
            date: 日期，默认为今天

        Returns:
            每日记忆文件路径
        """
        date = date or datetime.now()
        filename = date.strftime("%Y-%m-%d.md")
        return os.path.join(self.memory_path, filename)

    def append_to_daily_memory(self, content: str, date: datetime = None):
        """追加内容到每日记忆

        Args:
            content: 记忆内容
            date: 日期，默认为今天
        """
        memory_path = self.get_daily_memory_path(date)
        timestamp = datetime.now().strftime("%H:%M:%S")

        with open(memory_path, "a", encoding="utf-8") as f:
            f.write(f"\n## {timestamp}\n\n{content}\n")

    def search_memory(self, keyword: str, include_daily: bool = True) -> list:
        """搜索记忆

        Args:
            keyword: 搜索关键词
            include_daily: 是否包含每日记忆

        Returns:
            匹配的记忆片段列表
        """
        results = []

        # 搜索长期记忆
        memory_content = self.load_config("MEMORY")
        if memory_content and keyword.lower() in memory_content.lower():
            results.append({
                "source": "MEMORY.md",
                "content": memory_content,
            })

        # 搜索每日记忆
        if include_daily:
            for filename in os.listdir(self.memory_path):
                if filename.endswith(".md"):
                    filepath = os.path.join(self.memory_path, filename)
                    with open(filepath, "r", encoding="utf-8") as f:
                        content = f.read()
                        if keyword.lower() in content.lower():
                            results.append({
                                "source": f"memory/{filename}",
                                "content": content,
                            })

        return results

    def _create_default_config(self, name: str):
        """创建默认配置文件

        从模板文件读取内容，如果模板不存在则使用基础模板

        Args:
            name: 配置文件名称
        """
        template_path = TEMPLATES_DIR / f"{name}.md"

        if template_path.exists():
            with open(template_path, "r", encoding="utf-8") as f:
                content = f.read()
        else:
            # 回退到基础模板
            content = f"# {name}\n\n（待配置）"

        # 替换日期占位符
        content = content.replace("{date}", datetime.now().strftime("%Y-%m-%d"))

        self.save_config(name, content)
