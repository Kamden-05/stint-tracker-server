from app.repositories.base_crud import CRUDRepository
from app.models.stint_model import Stint

stint_crud = CRUDRepository(model=Stint)