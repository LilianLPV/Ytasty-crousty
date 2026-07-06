from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Permission(Base):
    __tablename__ = "permissions"
    
    id_permission: Mapped[int] = mapped_column(primary_key=True)
    tag_permission: Mapped[str]

    roles: Mapped[list["Role"]] = relationship(
        secondary="role_permission", back_populates="permissions"
    )