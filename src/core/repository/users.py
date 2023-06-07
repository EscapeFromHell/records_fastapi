import logging
import uuid

from fastapi import HTTPException

from src.core.crud import crud_users
from src.core.repository.repository import Repository
from src.core.schemas import User, UserCreate
from src.utils import get_logger

logger = get_logger(__file__, logging.DEBUG)


class UserRepo(Repository):
    def __check_username(self, username: str) -> bool:
        """
        Функция проверяет имя пользователя на наличие в БД.

        :param username: Имя пользователя
        :return bool: True если имя пользователя есть в БД, False если нет
        """
        if crud_users.get_user_by_username(db=self.db, username=username):
            return True
        return False

    async def add_user(self, username: str) -> User:
        """
        Функция для записи пользователя в БД.

        :param username: Имя пользователя
        :return User: User с уникальным id и токеном
        """
        if self.__check_username(username=username):
            logger.error("Пользователь с таким именем уже существует")
            raise HTTPException(status_code=422, detail="Пользователь с таким именем уже существует")
        token = str(uuid.uuid4())
        user = UserCreate(username=username, token=token)
        return crud_users.create(db=self.db, obj_in=user)
