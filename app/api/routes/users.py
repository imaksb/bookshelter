from fastapi import APIRouter

from app.api.deps import SessionDep
from app.infrastructure.crud import UserCRUD

router = APIRouter()


@router.get("/")
async def root(db: SessionDep):
    user = UserCRUD(db)

    await user.create("test", "", "test", True, False)

    return {"message": "Hello World"}
