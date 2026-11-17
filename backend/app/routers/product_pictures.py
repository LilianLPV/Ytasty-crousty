from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.product_pictures import ProductPictureRead, ProductPictureCreate
from app.utils.permissions import require_role
from app.models.user import User
from app.database import get_db
from app.services import product_picture_service

router = APIRouter(prefix="/product_pictures", tags=["product_pictures"])


# Lecture publique (le client voit les images de la carte)
@router.get("/", response_model=list[ProductPictureRead])
def liste_pictures(db: Session = Depends(get_db)):
    return product_picture_service.lister_pictures(db)


@router.get("/{id_picture}", response_model=ProductPictureRead)
def picture(id_picture: int, db: Session = Depends(get_db)):
    return product_picture_service.get_picture(db, id_picture)


@router.post("/", response_model=ProductPictureRead, status_code=201)
def creer_picture(data: ProductPictureCreate, db: Session = Depends(get_db),
                  current_user: User = Depends(require_role("administrateur", "personnel"))):
    return product_picture_service.creer_picture(db, data, current_user)


@router.delete("/{id_picture}", status_code=204)
def supprimer_picture(id_picture: int, db: Session = Depends(get_db),
                      current_user: User = Depends(require_role("administrateur", "personnel"))):
    product_picture_service.supprimer_picture(db, id_picture, current_user)