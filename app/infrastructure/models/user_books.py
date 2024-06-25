from sqlalchemy import BIGINT, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.infrastructure.models.base import Base, TableNameMixin, TimeoutMixin
from app.infrastructure.models.books import Book
from app.infrastructure.models.users import User


class UserBook(Base, TableNameMixin, TimeoutMixin):
    user_book_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, unique=True, autoincrement=True)
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    book: Mapped[Book] = ForeignKey("Book")
    user: Mapped[User] = ForeignKey("User")
