from pydantic import BaseModel, Field, computed_field
from typing import List, Optional
from stint_core.lap_base import LapBase as Lap

class StintBase(BaseModel):
    session_id: int
    stint_number: int = Field(..., alias="number")
    driver_name: str
    start_time: float
    start_position: int
    start_fuel: float
    end_position: Optional[int] = None
    stint_length: Optional[float] = Field(alias="length")
    end_fuel: Optional[float] = None
    refuel_amount: Optional[float] = None
    pit_service_duration: Optional[float] = None
    tire_change: Optional[bool] = None


class StintRead(StintBase):
    pass


class StintCreate(StintBase):
    pass


class StintUpdate(StintBase):
    pass
