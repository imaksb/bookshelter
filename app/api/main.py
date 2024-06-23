from fastapi import APIRouter
from app.api.routes import users, login

api_router = APIRouter()

api_router.include_router(users.router, tags=["users"])
api_router.include_router(login.router, tags=["login"])

