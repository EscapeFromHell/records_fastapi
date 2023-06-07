from sqlalchemy import Column, Integer, String

from src.core.models.base import Base


class User(Base):
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False, unique=True)
    token = Column(String, nullable=False, unique=True)
