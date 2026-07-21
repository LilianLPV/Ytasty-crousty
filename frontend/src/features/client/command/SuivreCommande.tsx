import "./SuivreCommande.css";
import { useState } from "react";
import { suivreCommande } from "./api";
import type { Command } from "../../../types/commands";

export function SuivreCommande() {
  const [numeroCommande, setNumeroCommande] = useState("");
  const [commande, setCommande] = useState<Command | null>(null);
  const [erreur, setErreur] = useState<string | null>(null);
  const [chargement, setChargement] = useState(false);

  const rechercher = async () => {
    setChargement(true);
    setErreur(null);
    try {
      const resultat = await suivreCommande(numeroCommande);
      setCommande(resultat);
    } catch {
      setErreur("Commande introuvable");
      setCommande(null);
    } finally {
      setChargement(false);
    }
  };

  return (
    <div className="page-suivi">
      <h1>Suivre ma commande</h1>
      <input
        type="text"
        placeholder="Numéro de commande (ex: CMD-0001)"
        value={numeroCommande}
        onChange={(e) => setNumeroCommande(e.target.value)}
      />
      <button onClick={rechercher} disabled={chargement}>
        {chargement ? "Recherche..." : "Suivre"}
      </button>

      {erreur && <p>{erreur}</p>}

      {commande && (
        <div className="resultat-suivi">
          <h2>Commande {commande.number_command}</h2>
          <p>
            Statut : <strong>{commande.status_command}</strong>
          </p>
          <p>Mode de retrait : {commande.withdrawal_method}</p>
          <p>Total : {commande.price_total.toFixed(2)} €</p>
        </div>
      )}
    </div>
  );
}