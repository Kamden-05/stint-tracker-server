from pydantic import BaseModel, ConfigDict

class LapBase(BaseModel):
    stint_id: int
    number: int
    time: float


class LapCreate(LapBase):
    pass


class LapRead(LapBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
