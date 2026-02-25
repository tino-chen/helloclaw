import api from './index'

export interface Session {
  id: string
  created_at: number
  updated_at: number
}

export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
}

export interface SessionHistory {
  session_id: string
  messages: ChatMessage[]
}

export const sessionApi = {
  list: async () => {
    return api.get<{ sessions: Session[] }>('/session/list')
  },
  create: async () => {
    return api.post<{ session_id: string }>('/session/create')
  },
  get: async (id: string) => {
    return api.get<Session>(`/session/${id}`)
  },
  delete: async (id: string) => {
    return api.delete(`/session/${id}`)
  },
  getHistory: async (id: string) => {
    return api.get<SessionHistory>(`/session/${id}/history`)
  },
}
