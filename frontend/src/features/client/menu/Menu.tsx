import "./Menu.css";
import { useEffect, useState } from "react";
import { useParams } from "react-router";
import { recupererRestaurant, listerMenu } from "./api";
import type { Restaurant } from "../../../types/restaurant";
import { Link } from "react-router";
import type { Product } from "../../../types/products";

export function Menu() {
  const { id_restaurant } = useParams();
  const id = Number(id_restaurant);
  const [produitSelectionne, setProduitSelectionne] = useState<Product | null>(
    null,
  );
  const [categorieActive, setCategorieActive] = useState("all");
  const [recherche, setRecherche] = useState("");
  const [restaurant, setRestaurant] = useState<Restaurant | null>(null);
  const [produits, setProduits] = useState<Product[]>([]);
  const [chargement, setChargement] = useState(true);
  const [erreur, setErreur] = useState<string | null>(null);
  const [panier, setPanier] = useState<Product[]>(() => {
    const sauvegarde = localStorage.getItem("mon_panier_react");
    return sauvegarde ? JSON.parse(sauvegarde) : [];
  });
  useEffect(() => {
    localStorage.setItem("mon_panier_react", JSON.stringify(panier));
  }, [panier]);
  useEffect(() => {
    localStorage.setItem("id_resto", String(id));
  }, [id]);
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

  const produitsFiltres = produits.filter((p) =>
    p.name.toLowerCase().includes(recherche.toLowerCase()),
  );
  // On regroupe les plats par catégorie
  const parCategorie = produitsFiltres.reduce<Record<string, Product[]>>(
    (acc, p) => {
      (acc[p.category] ??= []).push(p);
      return acc;
    },
    {},
  );
  const panierGroupe = panier.reduce(
    (acc, plat) => {
      const dejaLa = acc.find(
        (ligne) => ligne.plat.id_product === plat.id_product,
      );
      if (dejaLa) dejaLa.quantity += 1;
      else acc.push({ plat: plat, quantity: 1 });
      return acc;
    },
    [] as { plat: Product; quantity: number }[],
  );
  const retirerUnExemplaire = (id_product: number) => {
    setPanier((prev) => {
      const index = prev.findIndex((plat) => plat.id_product === id_product);
      if (index === -1) return prev;
      return prev.filter((_, i) => i !== index);
    });
  };

  const ajouterAuPanier = (plat: Product) => {
    setPanier((prevPanier) => [...prevPanier, plat]);
  };

  return (
    <div>
      <title>Ytasty Crousty</title>

      <h1>{restaurant.name}</h1>
      <p>
        {restaurant.restaurant_address.city} —{" "}
        {restaurant.restaurant_address.address}
      </p>
      <section className="panier">
        <Link to="/panier" className="bouton-panier">
          Valider mon panier ({panier.length} articles)
        </Link>
        {produits.length === 0 && <p>Aucun plat disponible pour le moment.</p>}
        <h2>Mon panier</h2>
        <ul className="panier">
          {panierGroupe.map((ligne) => (
            <li key={ligne.plat.id_product}>
              {ligne.plat.name} — {ligne.plat.price.toFixed(2)} € ×{" "}
              {ligne.quantity}
              <button onClick={() => ajouterAuPanier(ligne.plat)}>+</button>
              <button
                onClick={() => retirerUnExemplaire(ligne.plat.id_product)}
              >
                -
              </button>
            </li>
          ))}
        </ul>
      </section>
      <input
        type="text"
        placeholder="Rechercher un plat..."
        value={recherche}
        onChange={(e) => setRecherche(e.target.value)}
      />
      <div className="filtres-categories">
        <button onClick={() => setCategorieActive("all")}>Tout</button>
        {Object.keys(parCategorie).map((cat) => (
          <button key={cat} onClick={() => setCategorieActive(cat)}>
            {cat}
          </button>
        ))}
      </div>
      {Object.entries(parCategorie).map(([categorie, plats]) => {
        if (categorieActive !== "all" && categorie !== categorieActive) {
          return null;
        }
        return (
          <section key={categorie}>
            <h2 className="titre-categorie">{categorie}</h2>
            <ul className="liste">
              {plats.map((p) => (
                <li key={p.id_product}>
                  <div className="pictures">
                    {p.pictures[0] && (
                      <img
                        src={`/plats/${p.pictures[0].picture}`}
                        alt={p.name}
                        className="picture"
                        onClick={() => setProduitSelectionne(p)}
                      />
                    )}
                  </div>
                  <br />
                  <strong>{p.name}</strong> — {p.price.toFixed(2)} €
                  <br />
                  {p.description}
                  {!p.availability && <em> (indisponible)</em>}
                  <button onClick={() => ajouterAuPanier(p)}>+</button>
                </li>
              ))}
            </ul>
          </section>
        );
      })}
    {produitSelectionne && (
        <div
          className="modale-fond"
          onClick={() => setProduitSelectionne(null)}
        >
          <div className="modale-contenu" onClick={(e) => e.stopPropagation()}>
            <button
              className="modale-fermer"
              onClick={() => setProduitSelectionne(null)}
            >
              ✕
            </button>
            {produitSelectionne.pictures[0] && (
              <img
                src={`/plats/${produitSelectionne.pictures[0].picture}`}
                alt={produitSelectionne.name}
                className="modale-image"
              />
            )}
            <h2>{produitSelectionne.name}</h2>
            <p className="modale-prix">
              {produitSelectionne.price.toFixed(2)} €
            </p>
            <p>{produitSelectionne.description}</p>
            {!produitSelectionne.availability && (
              <p>
                <em>Actuellement indisponible</em>
              </p>
            )}
            <button
              onClick={() => {
                ajouterAuPanier(produitSelectionne);
                setProduitSelectionne(null);
              }}
            >
              Ajouter au panier
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
