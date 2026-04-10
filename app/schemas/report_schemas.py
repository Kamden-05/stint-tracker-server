import datetime
from typing import Optional

from pydantic import BaseModel


class StintReport(BaseModel):
    driver_name: str
    start_time: float
    duration: Optional[float]
    num_laps: int
    avg_lap_time: Optional[float]
    fastest_lap_time: Optional[float]
    out_lap_time: Optional[float]
    in_lap_time: Optional[float]
    start_fuel: float
    end_fuel: Optional[float]
    refuel_amount: Optional[float]
    tire_change: bool
    repairs: bool
    service_time: Optional[float]
    num_incidents: Optional[int]
    start_position: int
    end_position: Optional[int]


class RaceReport(BaseModel):
    session_id: int
    session_date: datetime.date
    race_duration: int
    track: str
    car_class: str
    car_name: str

    stints: list[StintReport]
