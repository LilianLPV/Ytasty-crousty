from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.role import RoleRead, RoleCreate
from app.utils.permissions import require_role
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db
from app.services import role_service

router = APIRouter(prefix="/roles", tags=["roles"])


@router.get("/", response_model=list[RoleRead])
def liste_role(db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return role_service.lister_roles(db)


@router.get("/{id_role}", response_model=RoleRead)
def role(id_role: int, db: Session = Depends(get_db),
         current_user: User = Depends(get_current_user)):
    return role_service.get_role(db, id_role)


@router.post("/", response_model=RoleRead, status_code=201)
def creer_role(data: RoleCreate, db: Session = Depends(get_db),
               current_user: User = Depends(require_role("administrateur"))):
    return role_service.creer_role(db, data)


@router.delete("/{id_role}", status_code=204)
def supprimer_role(id_role: int, db: Session = Depends(get_db),
                   current_user: User = Depends(require_role("administrateur"))):
    role_service.supprimer_role(db, id_role)


@router.put("/{id_role}", response_model=RoleRead)
def update_role(id_role: int, data: RoleCreate, db: Session = Depends(get_db),
                current_user: User = Depends(require_role("administrateur"))):
    return role_service.update_role(db, id_role, data)