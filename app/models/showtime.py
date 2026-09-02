from datetime import datetime
from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Showtime(Base):
    __tablename__ = "showtimes"

    id: Mapped[int] = mapped_column(primary_key=True)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id"), nullable=False)
    movie_id: Mapped[int] = mapped_column(ForeignKey("movies.id"), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(nullable=False)

    hall: Mapped["Hall"] = relationship()
    movie: Mapped["Movie"] = relationship()
    showtime_seats: Mapped[list["ShowtimeSeat"]] = relationship(back_populates="showtime")


class ShowtimeSeat(Base):
    """Место конкретного сеанса: связывает Сеанс с постоянным Местом Зала
    и хранит цену именно для этого сеанса (цена может отличаться между
    сеансами — дневной/вечерний тариф и т.п.). Существование строки в этой
    таблице означает «место продаётся на этот сеанс», её отсутствие —
    что место не предлагается вовсе (не обязательно всегда весь Зал
    задействован под каждый сеанс)."""

    __tablename__ = "showtime_seats"
    __table_args__ = (UniqueConstraint("showtime_id", "seat_id", name="uq_showtime_seat"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    showtime_id: Mapped[int] = mapped_column(ForeignKey("showtimes.id"), nullable=False)
    seat_id: Mapped[int] = mapped_column(ForeignKey("seats.id"), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)

    showtime: Mapped["Showtime"] = relationship(back_populates="showtime_seats")
    seat: Mapped["Seat"] = relationship()
