from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

from app.config import get_database_url


# Création de l'ORM
class Base(DeclarativeBase):
    pass


# Connexion à la BDD (URL lue depuis l'environnement, voir app/config.py)
# pool_pre_ping évite les erreurs sur une connexion fermée par le serveur
engine = create_engine(get_database_url(), pool_pre_ping=True)
