from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.restaurant import RestaurantRead, RestaurantCreate
from app.utils.permissions import require_role
from app.models.user import User
from app.database import get_db
from app.services import restaurant_service

router = APIRouter(prefix="/restaurants", tags=["restaurants"])


# Lecture publique : le client doit voir où commander
@router.get("/", response_model=list[RestaurantRead])
def liste_restaurants(db: Session = Depends(get_db)):
    return restaurant_service.lister_restaurants(db)


@router.get("/{id_restaurant}", response_model=RestaurantRead)
def restaurant(id_restaurant: int, db: Session = Depends(get_db)):
    return restaurant_service.get_restaurant(db, id_restaurant)


@router.post("/", response_model=RestaurantRead, status_code=201)
def creer_restaurant(data: RestaurantCreate, db: Session = Depends(get_db),
                     current_user: User = Depends(require_role("administrateur"))):
    return restaurant_service.creer_restaurant(db, data)


@router.delete("/{id_restaurant}", status_code=204)
def supprimer_restaurant(id_restaurant: int, db: Session = Depends(get_db),
                         current_user: User = Depends(require_role("administrateur"))):
    restaurant_service.supprimer_restaurant(db, id_restaurant)


@router.put("/{id_restaurant}", response_model=RestaurantRead)
def update_restaurant(id_restaurant: int, data: RestaurantCreate, db: Session = Depends(get_db),
                      current_user: User = Depends(require_role("administrateur"))):
    return restaurant_service.update_restaurant(db, id_restaurant, data)