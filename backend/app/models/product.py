from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.models.base import Base

# Création d'une classe qui hérite de Base

class Product(Base):

    # Nom de la table
    __tablename__ = "products"

    # Clé primaire de la table en INT
    id_product: Mapped[int] = mapped_column(primary_key=True)
   
    # Les colonnes standard elle sont NOT NULL automatiquement
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    availability: Mapped[bool]
    category: Mapped[str]
    ingredient_list: Mapped[str]
    
    # Clé étrangères il faut préciser la table et le nom de la colonne
    id_restaurant: Mapped[int] = mapped_column(ForeignKey("restaurants.id_restaurant"))
   
    # Lien direct vers l'objet lié
    restaurant: Mapped["Restaurant"] = relationship(back_populates="products")
    pictures: Mapped[list["Product_picture"]] = relationship(back_populates="product")
    command_lines: Mapped[list["Command_line"]] = relationship(back_populates="product")