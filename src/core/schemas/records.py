from pydantic import AnyHttpUrl, BaseModel, PositiveInt


class RecordBase(BaseModel):
    user_id: PositiveInt
    token: str
    file_path: str


class RecordCreate(RecordBase):
    pass


class RecordUpdate(RecordBase):
    pass


class RecordInDB(RecordBase):
    id: PositiveInt

    class Config:
        orm_mode = True


class Record(RecordInDB):
    pass


class RecordResponse(BaseModel):
    download_url: AnyHttpUrl
