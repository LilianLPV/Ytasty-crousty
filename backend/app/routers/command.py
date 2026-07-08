from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.command import Command
from app.schemas.command import CommandRead
from app.schemas.command import CommandCreate
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db

router = APIRouter(prefix="/commands", tags=["commands"])

@router.get("/", response_model=list[CommandRead])
def liste_command(db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return db.scalars(select(Command)).all()

@router.get("/{id_command}", response_model=CommandRead)
def command(id_command: int, db: Session = Depends(get_db)):
    comd = db.get(Command, id_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return comd

@router.post("/", response_model=CommandRead, status_code=201)
def creer_command(data: CommandCreate, db: Session = Depends(get_db)):
    comd = Command(**data.model_dump())
    db.add(comd)
    db.commit()
    db.refresh(comd)
    return comd

@router.delete("/{id_command}", status_code=204)
def supprimer_command(id_command: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comd = db.get(Command, id_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    db.delete(comd)
    db.commit()

@router.put("/{id_command}", response_model=CommandRead)
def update_command(id_command: int, data: CommandCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comd = db.get(Command, id_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
     # Parcourir la boucle pour appliquer le ou les changements sur les champ
    for champ, valeur in data.model_dump().items():
        setattr(comd, champ, valeur)
    db.commit()
    db.refresh(comd)
    return comd