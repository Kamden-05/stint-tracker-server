from pydantic import BaseModel, Field, ConfigDict
import datetime

class RaceSessionBase(BaseModel):
    track: str
    car_class: str
    car: str
    sim_time: datetime.time


class RaceSessionRead(RaceSessionBase):
    id: int
    session_date: datetime.date

    class Config:
        from_attributes = True

class RaceSessionCreate(RaceSessionBase):
    id: int

