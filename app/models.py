from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    model: Mapped[str] = mapped_column(String(100), nullable=False)
    year: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
        default="available",
    )

    rentals: Mapped[list["Rental"]] = relationship(
        back_populates="car"
    )


class Rental(Base):
    __tablename__ = "rentals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    car_id: Mapped[int] = mapped_column(
        ForeignKey("cars.id"),
        nullable=False,
    )
    customer_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    start_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
    )
    end_date: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True,
    )

    car: Mapped[Car] = relationship(
        back_populates="rentals"
    )