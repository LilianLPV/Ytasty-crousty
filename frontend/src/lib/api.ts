import axios from 'axios'

export const apiClient = axios.create({
  baseURL: '/api',
})

export class ApiError extends Error {
  status: number

  constructor(status: number, message: string) {
    super(message)
    this.status = status
    this.name = 'ApiError'
  }
}

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const status = error.response?.status ?? 0
    const message = error.response?.data?.detail ?? error.message
    return Promise.reject(new ApiError(status, message))
  },
)
