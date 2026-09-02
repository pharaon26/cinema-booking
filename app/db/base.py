from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Общий предок для всех моделей — нужен, чтобы у них была одна
    Base.metadata, по которой Alembic сможет строить миграции."""
