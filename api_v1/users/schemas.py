from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, EmailStr, ConfigDict


class UserBase(BaseModel):
    username: Annotated[
        str,
        MinLen(3),
        MaxLen(20),
    ]
    first_name: str | None
    last_name: str | None
    email: EmailStr
    phone: int | None
    geo: str | None
    push_email: bool = False
    telegram_id: int | None


class CreateUser(UserBase):
    pass


class User(UserBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
