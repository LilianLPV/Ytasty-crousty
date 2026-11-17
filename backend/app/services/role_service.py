from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.role import Role
from app.schemas.role import RoleCreate


def lister_roles(db: Session):
    return db.scalars(select(Role)).all()


def get_role(db: Session, id_role: int) -> Role:
    rol = db.get(Role, id_role)
    if rol is None:
        raise HTTPException(status_code=404, detail="Rôle introuvable")
    return rol


def creer_role(db: Session, data: RoleCreate) -> Role:
    rol = Role(**data.model_dump())
    db.add(rol)
    db.commit()
    db.refresh(rol)
    return rol


def supprimer_role(db: Session, id_role: int) -> None:
    rol = get_role(db, id_role)
    db.delete(rol)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ce rôle est attribué à des utilisateurs et ne peut pas être supprimé",
        )


def update_role(db: Session, id_role: int, data: RoleCreate) -> Role:
    rol = get_role(db, id_role)
    for champ, valeur in data.model_dump().items():
        setattr(rol, champ, valeur)
    db.commit()
    db.refresh(rol)
    return rol