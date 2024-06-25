from fastapi import APIRouter, HTTPException
from starlette import status

from app.api.deps import CurrentUser, SessionDep
from app.infrastructure.schemas import BookBase, UserBookIn

router = APIRouter(prefix="/users/books")


@router.post("/")
async def add_book(session: SessionDep, user: CurrentUser, book_id: int, is_read: bool = False):
    book = await session.books.get_book(book_id)

    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Book not found")

    note_obj = UserBookIn(user=user, book=book, is_read=is_read)
    await session.user_books.add_user_book(note_obj)

    return {"message": "Book added to your library"}
