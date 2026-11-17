from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.product_pictures import Product_picture
from app.models.product import Product
from app.models.user import User
from app.schemas.product_pictures import ProductPictureCreate
from app.utils.permissions import verify_restaurant_access


def lister_pictures(db: Session):
    return db.scalars(select(Product_picture)).all()


def get_picture(db: Session, id_picture: int) -> Product_picture:
    pic = db.get(Product_picture, id_picture)
    if pic is None:
        raise HTTPException(status_code=404, detail="Image introuvable")
    return pic


def creer_picture(db: Session, data: ProductPictureCreate, current_user: User) -> Product_picture:
    produit = db.get(Product, data.id_product)
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")
    verify_restaurant_access(current_user, produit.id_restaurant)

    pic = Product_picture(**data.model_dump())
    db.add(pic)
    db.commit()
    db.refresh(pic)
    return pic


def supprimer_picture(db: Session, id_picture: int, current_user: User) -> None:
    pic = get_picture(db, id_picture)
    verify_restaurant_access(current_user, pic.product.id_restaurant)
    db.delete(pic)
    db.commit()