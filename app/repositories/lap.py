from app.repositories.base import CRUDRepository
from app.models.lap import Lap

lap_crud = CRUDRepository(model=Lap)
