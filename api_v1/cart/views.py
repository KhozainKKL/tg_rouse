from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from api_v1.cart import crud
from core.models import db_helper
from api_v1.cart.schemas import Cart, CartCreate

router = APIRouter(tags=["Cart"])


@router.get("/{telegram_id}/", response_model=list[Cart])
async def get_cart(
    telegram_id: int,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    user = await crud.get_cart(session=session, telegram_id=telegram_id)
    if user:
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Cart from telegram_id:{telegram_id} not found",
    )


@router.post("/", response_model=Cart)
async def add_cart(
    user_in: CartCreate,
    session: AsyncSession = Depends(db_helper.scoped_session_dependency),
):
    return await crud.add_cart(session=session, product_in=user_in)
