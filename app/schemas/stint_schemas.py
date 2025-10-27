from pydantic import BaseModel
from typing import List, Optional
from app.schemas.lap_schemas import LapBase as Lap


class StintBase(BaseModel):
    number: int
    driver_name: str

    start_time: float
    start_position: int
    start_incidents: int
    start_fuel: float


class StintRead(StintBase):
    id: int
    session_id: int
    laps: List[Lap] = []

    end_time: float
    end_position: float
    end_fuel: float
    end_incidents: float

    class Config:
        from_attributes = True


class StintCreate(StintBase):
    session_id: int


class StintUpdate(BaseModel):
    end_time: Optional[float] = None
    end_position: Optional[int] = None
    end_fuel: Optional[float] = None
    end_incidents: Optional[float] = None
    is_complete: Optional[bool] = False
