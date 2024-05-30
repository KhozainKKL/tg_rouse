from typing import Annotated

from annotated_types import MinLen, MaxLen
from fastapi_users import schemas


class UserRead(schemas.BaseUser[int]):
    pass


class UserCreate(schemas.BaseUserCreate):
    first_name: str | None
    last_name: str | None
    telegram_id: int
    phone: int | None
    geo: str | None


class UserUpdate(schemas.BaseUserUpdate):
    pass
