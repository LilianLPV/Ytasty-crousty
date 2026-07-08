from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.restaurant import Restaurant
from app.schemas.restaurant import RestaurantRead
from app.schemas.restaurant import RestaurantCreate
from app.utils.jwt import get_current_user
from app.models.user import User
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
def creer_restaurant(data: RestaurantCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resto = Restaurant(**data.model_dump())
    db.add(resto)
    db.commit()
    db.refresh(resto)
    return resto

@router.delete("/{id_restaurant}", status_code=204)
def supprimer_restaurant(id_restaurant: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resto = db.get(Restaurant, id_restaurant)
    if resto is None:
        raise HTTPException(status_code=404, detail="Restaurant introuvable")
    db.delete(resto)
    db.commit()

@router.put("/{id_restaurant}", response_model=RestaurantRead)
def update_restaurant(id_restaurant: int, data: RestaurantCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    resto = db.get(Restaurant, id_restaurant)
    if resto is None:
        raise HTTPException(status_code=404, detail="Restaurant introuvable")
     # Parcourir la boucle pour appliquer le ou les changements sur les champ
    for champ, valeur in data.model_dump().items():
        setattr(resto, champ, valeur)
    db.commit()
    db.refresh(resto)
    return resto