from datetime import datetime

from pydantic import BaseModel


class ROIResponse(BaseModel):
    x: float
    y: float
    width: float
    height: float
    created_at: datetime
