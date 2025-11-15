import axios from 'axios'

// API 基础 URL - 在浏览器端使用相对路径或环境变量
const API_BASE_URL = 
  typeof window !== 'undefined' 
    ? process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'
    : process.env.API_URL || 'http://localhost:8000'

// 创建 axios 实例
const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000, // 30秒超时
  headers: {
    'Content-Type': 'application/json',
  },
})

// 请求拦截器
apiClient.interceptors.request.use(
  (config) => {
    // 可以在这里添加认证 token 等
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// 响应拦截器
apiClient.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // 统一错误处理
    if (error.response) {
      // 服务器返回了错误响应
      console.error('API Error:', error.response.data)
      throw new Error(error.response.data.detail || error.response.data.message || '请求失败')
    } else if (error.request) {
      // 请求已发出但没有收到响应
      console.error('Network Error:', error.request)
      throw new Error('网络错误，请检查后端服务是否运行')
    } else {
      // 其他错误
      console.error('Error:', error.message)
      throw new Error(error.message || '未知错误')
    }
  }
)

// API 接口定义
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
  question: string
  context: any
}

export interface ChatResponse {
  answer: string
}

// API 方法
export const api = {
  // 健康检查
  healthCheck: async (): Promise<{ status: string; llm_available: boolean }> => {
    const response = await apiClient.get('/health')
    return response.data
  },

  // 分析文件
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
        timeout: 60000, // 文件分析可能需要更长时间
      }
    )
    return response.data
  },

  // 聊天问答
  chat: async (request: ChatRequest): Promise<ChatResponse> => {
    const response = await apiClient.post<ChatResponse>('/api/chat', request)
    return response.data
  },

  // 导出报告
  exportReport: async (data: any, format: string = 'markdown'): Promise<{ content: string; filename: string }> => {
    const response = await apiClient.post<{ content: string; filename: string; format: string }>(
      `/api/export?format=${format}`,
      data
    )
    return response.data
  },
}

export default api

