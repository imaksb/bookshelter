from sqlalchemy import select
from app.infrastructure.repositories.base import BaseRepository
from app.infrastructure.models.user_books import UserBook
from app.infrastructure.schemas import UserBookIn


class UserBookRepository(BaseRepository):
    model = UserBookIn

    async def get_book_by_user_id(self, user_id: int):
        select_stmt = select(UserBook).where(UserBook.user.user_id == user_id)
        result = await self.session.execute(select_stmt)
        return result.scalars().all()
