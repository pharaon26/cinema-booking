from decimal import Decimal

from sqlalchemy import ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class Service(Base):
    """Справочник доп.услуг (напитки/еда), общий для всего кинотеатра."""

    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)


class BookingService(Base):
    """Конкретная услуга, добавленная к конкретной Брони (с количеством)."""

    __tablename__ = "booking_services"

    id: Mapped[int] = mapped_column(primary_key=True)
    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), nullable=False)
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id"), nullable=False)
    quantity: Mapped[int] = mapped_column(default=1, nullable=False)

    booking: Mapped["Booking"] = relationship(back_populates="services")
    service: Mapped["Service"] = relationship()
