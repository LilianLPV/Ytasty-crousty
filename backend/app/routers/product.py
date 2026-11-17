from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.product import ProductRead, ProductCreate
from app.utils.permissions import require_role
from app.models.user import User
from app.database import get_db
from app.services import product_service


# On définit le rtouer avec un tag ou le /docs
router = APIRouter(prefix="/products", tags=["products"])

# On READ (liste) accessible à tout le monde
@router.get("/", response_model=list[ProductRead])
def liste_product(
    category: str | None = None,
    search: str | None = None,
    id_restaurant: int | None = None,
    availability: bool | None = None,
    db: Session = Depends(get_db),
):
    return product_service.lister_products(db, category, search, id_restaurant, availability)

# READ (Détail) : Accessible à tout le monde
@router.get("/{id_product}", response_model=ProductRead)
def product(id_product: int, db: Session = Depends(get_db)):
    return product_service.get_product(db, id_product)

# CREATE : Création d'un produit seul les administrateur et le personnel peuvent
@router.post("/", response_model=ProductRead, status_code=201)
def creer_product(data: ProductCreate, db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur", "personnel"))):
    return product_service.creer_product(db, data, current_user)

# DELETE : Suppression d'un produit
@router.delete("/{id_product}", status_code=204)
def supprimer_product(id_product: int, db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur", "personnel"))):
    product_service.supprimer_product(db, id_product, current_user)

# 5. UPDATE (PUT) met à jour un produit éxistant seul les administrateurs et le personnel peuvent le faire 
@router.put("/{id_product}", response_model=ProductRead)
def update_product(id_product: int, data: ProductCreate, db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur", "personnel"))):
    return product_service.update_product(db, id_product, data, current_user)