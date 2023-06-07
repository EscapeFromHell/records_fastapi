from fastapi import APIRouter, Depends, UploadFile
from fastapi.responses import FileResponse
from pydantic import PositiveInt

from src.core.repository import RecordRepo
from src.core.schemas import RecordResponse
from src.deps import record_repo as deps_record_repo

router = APIRouter()


@router.post("/", status_code=201, response_model=RecordResponse)
async def upload_audio(
    *,
    user_id: PositiveInt,
    user_token: str,
    record: UploadFile,
    record_repo: RecordRepo = Depends(deps_record_repo),
) -> RecordResponse:
    """
    Функция для загрузки аудиозаписи.

    :param user_id: ID пользователя
    :param user_token: Токен пользователя
    :param record: Аудиозапись в формате WAV
    :param record_repo: RecordRepo
    :return: RecordResponse
    """
    return await record_repo.upload_record(user_id=user_id, user_token=user_token, record=record)


@router.get("/", status_code=200)
async def download_audio(
    *,
    record_id: PositiveInt,
    user_id: PositiveInt,
    record_repo: RecordRepo = Depends(deps_record_repo),
) -> FileResponse:
    """
    Функция для скачивания аудиозаписи.

    :param record_id: ID записи
    :param user_id: ID пользователя
    :param record_repo: RecordRepo
    :return: FileResponse (аудиозапись в формате MP3)
    """
    return await record_repo.download_record(record_id=record_id, user_id=user_id)
