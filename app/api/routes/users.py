from fastapi import APIRouter, HTTPException

from app.api.deps import SessionDep, CurrentUser, CurrentUserAdmin
from app.infrastructure.crud import UserCRUD
from app.infrastructure.schemas import UserIn, UserItem, UserCreate

router = APIRouter(prefix="/users")


@router.post("/join")
async def root(*, crud: SessionDep, user_in: UserCreate):
    user = await crud.users.get_user_by_email(user_in.email)
    if user:
        return HTTPException(status_code=400, detail="The user with this email already exists.")
    await crud.users.create(user_in)
    return {"message": "User created successfully."}


@router.get("/me")
async def read_me(user: CurrentUserAdmin):
    return {"username": user.username}
