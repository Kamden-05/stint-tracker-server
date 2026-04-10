import logging

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.lap_model import Laps
from app.repositories.base_crud import CRUDRepository

logger = logging.getLogger(__name__)


lap_crud = CRUDRepository(model=Laps)


def get_many(
    self, db: Session, *args, skip: int = 0, limit: int = 100, **kwargs
) -> list[Laps]:
    logger.debug(
        "Retrieving records for %s with skip %s and limit %s",
        self.model.__name__,
        skip,
        limit,
    )
    filters = [
        *args,
        *[getattr(self.model, k) == v for k, v in kwargs.items() if v is not None],
    ]
    stmt = (
        select(self.model)
        .where(*filters)
        .order_by(Laps.number)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()
