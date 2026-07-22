import { Navigate } from "react-router";
import type { ReactNode } from "react";

export function RouteProtegee({ children }: { children: ReactNode }) {
  const token = localStorage.getItem("token");

  if (!token) {
    // redirection si pas connecté
    return <Navigate to="/login" />;
  }
  //affichage du contenu si il est connecté
  return children;
}