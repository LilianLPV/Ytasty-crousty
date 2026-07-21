import { useState, useEffect } from "react";
import { useLocation, Link } from "react-router";
import type { Product } from "../../../types/products";
import "./panier.css";

export function Panier() {
  const location = useLocation();
  const idResto = location.state?.idResto;
  const [panier, setPanier] = useState<Product[]>(() => {
    if (
      location.state?.panierSauvegarde &&
      location.state.panierSauvegarde.length > 0
    ) {
      return location.state.panierSauvegarde;
    }

    const sauvegarde = localStorage.getItem("mon_panier_react");
    if (sauvegarde) {
      return JSON.parse(sauvegarde);
    }

    return [];
  });

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
      {panier.length === 0 ? (
        <div>
          <p>Votre panier est vide.</p>
          <Link to="/">Retourner au menu</Link>
        </div>
      ) : (
        <>
          <ul className="liste-panier">
            {panier.map((plat, index) => (
              <li key={index}>
                <strong>{plat.name}</strong> — {plat.price.toFixed(2)} €
                <button onClick={() => retirerDuPanier(index)}>Retirer</button>
              </li>
            ))}
          </ul>

          <div className="total-commande">
            <h3>Total à payer : {total.toFixed(2)} €</h3>
            <button className="bouton-payer">Passer la commande</button>
          </div>

          <br />
          <Link to={`/restaurants/${idResto}/menu`}>Retour au menu</Link>
        </>
      )}
    </div>
  );
}
