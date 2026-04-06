from datetime import datetime, date
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import TIMESTAMP, Date, String, ForeignKey, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models.stint_model import Stint
    from app.models.pitstop_model import PitStop
    from app.models.lap_model import Lap


class RaceSession(Base):
    __tablename__ = "session"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_date: Mapped[date] = mapped_column(Date, default=date.today)
    race_duration: Mapped[int]
    track: Mapped[str] = mapped_column(String)

    session_cars: Mapped[List["SessionCar"]] = relationship(
        back_populates="session", order_by="SessionCar.id"
    )
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )


class SessionCar(Base):
    __tablename__ = "session_car"

    id: Mapped[int] = mapped_column(primary_key=True)
    session_id: Mapped[int] = mapped_column(
        ForeignKey("session.id", ondelete="CASCADE")
    )
    car_id: Mapped[int]
    car_name: Mapped[str]
    car_class: Mapped[str]

    session: Mapped["RaceSession"] = relationship(back_populates="session_cars")

    stints: Mapped[List["Stint"]] = relationship(
        back_populates="session_car", order_by="Stint.start_time"
    )
    pit_stops: Mapped[List["PitStop"]] = relationship(
        back_populates="session_car", order_by="PitStop.road_enter_time"
    )
    laps: Mapped[List["Lap"]] = relationship(
        back_populates="session_car", order_by="Lap.start_time"
    )

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    __table_args__ = UniqueConstraint(
        "session_id", "car_id", name="unqiue_car_per_session"
    )
