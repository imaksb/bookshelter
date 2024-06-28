from sqlalchemy import insert, select, update

from app.core.security import get_hash_password, verify_password
from app.infrastructure import schemas

from app.infrastructure.repositories.base import BaseRepository
from app.infrastructure.models.users import User


class UserRepository(BaseRepository):
    async def get_user_by_user_id(self, user_id: int) -> User:
        select_stmt = select(User).where(User.user_id == user_id)
        result = await self.session.execute(select_stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User:
        select_stmt = select(User).where(User.email == email)
        result = await self.session.execute(select_stmt)
        return result.scalars().first()

    async def update_user_active_status(self, email: str, new_status: int = 1):
        update_stmt = update(User).where(User.email == email).values(
            is_active=new_status
        )
        await self.session.execute(update_stmt)
        await self.session.commit()

    async def create(self, user: schemas.UserIn):
        password_hash = get_hash_password(user.password)

        user = user.copy(exclude={"password"})
        user = schemas.UserInDB(**user.dict())
        user.hashed_password = password_hash

        db_user = User(**user.dict())

        self.session.add(db_user)
        await self.session.commit()

    async def authenticate(self, user_in: schemas.UserIn):
        user = await self.get_user_by_email(user_in.email)
        if not user:
            return False
        if not verify_password(user_in.password, user.hashed_password):
            return False
        return user
