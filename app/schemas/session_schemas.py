from pydantic import BaseModel
import datetime


class RaceSessionBase(BaseModel):
    track: str
    car_class: str
    car: str
    race_duration: int
    session_date: datetime.date


class RaceSessionRead(RaceSessionBase):
    class Config:
        from_attributes = True


class RaceSessionCreate(RaceSessionBase):
    id: int
