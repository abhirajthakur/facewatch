from datetime import datetime, timezone

from sqlalchemy import DateTime, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class ROIDetection(Base):
    __tablename__ = "roi_detections"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    x: Mapped[float] = mapped_column(Float)
    y: Mapped[float] = mapped_column(Float)

    width: Mapped[float] = mapped_column(Float)
    height: Mapped[float] = mapped_column(Float)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
