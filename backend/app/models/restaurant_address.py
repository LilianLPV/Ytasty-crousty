from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

# Création d'une classe qui hérite de Base

class Restaurant_address(Base):

    # Nom de la table
    __tablename__ = "restaurant_address"

    # Clé primaire de la table en INT
    id_address: Mapped[int] = mapped_column(primary_key=True)
    
    # Les colonnes standard elle sont NOT NULL automatiquement  
    city: Mapped[str]
    address: Mapped[str]
    
    # Lien direct vers l'objet lié
    restaurant: Mapped["Restaurant"] = relationship(back_populates="restaurant_address")

