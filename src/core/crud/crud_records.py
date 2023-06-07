from src.core.crud import CRUDBase
from src.core.models import Record
from src.core.schemas import RecordCreate, RecordUpdate


class CRUDRecord(CRUDBase[Record, RecordCreate, RecordUpdate]):
    pass


crud_records = CRUDRecord(Record)
