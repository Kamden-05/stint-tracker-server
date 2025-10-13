from app.repositories.base import CRUDRepository
from app.models.stint import Lap

lap_crud = CRUDRepository(model=Lap)
