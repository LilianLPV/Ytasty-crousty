import uuid
from datetime import datetime

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.command import Command
from app.models.command_lines import Command_line
from app.models.product import Product
from app.models.restaurant import Restaurant
from app.repositories import command_repository
from app.utils.permissions import (
    ROLES_GLOBAUX,
    verify_restaurant_access,
    verify_restaurant_read_access,
)

# Récupération de la liste de toutes les commandes
def lister_commands(db, current_user, status=None, id_restaurant=None):
    if current_user.role.role_name not in ROLES_GLOBAUX:
        if current_user.id_restaurant is None:
            raise HTTPException(status_code=403, detail="Aucun restaurant n'est rattaché à votre compte")

        id_restaurant = current_user.id_restaurant

    return command_repository.lister(db, status=status, id_restaurant=id_restaurant)

# Récupération d'une commande par son ID avec vérification 
def get_command(db, id_command, current_user):
    comd = command_repository.get_by_id(db, id_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    verify_restaurant_read_access(current_user, comd.id_restaurant)
    return comd

# Récupération d'une commande via son numéro de suivi UNIQUE !
def get_par_numero(db, number_command):
    comd = command_repository.get_by_number(db, number_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return comd

# Met à jour le statut d'une commande 
def update_statut(db, id_command, nouveau_statut, current_user):
    comd = command_repository.get_by_id(db, id_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    verify_restaurant_access(current_user, comd.id_restaurant)

    comd.status_command = nouveau_statut
    db.commit()
    db.refresh(comd)
    return comd


# Recalcule et met à jour le prix total d'une commande
def update_command_total_price(db: Session, id_command: int) -> float:
    total = command_repository.somme_lignes(db, id_command)
    commande = command_repository.get_by_id(db, id_command)
    if commande:
        commande.price_total = total
        db.flush()
    return total

# Vérification que le produit existe, qu'il appartient au bon restaurant et qu'il est disponible
def valider_produit(db: Session, id_product: int, id_restaurant: int) -> Product:
    produit = db.get(Product, id_product)
    if produit is None:
        raise HTTPException(status_code=404, detail=f"Produit {id_product} introuvable")
    if produit.id_restaurant != id_restaurant:
        raise HTTPException(status_code=400, detail=f"Le produit {produit.name} n'appartient pas à ce restaurant")
    if not produit.availability:
        raise HTTPException(status_code=400, detail=f"Le produit {produit.name} n'est pas disponible")
    return produit

# Création des lignes de commandes
def creer_lignes_command(db: Session, id_command: int, id_restaurant: int, lignes) -> None:
    for ligne in lignes:
        produit = valider_produit(db, ligne.id_product, id_restaurant)
        db.add(Command_line(
            quantity=ligne.quantity,
            unit_price=produit.price,   
            id_command=id_command,
            id_product=produit.id_product,
        ))

# Création d'une nouvelle commande
def creer_command(db, data):
    resto = db.get(Restaurant, data.id_restaurant)
    if resto is None:
        raise HTTPException(status_code=404, detail="Restaurant introuvable")
    if not resto.opening_status:
        raise HTTPException(status_code=400, detail="Ce restaurant n'accepte pas de commande actuellement")

    comd = Command(
        number_command=f"CMD-{uuid.uuid4().hex[:6].upper()}",
        creation_date_and_time=datetime.now(),
        status_command="en attente",
        withdrawal_method=data.withdrawal_method,
        customer_information=data.customer_information,
        id_restaurant=data.id_restaurant,
        price_total=0.0,
    )
    db.add(comd)
    db.flush()  # génère l'id_command sans commiter

    creer_lignes_command(db, comd.id_command, data.id_restaurant, data.lines)

    db.flush()
    update_command_total_price(db, id_command=comd.id_command)
    db.commit()
    db.refresh(comd)
    return comd

# Suppréssion définitive d'une commande 
def supprimer_command(db: Session, id_command: int) -> None:
    comd = command_repository.get_by_id(db, id_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    db.delete(comd)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=409,
            detail="Cette commande a des lignes et ne peut pas être supprimée",
        )