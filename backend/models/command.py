from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from models.base import Base
from sqlalchemy import ForeignKey


class Command(Base):
    __tablename__ = "commands"

    id_command: Mapped[int] = mapped_column(primary_key=True)
    number_command: Mapped[str]
    creation_date_and_time: Mapped[datetime]
    status_command: Mapped[str]
    withdrawal_method: Mapped[str]
    customer_information: Mapped[str]
    price_total: Mapped[float]

    id_restaurant: Mapped[int] = mapped_column(ForeignKey("restaurants.id_restaurant"))

    restaurant: Mapped["Restaurant"] = relationship(back_populates="commands")
    command_lines: Mapped[list["Command_line"]] = relationship(back_populates="command")
