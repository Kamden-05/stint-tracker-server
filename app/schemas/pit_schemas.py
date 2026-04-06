from typing import Optional
from pydantic import BaseModel, Field, computed_field, ConfigDict


class PitBase(BaseModel):
    road_enter_time: float
    service_start_time: float
    fuel_start_amount: float
    required_repair_time: float
    optional_repair_time: float
    left_front_tire_change: bool
    left_rear_tire_change: bool
    right_front_tire_change: bool
    right_rear_tire_change: bool


class PitRead(PitBase):
    id: int

    stint_id: int
    car_id: int
    session_id: int
    road_enter_time: float = Field(exclude=True)
    service_start_time: float = Field(exclude=True)
    service_end_time: Optional[float] = Field(exclude=True, default=None)
    road_exit_time: Optional[float] = Field(exclude=True, default=None)
    fuel_end_amount: Optional[float] = Field(exclude=True, default=None)

    @computed_field
    def service_time(self) -> float:
        end_time = self.service_end_time

        if end_time is None:
            return None

        if end_time < self.service_start_time:
            end_time += 86400

        return end_time - self.service_start_time

    @computed_field
    def total_pit_time(self) -> float:
        end_time = self.road_exit_time

        if end_time is None:
            return None

        if end_time < self.road_enter_time:
            end_time += 86400

        return end_time - self.road_enter_time

    @computed_field
    def refuel_amount(self) -> float:
        end_fuel = self.fuel_end_amount

        if end_fuel is None:
            return None

        if end_fuel < self.fuel_start_amount:
            return 0.0

        return end_fuel - self.fuel_start_amount

    model_config = ConfigDict(from_attributes=True)


class PitCreate(PitBase):
    pass


class PitUpdate(BaseModel):
    service_end_time: float
    fuel_end_amount: float
    road_exit_time: float
