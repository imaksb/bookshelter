from datetime import timedelta
from typing import Annotated

import jwt
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr
from starlette import status

from app.api.deps import SessionDep, RateLimitChecker, UserByEmailDep
from app.core import security
from app.core.config import settings
from app.core.security import generate_uuid
from app.infrastructure.database import redis
from app.infrastructure.schemas import UserIn, Tokens, NewPassword

router = APIRouter()
ResetPasswordLimiter = RateLimitChecker()


@router.post("/login", response_model=Tokens)
async def log_in(*, crud: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user_in = UserIn(email=form_data.username, password=form_data.password)
    user = await crud.users.authenticate(user_in)

    if not user:
        raise HTTPException(status_code=400, detail="Password or email is not valid")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = timedelta(minutes=settings.REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = security.create_jwt_token(user.user_id, access_token_expires, "access")
    refresh_token = security.create_jwt_token(user.user_id, refresh_token_expires, "refresh_token")
    return Tokens(access=access_token, refresh=refresh_token)


@router.post("/refresh")
async def get_refresh_token(*, refresh: str) -> Tokens:
    try:
        tokens = security.get_new_access_token(refresh)

        if not tokens:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Refresh token not valid")

        return tokens
    except jwt.InvalidSignatureError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Something went wrong")


@router.post("/password-recovery-request", dependencies=[Depends(ResetPasswordLimiter)])
async def recovery_password(*, session: SessionDep, email: EmailStr):
    _redis_key = f"otp:{email}"
    user = await session.users.get_user_by_email(email)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    reset_token = str(generate_uuid())
    restore_link = (settings.server_host + "/reset-password?email=" + email + "&token=" + reset_token)

    await redis.delete(_redis_key)
    await redis.setex(_redis_key, 300, reset_token)

    return {"message": restore_link}


@router.post("/reset-password")
async def reset_password(session: SessionDep, user: UserByEmailDep, token: str, password: str):
    _redis_key = f"otp:{user.email}"

    user_otp = await redis.get(_redis_key)
    await redis.delete(_redis_key)

    if user_otp == token:
        await session.users.update_password(user.email, password)

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
