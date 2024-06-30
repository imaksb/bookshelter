import uuid
from datetime import timedelta, datetime
from typing import Any
import jwt
import pyotp
from fastapi import HTTPException
from jwt import InvalidTokenError
from passlib.context import CryptContext
from pydantic import ValidationError
from starlette import status

from app.core.config import settings
from app.infrastructure.schemas import TokenPayload, Tokens

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"
totp = pyotp.TOTP(settings.SECRET_KEY)


def create_jwt_token(subject: str | Any, expires_delta: timedelta, token_type: str) -> str:
    expire = datetime.now() + expires_delta
    to_encode = {"exp": expire, "sub": str(subject), "token_type": token_type}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_new_access_token(token: str):
    payload = jwt.decode(
        token, settings.SECRET_KEY, algorithms=[ALGORITHM]
    )

    token_data = TokenPayload(**payload)
    if token_data.exp < datetime.now():
        raise jwt.ExpiredSignatureError

    access = create_jwt_token(token_data.sub, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                              "access")
    refresh = create_jwt_token(token_data.sub, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
                               "refresh")
    return Tokens(access=access, refresh=refresh)


def generate_confirm_email_token(subject: str | Any, email):
    to_encode = {"sub": str(subject),
                 "email": str(email),
                 "token_type": "reset_password"}
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_payload(token: str):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY,
            algorithms=[ALGORITHM],
        )
    except (InvalidTokenError, ValidationError) as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Not valid token")

    return payload


def get_hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def generate_uuid():
    return uuid.uuid4()