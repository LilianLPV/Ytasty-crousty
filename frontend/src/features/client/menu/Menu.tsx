import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { recupererRestaurant, listerMenu } from "./api";
import type { Restaurant } from "../../../types/restaurant";
import type { Product } from "../../../types/products";
import "./menu.css";

export function Menu() {
  const { id_restaurant } = useParams();
  const id = Number(id_restaurant);

  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [produits, setProduits] = useState<Product[]>([]);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState<string | null>(null);

  useEffect(() => {
    setChargement(true);
    Promise.all([recupererRestaurant(id), listerMenu(id)])
      .then(([resto, menu]) => {
        setRestaurant(resto);
        setProduits(menu);
      })
      .catch(() => setErreur("Impossible de charger le menu"))
      .finally(() => setChargement(false));
  }, [id]);

  if (chargement) return <p>Chargement…</p>;
  if (erreur) return <p>{erreur}</p>;
  if (!restaurant) return <p>Aucun restaurant trouvé</p>;

  // On regroupe les plats par catégorie
  const parCategorie = produits.reduce<Record<string, Product[]>>((acc, p) => {
    // acc = append / ??= si y a rien undefined
    (acc[p.category] ??= []).push(p);
    return acc;
  }, {});

  return (
    <div>
      <h1>{restaurant.name}</h1>
      <p>
        {restaurant.restaurant_address.city} —{" "}
        {restaurant.restaurant_address.address}
      </p>

      {produits.length === 0 && <p>Aucun plat disponible pour le moment.</p>}

      {Object.entries(parCategorie).map(([categorie, plats]) => (
        <section key={categorie}>
          <h2 className="titre-categorie">{categorie}</h2>
          <ul className="liste">
            {plats.map((p) => (
              <li key={p.id_product}>
                <div className="pictures">
                {p.pictures[0] && (
                  <img src={`/plats/${p.pictures[0].picture}`} alt={p.name} className="picture" />
                )}
                </div>
                <br />
                <strong>{p.name}</strong> — {p.price.toFixed(2)} €
                <br />
                {p.description}
                {!p.availability && <em> (indisponible)</em>}
              </li>
            ))}
          </ul>
        </section>
      ))}
    </div>
  );
}
