from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductRead
from app.schemas.product import ProductCreate
from app.database import get_db

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=list[ProductRead])
def liste_product(db : Session = Depends(get_db)):
    return db.scalars(select(Product)).all()

@router.get("/{id_product}", response_model=ProductRead)
def product(id_product: int, db: Session = Depends(get_db)):
    prod = db.get(Product, id_product)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return prod

@router.post("/", response_model=ProductRead, status_code=201)
def creer_product(data: ProductCreate, db: Session = Depends(get_db)):
    prod = Product(**data.model_dump())
    db.add(prod)
    db.commit()
    db.refresh(prod)
    return prod

@router.delete("/{id_product}", status_code=204)
def supprimer_product(id_product: int, db: Session = Depends(get_db)):
    prod = db.get(Product, id_product)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    db.delete(prod)
    db.commit()

@router.put("/{id_product}", response_model=ProductRead)
def update_product(id_product: int, data: ProductCreate, db: Session = Depends(get_db)):
    prod = db.get(Product, id_product)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
     # Parcourir la boucle pour appliquer le ou les changements sur les champ
    for champ, valeur in data.model_dump().items():
        setattr(prod, champ, valeur)
    db.commit()
    db.refresh(prod)
    return prod