from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import Base

class Product_picture(Base):
    __tablename__ = "product_pictures"

    id_picture: Mapped[int] = mapped_column(primary_key=True)
    picture: Mapped[str]
    id_product: Mapped[int] = mapped_column(ForeignKey("products.id_product"))  # la FK !

    product: Mapped["Product"] = relationship(back_populates="pictures")
