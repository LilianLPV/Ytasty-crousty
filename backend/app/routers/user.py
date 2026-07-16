from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserRead, UserCreate, UserUpdate
from app.utils.permissions import require_role
from app.utils.jwt import get_current_user
from app.database import get_db
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])


# Récupère la liste de tous les utilisateurs
@router.get("/", response_model=list[UserRead])
def liste_user(db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur"))):
    return user_service.lister_users(db)

# Récupère les informations d'un utilisateur via son ID
@router.get("/{id_user}", response_model=UserRead)
def user(id_user: int, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    return user_service.get_user(db, id_user)

# Création d'un nouvel utilisateur avec hashage et vérification de l'username
@router.post("/", response_model=UserRead, status_code=201)
def creer_user(data: UserCreate, db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur"))):
    return user_service.creer_user(db, data)

# Suppression définitive d'un utilisateur
@router.delete("/{id_user}", status_code=204)
def supprimer_user(id_user: int, db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur"))):
    user_service.supprimer_user(db, id_user)

# Met à jour les information d'un utilisateur grâce à son ID
@router.put("/{id_user}", response_model=UserRead)
def update_user(id_user: int, data: UserUpdate, db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur"))):
    return user_service.update_user(db, id_user, data)