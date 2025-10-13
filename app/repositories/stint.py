from app.repositories.base import CRUDRepository
from app.models.stint import Stint

stint_crud = CRUDRepository(model=Stint)