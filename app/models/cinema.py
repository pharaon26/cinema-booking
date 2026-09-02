from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Cinema(Base):
    __tablename__ = "cinemas"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    address: Mapped[str] = mapped_column(nullable=False)

    halls: Mapped[list["Hall"]] = relationship(back_populates="cinema")


class Hall(Base):
    __tablename__ = "halls"

    id: Mapped[int] = mapped_column(primary_key=True)
    cinema_id: Mapped[int] = mapped_column(ForeignKey("cinemas.id"), nullable=False)
    name: Mapped[str] = mapped_column(nullable=False)

    cinema: Mapped["Cinema"] = relationship(back_populates="halls")
    seats: Mapped[list["Seat"]] = relationship(back_populates="hall")


class Seat(Base):
    """Постоянное место в Зале (ряд + номер). Существует один раз для
    Зала и переиспользуется каждым Сеансом через ShowtimeSeat — так не
    приходится заново описывать схему зала при создании нового сеанса."""

    __tablename__ = "seats"
    __table_args__ = (
        UniqueConstraint("hall_id", "row_number", "seat_number", name="uq_seat_hall_row_number"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id"), nullable=False)
    row_number: Mapped[int] = mapped_column(nullable=False)
    seat_number: Mapped[int] = mapped_column(nullable=False)

    hall: Mapped["Hall"] = relationship(back_populates="seats")
