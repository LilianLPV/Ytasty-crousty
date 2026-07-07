from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base

# Création d'une classe qui hérite de Base

class Permission(Base):
   
    # Nom de la table
    __tablename__ = "permissions"
   
    # Clé primaire de la table en INT
    id_permission: Mapped[int] = mapped_column(primary_key=True)
    
    # Les colonnes standard elle sont NOT NULL automatiquement
    tag_permission: Mapped[str]
    
    # C'est une relation a plusieurs parce que une permission peut être associée  à plusieurs rôle
    roles: Mapped[list["Role"]] = relationship(
        secondary="role_permission", back_populates="permissions"
    )