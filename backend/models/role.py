from sqlalchemy import ForeignKey, Table, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base


# Table de jointure !

role_permission = Table(
    "role_permission",                                              
    Base.metadata,                                                  
    Column("id_role", ForeignKey("roles.id_role"), primary_key=True),          
    Column("id_permission", ForeignKey("permissions.id_permission"), primary_key=True),  
)

class Role(Base):
    __tablename__ = "roles"
    
    id_role: Mapped[int] = mapped_column(primary_key=True)
    role_name: Mapped[str]

    users: Mapped[list["User"]] = relationship(back_populates="role")
    permissions: Mapped[list["Permission"]] = relationship(
        secondary=role_permission, back_populates="roles"
    )