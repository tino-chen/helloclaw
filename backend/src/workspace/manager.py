"""工作空间管理器"""

import os
import re
from datetime import datetime
from pathlib import Path
from typing import Optional


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

    def is_onboarding_completed(self) -> bool:
        """检查入职是否完成

        入职完成的标志：BOOTSTRAP.md 不存在。
        同时会检查身份是否已确定，如果是则自动删除 BOOTSTRAP.md。

        Returns:
            入职是否已完成
        """
        # 先检查是否需要删除 BOOTSTRAP（身份已确定但文件还在）
        self._check_and_delete_bootstrap()

        return not os.path.exists(self.get_config_path("BOOTSTRAP"))

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

        # 检查是否需要删除 BOOTSTRAP（遗留工作空间迁移）
        self._check_and_delete_bootstrap()

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

        # 如果保存的是 IDENTITY，检查是否需要删除 BOOTSTRAP
        if name == "IDENTITY":
            self._check_and_delete_bootstrap()

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

    def _check_and_delete_bootstrap(self):
        """检查身份是否已确定，如果是则删除 BOOTSTRAP.md"""
        bootstrap_path = self.get_config_path("BOOTSTRAP")

        # BOOTSTRAP 不存在，无需处理
        if not os.path.exists(bootstrap_path):
            return

        # 检查身份是否已确定
        if self._is_identity_established():
            os.remove(bootstrap_path)

    def _is_identity_established(self) -> bool:
        """检查身份是否已确定（名称字段有实际内容）

        Returns:
            身份是否已确定
        """
        identity = self.load_config("IDENTITY")
        if not identity:
            return False

        # 尝试匹配名称字段
        # 格式: - **名称：** xxx 或 - **名称:** xxx
        match = re.search(r'\*\*名称[：:]\*\*\s*(.+?)(?:\n|$)', identity)
        if match:
            name = match.group(1).strip()
            # 如果名称不是占位符，则认为身份已确定
            # 占位符特征：以下划线开头、包含"选一个"、包含"（"
            if name and not name.startswith('_') and '选一个' not in name and '（' not in name:
                return True

        return False

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

    def reset_to_templates(self, reset_sessions: bool = False, reset_memory: bool = False, reset_global_config: bool = False):
        """重置工作空间到初始模板

        Args:
            reset_sessions: 是否清除会话
            reset_memory: 是否清除每日记忆
            reset_global_config: 是否重置全局配置

        警告：这将覆盖所有配置文件！
        """
        # 重置配置文件（包括 BOOTSTRAP）
        for config_name in CONFIG_FILES:
            self._create_default_config(config_name)

        # 清除会话
        if reset_sessions:
            self._clear_sessions()

        # 清除每日记忆
        if reset_memory:
            self._clear_daily_memory()

        # 重置全局配置
        if reset_global_config:
            self._reset_global_config()

    def _clear_sessions(self):
        """清除所有会话"""
        if os.path.exists(self.sessions_path):
            for filename in os.listdir(self.sessions_path):
                if filename.endswith(".json"):
                    filepath = os.path.join(self.sessions_path, filename)
                    os.remove(filepath)

    def _clear_daily_memory(self):
        """清除所有每日记忆"""
        if os.path.exists(self.memory_path):
            for filename in os.listdir(self.memory_path):
                if filename.endswith(".md"):
                    filepath = os.path.join(self.memory_path, filename)
                    os.remove(filepath)

    def _reset_global_config(self):
        """重置全局配置文件"""
        import json
        config_path = os.path.expanduser("~/.helloclaw/config.json")
        os.makedirs(os.path.dirname(config_path), exist_ok=True)

        default_config = {
            "llm": {
                "model_id": "glm-4",
                "api_key": "",
                "base_url": "",
            },
            "proxy": {
                "enabled": False,
                "http": "",
                "https": "",
            },
            "agent": {
                "max_steps": 10,
                "temperature": 0.7,
            },
        }

        with open(config_path, "w", encoding="utf-8") as f:
            json.dump(default_config, f, indent=2, ensure_ascii=False)
