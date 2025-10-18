from pydantic import BaseModel, Field, ConfigDict
import datetime

class RaceSessionBase(BaseModel):
    session_date: datetime.date
    track: str
    car_class: str
    car: str
    sim_date: datetime.date
    sim_time: datetime.time

class RaceSessionRead(RaceSessionBase):
    pass

class RaceSessionCreate(RaceSessionBase):
    id: int

