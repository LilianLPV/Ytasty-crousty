from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.product import Product
from app.models.user import User
from app.schemas.product import ProductCreate
from app.utils.permissions import verify_restaurant_access

# Récupération de la liste des produits avec une possiblité d'appliquer des filtres
def lister_products(db: Session, category=None, search=None, id_restaurant=None, availability=None):
    requete = select(Product)

    if category is not None:
        requete = requete.where(Product.category == category)
    if search is not None:
        requete = requete.where(Product.name.ilike(f"%{search}%"))
    if id_restaurant is not None:
        requete = requete.where(Product.id_restaurant == id_restaurant)
    if availability is not None:
        requete = requete.where(Product.availability == availability)

    # On execute la variable qui contient le filtre ou les filtres
    return db.scalars(requete).all()

# On récupère un produit spécifique grâce à son ID
def get_product(db: Session, id_product: int) -> Product:

    prod = db.get(Product, id_product)
    if prod is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    return prod

# Création d'un produit 
def creer_product(db: Session, data: ProductCreate, current_user: User):

    verify_restaurant_access(current_user, data.id_restaurant)

    prod = Product(**data.model_dump())
    db.add(prod)
    db.commit() # Sauvegarde en base
    db.refresh(prod) # Recharge l'objet pour récupérer les ID générés par la BDD
    return prod

# Suppréssion d'un produit déjà existant si l'utilisateur a les droits 
def supprimer_product(db: Session, id_product: int, current_user: User) -> None:
    prod = get_product(db, id_product)
    verify_restaurant_access(current_user, prod.id_restaurant)
    db.delete(prod)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Ce produit figure dans des commandes et ne peut pas être supprimé",
        )
    
# Mise à jour d'un produit 
def update_product(db: Session, id_product: int, data: ProductCreate, current_user: User):
    prod = get_product(db, id_product)
    verify_restaurant_access(current_user, prod.id_restaurant)
    verify_restaurant_access(current_user, data.id_restaurant)
    # Parcourir la boucle pour appliquer le ou les changements sur les champ
    # 'setattr' modifie l'attribut de l'objet Python
    for champ, valeur in data.model_dump().items():
        setattr(prod, champ, valeur)
    db.commit()
    db.refresh(prod)
    return prod