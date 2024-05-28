"""
Create
Read
Update
Delete
"""

from typing import Tuple, Sequence

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession
from core.models import Product
from sqlalchemy.engine import Result
from .schemas import ProductCreate


async def get_products(session: AsyncSession) -> list[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> Product | None:
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> Product:
    product = Product(**product_in.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def get_search_products(
    session: AsyncSession,
    name: str,
) -> Sequence[Product]:
    search_pattern = f"%{name}%"
    result = await session.execute(
        select(Product).filter(Product.name.like(search_pattern))
    )
    return result.scalars().all()
