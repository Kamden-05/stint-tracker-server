from app.repositories.base import CRUDRepository
from app.models.stint import Session

session_crud = CRUDRepository(model=Session)
