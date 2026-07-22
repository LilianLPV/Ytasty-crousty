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

export const listerCommandes = () =>
  apiClient.get<Command[]>("/commands/").then((res) => res.data);

export const changerStatutCommande = (id_command: number, statut: string) =>
  apiClient
    .put<Command>(`/commands/${id_command}`, { status_command: statut })
    .then((res) => res.data);
