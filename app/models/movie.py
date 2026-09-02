from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Movie(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(nullable=False)
    duration_minutes: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str | None] = mapped_column(default=None)
