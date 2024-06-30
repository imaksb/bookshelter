from typing import Annotated
import jwt
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import InvalidTokenError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from app.core import security
from app.core.config import settings
from app.infrastructure.repositories.requests import RequestsCRUD
from app.infrastructure.database import create_session_pool, redis
from app.infrastructure.models.users import User
from app.infrastructure.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=settings.API_V1_STR + "/login"
)


async def get_session() -> RequestsCRUD:
    session_pool = await create_session_pool()

    async with session_pool() as session:
        yield RequestsCRUD(session)


SessionDep = Annotated[RequestsCRUD, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def is_email_exist(session: SessionDep, email: str):
    user = await session.users.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

    return user

UserByEmailDep = Annotated[User, Depends(is_email_exist)]


async def get_current_user(session: SessionDep, token: TokenDep) -> HTTPException | User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )

        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError) as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    user = await session.users.get_user_by_user_id(token_data.sub)

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.is_active:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user please confirm email")

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_admin(current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


class RateLimitChecker:
    def __init__(self, rate_time: int = 300, rate_attempt: int = 5, key_name: str = "reset"):
        self.rate_time = rate_time
        self.rate_attempt = rate_attempt
        self.key_name = key_name

    async def __call__(self, email: str):
        key = f"{self.key_name}:{email}"
        attempts = await redis.get(key)
        if attempts is None:
            await redis.setex(key, 300, 1)
        else:
            attempts = int(attempts)
            if attempts >= 5:
                raise HTTPException(
                    status_code=429,
                    detail="Too many attempts. Please try again later."
                )
            await redis.incr(key)


CurrentUserAdmin = Depends(get_current_active_admin)
