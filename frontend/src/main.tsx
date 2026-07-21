import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import "./index.css";
import { ChoixRestaurant } from "./features/client/choix-restaurant/ChoixRestaurant.tsx";
import { Menu } from "./features/client/menu/Menu.tsx";
import { Panier } from "./features/client/panier/Panier.tsx";
import { SuivreCommande } from "./features/client/command/SuivreCommande.tsx";
const root = document.getElementById("root")!;

ReactDOM.createRoot(root).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<ChoixRestaurant />} />
      <Route path="/restaurants/:id_restaurant/menu" element={<Menu />} />
      <Route path="/panier" element={<Panier />} />
      <Route path="/suivre-commande" element={<SuivreCommande />} />
    </Routes>
  </BrowserRouter>,
);
