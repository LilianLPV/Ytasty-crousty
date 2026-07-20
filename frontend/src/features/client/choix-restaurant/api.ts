import { api } from '../../../lib/api'
import type { Restaurant } from '../../../types/restaurant'

export const listerRestaurants = () => api<Restaurant[]>('/restaurants/')