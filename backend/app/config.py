"""Configuration de l'API, lue uniquement depuis les variables d'environnement.

En local, les valeurs viennent du fichier .env (voir .env.example).
Sur Scalingo, elles sont définies dans les variables d'environnement de l'app.
"""
import os

from dotenv import load_dotenv

load_dotenv()


def get_database_url() -> str:
    """Retourne l'URL de la base au format attendu par SQLAlchemy + psycopg 3.

    Sur Scalingo, l'addon PostgreSQL fournit SCALINGO_POSTGRESQL_URL (et son alias
    DATABASE_URL) au format postgres:// ou postgresql://. SQLAlchemy a besoin de
    postgresql+psycopg:// pour utiliser le pilote psycopg 3 installé.
    """
    url = os.getenv("DATABASE_URL") or os.getenv("SCALINGO_POSTGRESQL_URL")
    if not url:
        raise RuntimeError(
            "DATABASE_URL n'est pas définie : copiez .env.example en .env en local, "
            "ou ajoutez l'addon PostgreSQL sur Scalingo."
        )
    for prefix in ("postgres://", "postgresql://"):
        if url.startswith(prefix):
            return "postgresql+psycopg://" + url[len(prefix):]
    return url


def get_cors_origins() -> list[str]:
    """Origines autorisées à appeler l'API, séparées par des virgules."""
    raw = os.getenv("CORS_ORIGINS", "http://localhost:5173")
    return [origin.strip().rstrip("/") for origin in raw.split(",") if origin.strip()]

