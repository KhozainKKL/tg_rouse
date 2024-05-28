"""
Create
Read
Update
Delete
"""

from typing import Sequence

from sqlalchemy import Result, select
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.database import Cart
from api_v1.cart.schemas import CartCreate


async def add_cart(session: AsyncSession, product_in: CartCreate) -> Cart:
    product = Cart(**product_in.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def get_cart(session: AsyncSession, telegram_id: int) -> Sequence[Cart]:
    result = await session.execute(select(Cart).filter(Cart.user == telegram_id))
    return result.scalars().all()
