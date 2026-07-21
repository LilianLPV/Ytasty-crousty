import { apiClient } from "../../../lib/api";
import type { CommandeAEnvoyer, Command } from "../../../types/commands";

export const passerCommande = (commande: CommandeAEnvoyer) =>
  apiClient
    .post<Command>("/commands/", commande)
    .then((response) => response.data);