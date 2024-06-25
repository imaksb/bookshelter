from sqlalchemy import select
from app.infrastructure.crud.base import BaseCRUD
from app.infrastructure.models.user_books import UserBook
from app.infrastructure.schemas import UserBookIn


class UserBookCRUD(BaseCRUD):
    async def add_user_book(self, user_book: UserBookIn):
        self.session.add(UserBook(**user_book.dict()))
        await self.session.commit()

    async def get_book_by_user_id(self, user_id: int):
        select_stmt = select(UserBook).where(UserBook.user.user_id == user_id)
        result = await self.session.execute(select_stmt)
        return result.scalars().all()
