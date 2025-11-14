from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import TIMESTAMP, ForeignKey, String, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models.lap_model import Lap
    from app.models.session_model import RaceSession
    from app.models.pitstop_model import PitStop


class Stint(Base):
    __tablename__ = "stint"

    id: Mapped[int] = mapped_column(primary_key=True)

    session_id: Mapped[int] = mapped_column(
        ForeignKey("session.id", ondelete="CASCADE")
    )
    session: Mapped["RaceSession"] = relationship(back_populates="stints")
    laps: Mapped[List["Lap"]] = relationship(
        back_populates="stint", order_by="Lap.number"
    )
    pit_stop: Mapped["PitStop"] = relationship(back_populates="stint", uselist=False)

    driver_name: Mapped[str] = mapped_column(String)
    number: Mapped[int]
    start_time: Mapped[float]
    start_position: Mapped[int]
    start_incidents: Mapped[int]
    start_fuel: Mapped[float]
    end_time: Mapped[Optional[float]]
    end_position: Mapped[Optional[int]]
    end_fuel: Mapped[Optional[float]]
    end_incidents: Mapped[Optional[int]]

    is_complete: Mapped[bool] = mapped_column(default=False)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("session_id", "number", name="unique_stint_per_session"),
    )
