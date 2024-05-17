import datetime
from typing import Annotated

from annotated_types import MinLen, MaxLen
from pydantic import BaseModel, ConfigDict


class ProductBase(BaseModel):
    name: Annotated[str, MinLen(3), MaxLen(20)]
    description: Annotated[str, MaxLen(250)]
    price: int
    created_at: datetime.datetime = datetime.datetime.utcnow()
    updated_at: datetime.datetime = datetime.datetime.utcnow()
    archived: bool | None = False


class ProductCreate(ProductBase):
    pass


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
