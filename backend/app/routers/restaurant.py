from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantRead
from app.schemas.restaurant import RestaurantCreate

from app.database import get_db

router = APIRouter(prefix="/restaurants", tags=["restaurants"])

@router.get("/", response_model=list[RestaurantRead])
def liste_restaurants(db : Session = Depends(get_db)):
    return db.scalars(select(Restaurant)).all()

@router.get("/{id_restaurant}", response_model=RestaurantRead)
def restaurant(id_restaurant: int, db: Session = Depends(get_db)):
    resto = db.get(Restaurant, id_restaurant)
    if resto is None:
        raise HTTPException(status_code=404, detail="Restaurant introuvable")
    return resto

@router.post("/", response_model=RestaurantRead, status_code=201)
def creer_restaurant(data: RestaurantCreate, db: Session = Depends(get_db)):
    resto = Restaurant(**data.model_dump())
    db.add(resto)
    db.commit()
    db.refresh(resto)
    return resto