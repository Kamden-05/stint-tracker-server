from pydantic import BaseModel, Field, ConfigDict
import datetime

class RaceSessionBase(BaseModel):
    session_date: datetime.date
    track: str
    car_class: str
    car: str
    sim_date: datetime.date
    sim_time: datetime.time

    class Config:
        from_attributes = True


class RaceSessionRead(RaceSessionBase):
    id: int

class RaceSessionCreate(RaceSessionBase):
    id: int
