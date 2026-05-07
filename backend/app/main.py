from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.routers.frame import router as frame_router
from app.core.config import settings


app = FastAPI(
    title="FaceWatch - Face Detection API",
    version="1.0.0",
)

app.include_router(frame_router, prefix=settings.api_prefix)

@app.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db),
):
    await db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
