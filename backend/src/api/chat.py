"""聊天 API 路由"""
from typing import Optional
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/chat", tags=["chat"])


class ChatRequest(BaseModel):
    """聊天请求"""
    message: str
    session_id: Optional[str] = None


class ChatResponse(BaseModel):
    """聊天响应"""
    content: str
    session_id: Optional[str] = None


def get_agent():
    """获取全局 Agent 实例"""
    from ..main import get_agent as _get_agent
    return _get_agent()


@router.post("/send/sync", response_model=ChatResponse)
async def send_message_sync(request: ChatRequest):
    """发送消息并获取同步响应"""
    agent = get_agent()
    if not agent:
        return ChatResponse(content="Agent not initialized", session_id=request.session_id)

    response = agent.chat(request.message, request.session_id)
    return ChatResponse(content=response, session_id=request.session_id)


@router.post("/send")
async def send_message(request: ChatRequest):
    """发送消息（暂返回同步响应）"""
    return await send_message_sync(request)
