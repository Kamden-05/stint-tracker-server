from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import TIMESTAMP, ForeignKey, String, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from . import Base

if TYPE_CHECKING:
    from .lap_model import Lap
    from .session_model import RaceSession


class Stint(Base):
    __tablename__ = "stint"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("session.id", ondelete="CASCADE")
    )
    number: Mapped[int]
    session: Mapped["RaceSession"] = relationship(back_populates="stints")
    laps: Mapped[List["Lap"]] = relationship(
        back_populates="stint", order_by="Lap.number"
    )
    driver_name: Mapped[str] = mapped_column(String)
    start_time: Mapped[float]
    length: Mapped[Optional[float]]
    start_position: Mapped[int]
    end_position: Mapped[Optional[int]]
    start_fuel: Mapped[float]
    end_fuel: Mapped[Optional[float]]
    refuel_amount: Mapped[Optional[float]]
    tire_change: Mapped[Optional[bool]]
    repairs: Mapped[Optional[bool]]
    pit_service_duration: Mapped[Optional[float]]
    incidents: Mapped[Optional[int]]
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("session_id", "number", name="unique_stint_per_session"),
    )
