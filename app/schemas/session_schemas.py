import datetime

from pydantic import BaseModel, ConfigDict


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
