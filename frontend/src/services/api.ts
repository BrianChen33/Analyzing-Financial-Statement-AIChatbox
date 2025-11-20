import axios from 'axios'

// Resolve API base URL from env (browser vs server)
const API_BASE_URL = 
  typeof window !== 'undefined' 
    ? process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    : process.env.API_URL || 'http://localhost:8000'

// Shared axios instance
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30s timeout
  headers: {
    'Content-Type': 'application/json',
  },
})

// Request interceptor (auth headers can be added here)
apiClient.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证 token 等
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor with unified error handling
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    if (error.response) {
      console.error('API Error:', error.response.data)
      throw new Error(error.response.data.detail || error.response.data.message || 'Request failed')
    } else if (error.request) {
      console.error('Network Error:', error.request)
      throw new Error('Network error. Please confirm the backend server is running.')
    } else {
      console.error('Error:', error.message)
      throw new Error(error.message || 'Unknown error')
    }
  }
)

// API models
export interface AnalysisResponse {
  filename?: string
  period?: string
  type?: string
  files_analyzed?: number
  financial_data: Record<string, any>
  ratios: Record<string, number>
  risks: Array<{
    type: string
    severity: string
    description: string
  }>
  dupont?: Record<string, any>
  cash_flow?: {
    operating?: number
    investing?: number
    financing?: number
    free_cash_flow?: number
  }
  benchmark?: {
    industry: string
    metrics: Array<{
      metric: string
      company: number
      benchmark: number
      difference: number
    }>
    alerts?: string[]
    summary?: string
  }
  industry?: string
  trends?: any
  historical_data?: Array<Record<string, any>>
  insights?: string
  results?: AnalysisResponse[]
}

export interface ChatRequest {
  user_id: string
  question: string
  context: any
}

export interface ChatResponse {
  answer: string
  entry?: ChatHistoryEntry
}

export interface AuthUser {
  id: string
  name: string
  email: string
}

export interface AuthResponse {
  user: AuthUser
}

export interface AuthCredentials {
  email: string
  password: string
  name?: string
}

export interface ChatHistoryEntry {
  id: string
  question: string
  answer: string
  timestamp: string
}

// API methods
export const api = {
  healthCheck: async (): Promise<{ status: string; llm_available: boolean }> => {
    const response = await apiClient.get('/health')
    return response.data
  },

  analyzeFiles: async (files: File[], options?: { industry?: string }): Promise<AnalysisResponse> => {
    const formData = new FormData()
    files.forEach((file) => {
      formData.append('files', file)
    })
    if (options?.industry) {
      formData.append('industry', options.industry)
    }

    const response = await apiClient.post<AnalysisResponse>(
      '/api/analyze',
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        timeout: 60000, // file parsing can take longer
      }
    )
    return response.data
  },

  chat: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await apiClient.post<ChatResponse>('/api/chat', request)
    return response.data
  },

  register: async (credentials: AuthCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/api/auth/register', credentials)
    return response.data
  },

  login: async (credentials: AuthCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post<AuthResponse>('/api/auth/login', credentials)
    return response.data
  },

  getChatHistory: async (userId: string): Promise<{ history: ChatHistoryEntry[] }> => {
    const response = await apiClient.get<{ history: ChatHistoryEntry[] }>(`/api/chat/history/${userId}`)
    return response.data
  },

  exportReport: async (data: any, format: string = 'markdown'): Promise<{ content: string; filename: string }> => {
    const response = await apiClient.post<{ content: string; filename: string; format: string }>(
      `/api/export?format=${format}`,
      data
    )
    return response.data
  },
}

export default api

