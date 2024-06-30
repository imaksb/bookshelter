import requests
from fastapi import APIRouter, HTTPException
from starlette import status

from app.api.deps import CurrentUser, SessionDep
from app.infrastructure.schemas import BookBase, UserBookIn

router = APIRouter(prefix="/users/books", tags=['user-books'])


@router.post("/")
async def add_book(session: SessionDep, user: CurrentUser, book_id: int, is_read: bool = False):
    book = await session.books.get_book(book_id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    note_obj = UserBookIn(user=user, book=book, is_read=is_read)
    await session.user_books.create_one(note_obj)

    return {"message": "Book added to your library"}


@router.get("/")
async def get_user_books(*, session: SessionDep, user: CurrentUser):
    books = await session.user_books.get_book_by_user_id(user.user_id)
    return books
