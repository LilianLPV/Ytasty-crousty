from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from models.base import Base



class Command_line(Base):
    __tablename__ = "command_lines"

    id_command_line: Mapped[int] = mapped_column(primary_key=True)
    quantity: Mapped[int]
    unit_price: Mapped[float]

    id_command: Mapped[int] = mapped_column(ForeignKey("commands.id_command"))
    id_product: Mapped[int] = mapped_column(ForeignKey("products.id_product"))

    command: Mapped["Command"] = relationship(back_populates="command_lines")
    product: Mapped["Product"] = relationship(back_populates="command_lines")