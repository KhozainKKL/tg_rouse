from datetime import datetime
from sqlalchemy import ForeignKey, text
from sqlalchemy.orm import Mapped, mapped_column
from .base import Base


class Product(Base):
    name: Mapped[str]
    description: Mapped[str | None]
    price: Mapped[int]
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow(), onupdate=datetime.utcnow
    )
    archived: Mapped[bool] = mapped_column(default=False, nullable=True)


class Profile(Base):
    username: Mapped[str]
    first_name: Mapped[str | None]
    last_name: Mapped[str | None]
    email: Mapped[str | None]
    phone: Mapped[int | None]
    geo: Mapped[str | None]
    push_email: Mapped[bool] = mapped_column(default=False, nullable=True)
    telegram_id: Mapped[int]


class Cart(Base):
    user: Mapped[int] = mapped_column(
        ForeignKey(Profile.telegram_id, ondelete="CASCADE")
    )
    product: Mapped[int] = mapped_column(ForeignKey(Product.id, ondelete="CASCADE"))
    quantity: Mapped[int] = mapped_column(default=1)


class Order(Base):
    user: Mapped[int] = mapped_column(
        ForeignKey(Profile.telegram_id, ondelete="CASCADE")
    )
    cart: Mapped[int] = mapped_column(ForeignKey(Cart.id, ondelete="CASCADE"))
    paid: Mapped[bool] = mapped_column(default=False, nullable=True)
