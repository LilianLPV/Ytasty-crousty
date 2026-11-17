from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.restaurant_address import Restaurant_address
from app.schemas.restaurant_address import RestaurantAddressCreate


def lister_addresses(db: Session):
    return db.scalars(select(Restaurant_address)).all()


def get_address(db: Session, id_address: int) -> Restaurant_address:
    restoaddress = db.get(Restaurant_address, id_address)
    if restoaddress is None:
        raise HTTPException(status_code=404, detail="Adresse du restaurant introuvable")
    return restoaddress


def creer_address(db: Session, data: RestaurantAddressCreate) -> Restaurant_address:
    restoaddress = Restaurant_address(**data.model_dump())
    db.add(restoaddress)
    db.commit()
    db.refresh(restoaddress)
    return restoaddress


def supprimer_address(db: Session, id_address: int) -> None:
    restoaddress = get_address(db, id_address)
    db.delete(restoaddress)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Cette adresse est utilisée par un restaurant et ne peut pas être supprimée",
        )


def update_address(db: Session, id_address: int, data: RestaurantAddressCreate) -> Restaurant_address:
    restoaddress = get_address(db, id_address)
    for champ, valeur in data.model_dump().items():
        setattr(restoaddress, champ, valeur)
    db.commit()
    db.refresh(restoaddress)
    return restoaddress