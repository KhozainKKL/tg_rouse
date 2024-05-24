"""
Create
Read
Update
Delete
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.engine import Result

from api_v1.users.schemas import CreateUser, User
from core.models.database import Profile


async def get_users(session: AsyncSession) -> list[Profile]:
    stmt = select(Profile).order_by(Profile.id)
    result: Result = await session.execute(stmt)
    users = result.scalars().all()
    return list(users)


async def get_user(session: AsyncSession, telegram_id: int) -> Profile | None:
    result = await session.execute(select(Profile).filter_by(telegram_id=telegram_id))
    return result.scalars().first()


async def create_user(session: AsyncSession, user_in: CreateUser) -> Profile:
    user = Profile(**user_in.model_dump())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
