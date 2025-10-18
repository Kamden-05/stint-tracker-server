from pydantic import BaseModel, Field, ConfigDict
import datetime

class RaceSessionBase(BaseModel):
    model_config = ConfigDict(frozen=True)

    session_id: int = Field(..., alias="id")
    session_date: datetime.date
    track: str
    car_class: str
    car: str
    sim_date: datetime.date
    sim_time: datetime.time

class RaceSessionCreate(RaceSessionBase):
    pass
