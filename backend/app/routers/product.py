from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product import Product
from app.schemas.product import ProductRead
from app.schemas.product import ProductCreate
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db

# On définit le rtouer avec un tag ou le /docs
router = APIRouter(prefix="/products", tags=["products"])

# On READ (liste) accessible à tout le monde
@router.get("/", response_model=list[ProductRead])

# Cela permet d'avoir une recherche optionnelle via une query params
def liste_product(category: str | None = None, search: str | None = None, db: Session = Depends(get_db)):

    # On initialise la requête de base
    requete = select(Product)

    # Si l'utilisateur a fourni une catégorie, on ajoute un filtre WHERE
    if category is not None:
        requete = requete.where(Product.category == category)
    if search is not None:
        requete = requete.where(Product.name.ilike(f"%{search}%"))

    # On execute la variable qui contient le filtre 
    return db.scalars(requete).all()

# READ (Détail) : Accessible à tout le monde
@router.get("/{id_product}", response_model=ProductRead)
def product(id_product: int, db: Session = Depends(get_db)):

    # Cherche un resto par son ID
    prod = db.get(Product, id_product)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return prod

# CREATE : Protégé par get_current_user
@router.post("/", response_model=ProductRead, status_code=201)
def creer_product(data: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):

    # Crée une instance avec les données validées par Pydantic (data.model_dump)
    prod = Product(**data.model_dump())
    db.add(prod)
    db.commit() # Sauvegarde en base
    db.refresh(prod) # Recharge l'objet pour récupérer les ID générés par la BDD
    return prod

# DELETE : Protégé par get_current_user
@router.delete("/{id_product}", status_code=204)
def supprimer_product(id_product: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prod = db.get(Product, id_product)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    db.delete(prod)
    db.commit()

# 5. UPDATE (PUT) : Protégé par get_current_user
@router.put("/{id_product}", response_model=ProductRead)
def update_product(id_product: int, data: ProductCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    prod = db.get(Product, id_product)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    # Parcourir la boucle pour appliquer le ou les changements sur les champ
    # 'setattr' modifie l'attribut de l'objet Python
    for champ, valeur in data.model_dump().items():
        setattr(prod, champ, valeur)
    db.commit()
    db.refresh(prod)
    return prod