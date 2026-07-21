import { apiClient } from "../../../lib/api";
import type { CommandeAEnvoyer, Command } from "../../../types/commands";

export const passerCommande = (commande: CommandeAEnvoyer) =>
  apiClient
    .post<Command>("/commands/", commande)
    .then((response) => response.data);

export const suivreCommande = (numero: string) =>
  apiClient
    .get<Command>(`/commands/by-number/${numero}`)
    .then((res) => res.data);
