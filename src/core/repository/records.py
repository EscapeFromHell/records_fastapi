import logging
import os
import uuid

from fastapi import HTTPException, UploadFile
from fastapi.responses import FileResponse
from pydantic import PositiveInt
from pydub import AudioSegment

from src.core.crud import crud_records, crud_users
from src.core.repository.repository import Repository
from src.core.schemas import Record, RecordCreate, RecordResponse
from src.utils import get_logger

logger = get_logger(__file__, logging.DEBUG)


class RecordRepo(Repository):
    def __check_user(self, user_id: PositiveInt, token: str) -> bool:
        """
        Функция проверяет пользователя на наличие в БД.

        :param user_id: ID пользователя
        :param token: Токен пользователя
        :return: Возвращает True если ID пользователя и токен указаны верно.
        """
        user = crud_users.get(db=self.db, id=user_id)
        if not user:
            logger.error(f"Пользователь с ID: {user_id} не найден")
            raise HTTPException(status_code=404, detail=f"Пользователь с ID: {user_id} не найден")
        if user.token != token:
            logger.error("Указан неверный токен")
            raise HTTPException(status_code=403, detail="Указан неверный токен")
        return True

    def __check_file(self, record: UploadFile) -> bool:
        """
        Проверяет формат загружаемого файла.

        :param record: UploadFile
        :return: Возвращает True если аудиозапись в формате WAV
        """
        if not record.filename.endswith(".wav"):
            raise HTTPException(status_code=422, detail="Файл должен быть в формате WAV")
        return True

    def __add_record_to_db(self, user_id: PositiveInt, token: str, file_path: str) -> Record:
        """
        Добавляет запись в БД.

        :param user_id: ID пользователя
        :param token: Токен записи
        :param file_path: Расположение файла
        :return: Record
        """
        record = RecordCreate(user_id=user_id, token=token, file_path=file_path)
        return crud_records.create(db=self.db, obj_in=record)

    def __save_audio_mp3(self, user_id: PositiveInt, record: UploadFile) -> Record:
        """
        Функция для преобразования в формат MP3 и сохранения аудиозаписи.

        :param user_id: ID пользователя
        :param record: Аудиозапись в формате WAV
        :return: Record
        """
        if not os.path.exists("../../audio"):
            os.makedirs("../../audio")

        token = str(uuid.uuid4())
        file_path = f"../../audio/{token}.wav"

        with open(file_path, "wb") as audio_file:
            audio_file.write(record.file.read())

        mp3_path = f"../../audio/{token}.mp3"
        audio = AudioSegment.from_wav(file_path)
        audio.export(mp3_path, format="mp3")
        os.remove(file_path)
        return self.__add_record_to_db(user_id=user_id, token=token, file_path=mp3_path)

    async def upload_record(self, user_id: PositiveInt, user_token: str, record: UploadFile) -> RecordResponse:
        """
        Функция для загрузки аудиозаписи.

        :param user_id: ID пользователя
        :param user_token: Токен пользователя
        :param record: Аудиозапись в формате WAV
        :return: RecordResponse
        """
        if self.__check_user(user_id=user_id, token=user_token) and self.__check_file(record=record):
            record = self.__save_audio_mp3(user_id=user_id, record=record)
        download_url = f"http://127.0.0.1:8001/api_v1/records/?record_id={record.id}&user_id={user_id}"
        return RecordResponse(download_url=download_url)

    async def download_record(self, record_id: PositiveInt, user_id: PositiveInt) -> FileResponse:
        """
        Функция для скачивания аудиозаписи.

        :param record_id: ID записи
        :param user_id: ID пользователя
        :return: FileResponse (аудиозапись в формате MP3)
        """
        record = crud_records.get(db=self.db, id=record_id)
        if not record:
            logger.error(f"Запись с ID: {record_id} не найдена")
            raise HTTPException(status_code=404, detail=f"Запись с ID: {record_id} не найдена")
        if record.user_id != user_id:
            logger.error("Не совпадает User ID")
            raise HTTPException(status_code=403, detail="Не совпадает User ID")

        mp3_path = f"../../audio/{record.token}.mp3"
        if not os.path.isfile(mp3_path):
            logger.error("Запись не найдена")
            raise HTTPException(status_code=404, detail="Запись не найдена")
        return FileResponse(mp3_path, media_type="audio/mpeg", filename=f"{record.token}.mp3")
