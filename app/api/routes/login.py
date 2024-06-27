from datetime import timedelta

import jwt
from fastapi import APIRouter, HTTPException
from starlette import status

from app.api.deps import SessionDep
from app.core import security
from app.core.config import settings
from app.infrastructure.schemas import UserIn, Tokens

router = APIRouter()


@router.post("/login")
async def log_in(*, crud: SessionDep, user_in: UserIn):
    user = await crud.users.authenticate(user_in)

    if not user:
        return HTTPException(status_code=400, detail="Password or email is not valid")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access = security.create_jwt_token(user.user_id, access_token_expires, "access")
    refresh = security.create_jwt_token(user.user_id, refresh_token_expires, "refresh")
    return Tokens(access=access, refresh=refresh)


@router.post("/refresh")
async def refresh_token(*, refresh: str) -> Tokens:
    try:
        tokens = security.get_new_access_token(refresh)

        if not tokens:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not valid")

        return tokens
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Something went wrong")


# @router.post("/reset-password")
# async def reset_password(*, crud: SessionDep, email: EmailStr | None = None):
#     user = await crud.users.get_user_by_email(email)
#
#     if not user:
#         return HTTPException(status_code=400, detail="User not found")
#
#     await crud.users.reset_password(user, user_in.password)
#
#     return {"message": "Password reset successfully"}