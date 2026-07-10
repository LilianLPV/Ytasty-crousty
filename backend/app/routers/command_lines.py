from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.command_lines import Command_line
from app.models.product import Product
from app.schemas.command_lines import CommandLineRead, CommandLineCreate
from app.database import get_db

router = APIRouter(prefix="/command_lines", tags=["command_lines"])


@router.get("/", response_model=list[CommandLineRead])
def liste_lignes(db: Session = Depends(get_db)):
    return db.scalars(select(Command_line)).all()

@router.post("/", response_model=CommandLineRead, status_code=201)
def creer_ligne(data: CommandLineCreate, db: Session = Depends(get_db)):
    produit = db.get(Product, data.id_product)
    if produit is None:
        raise HTTPException(status_code=404, detail="Produit introuvable")

    if not produit.availability:
        raise HTTPException(status_code=400, detail="Ce produit n'est pas disponible")

    ligne = Command_line(
        quantity=data.quantity,
        unit_price=produit.price,
        id_command=data.id_command,
        id_product=data.id_product,
    )
    db.add(ligne)
    db.commit()
    db.refresh(ligne)
    return ligne

@router.delete("/{id_command_line}", status_code=204)
def supprimer_ligne(id_command_line: int, db: Session = Depends(get_db)):
    ligne = db.get(Command_line, id_command_line)
    if ligne is None:
        raise HTTPException(status_code=404, detail="Ligne introuvable")
    db.delete(ligne)
    db.commit()