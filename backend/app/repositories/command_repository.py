from sqlalchemy import select, func
from sqlalchemy.orm import Session
from app.models.command import Command
from app.models.command_lines import Command_line

# Récupère une commande grâce à son ID
def get_by_id(db: Session, id_command: int) -> Command | None:
    return db.get(Command, id_command)

# Recherche d'une commande via son numéro
def get_by_number(db: Session, number_command: str) -> Command | None:
    return db.scalars(
        select(Command).where(Command.number_command == number_command)
    ).first()

# Récupère la liste des commandes en appliquant des filtres
def lister(db: Session, status: str | None = None, id_restaurant: int | None = None):
    requete = select(Command)
    if status is not None:
        requete = requete.where(Command.status_command == status)
    if id_restaurant is not None:
        requete = requete.where(Command.id_restaurant == id_restaurant)
    return db.scalars(requete).all()

# Calcule le prix total total d'une commande 
def somme_lignes(db: Session, id_command: int) -> float:
    total = db.scalar(
        select(func.sum(Command_line.quantity * Command_line.unit_price))
        .where(Command_line.id_command == id_command)
    )
    return total or 0.0