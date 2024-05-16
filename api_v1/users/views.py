from fastapi import APIRouter

from api_v1.users.schemas import CreateUser
from api_v1.users import crud

router = APIRouter(tags=["Users"])


@router.post("/")
def create_user(user: CreateUser):
    return crud.create_user(user_in=user)
