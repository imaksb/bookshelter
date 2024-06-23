from dataclasses import dataclass

from sqlalchemy.ext.asyncio import AsyncSession

from app.infrastructure.crud import UserCRUD


@dataclass
class RequestsCRUD:
    session: AsyncSession

    @property
    def users(self) -> UserCRUD:
        return UserCRUD(self.session)
