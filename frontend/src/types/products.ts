export interface ProductPicture {
  id_picture: number
  picture: string
  id_product: number
}

export interface Product {
  id_product: number
  name: string
  description: string
  price: number
  availability: boolean
  category: string
  ingredient_list: string
  id_restaurant: number
  pictures: ProductPicture[]
}