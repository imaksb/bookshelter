from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.crud import UserCRUD
from app.infrastructure.crud.books import BookCRUD


@dataclass
class RequestsCRUD:
    session: AsyncSession

    @property
    def users(self) -> UserCRUD:
        return UserCRUD(self.session)

    @property
    def books(self) -> BookCRUD:
        return BookCRUD(self.session)
