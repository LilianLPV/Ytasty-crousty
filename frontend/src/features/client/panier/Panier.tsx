import { useState, useEffect } from "react";
import { Link } from "react-router";
import type { Product } from "../../../types/products";
import { passerCommande } from "../command/api";
import "./Panier.css";

export function Panier() {
  const [envoiEnCours, setEnvoiEnCours] = useState(false);
  const [numeroCommande, setNumeroCommande] = useState("");
  const [modeRetrait, setModeRetrait] = useState("sur place");
  const [panier, setPanier] = useState<Product[]>(() => {
    const sauvegarde = localStorage.getItem("mon_panier_react");
    return sauvegarde ? JSON.parse(sauvegarde) : [];
    });
  const idResto = Number(localStorage.getItem("id_resto"));


  const lines = panier.reduce(
    (acc, plat) => {
      const dejaLa = acc.find((ligne) => ligne.id_product === plat.id_product);
      if (dejaLa) {
        dejaLa.quantity += 1;
      } else {
        acc.push({ id_product: plat.id_product, quantity: 1 });
      }
      return acc;
    },
    [] as { id_product: number; quantity: number }[],
  );
  const envoyerCommande = async () => {
    const commande = {
      withdrawal_method: modeRetrait,
      customer_information: "Client",
      id_restaurant: idResto,
      lines: lines,
    };
    setEnvoiEnCours(true);
    try {
      const commandeCreee = await passerCommande(commande);
      setNumeroCommande(commandeCreee.number_command);
      setPanier([]);
    } catch (error) {
      console.error("Erreur lors de l'envoi de la commande :", error);
      alert("Une erreur est survenue lors de l'envoi de la commande.");
    } finally {
      setEnvoiEnCours(false);
    }
  };
  useEffect(() => {
    localStorage.setItem("mon_panier_react", JSON.stringify(panier));
  }, [panier]);

  const retirerDuPanier = (index: number) => {
    setPanier((ancien) => ancien.filter((_, i) => i !== index));
  };

  const total = panier.reduce((somme, plat) => somme + plat.price, 0);

  return (
    <div className="page-panier">
      <title>Ytasty Crousty</title>
      <h1>Récapitulatif de votre commande</h1>

      {numeroCommande ? (
        <div className="confirmation">
          <h2>Merci ! Votre commande est enregistrée.</h2>
          <p>
            Numéro de commande : <strong>{numeroCommande}</strong>
          </p>
          <Link to="/">Retour à l'accueil</Link>
        </div>
      ) : panier.length === 0 ? (
        <div>
          <p>Votre panier est vide.</p>
          <Link to="/">Retourner au menu</Link>
        </div>
      ) : (
        <>
          <ul className="liste-panier">
            {panier.map((plat, index) => (
              <li key={index} className="panier-item">
                <div className="panier-item-info">
                  <strong>{plat.name}</strong>
                  <span>— {plat.price.toFixed(2)} €</span>
                </div>
                <button
                  onClick={() => retirerDuPanier(index)}
                  className="bouton-supprimer"
                >
                  Retirer
                </button>
              </li>
            ))}
          </ul>

          <select
            className="select-retrait"
            value={modeRetrait}
            onChange={(e) => setModeRetrait(e.target.value)}
          >
            <option value="sur place">Sur place</option>
            <option value="à emporter">À emporter</option>
          </select>

          <div className="total-commande">
            <h3>Total à payer : {total.toFixed(2)} €</h3>
            <button
              className="bouton-payer"
              onClick={envoyerCommande}
              disabled={envoiEnCours}
            >
              {envoiEnCours ? "Envoi..." : "Passer la commande"}
            </button>
          </div>

          <br />
          <Link to={`/restaurants/${idResto}/menu`}>Retour au menu</Link>
        </>
      )}
    </div>
  );
}
