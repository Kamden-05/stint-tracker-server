from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class LapBase(BaseModel):
    stint_id: int
    lap_number: int = Field(..., alias='number')
    time:float

class LapCreate(LapBase):
    pass
