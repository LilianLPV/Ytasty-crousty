from fastapi import Depends, HTTPException, status
from app.utils.jwt import get_current_user
from app.models.user import User

ROLES_GLOBAUX = ("administrateur", "direction")

def require_role(*roles_autorises: str):
    def checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role.role_name not in roles_autorises:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Vous n'avez pas les droits nécessaires pour cette action",
            )
        return current_user
    return checker

# Vérification des rôles si l'utilisateur est un admin ou direction alors ils voient tout sinon il voit que son restaurant ou il travail
def verify_restaurant_read_access(current_user: User, id_restaurant: int) -> None:
    if current_user.role.role_name in ROLES_GLOBAUX:
        return
    if current_user.id_restaurant != id_restaurant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez pas consulter les données d'un autre restaurant",
        )

# Chaque membre du personnel ne peut que modifier son restaurant
def verify_restaurant_access(current_user: User, id_restaurant: int) -> None:
    if current_user.role.role_name == "administrateur":
        return
    if current_user.id_restaurant != id_restaurant:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous ne pouvez pas agir sur les données d'un autre restaurant",
        )
 