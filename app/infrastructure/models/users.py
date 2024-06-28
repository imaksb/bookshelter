from sqlalchemy import BIGINT, VARCHAR, Boolean
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base, TableNameMixin


class User(Base, TableNameMixin):
    user_id: Mapped[int] = mapped_column(BIGINT, primary_key=True, unique=True, autoincrement=True)
    username: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, unique=True)
    email: Mapped[str] = mapped_column(VARCHAR(50), nullable=False, unique=True)
    hashed_password: Mapped[str] = mapped_column(VARCHAR(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    is_admin: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
