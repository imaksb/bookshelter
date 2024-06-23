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
from app.infrastructure.crud.requests import RequestsCRUD
from app.infrastructure.database import create_session_pool
from app.infrastructure.models.users import User
from app.infrastructure.schemas import TokenPayload

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=settings.API_V1_STR + "/login/access"
)


async def get_session() -> RequestsCRUD:
    session_pool = await create_session_pool()

    async with session_pool() as session:
        yield RequestsCRUD(session)


SessionDep = Annotated[RequestsCRUD, Depends(get_session)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


async def get_current_user(session: SessionDep, token: TokenDep) -> HTTPException | User:
    print(token)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        print(payload)
        token_data = TokenPayload(**payload)
    except (InvalidTokenError, ValidationError) as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Could not validate credentials")

    user = await session.users.get_user_by_user_id(token_data.sub)

    if not user:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not user.is_active:
        return HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Inactive user")

    return user

CurrentUser = Annotated[User, Depends(get_current_user)]


def get_current_active_admin(current_user: CurrentUser) -> User:
    if not current_user.is_admin:
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    return current_user


CurrentUserAdmin = Annotated[User, Depends(get_current_active_admin)]
