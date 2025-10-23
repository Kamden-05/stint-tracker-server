from pydantic import BaseModel

class LapBase(BaseModel):
    number: int
    time: float


class LapCreate(LapBase):
    stint_id: int


class LapRead(LapBase):
    stint_id: int

    class Config:
        from_attributes = True
