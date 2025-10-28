from pydantic import BaseModel

class LapBase(BaseModel):
    stint_id: int
    number: int
    time: float


class LapCreate(LapBase):
    pass


class LapRead(LapBase):
    id: int

    class Config:
        from_attributes = True
