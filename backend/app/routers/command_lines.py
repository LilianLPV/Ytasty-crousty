from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.command_lines import CommandLineRead, CommandLineCreate
from app.database import get_db
from app.utils.permissions import require_role
from app.services import command_line_service


router = APIRouter(prefix="/command_lines", tags=["command_lines"])

# Récupération de la liste des commandes existantes mais seuls l'administrateur peut y avoir accès
@router.get("/", response_model=list[CommandLineRead])
def liste_lignes(db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur"))):
    return command_line_service.lister_lignes(db)

# Ajout d'une nouvelle ligne à ne commande existante (administrateur, personnel)
@router.post("/", response_model=CommandLineRead, status_code=201)
def creer_ligne(data: CommandLineCreate, db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur", "personnel"))):
    return command_line_service.creer_ligne(db, data, current_user)


# Supprimer une ligne de commande grâce à son ID (administrateur, personnel)
@router.delete("/{id_command_line}", status_code=204)
def supprimer_ligne(id_command_line: int, db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur", "personnel"))):
    command_line_service.supprimer_ligne(db, id_command_line, current_user)