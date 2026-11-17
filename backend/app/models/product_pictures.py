from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
# Création d'une classe qui hérite de Base

class Product_picture(Base):
    # Nom de la table
    __tablename__ = "product_pictures"

    # Clé primaire de la table en INT
    id_picture: Mapped[int] = mapped_column(primary_key=True)

    # Les colonnes standard elle sont NOT NULL automatiquement
    picture: Mapped[str]

    # Clé étrangères il faut préciser la table et le nom de la colonne
    id_product: Mapped[int] = mapped_column(ForeignKey("products.id_product"))
    
    # Lien direct vers l'objet lié
    product: Mapped["Product"] = relationship(back_populates="pictures")
