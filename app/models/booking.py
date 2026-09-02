import enum
from datetime import datetime

from sqlalchemy import Enum, ForeignKey, Index, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class BookingStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    cancelled = "cancelled"


class Booking(Base):
    """Бронь связывает Пользователя с конкретным ShowtimeSeat.

    Защита от race condition — не Python-код, а индекс в БД:
    уникальный индекс на showtime_seat_id, но ЧАСТИЧНЫЙ — действует
    только для строк, где status != 'cancelled' (postgresql_where).
    Поэтому:
      - Две активные (pending/confirmed) брони на одно и то же место
        физически не смогут существовать одновременно — вторая INSERT
        упадёт с UniqueViolation, кто бы что ни делал в Python.
      - Отменённая бронь остаётся в таблице (история сохранена), но
        не мешает создать новую бронь на то же место, потому что для
        cancelled-строк индекс её не учитывает.
    """

    __tablename__ = "bookings"
    __table_args__ = (
        Index(
            "uq_active_booking_per_showtime_seat",
            "showtime_seat_id",
            unique=True,
            postgresql_where=text("status != 'cancelled'"),
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    showtime_seat_id: Mapped[int] = mapped_column(ForeignKey("showtime_seats.id"), nullable=False)
    status: Mapped[BookingStatus] = mapped_column(
        Enum(BookingStatus, name="booking_status"),
        default=BookingStatus.pending,
        nullable=False,
    )
    expires_at: Mapped[datetime] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())

    user: Mapped["User"] = relationship()
    showtime_seat: Mapped["ShowtimeSeat"] = relationship()
    services: Mapped[list["BookingService"]] = relationship(back_populates="booking")
    payment: Mapped["Payment"] = relationship(back_populates="booking", uselist=False)
