from sqlalchemy import insert

from app.infrastructure.crud.base import BaseCRUD
from app.infrastructure.models.users import User


class UserCRUD(BaseCRUD):
    async def create(self, username: str, email: str, hashed_password: str, is_active: bool, is_superuser: bool):
        insert_stmt = insert(User).values(
            username=username,
            email=email,
            hashed_password=hashed_password,
            is_active=is_active
        )
        await self.session.execute(insert_stmt)
        await self.session.commit()
