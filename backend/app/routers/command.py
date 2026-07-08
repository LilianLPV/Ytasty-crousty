from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.command import Command
from app.schemas.command import CommandRead
from app.schemas.command import CommandCreate
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db

# On définit le rtouer avec un tag ou le /docs
router = APIRouter(prefix="/commands", tags=["commands"])

# On READ (liste) accessible à tout le monde
@router.get("/", response_model=list[CommandRead])
def liste_command(status: str | None = None, id_restaurant: int | None = None, db : Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    
    # On initialise la requête de base
    requete = select(Command)
    
    # Si l'utilisateur a fourni une catégorie, on ajoute un filtre WHERE
    if status is not None:
        requete = requete.where(Command.status_command == status)
    if id_restaurant is not None:
        requete = requete.where(Command.id_restaurant== id_restaurant)
    # On récupère tous les restaurants en base
    return db.scalars(requete).all()

# READ (Détail) : Accessible à tout le monde
@router.get("/{id_command}", response_model=CommandRead)
def command(id_command: int, db: Session = Depends(get_db)):
    
    # Cherche un resto par son ID
    comd = db.get(Command, id_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    return comd

# CREATE : Protégé par get_current_user
@router.post("/", response_model=CommandRead, status_code=201)
def creer_command(data: CommandCreate, db: Session = Depends(get_db)):
    
    # Crée une instance avec les données validées par Pydantic (data.model_dump)
    comd = Command(**data.model_dump())
    db.add(comd)
    db.commit() # Sauvegarde en base
    db.refresh(comd) # Recharge l'objet pour récupérer les ID générés par la BDD
    return comd

# DELETE : Protégé par get_current_user
@router.delete("/{id_command}", status_code=204)
def supprimer_command(id_command: int, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comd = db.get(Command, id_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    db.delete(comd)
    db.commit()

# 5. UPDATE (PUT) : Protégé par get_current_user
@router.put("/{id_command}", response_model=CommandRead)
def update_command(id_command: int, data: CommandCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    comd = db.get(Command, id_command)
    if comd is None:
        raise HTTPException(status_code=404, detail="Commande introuvable")
    
    # Parcourir la boucle pour appliquer le ou les changements sur les champ
    # 'setattr' modifie l'attribut de l'objet Python
    for champ, valeur in data.model_dump().items():
        setattr(comd, champ, valeur)
    db.commit()
    db.refresh(comd)
    return comd