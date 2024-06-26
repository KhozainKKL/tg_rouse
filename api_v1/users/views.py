from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.users.schemas import CreateUser, User
from api_v1.users import crud
from core.models import db_helper

router = APIRouter(tags=["Users"])


@router.post("/", response_model=User)
async def create_user(
    user_in: CreateUser,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_user(session=session, user_in=user_in)


@router.get("/", response_model=list[User])
async def get_users(
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.get_users(session=session)


@router.get("/{telegram_id}/", response_model=User)
async def get_user(
    telegram_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.get_user(session=session, telegram_id=telegram_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User from telegram_id:{telegram_id} not found",
    )
