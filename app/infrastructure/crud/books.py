from typing import Sequence

from sqlalchemy import select, delete

from app.infrastructure.crud.base import BaseCRUD
from app.infrastructure.models.books import Book
from app.infrastructure.schemas import BookBase


class BookCRUD(BaseCRUD):
    async def create_book(self, book_in: BookBase):
        book_obj = Book(**book_in.dict())
        self.session.add(book_obj)
        await self.session.commit()

    async def delete_book(self, book_id: int):
        delete_stmt = delete(Book).where(Book.book_id == book_id)
        await self.session.execute(delete_stmt)
        await self.session.commit()

    async def get_books(self, page: int) -> list[Book]:
        select_stmt = select(Book).limit(10).offset((page - 1) * 10)
        result = await self.session.execute(select_stmt)
        return result.scalars().all()

    async def get_book(self, book_id: int) -> Book:
        select_stmt = select(Book).where(Book.book_id == book_id)
        result = await self.session.execute(select_stmt)
        return result.scalar_one()
