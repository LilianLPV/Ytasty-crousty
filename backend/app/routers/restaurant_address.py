from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.restaurant_address import Restaurant_address
from app.schemas.restaurant_address import RestaurantAddressRead
from app.schemas.restaurant_address import RestaurantAddressCreate

from app.database import get_db

router = APIRouter(prefix="/restaurant_address", tags=["restaurant_address"])

@router.get("/", response_model=list[RestaurantAddressRead])
def liste_restaurant_address(db : Session = Depends(get_db)):
    return db.scalars(select(Restaurant_address)).all()

@router.get("/{id_address}", response_model=RestaurantAddressRead)
def restaurant_address(id_address: int, db: Session = Depends(get_db)):
    restoaddress = db.get(Restaurant_address, id_address)
    if restoaddress is None:
        raise HTTPException(status_code=404, detail="Adresse du restaurant introuvable")
    return restoaddress

@router.post("/", response_model=RestaurantAddressRead, status_code=201)
def creer_restaurant_address(data: RestaurantAddressCreate, db: Session = Depends(get_db)):
    restoaddress = Restaurant_address(**data.model_dump())
    db.add(restoaddress)
    db.commit()
    db.refresh(restoaddress)
    return restoaddress