from pydantic import BaseModel, computed_field, Field
from typing import List, Optional
from app.schemas.lap_schemas import LapBase as Lap


class StintBase(BaseModel):
    number: int
    driver_name: str

    start_time: float
    start_position: int
    start_incidents: int
    start_fuel: float


class StintReadRaw(StintBase):
    id: int
    session_id: int
    laps: List[Lap] = []

    end_time: Optional[float] = None
    end_position: Optional[float] = None
    end_fuel: Optional[float] = None
    end_incidents: Optional[float] = None

    @computed_field
    def duration(self) -> Optional[float]:
        if self.end_time is None:
            return None

        end = self.end_time

        if end < self.start_time:
            end += 86400

        return end - self.start_time

    @computed_field
    def incidents(self) -> Optional[int]:
        if self.end_incidents is None:
            return None
        else:
            return self.end_incidents - self.start_incidents

    class Config:
        from_attributes = True


class StintRead(StintReadRaw):
    end_time: Optional[float] = Field(default=None, exclude=True)
    end_incidents: Optional[int] = Field(default=None, exclude=True)


class StintCreate(StintBase):
    session_id: int


class StintUpdate(BaseModel):
    end_time: Optional[float] = None
    end_position: Optional[int] = None
    end_fuel: Optional[float] = None
    end_incidents: Optional[float] = None
    is_complete: bool = False
