from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.models.base import Base


# Table de jointure !

role_permission = Table(
    "role_permission",                                              
    Base.metadata,                                                  
    Column("id_role", ForeignKey("roles.id_role"), primary_key=True),          
    Column("id_permission", ForeignKey("permissions.id_permission"), primary_key=True),  
)

# Création d'une classe qui hérite de Base

class Role(Base):
    
    # Nom de la table
    __tablename__ = "roles"

    # Clé primaire de la table en INT
    id_role: Mapped[int] = mapped_column(primary_key=True)

    # Les colonnes standard elle sont NOT NULL automatiquement
    role_name: Mapped[str]

    # Lien direct vers l'objet lié
    users: Mapped[list["User"]] = relationship(back_populates="role")

    # C'est une relation a plusieurs parce que une permission peut être associée  à plusieurs rôle
    permissions: Mapped[list["Permission"]] = relationship(
        secondary=role_permission, back_populates="roles"
    )