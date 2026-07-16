from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.permissions import Permission
from app.schemas.permissions import PermissionsCreate


def lister_permissions(db: Session):
    return db.scalars(select(Permission)).all()


def get_permission(db: Session, id_permission: int) -> Permission:
    perm = db.get(Permission, id_permission)
    if perm is None:
        raise HTTPException(status_code=404, detail="Permission introuvable")
    return perm


def creer_permission(db: Session, data: PermissionsCreate) -> Permission:
    perm = Permission(**data.model_dump())
    db.add(perm)
    db.commit()
    db.refresh(perm)
    return perm


def supprimer_permission(db: Session, id_permission: int) -> None:
    perm = get_permission(db, id_permission)
    db.delete(perm)
    db.commit()


def update_permission(db: Session, id_permission: int, data: PermissionsCreate) -> Permission:
    perm = get_permission(db, id_permission)
    for champ, valeur in data.model_dump().items():
        setattr(perm, champ, valeur)
    db.commit()
    db.refresh(perm)
    return perm