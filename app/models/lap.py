from sqlalchemy import ForeignKey, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column
from typing import Optional
from datetime import datetime
from app.database.base_class import Base


class Lap(Base):
    __tablename__ = "lap"

    lap_id: Mapped[int] = mapped_column(primary_key=True)
    stint_id: Mapped[int] = mapped_column(ForeignKey("stint.id"))
    number: Mapped[int]
    time: Mapped[float]
    incidents: Mapped[Optional[int]]
    start_position: Mapped[Optional[int]]
    end_position: Mapped[Optional[int]]
    pit: Mapped[Optional[bool]]
    created_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
    updated_at: Mapped[Optional[datetime]] = mapped_column(TIMESTAMP(timezone=True))
