from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.permissions import PermissionsRead, PermissionsCreate
from app.utils.permissions import require_role
from app.utils.jwt import get_current_user
from app.models.user import User
from app.database import get_db
from app.services import permission_service

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.get("/", response_model=list[PermissionsRead])
def liste_permission(db: Session = Depends(get_db),
                     current_user: User = Depends(get_current_user)):
    return permission_service.lister_permissions(db)


@router.get("/{id_permission}", response_model=PermissionsRead)
def permission(id_permission: int, db: Session = Depends(get_db),
               current_user: User = Depends(get_current_user)):
    return permission_service.get_permission(db, id_permission)


@router.post("/", response_model=PermissionsRead, status_code=201)
def creer_permission(data: PermissionsCreate, db: Session = Depends(get_db),
                     current_user: User = Depends(require_role("administrateur"))):
    return permission_service.creer_permission(db, data)


@router.delete("/{id_permission}", status_code=204)
def supprimer_permission(id_permission: int, db: Session = Depends(get_db),
                         current_user: User = Depends(require_role("administrateur"))):
    permission_service.supprimer_permission(db, id_permission)


@router.put("/{id_permission}", response_model=PermissionsRead)
def update_permission(id_permission: int, data: PermissionsCreate, db: Session = Depends(get_db),
                      current_user: User = Depends(require_role("administrateur"))):
    return permission_service.update_permission(db, id_permission, data)