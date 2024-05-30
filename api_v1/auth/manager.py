from typing import Optional

from environs import Env
from fastapi import Depends
from starlette.requests import Request

from core.models import DatabaseHelper
from core.models.database import Profile
from fastapi_users import BaseUserManager, IntegerIDMixin, models

from core.models.db_helper import get_user_db

env = Env()
env.read_env()
SECRET_JWT = env.str("SECRET_JWT")


class UserManager(IntegerIDMixin, BaseUserManager[Profile, int]):
    reset_password_token_secret = SECRET_JWT
    verification_token_secret = SECRET_JWT

    async def on_after_register(
        self, user: Profile, request: Optional[Request] = None
    ) -> None:
        print(f"User {user.id} has registrated.")


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)
