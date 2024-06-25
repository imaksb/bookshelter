from fastapi import APIRouter
from app.api.routes import users, login, books, user_books

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"])
api_router.include_router(user_books.router, tags=["users"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(books.router, tags=['books'])
