from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permissions import Permission
from app.schemas.permissions import PermissionsRead
from app.schemas.permissions import PermissionsCreate
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db

router = APIRouter(prefix="/permissions", tags=["permissions"])

@router.get("/", response_model=list[PermissionsRead])
def liste_permission(db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.scalars(select(Permission)).all()

@router.get("/{id_permission}", response_model=PermissionsRead)
def permission(id_permission: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    perm = db.get(Permission, id_permission)
    if perm is None:
        raise HTTPException(status_code=404, detail="Permission introuvable")
    return perm

@router.post("/", response_model=PermissionsRead, status_code=201)
def creer_permission(data: PermissionsCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    perm = Permission(**data.model_dump())
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm

@router.delete("/{id_permission}", status_code=204)
def supprimer_permission(id_permission: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    perm = db.get(Permission, id_permission)
    if perm is None:
        raise HTTPException(status_code=404, detail="Permission introuvable")
    db.delete(perm)
    db.commit()

@router.put("/{id_permission}", response_model=PermissionsRead)
def update_permission(id_permission: int, data: PermissionsCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    perm = db.get(Permission, id_permission)
    if perm is None:
        raise HTTPException(status_code=404, detail="Permission introuvable")
     # Parcourir la boucle pour appliquer le ou les changements sur les champ
    for champ, valeur in data.model_dump().items():
        setattr(perm, champ, valeur)
    db.commit()
    db.refresh(perm)
    return perm