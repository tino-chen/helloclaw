import api from './index'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface ChatResponse {
  content: string
  session_id: string | null
}

export const chatApi = {
  // 流式发送消息 (SSE)
  sendMessage: async (message: string, sessionId?: string) => {
    return api.post('/chat/send', { message, session_id: sessionId })
  },

  // 同步发送消息（支持取消）
  sendMessageSync: async (
    message: string,
    sessionId?: string,
    signal?: AbortSignal
  ): Promise<ChatResponse> => {
    return api.post('/chat/send/sync', { message, session_id: sessionId }, { signal })
  },
}
