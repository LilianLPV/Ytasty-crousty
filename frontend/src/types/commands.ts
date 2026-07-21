export interface CommandeAEnvoyer {
  withdrawal_method: string
  customer_information: string 
  id_restaurant: number
  lines: { id_product: number; quantity: number }[]
}

export interface Command {
  id_command: number
  number_command: string
  creation_date_and_time: string
  status_command: string
  withdrawal_method: string
  customer_information: string
  price_total: number
  id_restaurant: number
}