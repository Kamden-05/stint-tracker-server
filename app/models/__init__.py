from sqlalchemy.orm import DeclarativeBase

class BaseModel(DeclarativeBase):
    pass

from .lap import Lap
from .stint import Stint
from .session import Session