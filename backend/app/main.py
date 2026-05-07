from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.config import settings

from app.routers.frame import router as frame_router
from app.routers.roi import router as roi_router
from app.routers.video import router as video_router
from app.routers.websocket import router as websocket_router


app = FastAPI(
    title="FaceWatch - Face Detection API",
    version="1.0.0",
)

app.include_router(frame_router, prefix=settings.api_prefix)
app.include_router(roi_router, prefix=settings.api_prefix)
app.include_router(video_router, prefix=settings.api_prefix)
app.include_router(websocket_router)


@app.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db),
):
    await db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
