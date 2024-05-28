from pydantic import BaseModel, ConfigDict


class CartBase(BaseModel):
    user: int
    product: int
    quantity: int = 1


class CartCreate(CartBase):
    pass


class Cart(CartBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
