import api from './index'

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export const chatApi = {
  sendMessage: async (message: string, sessionId?: string) => {
    return api.post('/chat/send', { message, session_id: sessionId })
  },
}
