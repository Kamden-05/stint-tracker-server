from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import TIMESTAMP, Date, Time, String
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from .stint_model import Stint


class RaceSession(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_date: Mapped[datetime] = mapped_column(Date)
    sim_date: Mapped[datetime] = mapped_column(Date)
    sim_time: Mapped[datetime] = mapped_column(Time)
    stints: Mapped[List["Stint"]] = relationship(
        back_populates="session", order_by="Stint.number"
    )
    track: Mapped[str] = mapped_column(String)
    car_class: Mapped[str] = mapped_column(String)
    car: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
