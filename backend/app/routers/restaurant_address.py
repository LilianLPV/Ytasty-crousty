from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.restaurant_address import RestaurantAddressRead, RestaurantAddressCreate
from app.utils.permissions import require_role
from app.models.user import User
from app.database import get_db
from app.services import restaurant_address_service

router = APIRouter(prefix="/restaurant_address", tags=["restaurant_address"])


# Lecture publique
@router.get("/", response_model=list[RestaurantAddressRead])
def liste_restaurant_address(db: Session = Depends(get_db)):
    return restaurant_address_service.lister_addresses(db)


@router.get("/{id_address}", response_model=RestaurantAddressRead)
def restaurant_address(id_address: int, db: Session = Depends(get_db)):
    return restaurant_address_service.get_address(db, id_address)


@router.post("/", response_model=RestaurantAddressRead, status_code=201)
def creer_restaurant_address(data: RestaurantAddressCreate, db: Session = Depends(get_db),
                            current_user: User = Depends(require_role("administrateur"))):
    return restaurant_address_service.creer_address(db, data)


@router.delete("/{id_address}", status_code=204)
def supprimer_restaurant_address(id_address: int, db: Session = Depends(get_db),
                                 current_user: User = Depends(require_role("administrateur"))):
    restaurant_address_service.supprimer_address(db, id_address)


@router.put("/{id_address}", response_model=RestaurantAddressRead)
def update_restaurant_address(id_address: int, data: RestaurantAddressCreate, db: Session = Depends(get_db),
                              current_user: User = Depends(require_role("administrateur"))):
    return restaurant_address_service.update_address(db, id_address, data)