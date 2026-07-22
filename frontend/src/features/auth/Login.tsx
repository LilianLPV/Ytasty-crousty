import { useState } from "react";
import { login } from "./auth";
import "./Login.css";
import { useNavigate } from "react-router";
export function ConnexionUtilisateur() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();
  const seConnecter = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    try {
      const reponse = await login(username, password);
      localStorage.setItem("token", reponse.access_token);
      console.log("connexion OK, redirection...");
      navigate("/staff/commandes");
    } catch (error) {
      console.error("Erreur lors de la connexion :", error);
    }
  };

  return (
    <div className="login-container">
      <title>Ytasty Crousty</title>
      <h1>Connexion</h1>
      <form onSubmit={seConnecter}>
        <input
          type="text"
          placeholder="Nom d'utilisateur"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
        />
        <input
          type="password"
          placeholder="Mot de passe"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button type="submit">Se connecter</button>
      </form>
    </div>
  );
}
