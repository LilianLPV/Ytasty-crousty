import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase

# Lecture du fichier .env

load_dotenv() 

# Création de l'ORM
class Base(DeclarativeBase):
    pass

# Connexion à la BDD
engine = create_engine(os.getenv("DATABASE_URL"))