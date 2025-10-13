from fastapi import APIRouter, FastAPI
from stint_core.lap_base import LapCreate

router = APIRouter(prefix="/laps", tags=["laps"])
