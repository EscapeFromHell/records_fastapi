from pydantic import BaseModel, PositiveInt


class UserBase(BaseModel):
    username: str
    token: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class UserInDB(UserBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class User(UserInDB):
    pass
