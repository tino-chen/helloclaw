"""会话 API 路由"""
import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional, Dict, Any, Union, Literal

router = APIRouter(prefix="/session", tags=["session"])


class SessionInfo(BaseModel):
    """会话信息"""
    id: str
    created_at: float
    updated_at: float


class SessionListResponse(BaseModel):
    """会话列表响应"""
    sessions: List[SessionInfo]


class SessionCreateResponse(BaseModel):
    """创建会话响应"""
    session_id: str
    message: str = "Session created successfully"


# ==================== OpenAI 标准消息格式 ====================

class ToolCallFunction(BaseModel):
    """工具调用函数"""
    name: str
    arguments: str  # JSON 字符串


class ToolCall(BaseModel):
    """工具调用"""
    id: str
    type: Literal["function"] = "function"
    function: ToolCallFunction


class ChatMessage(BaseModel):
    """聊天消息（OpenAI 标准格式）"""
    role: Literal["user", "assistant", "tool"]
    content: Optional[str] = None
    tool_calls: Optional[List[ToolCall]] = None  # assistant 消息中的工具调用
    tool_call_id: Optional[str] = None  # tool 消息中的调用 ID


class SessionHistoryResponse(BaseModel):
    """会话历史响应"""
    session_id: str
    messages: List[ChatMessage]


def get_agent():
    """获取全局 Agent 实例"""
    from ..main import get_agent as _get_agent
    return _get_agent()


@router.get("/list", response_model=SessionListResponse)
async def list_sessions():
    """获取会话列表

    返回所有会话，按更新时间倒序排列
    """
    agent = get_agent()
    if not agent:
        return SessionListResponse(sessions=[])

    sessions = agent.list_sessions()
    return SessionListResponse(sessions=[
        SessionInfo(
            id=s["id"],
            created_at=s["created_at"],
            updated_at=s["updated_at"]
        )
        for s in sessions
    ])


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


@router.get("/{session_id}/history", response_model=SessionHistoryResponse)
async def get_session_history(session_id: str):
    """获取会话历史消息

    返回会话的所有聊天记录，按照 OpenAI 标准格式
    """
    agent = get_agent()
    if not agent:
        raise HTTPException(status_code=500, detail="Agent not initialized")

    raw_messages = agent.get_session_history(session_id)
    if raw_messages is None:
        raw_messages = []

    # 转换为 OpenAI 标准格式
    chat_messages: List[ChatMessage] = []

    for m in raw_messages:
        role = m.get("role", "")
        content = m.get("content", "")
        metadata = m.get("metadata", {})

        if role == "user":
            chat_messages.append(ChatMessage(role="user", content=content))

        elif role == "assistant":
            tool_calls_data = metadata.get("tool_calls")
            if tool_calls_data:
                # 包含工具调用的 assistant 消息
                tool_calls = [
                    ToolCall(
                        id=tc.get("id", ""),
                        type="function",
                        function=ToolCallFunction(
                            name=tc.get("function", {}).get("name", ""),
                            arguments=tc.get("function", {}).get("arguments", "{}")
                        )
                    )
                    for tc in tool_calls_data
                ]
                chat_messages.append(ChatMessage(
                    role="assistant",
                    content=content if content else None,
                    tool_calls=tool_calls
                ))
            elif content:
                # 普通的 assistant 文本消息
                chat_messages.append(ChatMessage(role="assistant", content=content))

        elif role == "tool":
            # tool 消息
            tool_call_id = metadata.get("tool_call_id")
            chat_messages.append(ChatMessage(
                role="tool",
                content=content,
                tool_call_id=tool_call_id
            ))

    return SessionHistoryResponse(
        session_id=session_id,
        messages=chat_messages
    )


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
