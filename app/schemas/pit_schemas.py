from typing import Optional
from pydantic import BaseModel, Field, computed_field


class PitBase(BaseModel):
    stint_id: int
    road_enter_time: float
    service_start_time: float
    fuel_start_amount: float
    repairs: bool
    tire_change: bool


class PitRead(PitBase):
    id: int

    road_enter_time: float = Field(exclude=True)
    service_start_time: float = Field(exclude=True)
    service_end_time: Optional[float] = Field(exclude=True, default=None)
    road_exit_time: Optional[float] = Field(exclude=True, default=None)

    @computed_field
    def service_time(self) -> float:
        if self.service_end_time:
            end = self.service_end_time

            if end < self.service_start_time:
                end += 86400

            return end - self.service_start_time
        else:
            return -1.0

    @computed_field
    def pit_time(self) -> float:
        if self.road_exit_time:
            end = self.road_exit_time

            if end < self.road_enter_time:
                end += 86400

            return end - self.road_enter_time
        else:
            return -1.0

    class Config:
        from_attributes = True


class PitCreate(PitBase):
    pass


class PitUpdate(BaseModel):
    service_end_time: float
    fuel_end_amount: float
    road_exit_time: float
