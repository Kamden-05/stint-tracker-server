from pydantic import BaseModel, computed_field, Field, field_serializer, ConfigDict
from enum import Enum
from typing import List, Optional
from app.schemas.lap_schemas import LapBase as Lap


class Skies(Enum):
    CLEAR = 0
    PARTLY_CLOUDY = 1
    MOST_CLOUDLY = 2
    OVERCAST = 3


class TrackWetness(Enum):
    UNKNOWN = 0
    DRY = 1
    MOSTLY_DRY = 2
    VERY_LIGHTLY_WET = 3
    LIGHTLY_WET = 4
    MODERATELY_WET = 5
    VERY_WET = 6
    EXTREMELY_WET = 7


class StintBase(BaseModel):
    driver_name: str
    start_time: float
    start_position: int
    start_incidents: int
    start_fuel: float
    track_temp: float
    track_wetness: int
    sky_cover: int
    precipitation: float


class StintRead(StintBase):
    id: int
    session_id: int
    car_id: int
    laps: List[Lap] = []

    track_wetness: TrackWetness
    sky_cover: Skies
    end_time: Optional[float] = Field(default=None, exclude=True)
    end_position: Optional[float] = None
    end_fuel: Optional[float] = None
    end_incidents: Optional[float] = Field(default=None, exclude=True)

    @field_serializer("track_wetness", "sky_cover")
    def serialize_enums(self, value, _info):
        return value.name.replace("_", " ").title()

    @computed_field
    def duration(self) -> Optional[float]:
        end = self.end_time

        if end is None:
            return None

        if end < self.start_time:
            end += 86400

        return end - self.start_time

    @computed_field
    def incidents(self) -> Optional[int]:
        if self.end_incidents is None:
            return None
        else:
            return self.end_incidents - self.start_incidents

    model_config = ConfigDict(from_attributes=True)


class StintCreate(StintBase):
    session_id: int
    car_id: int


class StintUpdate(BaseModel):
    end_time: Optional[float] = None
    end_position: Optional[int] = None
    end_fuel: Optional[float] = None
    end_incidents: Optional[float] = None
    is_complete: bool = False
