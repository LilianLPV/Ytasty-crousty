from app.models.base import engine
from app.models.user import User
from app.models.role import Role
from app.utils.jwt import hash_password
from sqlalchemy.orm import Session
from sqlalchemy import select
import os
from dotenv import load_dotenv

load_dotenv()

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")

# On ouvre une session de la BDD
with Session(engine) as session:
    # On vérifie si le rôle administrateur est crée
    role_admin = session.scalars(
        select(Role).where(Role.role_name == "administrateur")
    ).first()
    # Si le rôle n'existe pas on le crée
    if role_admin is None:
        role_admin = Role(role_name="administrateur")
        # On le synchornise avec la bdd
        session.add(role_admin)
        session.flush() 
    # Vérification de l'utilisateur dmin
    admin_existe = session.scalars(
        select(User).where(User.username == "admin")
    ).first()
    # Si le l'utilisateur admin n'existe pas on inscrit les données
    if admin_existe is None:
        admin = User(
            name="Admin",
            first_name="Super",
            username=ADMIN_USERNAME, # Dans votre .env
            password=hash_password(ADMIN_PASSWORD),  # Dans votre .env
            id_role=role_admin.id_role,
        )
        session.add(admin)
        # On valide tout et on envoie
        session.commit()
        print("Admin créé : username={ADMIN_USERNAME}")
    else:
        # Si l'utilisateur existe déjà
        print("L'admin existe déjà, rien à faire.")