from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base
from sqlalchemy import ForeignKey

# Création d'une classe qui hérite de Base

class User(Base):

    # Nom de la table
    __tablename__ = "users"

    # Clé primaire de la table en INT
    id_user: Mapped[int] = mapped_column(primary_key=True)

    # Les colonnes standard elle sont NOT NULL automatiquement
    name: Mapped[str]
    first_name: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    # Clé étrangères il faut préciser la table et le nom de la colonne
    id_role: Mapped[int] = mapped_column(ForeignKey("roles.id_role"))
    id_restaurant: Mapped[int | None] = mapped_column(ForeignKey("restaurants.id_restaurant"), nullable=True)
    # Lien direct vers l'objet lié
    role: Mapped["Role"] = relationship(back_populates="users")  
    restaurant: Mapped["Restaurant | None"] = relationship(foreign_keys=[id_restaurant])