import api from './index'

export interface Session {
  id: string
  created_at: string
  updated_at: string
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
}
