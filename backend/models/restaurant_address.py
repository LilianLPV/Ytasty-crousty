from sqlalchemy.orm import Mapped, mapped_column, relationship
from models.base import Base

class Restaurant_address(Base):
    __tablename__ = "restaurant_address"

    id_address: Mapped[int] = mapped_column(primary_key=True)
    city: Mapped[str]
    address: Mapped[str]

    restaurant: Mapped["Restaurant"] = relationship(back_populates="restaurant_address")

