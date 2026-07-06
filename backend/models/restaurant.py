from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import Base

class Restaurant(Base):
    __tablename__ = "restaurants"

    id_restaurant: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    opening_status: Mapped[bool]
    opening_hours: Mapped[str]
    contact_details: Mapped[str]
    id_address: Mapped[int] = mapped_column(
        ForeignKey("restaurant_address.id_address"), unique=True  
    )
    products: Mapped[list["Product"]] = relationship(back_populates="restaurant")
    commands: Mapped[list["Command"]] = relationship(back_populates="restaurant")
    restaurant_address: Mapped["Restaurant_address"] = relationship(back_populates="restaurant")
