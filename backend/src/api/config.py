"""配置 API 路由"""
import json
import os
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional

from ..workspace.manager import WorkspaceManager

router = APIRouter(prefix="/config", tags=["config"])


class ConfigUpdateRequest(BaseModel):
    """配置更新请求"""
    content: str


# 全局 workspace 实例（由 main.py 在启动时设置）
_workspace: Optional[WorkspaceManager] = None


def set_workspace(ws: WorkspaceManager):
    """设置全局 workspace 实例"""
    global _workspace
    _workspace = ws


def get_workspace() -> WorkspaceManager:
    """获取 workspace 实例"""
    if _workspace is None:
        ws = WorkspaceManager(os.getenv("WORKSPACE_PATH", "~/.helloclaw/workspace"))
        ws.ensure_workspace_exists()
        set_workspace(ws)
    return _workspace


def get_config_json_path() -> str:
    """获取全局 config.json 路径"""
    return os.path.expanduser("~/.helloclaw/config.json")


def ensure_config_json_exists():
    """确保 config.json 存在"""
    config_path = get_config_json_path()
    if not os.path.exists(config_path):
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


@router.get("/list")
async def list_configs(ws: WorkspaceManager = Depends(get_workspace)):
    """获取配置文件列表"""
    configs = ws.list_configs()
    # 添加 config.json
    configs.insert(0, "CONFIG")
    return {"configs": configs}


@router.get("/{name}")
async def get_config(name: str, ws: WorkspaceManager = Depends(get_workspace)):
    """获取指定配置文件内容"""
    # 特殊处理 CONFIG (config.json)
    if name == "CONFIG":
        ensure_config_json_exists()
        config_path = get_config_json_path()
        with open(config_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {"name": name, "content": content}

    # 处理 .md 配置文件
    content = ws.load_config(name)
    if content is None:
        raise HTTPException(status_code=404, detail=f"配置文件 {name} 不存在")
    return {"name": name, "content": content}


@router.put("/{name}")
async def update_config(name: str, request: ConfigUpdateRequest, ws: WorkspaceManager = Depends(get_workspace)):
    """更新配置文件"""
    # 特殊处理 CONFIG (config.json)
    if name == "CONFIG":
        ensure_config_json_exists()
        # 验证 JSON 格式
        try:
            json.loads(request.content)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="无效的 JSON 格式")

        config_path = get_config_json_path()
        with open(config_path, "w", encoding="utf-8") as f:
            f.write(request.content)
        return {"name": name, "status": "updated"}

    # 处理 .md 配置文件
    if name not in ws.list_configs():
        raise HTTPException(status_code=404, detail=f"配置文件 {name} 不存在")

    ws.save_config(name, request.content)
    return {"name": name, "status": "updated"}
