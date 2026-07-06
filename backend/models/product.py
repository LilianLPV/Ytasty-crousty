from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import Base

class Product(Base):
    __tablename__ = "products"

    id_product: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    description: Mapped[str]
    price: Mapped[float]
    availability: Mapped[bool]
    category: Mapped[str]
    ingredient_list: Mapped[str]
    id_restaurant: Mapped[int] = mapped_column(ForeignKey("restaurants.id_restaurant"))

    restaurant: Mapped["Restaurant"] = relationship(back_populates="products")
    pictures: Mapped[list["Product_picture"]] = relationship(back_populates="product")
    command_lines: Mapped[list["Command_line"]] = relationship(back_populates="product")