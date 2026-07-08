from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.role import Role
from app.schemas.role import RoleRead
from app.schemas.role import RoleCreate 
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db

# On définit le rtouer avec un tag ou le /docs
router = APIRouter(prefix="/roles", tags=["roles"])

# On READ (liste) accessible à tout le monde
@router.get("/", response_model=list[RoleRead])
def liste_role(db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # On récupère tous les restaurants en base
    return db.scalars(select(Role)).all()

# READ (Détail) : Accessible à tout le monde
@router.get("/{id_role}", response_model=RoleRead)
def role(id_role: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rol = db.get(Role, id_role)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rôle introuvable")
    return rol

# CREATE : Protégé par get_current_user
@router.post("/", response_model=RoleRead, status_code=201)
def creer_role(data: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Crée une instance avec les données validées par Pydantic (data.model_dump)
    rol = Role(**data.model_dump())
    db.add(rol)
    db.commit() # Sauvegarde en base
    db.refresh(rol) # Recharge l'objet pour récupérer les ID générés par la BDD
    return rol

# DELETE : Protégé par get_current_user
@router.delete("/{id_role}", status_code=204)
def supprimer_role(id_role: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rol = db.get(Role, id_role)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rôle introuvable")
    db.delete(rol)
    db.commit()

@router.put("/{id_role}", response_model=RoleRead)
def update_role(id_role: int, data: RoleCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    rol = db.get(Role, id_role)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rôle introuvable")
     # Parcourir la boucle pour appliquer le ou les changements sur les champ
    for champ, valeur in data.model_dump().items():
        setattr(rol, champ, valeur)
    db.commit()
    db.refresh(rol)
    return rol

