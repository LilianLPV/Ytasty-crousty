from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.restaurant_address import Restaurant_address
from app.schemas.restaurant_address import RestaurantAddressRead
from app.schemas.restaurant_address import RestaurantAddressCreate
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db

# On définit le rtouer avec un tag ou le /docs
router = APIRouter(prefix="/restaurant_address", tags=["restaurant_address"])

# On READ (liste) accessible à tout le monde
@router.get("/", response_model=list[RestaurantAddressRead])
def liste_restaurant_address(db : Session = Depends(get_db)):
    # On récupère tous les restaurants en base
    return db.scalars(select(Restaurant_address)).all()

# READ (Détail) : Accessible à tout le monde
@router.get("/{id_address}", response_model=RestaurantAddressRead)
def restaurant_address(id_address: int, db: Session = Depends(get_db)):
    # Cherche un resto par son ID
    restoaddress = db.get(Restaurant_address, id_address)
    if restoaddress is None:
        raise HTTPException(status_code=404, detail="Adresse du restaurant introuvable")
    return restoaddress

# CREATE : Protégé par get_current_user
@router.post("/", response_model=RestaurantAddressRead, status_code=201)
def creer_restaurant_address(data: RestaurantAddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    # Crée une instance avec les données validées par Pydantic (data.model_dump)
    restoaddress = Restaurant_address(**data.model_dump())
    db.add(restoaddress)
    db.commit() # Sauvegarde en base
    db.refresh(restoaddress) # Recharge l'objet pour récupérer les ID générés par la BDD
    return restoaddress

# DELETE : Protégé par get_current_user
@router.delete("/{id_address}", status_code=204)
def supprimer_restaurant_address(id_address: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    restoaddress = db.get(Restaurant_address, id_address)
    if restoaddress is None:
        raise HTTPException(status_code=404, detail="Adresse du restaurant introuvable")
    db.delete(restoaddress)
    db.commit()

# 5. UPDATE (PUT) : Protégé par get_current_user
@router.put("/{id_address}", response_model=RestaurantAddressRead)
def update_restaurant_address(id_address: int, data: RestaurantAddressCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    restoaddress = db.get(Restaurant_address, id_address)
    if restoaddress is None:
        raise HTTPException(status_code=404, detail="Adresse du restaurant introuvable")
    # Parcourir la boucle pour appliquer le ou les changements sur les champ
    # 'setattr' modifie l'attribut de l'objet Python
    for champ, valeur in data.model_dump().items():
        setattr(restoaddress, champ, valeur)
    db.commit()
    db.refresh(restoaddress)
    return restoaddress