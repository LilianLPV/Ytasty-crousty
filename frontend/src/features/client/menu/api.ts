import { apiClient } from '../../../lib/api'
import type { Restaurant } from '../../../types/restaurant'
import type { Product } from '../../../types/products'

export const recupererRestaurant = (id: number) => apiClient.get<Restaurant>(`/restaurants/${id}`).then((response) => response.data)

export const listerMenu = (id: number) => apiClient.get<Product[]>(`/products/?id_restaurant=${id}`).then((response) => response.data)