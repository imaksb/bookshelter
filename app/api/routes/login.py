from datetime import timedelta

from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep
from app.core import security
from app.core.config import settings
from app.infrastructure.schemas import UserIn, Token

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
    return Token(access=access, refresh=refresh)
