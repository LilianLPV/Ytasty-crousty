from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from app.models.base import Base


# Création d'une classe qui hérite de Base

class Command_line(Base):

    # Nom de la table
    __tablename__ = "command_lines"

    # Clé primaire de la table en INT
    id_command_line: Mapped[int] = mapped_column(primary_key=True)
    
    # Les colonnes standard elle sont NOT NULL automatiquement
    quantity: Mapped[int]
    unit_price: Mapped[float]
    
    # Clé étrangères il faut préciser la table et le nom de la colonne
    id_command: Mapped[int] = mapped_column(ForeignKey("commands.id_command"))
    id_product: Mapped[int] = mapped_column(ForeignKey("products.id_product"))
    
    # Lien direct vers l'objet lié
    command: Mapped["Command"] = relationship(back_populates="command_lines")
    product: Mapped["Product"] = relationship(back_populates="command_lines")