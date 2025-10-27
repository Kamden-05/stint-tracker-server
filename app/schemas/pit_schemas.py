from pydantic import BaseModel, computed_field


class PitBase(BaseModel):
    stint_id: int
    road_enter_time: float
    service_start_time: float
    refuel_amount: float
    repairs: bool
    tire_change: bool
    service_end_time: float
    road_exit_time: float


class PitRead(PitBase):
    id: int

    @computed_field
    def service_time(self) -> float:
        end = self.service_end_time

        if end < self.service_start_time:
            end += 86400

        return end - self.service_start_time

    @computed_field
    def pit_time(self) -> float:
        end = self.road_exit_time

        if end < self.road_enter_time:
            end += 86400

        return end - self.road_enter_time

    class Config:
        from_attributes = True


class PitCreate(PitBase):
    pass
