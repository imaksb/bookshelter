from sqlalchemy import insert, select

from app.core.security import get_hash_password, verify_password
from app.infrastructure import schemas

from app.infrastructure.crud.base import BaseCRUD
from app.infrastructure.models.users import User


class UserCRUD(BaseCRUD):
    async def get_user_by_user_id(self, user_id: int) -> User:
        select_stmt = select(User).where(User.user_id == user_id)
        result = await self.session.execute(select_stmt)
        return result.scalars().first()

    async def get_user_by_email(self, email: str) -> User:
        select_stmt = select(User).where(User.email == email)
        result = await self.session.execute(select_stmt)
        return result.scalars().first()

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
