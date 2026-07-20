export interface RestaurantAddress {
  id_address: number
  city: string
  address: string
}

export interface Restaurant {
  id_restaurant: number
  name: string
  opening_status: boolean
  opening_hours: string
  contact_details: string
  restaurant_address: RestaurantAddress
}