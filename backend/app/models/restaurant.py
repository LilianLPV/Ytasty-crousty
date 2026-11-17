from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.models.base import Base

# Création d'une classe qui hérite de Base

class Restaurant(Base):

    # Nom de la table
    __tablename__ = "restaurants"

    # Clé primaire de la table en INT
    id_restaurant: Mapped[int] = mapped_column(primary_key=True)

    # Les colonnes standard elle sont NOT NULL automatiquement
    name: Mapped[str]
    opening_status: Mapped[bool]
    opening_hours: Mapped[str]
    contact_details: Mapped[str]
    
    # Clé étrangères il faut préciser la table et le nom de la colonne
    # Unique garantit une seul adresse par restaurant
    id_address: Mapped[int] = mapped_column(
        ForeignKey("restaurant_address.id_address"), unique=True  
    )
    
    # Lien direct vers l'objet lié
    products: Mapped[list["Product"]] = relationship(back_populates="restaurant")
    commands: Mapped[list["Command"]] = relationship(back_populates="restaurant")
    restaurant_address: Mapped["Restaurant_address"] = relationship(back_populates="restaurant")
