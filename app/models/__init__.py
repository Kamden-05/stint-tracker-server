from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


from app.models.lap_model import Lap
from app.models.stint_model import Stint
from app.models.session_model import RaceSession
from app.models.pitstop_model import PitStop
