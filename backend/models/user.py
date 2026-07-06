from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base
from sqlalchemy import ForeignKey



class User(Base):
    __tablename__ = "users"

    id_user: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    first_name: Mapped[str]
    username: Mapped[str]
    password: Mapped[str]
    id_role: Mapped[int] = mapped_column(ForeignKey("roles.id_role"))

    role: Mapped["Role"] = relationship(back_populates="users")  # UN rôle, singulier
