from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.schemas.command import CommandRead
from app.schemas.command import CommandCreate
from app.schemas.command import CommandUpdateStatus
from app.utils.permissions import require_role
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db

# On READ (liste) accessible à tout le monde
from app.services import command_service

router = APIRouter(prefix="/commands", tags=["commands"])

# Récupération de la liste de commande, les deux paramètres sont optionnels
@router.get("/", response_model=list[CommandRead])
def liste_command(status: str | None = None, id_restaurant: int | None = None,
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return command_service.lister_commands(db, current_user, status, id_restaurant)

# Récupération d'une commande via son numéro de suivi
@router.get("/by-number/{number_command}", response_model=CommandRead)
def command_par_numero(number_command: str, db: Session = Depends(get_db)):
    return command_service.get_par_numero(db, number_command)

# Récupère les détails d'une commande via son ID
@router.get("/{id_command}", response_model=CommandRead)
def command(id_command: int, db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)):
    return command_service.get_command(db, id_command, current_user)

# Création d'une nouvelle commande
@router.post("/", response_model=CommandRead, status_code=201)
def creer_command(data: CommandCreate, db: Session = Depends(get_db)):
    return command_service.creer_command(db, data)

# Supprime définitivement (administrateur)
@router.delete("/{id_command}", status_code=204)
def supprimer_command(id_command: int, db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur"))):
    command_service.supprimer_command(db, id_command)

# Met à jour le statut d'une commande seul les administrateur et le personnel
@router.put("/{id_command}", response_model=CommandRead)
def update_command(id_command: int, data: CommandUpdateStatus, db: Session = Depends(get_db),
    current_user: User = Depends(require_role("administrateur", "personnel"))):
    return command_service.update_statut(db, id_command, data.status_command, current_user)