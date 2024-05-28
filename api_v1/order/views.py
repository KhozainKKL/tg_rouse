from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.order import crud
from core.models import db_helper
from api_v1.order.schemas import Order, OrderCreate

router = APIRouter(tags=["Order"])


@router.post("/", response_model=Order)
async def add_cart(
    user_in: OrderCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.create_order(session=session, cart_in=user_in)


@router.get("/{telegram_id}/", response_model=list[Order])
async def get_order(
    telegram_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.get_order(session=session, telegram_id=telegram_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Order from telegram_id:{telegram_id} not found",
    )
