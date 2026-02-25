"""会话 API 路由"""
from fastapi import APIRouter

router = APIRouter(prefix="/session", tags=["session"])


@router.get("/list")
async def list_sessions():
    """获取会话列表"""
    # TODO: 实现会话列表逻辑
    return {"sessions": []}


@router.post("/create")
async def create_session():
    """创建新会话"""
    # TODO: 实现创建会话逻辑
    return {"session_id": "new-session-id"}
