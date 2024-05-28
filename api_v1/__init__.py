from fastapi import APIRouter

from .products.views import router as product_router
from .users.views import router as users_router
from .cart.views import router as cart_router
from .order.views import router as order_router

router = APIRouter()
router.include_router(router=product_router, prefix="/products")
router.include_router(router=users_router, prefix="/users")
router.include_router(router=cart_router, prefix="/cart")
router.include_router(router=order_router, prefix="/order")
