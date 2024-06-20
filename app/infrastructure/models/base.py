from datetime import datetime

from sqlalchemy import func, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, declared_attr, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TableNameMixin:
    @declared_attr.directive
    def __tablename__(cls):
        return cls.__name__.lower()


class TimeoutMixin:
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP,
                                                 server_default=func.now(),
                                                 )
