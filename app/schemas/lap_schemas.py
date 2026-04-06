from pydantic import BaseModel, ConfigDict


class LapBase(BaseModel):
    number: int
    start_time: float
    lap_time: float


class LapCreate(LapBase):
    session_id: int
    car_id: int
    stint_id: int


class LapRead(LapBase):
    id: int
    stint_id: int
    model_config = ConfigDict(from_attributes=True)
