from sqlalchemy import String, DateTime, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional, TYPE_CHECKING
from datetime import datetime
from . import BaseModel

if TYPE_CHECKING:
    from .stint import Stint

class Session(BaseModel):
    __tablename__ = "session"

    session_id: Mapped[int] = mapped_column(primary_key=True)
    session_type: Mapped[int]
    session_date: Mapped[datetime] = mapped_column(DateTime)
    sim_time: Mapped[datetime] = mapped_column(TIMESTAMP)
    stints: Mapped[List["Stint"]] = relationship(back_populates='session')
    track: Mapped[str] = mapped_column(String)
    car_class: Mapped[str] = mapped_column(String)
    car = Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))