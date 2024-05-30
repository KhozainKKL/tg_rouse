from fastapi import APIRouter
from fastapi_users import FastAPIUsers

from core.models.database import Profile
from .auth.auth import auth_backend
from .auth.manager import get_user_manager
from .auth.schemas import UserRead, UserCreate
from .products.views import router as product_router
from .users.views import router as users_router
from .cart.views import router as cart_router
from .order.views import router as order_router

fastapi_users = FastAPIUsers[Profile, int](get_user_manager, [auth_backend])

router = APIRouter()
router.include_router(router=product_router, prefix="/products")
router.include_router(router=users_router, prefix="/users")
router.include_router(router=cart_router, prefix="/cart")
router.include_router(router=order_router, prefix="/order")
router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/auth/jwt", tags=["Auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)
