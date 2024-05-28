from pydantic import BaseModel, ConfigDict


class OrderBase(BaseModel):
    user: int
    cart: int
    paid: bool = False


class OrderCreate(OrderBase):
    pass


class Order(OrderBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
