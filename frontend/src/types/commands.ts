export interface CommandeAEnvoyer {
  withdrawal_method: string;
  customer_information: string;
  id_restaurant: number;
  lines: { id_product: number; quantity: number }[];
}

export interface CommandLine {
  id_command_line: number;
  quantity: number;
  unit_price: number;
  name: string;
  id_command: number;
  id_product: number;
}

export interface Command {
  id_command: number;
  number_command: string;
  creation_date_and_time: string;
  status_command: string;
  withdrawal_method: string;
  customer_information: string;
  price_total: number;
  id_restaurant: number;
  command_lines: CommandLine[];
}
