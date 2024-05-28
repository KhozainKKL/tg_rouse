"""
Create
Read
Update
Delete
"""

from typing import Sequence

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from api_v1.order.schemas import OrderCreate
from core.models.database import Order


async def create_order(session: AsyncSession, cart_in: OrderCreate) -> Order:
    product = Order(**cart_in.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def get_order(session: AsyncSession, telegram_id: int) -> Sequence[Order]:
    result = await session.execute(select(Order).filter(Order.user == telegram_id))
    return result.scalars().all()
