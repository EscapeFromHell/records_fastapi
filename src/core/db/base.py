# Import all the models, so that Base has them before being imported by Alembic
from src.core.models import User  # noqa
