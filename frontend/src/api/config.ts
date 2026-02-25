import api from './index'

export interface ConfigFile {
  name: string
  content: string
}

export const configApi = {
  list: async () => {
    return api.get<{ configs: string[] }>('/config/list')
  },
  get: async (name: string) => {
    return api.get<ConfigFile>(`/config/${name}`)
  },
  update: async (name: string, content: string) => {
    return api.put<{ name: string; status: string }>(`/config/${name}`, { content })
  },
}
