from fastapi import APIRouter, Depends, Query

from src.core.repository import UserRepo
from src.core.schemas import User
from src.deps import user_repo as deps_user_repo

router = APIRouter()


@router.post("/", status_code=201, response_model=User)
async def add_user(
    *,
    username: str = Query(min_length=5, max_length=20),
    user_repo: UserRepo = Depends(deps_user_repo),
) -> User:
    """
    Добавление нового пользователя.

    :param username: Имя пользователя
    :param user_repo: UserRepo
    :return User: Пользователь с id и токеном
    """
    return await user_repo.add_user(username=username)
