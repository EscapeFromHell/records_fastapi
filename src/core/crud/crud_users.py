from sqlalchemy.orm import Session

from src.core.crud import CRUDBase
from src.core.models import User
from src.core.schemas import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_user_by_username(self, db: Session, username: str) -> User:
        """Возвращает пользователя по username."""
        return db.query(self.model).filter(self.model.username == username).first()


crud_users = CRUDUser(User)
