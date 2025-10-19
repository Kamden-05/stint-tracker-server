from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from .lap_model import Lap
from .stint_model import Stint
from .session_model import RaceSession
