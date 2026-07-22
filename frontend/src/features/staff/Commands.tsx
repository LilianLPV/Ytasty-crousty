import { useNavigate } from "react-router";
import type { Command } from "../../types/commands";
import { useState, useEffect } from "react";
import { changerStatutCommande, listerCommandes } from "../client/command/api";
import { listerMenu } from "../client/menu/api";
import type { Product } from "../../types/products";

export function Commandes() {
  const [commandes, setCommandes] = useState<Command[]>([]);
  const [filtreStatut, setFiltreStatut] = useState("tous");
  const [produits, setProduits] = useState<Product[]>([]);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState<string | null>(null);
  const navigate = useNavigate();

  const seDeconnecter = () => {
    localStorage.removeItem("token");
    navigate("/login");
  };

  useEffect(() => {
    Promise.all([
      listerCommandes(),
      listerMenu(1),
      listerMenu(2),
      listerMenu(3),
    ])
      .then(([cmds, p1, p2, p3]) => {
        setCommandes(cmds);
        setProduits([...p1, ...p2, ...p3]);
      })
      .catch(() => setErreur("Impossible de charger les données"))
      .finally(() => setChargement(false));
  }, []);

  const changerStatut = async (id_command: number, nouveauStatut: string) => {
    try {
      const cmdMaj = await changerStatutCommande(id_command, nouveauStatut);
      setCommandes((prev) =>
        prev.map((cmd) => (cmd.id_command === id_command ? cmdMaj : cmd)),
      );
    } catch {
      setErreur("Impossible de changer le statut de la commande");
    }
  };

  if (chargement) return <p>Chargement…</p>;
  if (erreur) return <p>Erreur : {erreur}</p>;
  const nomsProduits: Record<number, string> = {};
  produits.forEach((p) => {
    nomsProduits[p.id_product] = p.name;
  });
  const commandesFiltrees = commandes.filter(
    (cmd) => filtreStatut === "tous" || cmd.status_command === filtreStatut,
  );
  return (
    <div>
      <button onClick={seDeconnecter}>Se déconnecter</button>
      <h1>Commandes en cours</h1>
      <div>
        <select
          value={filtreStatut}
          onChange={(e) => setFiltreStatut(e.target.value)}
        >
          <option value="tous">Tous les statuts</option>
          <option value="en attente">En attente</option>
          <option value="validée">Validée</option>
          <option value="en préparation">En préparation</option>
          <option value="prête">Prête</option>
          <option value="récupérée">Récupérée</option>
          <option value="annulée">Annulée</option>
        </select>
      </div>
      <ul>
        {commandesFiltrees.map((cmd) => (
          <li key={cmd.id_command}>
            <strong>{cmd.number_command}</strong> — {cmd.status_command} —{" "}
            {cmd.price_total.toFixed(2)} €
            <ul>
              {cmd.command_lines.map((ligne) => (
                <li key={ligne.id_command_line}>
                  {nomsProduits[ligne.id_product] ??
                    `Produit #${ligne.id_product}`}{" "}
                  × {ligne.quantity} — {ligne.unit_price.toFixed(2)} € l'unité
                </li>
              ))}
            </ul>
            <select
              value={cmd.status_command}
              onChange={(e) => changerStatut(cmd.id_command, e.target.value)}
            >
              <option value="en attente">En attente</option>
              <option value="validée">Validée</option>
              <option value="en préparation">En préparation</option>
              <option value="prête">Prête</option>
              <option value="récupérée">Récupérée</option>
              <option value="annulée">Annulée</option>
            </select>
            <button
              onClick={() => {
                if (confirm(`Annuler la commande ${cmd.number_command} ?`)) {
                  changerStatut(cmd.id_command, "annulée");
                }
              }}
            >
              Annuler
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
