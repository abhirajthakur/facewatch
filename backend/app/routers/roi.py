from fastapi import APIRouter, HTTPException

from app.core.state import app_state

router = APIRouter(
    prefix="/roi",
    tags=["roi"],
)


@router.get("/latest")
async def get_latest_roi():
    if app_state.latest_roi is None:
        raise HTTPException(
            status_code=404,
            detail="No ROI data available",
        )

    return app_state.latest_roi
