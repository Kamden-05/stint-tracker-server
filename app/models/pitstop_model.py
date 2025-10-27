from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models import Base

if TYPE_CHECKING:
    from app.models.stint_model import Stint


class PitStop(Base):
    __tablename__ = "pit_stop"

    id: Mapped[int] = mapped_column(primary_key=True)

    stint_id: Mapped[int] = mapped_column(
        ForeignKey("stint.id", ondelete="SET NULL"), nullable=True, unique=True
    )
    stint: Mapped["Stint"] = relationship(back_populates="pit_stop")

    road_enter_time: Mapped[float]
    service_start_time: Mapped[float]
    refuel_amount: Mapped[float]
    repairs: Mapped[bool]
    tire_change: Mapped[bool]
    service_end_time: Mapped[float]
    road_exit_time: Mapped[float]

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[Optional[datetime]] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )
