"""聊天 API 路由"""
from fastapi import APIRouter

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("/send")
async def send_message(message: str, session_id: str = None):
    """发送消息并获取流式响应"""
    # TODO: 实现聊天逻辑
    return {"message": "Not implemented yet", "session_id": session_id}
