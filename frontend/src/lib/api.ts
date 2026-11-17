import axios from 'axios'

// En production, VITE_API_URL contient l'URL publique de l'API (fixée au build).
// En local, elle est vide : on passe par le proxy Vite défini sur /api.
export const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '/api',
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

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});