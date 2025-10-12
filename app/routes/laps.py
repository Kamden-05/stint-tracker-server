from fastapi import APIRouter, FastAPI
from stint_core.lap_base import Lap

router = APIRouter(prefix="/laps", tags=["laps"])
