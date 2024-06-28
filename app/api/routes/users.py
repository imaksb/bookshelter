from fastapi import APIRouter, HTTPException
from starlette import status

from app.api.deps import SessionDep, CurrentUser, CurrentUserAdmin
from app.core.security import get_payload, generate_confirm_email_token
from app.infrastructure.schemas import UserIn, UserItem, UserCreate, EmailTokenPayload
from fastapi import BackgroundTasks

from app.utils import generate_confirm_email

router = APIRouter(tags=['users'])


@router.post("/join")
async def root(*, crud: SessionDep, user_in: UserCreate, background_tasks: BackgroundTasks):
    user = await crud.users.get_user_by_email(user_in.email)
    if user:
        return HTTPException(status_code=400, detail="The user with this email already exists.")
    await crud.users.create(user_in)

    confirm_token = generate_confirm_email_token(
        subject=user_in.username,
        email=user_in.email,
    )
    print(confirm_token)

    background_tasks.add_task(generate_confirm_email, mail_to=user_in.email,
                              username=user_in.username, confirm_token=confirm_token)
    return {"message": "User created successfully. Please confirm mail to continue"}


@router.get("/confirm-email")
async def confirm_email(*, session: SessionDep,
                        email: str, token: str):
    email_token = EmailTokenPayload(**get_payload(token))

    if email_token.email == email:
        user = await session.users.get_user_by_email(email)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail="User not found")

        if user.is_active:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="User already active")

        await session.users.update_user_active_status(
            email=email
        )

        return {"message": "Mail confirmed"}

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User with this email not found")


@router.get("/users/me")
async def read_me(user: CurrentUser):
    return {"username": user.username}
