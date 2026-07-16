from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantCreate


def lister_restaurants(db: Session):
    return db.scalars(select(Restaurant)).all()


def get_restaurant(db: Session, id_restaurant: int) -> Restaurant:
    resto = db.get(Restaurant, id_restaurant)
    if resto is None:
        raise HTTPException(status_code=404, detail="Restaurant introuvable")
    return resto


def creer_restaurant(db: Session, data: RestaurantCreate) -> Restaurant:
    resto = Restaurant(**data.model_dump())
    db.add(resto)
    db.commit()
    db.refresh(resto)
    return resto


def supprimer_restaurant(db: Session, id_restaurant: int) -> None:
    resto = get_restaurant(db, id_restaurant)
    db.delete(resto)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()  
        raise HTTPException(
            status_code=409,
            detail="Ce restaurant a des produits ou des commandes et ne peut pas être supprimé",
        )


def update_restaurant(db: Session, id_restaurant: int, data: RestaurantCreate) -> Restaurant:
    resto = get_restaurant(db, id_restaurant)
    for champ, valeur in data.model_dump().items():
        setattr(resto, champ, valeur)
    db.commit()
    db.refresh(resto)
    return resto