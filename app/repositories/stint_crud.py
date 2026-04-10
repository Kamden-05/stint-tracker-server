from app.repositories.base_crud import CRUDRepository
from app.models.stint_model import Stints

stint_crud = CRUDRepository(model=Stints)
