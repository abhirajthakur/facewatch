from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db

app = FastAPI(
    title="FaceWatch - Face Detection API",
    version="1.0.0",
)


@app.get("/health")
async def health_check(
    db: AsyncSession = Depends(get_db),
):
    await db.execute(text("SELECT 1"))

    return {
        "status": "ok",
        "database": "connected",
    }
