from app.repositories.base_crud import CRUDRepository
from app.models import ApiKey

api_crud = CRUDRepository(model=ApiKey)
