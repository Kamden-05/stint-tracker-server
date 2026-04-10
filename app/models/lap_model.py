from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy import func, UniqueConstraint, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models import SessionCars, Stints


class Laps(Base):
    __tablename__ = "laps"

    id: Mapped[int] = mapped_column(primary_key=True)

    session_id: Mapped[int]
    car_id: Mapped[int]

    __table_args__ = (
        ForeignKeyConstraint(
            ["session_id", "car_id"],
            ["session_cars.session_id", "session_cars.car_id"],
            ondelete="CASCADE",
        ),
        UniqueConstraint("stint_id", "number", name="unique_stint_lap_number"),
    )
    stint_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("stints.id", ondelete="SET NULL")
    )
    session_car: Mapped["SessionCars"] = relationship(back_populates="laps")
    stint: Mapped["Stints"] = relationship(back_populates="laps")
    number: Mapped[int]
    lap_time: Mapped[float]
    end_fuel: Mapped[float]
    end_time: Mapped[float]

    # pylint: disable=not-callable
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
