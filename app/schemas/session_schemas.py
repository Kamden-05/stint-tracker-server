from pydantic import BaseModel, ConfigDict
import datetime

from app.schemas.stint_schemas import StintRead
from app.schemas.pit_schemas import PitRead
from app.schemas.lap_schemas import LapRead


class RaceSessionBase(BaseModel):
    id: int
    track: str
    race_duration: int
    session_date: datetime.date

    model_config = ConfigDict(from_attributes=True)


class SessionCarBase(BaseModel):
    car_id: int
    car_name: str
    car_class: str

    model_config = ConfigDict(from_attributes=True)


class SessionCarRead(SessionCarBase):
    session_id: int


class SessionCarCreate(SessionCarBase):
    session_id: int


class RaceSessionRead(RaceSessionBase):
    session_cars: list["SessionCarRead"] = []


class RaceSessionCreate(RaceSessionBase, SessionCarBase):
    pass
