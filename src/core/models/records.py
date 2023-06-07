from sqlalchemy import Column, Integer, String

from src.core.models.base import Base


class Record(Base):
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    token = Column(String, nullable=False, unique=True)
    file_path = Column(String, nullable=False, unique=True)
