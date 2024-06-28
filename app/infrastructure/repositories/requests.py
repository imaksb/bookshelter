from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.repositories import UserRepository
from app.infrastructure.repositories.books import BookRepository
from app.infrastructure.repositories.user_books import UserBookRepository


@dataclass
class RequestsCRUD:
    session: AsyncSession

    @property
    def users(self) -> UserRepository:
        return UserRepository(self.session)

    @property
    def books(self) -> BookRepository:
        return BookRepository(self.session)

    @property
    def user_books(self) -> UserBookRepository:
        return UserBookRepository(self.session)
