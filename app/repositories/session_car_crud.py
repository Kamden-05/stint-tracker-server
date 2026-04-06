from app.repositories.base_crud import CRUDRepository
from app.models.session_model import SessionCar

session_car_crud = CRUDRepository(model=SessionCar)
