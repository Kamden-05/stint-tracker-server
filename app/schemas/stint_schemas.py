from pydantic import BaseModel
from typing import List, Optional
from app.schemas.lap_schemas import LapBase as Lap

class StintBase(BaseModel):
    number: int
    driver_name: str
    start_time: float
    start_position: int
    start_fuel: float
    end_position: Optional[int] = None
    end_fuel: Optional[float] = None
    length: Optional[float] = None
    refuel_amount: Optional[float] = None
    pit_service_duration: Optional[float] = None
    repairs: Optional[bool] = None
    tire_change: Optional[bool] = None


class StintRead(StintBase):
    id: int
    session_id: int
    laps: List[Lap] = []

    class Config:
        from_attributes = True


class StintCreate(StintBase):
    session_id: int


class StintUpdate(BaseModel):
    end_position: Optional[int] = None
    end_fuel: Optional[float] = None
    refuel_amount: Optional[float] = None
    tire_change: Optional[bool] = None
    repairs: Optional[bool] = None
    pit_service_duration: Optional[float] = None
    incidents: Optional[int] = None
    length: Optional[float] = None
