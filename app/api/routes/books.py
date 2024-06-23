from typing import Sequence

from fastapi import APIRouter

from app.api.deps import SessionDep, CurrentUserAdmin, CurrentUser
from app.infrastructure.models.books import Book
from app.infrastructure.schemas import BookBase

router = APIRouter(prefix="/books")


@router.get("/")
async def get_books(session: SessionDep) -> list[BookBase]:
    return await session.books.get_books()


@router.post("/", dependencies=[CurrentUser])
async def create_book(session: SessionDep, book_in: BookBase):
    return await session.books.create_book(book_in)


@router.delete("/{book_id}", dependencies=[CurrentUserAdmin])
async def delete_book(session: SessionDep, book_id: int):
    return await session.books.delete_book(book_id)
