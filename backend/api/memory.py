"""记忆 API 路由"""
import os
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from typing import Optional, List

from workspace.manager import WorkspaceManager

router = APIRouter(prefix="/memory", tags=["memory"])


class MemoryEntry(BaseModel):
    """记忆条目"""
    date: str
    filename: str
    content: str
    preview: str


class MemoryListResponse(BaseModel):
    """记忆列表响应"""
    memories: List[MemoryEntry]
    total: int


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


def get_preview(content: str, max_length: int = 100) -> str:
    """获取内容预览"""
    # 移除 markdown 标记，获取纯文本预览
    lines = content.strip().split('\n')
    for line in lines:
        line = line.strip()
        if line and not line.startswith('#'):
            return line[:max_length] + ('...' if len(line) > max_length else '')
    return '(空)'


@router.get("/list", response_model=MemoryListResponse)
async def list_memories(ws: WorkspaceManager = Depends(get_workspace)):
    """获取每日记忆列表"""
    memories = []

    if os.path.exists(ws.memory_path):
        files = sorted(
            [f for f in os.listdir(ws.memory_path) if f.endswith('.md')],
            reverse=True  # 最新的在前面
        )

        for filename in files:
            filepath = os.path.join(ws.memory_path, filename)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # 从文件名提取日期 (YYYY-MM-DD.md)
            date = filename.replace('.md', '')

            memories.append(MemoryEntry(
                date=date,
                filename=filename,
                content=content,
                preview=get_preview(content)
            ))

    return MemoryListResponse(memories=memories, total=len(memories))


@router.get("/{filename}")
async def get_memory(filename: str, ws: WorkspaceManager = Depends(get_workspace)):
    """获取指定日期的记忆内容"""
    if not filename.endswith('.md'):
        filename += '.md'

    filepath = os.path.join(ws.memory_path, filename)

    if not os.path.exists(filepath):
        raise HTTPException(status_code=404, detail=f"记忆文件 {filename} 不存在")

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    return {
        "filename": filename,
        "date": filename.replace('.md', ''),
        "content": content
    }


@router.post("/today")
async def add_to_today(content: str, ws: WorkspaceManager = Depends(get_workspace)):
    """添加内容到今日记忆"""
    ws.append_to_daily_memory(content)
    return {"status": "ok", "message": "已添加到今日记忆"}
