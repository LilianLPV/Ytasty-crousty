import { useEffect, useState } from "react";
import { listerRestaurants } from "./api";
import "./ChoixRestaurant.css";
import { Link } from "react-router";
import type { Restaurant } from "../../../types/restaurant";

export function ChoixRestaurant() {
  const [restaurants, setRestaurants] = useState<Restaurant[]>([]);
  const [erreur, setErreur] = useState<string | null>(null);
  const [chargement, setChargement] = useState(true);

  useEffect(() => {
    listerRestaurants()
      .then(setRestaurants)
      .catch((e: Error) => setErreur(e.message))
      .finally(() => setChargement(false));
  }, []);

  if (chargement) return <p>Chargement…</p>;
  if (erreur) return <p>Erreur : {erreur}</p>;

  return (
    <div>
      <title>Ytasty Crousty</title>
      <h1>Où voulez-vous commander ?</h1>
      <ul className="liste-restaurants">
        {restaurants.map((r) => (
          <li key={r.id_restaurant}>
            <Link to={`/restaurants/${r.id_restaurant}/menu`}>
              {r.restaurant_address.city}{" "}
            </Link>
          </li>
        ))}
      </ul>
      <Link to="/login">Se connecter</Link>
      <br />
      <Link to="/suivre-commande">Suivre ma commande</Link>
    </div>
  );
}
