"""会话 API 路由"""
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional

router = APIRouter(prefix="/session", tags=["session"])


class SessionInfo(BaseModel):
    """会话信息"""
    id: str
    created_at: float
    updated_at: float


class SessionCreateResponse(BaseModel):
    """创建会话响应"""
    session_id: str
    message: str = "Session created successfully"


def get_agent():
    """获取全局 Agent 实例"""
    from main import get_agent as _get_agent
    return _get_agent()


@router.get("/list", response_model=List[SessionInfo])
async def list_sessions():
    """获取会话列表

    返回所有会话，按更新时间倒序排列
    """
    agent = get_agent()
    if not agent:
        return []

    sessions = agent.list_sessions()
    return [
        SessionInfo(
            id=s["id"],
            created_at=s["created_at"],
            updated_at=s["updated_at"]
        )
        for s in sessions
    ]


@router.post("/create", response_model=SessionCreateResponse)
async def create_session():
    """创建新会话

    返回新会话的 ID
    """
    agent = get_agent()
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")

    session_id = agent.create_session()
    return SessionCreateResponse(session_id=session_id)


@router.get("/{session_id}")
async def get_session(session_id: str):
    """获取会话详情

    返回会话的基本信息
    """
    agent = get_agent()
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")

    sessions = agent.list_sessions()
    for s in sessions:
        if s["id"] == session_id:
            return SessionInfo(
                id=s["id"],
                created_at=s["created_at"],
                updated_at=s["updated_at"]
            )

    raise HTTPException(status_code=404, detail="Session not found")


@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """删除会话

    删除指定会话及其历史记录
    """
    agent = get_agent()
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")

    success = agent.delete_session(session_id)
    if success:
        return {"message": "Session deleted successfully", "session_id": session_id}

    raise HTTPException(status_code=404, detail="Session not found")
