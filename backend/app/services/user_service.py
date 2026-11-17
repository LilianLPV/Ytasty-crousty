from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.utils.jwt import hash_password

# On récupère la liste des tous les utilisateurs 
def lister_users(db : Session):
    return db.scalars(select(User)).all()

# Récupération d'un utilisateur spécifique grâce à son ID
def get_user(db: Session, id_user: int) -> User:
    usr = db.get(User, id_user)
    if usr is None:
        raise HTTPException(status_code=404, detail="Utilisateur introuvable")
    return usr

# On vérifie si l'username est déjà pris si oui erreur 409
def verifier_username_libre(db: Session, username: str, id_user: int | None = None) -> None:
    requete = select(User).where(User.username == username)
    if id_user is not None:
        requete = requete.where(User.id_user != id_user)   # on s'exclut soi-même
    if db.scalars(requete).first() is not None:
        raise HTTPException(status_code=409, detail="Cet identifiant est déjà utilisé")

# Création d'un nouveau user après avoir vérifier son username et hashé son mdp
def creer_user(db: Session, data: UserCreate) -> User:
    verifier_username_libre(db, data.username)

    user_data = data.model_dump()
    user_data["password"] = hash_password(data.password)
    usr = User(**user_data)
    db.add(usr)
    db.commit()
    db.refresh(usr)
    return usr

# Supprésion d'un utilisateur par son ID
def supprimer_user(db: Session, id_user: int) -> None:
    usr = get_user(db, id_user)
    db.delete(usr)
    db.commit()

# Met à jour les informations d'un utilisateur existant.
def update_user(db: Session, id_user: int, data: UserUpdate) -> User:
    usr = get_user(db, id_user)

    user_data = data.model_dump(exclude_unset=True)
    # Uniquement si un nouvel identifiant est trouvé
    if "username" in user_data:
        verifier_username_libre(db, user_data["username"], id_user=id_user)

    # Si changement de mdp alors on le hash de nouveau
    if "password" in user_data:
        user_data["password"] = hash_password(user_data["password"])

     # Parcourir la boucle pour appliquer le ou les changements sur les champ
    for champ, valeur in user_data.items():
        setattr(usr, champ, valeur)
    db.commit()
    db.refresh(usr)
    return usr