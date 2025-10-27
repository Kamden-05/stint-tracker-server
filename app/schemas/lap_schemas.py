from pydantic import BaseModel

class LapBase(BaseModel):
    stint_id: int
    number: int
    time: float


class LapCreate(LapBase):
    pass


class LapRead(LapBase):

    class Config:
        from_attributes = True
