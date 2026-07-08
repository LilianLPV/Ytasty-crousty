from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permissions import Permission
from app.schemas.permissions import PermissionsRead
from app.schemas.permissions import PermissionsCreate
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db

# On définit le rtouer avec un tag ou le /docs
router = APIRouter(prefix="/permissions", tags=["permissions"])

# On READ (liste) accessible à tout le monde
@router.get("/", response_model=list[PermissionsRead])
def liste_permission(db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # On récupère tous les restaurants en base
    return db.scalars(select(Permission)).all()

# READ (Détail) : Accessible à tout le monde
@router.get("/{id_permission}", response_model=PermissionsRead)
def permission(id_permission: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Cherche un resto par son ID
    perm = db.get(Permission, id_permission)
    if perm is None:
        raise HTTPException(status_code=404, detail="Permission introuvable")
    return perm

# CREATE : Protégé par get_current_user
@router.post("/", response_model=PermissionsRead, status_code=201)
def creer_permission(data: PermissionsCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Crée une instance avec les données validées par Pydantic (data.model_dump)
    perm = Permission(**data.model_dump())
    db.add(perm)
    db.commit() # Sauvegarde en base
    db.refresh(perm) # Recharge l'objet pour récupérer les ID générés par la BDD
    return perm

# DELETE : Protégé par get_current_user
@router.delete("/{id_permission}", status_code=204)
def supprimer_permission(id_permission: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    perm = db.get(Permission, id_permission)
    if perm is None:
        raise HTTPException(status_code=404, detail="Permission introuvable")
    db.delete(perm)
    db.commit()

# 5. UPDATE (PUT) : Protégé par get_current_user
@router.put("/{id_permission}", response_model=PermissionsRead)
def update_permission(id_permission: int, data: PermissionsCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    perm = db.get(Permission, id_permission)
    if perm is None:
        raise HTTPException(status_code=404, detail="Permission introuvable")
    # Parcourir la boucle pour appliquer le ou les changements sur les champ
    # 'setattr' modifie l'attribut de l'objet Python
    for champ, valeur in data.model_dump().items():
        setattr(perm, champ, valeur)
    db.commit()
    db.refresh(perm)
    return perm