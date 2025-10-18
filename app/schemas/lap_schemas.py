from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class LapBase(BaseModel):
    number: int
    time: float


class LapCreate(LapBase):
    stint_id: int


class LapRead(LapBase):
    stint_id: int

    class Config:
        from_attributes = True
