from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from app.models.base import Base
from sqlalchemy import ForeignKey

# Création d'une classe qui hérite de Base

class Command(Base):    
    
    # Nom de la table
    __tablename__ = "commands"
    
    # Clé primaire de la table en INT
    id_command: Mapped[int] = mapped_column(primary_key=True)
    
    # Les colonnes standard elle sont NOT NULL automatiquement
    number_command: Mapped[str]
    creation_date_and_time: Mapped[datetime]
    status_command: Mapped[str]
    withdrawal_method: Mapped[str]
    customer_information: Mapped[str]
    price_total: Mapped[float]

    # Clé étrangères il faut préciser la table et le nom de la colonne
    id_restaurant: Mapped[int] = mapped_column(ForeignKey("restaurants.id_restaurant"))
    
    # Lien direct vers l'objet lié
    restaurant: Mapped["Restaurant"] = relationship(back_populates="commands")
    command_lines: Mapped[list["Command_line"]] = relationship(back_populates="command")
