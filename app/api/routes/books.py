from typing import Sequence, Annotated

import aiofiles
from fastapi import APIRouter, UploadFile, Form
from fastapi_cache.decorator import cache

from app.api.deps import SessionDep, CurrentUserAdmin, CurrentUser
from app.infrastructure.models.books import Book
from app.infrastructure.schemas import BookBase

router = APIRouter(prefix="/books")


@router.get("/")
@cache(expire=60)
async def get_books(session: SessionDep) -> list[BookBase]:
    return await session.books.get_books(1)


@router.get("/{book_id}")
async def get_book(session: SessionDep, book_id: int):
    return await session.books.get_book(book_id)


@router.post("/", status_code=201)
async def create_book(session: SessionDep, name: str = Form(min_length=4, max_length=50),
                      author: str = Form(min_length=5, max_length=50),
                      isbn: Annotated[str | None, Form(min_length=10, max_length=13)] = None,
                      image: UploadFile | None = None):
    path_to_file = f"static/{image.filename}"

    async with aiofiles.open(path_to_file, 'wb') as out_file:
        content = await image.read()
        await out_file.write(content)

    book_in = BookBase(name=name, author=author, image=path_to_file, isbn=isbn)
    await session.books.create_one(book_in)
    return {"message": "Book created successfully."}


@router.delete("/{book_id}", dependencies=[CurrentUserAdmin])
async def delete_book(session: SessionDep, book_id: int):
    return await session.books.delete_book(book_id)
