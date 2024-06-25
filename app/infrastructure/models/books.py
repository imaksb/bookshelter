from sqlalchemy import BIGINT, VARCHAR
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.models.base import Base, TableNameMixin


class Book(Base, TableNameMixin):
    book_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, unique=True, autoincrement=True)
    name: Mapped[str] = mapped_column(VARCHAR(75))
    author: Mapped[str] = mapped_column(VARCHAR(50))
    image: Mapped[str] = mapped_column(VARCHAR(200), nullable=True)
    isbn: Mapped[str] = mapped_column(VARCHAR(100), nullable=True)
