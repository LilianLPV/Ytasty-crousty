from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.repositories import command_repository
from app.models.command_lines import Command_line
from app.models.user import User
from app.schemas.command_lines import CommandLineCreate
from app.services import command_service
from app.utils.permissions import verify_restaurant_access

# Récupération de toutes les lignes de commande
def lister_lignes(db: Session):
    return db.scalars(select(Command_line)).all()

# Récupération d'une ligne de commande par son ID
def get_ligne(db: Session, id_command_line: int) -> Command_line:
    ligne = db.get(Command_line, id_command_line)
    if ligne is None:
        raise HTTPException(status_code=404, detail="Ligne introuvable")
    return ligne

# Ajout d'un nouvel article dans une commande existante
def creer_ligne(db: Session, data: CommandLineCreate, current_user: User) -> Command_line:
    comd = command_repository.get_by_id(db, data.id_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    verify_restaurant_access(current_user, comd.id_restaurant)


    produit = command_service.valider_produit(db, data.id_product, comd.id_restaurant)

    ligne = Command_line(
        quantity=data.quantity,
        unit_price=produit.price,   
        id_command=comd.id_command,
        id_product=produit.id_product,
    )
    db.add(ligne)
    db.flush()
    command_service.update_command_total_price(db, id_command=ligne.id_command)
    db.commit()
    db.refresh(ligne)
    return ligne


# Suppréssion d'un article donc d'une ligne de commande
def supprimer_ligne(db: Session, id_command_line: int, current_user: User) -> None:
    ligne = get_ligne(db, id_command_line)
    id_de_la_command = ligne.id_command

    comd = command_repository.get_by_id(db, id_de_la_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    verify_restaurant_access(current_user, comd.id_restaurant)

    db.delete(ligne)
    db.flush()
    command_service.update_command_total_price(db, id_command=id_de_la_command)
    db.commit()