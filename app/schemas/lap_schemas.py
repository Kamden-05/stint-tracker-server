from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class LapBase(BaseModel):
    lap_number: int = Field(..., alias='number')
    time:float

class LapCreate(LapBase):
    stint_id: int
