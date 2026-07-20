import { api } from '../../../lib/api'
import type { Restaurant } from '../../../types/restaurant'
import type { Product } from '../../../types/products'

export const recupererRestaurant = (id: number) => api<Restaurant>(`/restaurants/${id}`)

export const listerMenu = (id: number) => api<Product[]>(`/products/?id_restaurant=${id}`)