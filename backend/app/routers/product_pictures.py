from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product_pictures import Product_picture
from app.schemas.product_pictures import ProductPictureRead, ProductPictureCreate
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db

router = APIRouter(prefix="/product_pictures", tags=["product_pictures"])

# Lecture publique (le client voit les images de la carte)
@router.get("/", response_model=list[ProductPictureRead])
def liste_pictures(db: Session = Depends(get_db)):
    return db.scalars(select(Product_picture)).all()

@router.get("/{id_picture}", response_model=ProductPictureRead)
def picture(id_picture: int, db: Session = Depends(get_db)):
    pic = db.get(Product_picture, id_picture)
    if pic is None:
        raise HTTPException(status_code=404, detail="Image introuvable")
    return pic

# Création protégée (seul le personnel ajoute des images)
@router.post("/", response_model=ProductPictureRead, status_code=201)
def creer_picture(data: ProductPictureCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    pic = Product_picture(**data.model_dump())
    db.add(pic)
    db.commit()
    db.refresh(pic)
    return pic

# Suppression protégée
@router.delete("/{id_picture}", status_code=204)
def supprimer_picture(id_picture: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    pic = db.get(Product_picture, id_picture)
    if pic is None:
        raise HTTPException(status_code=404, detail="Image introuvable")
    db.delete(pic)
    db.commit()