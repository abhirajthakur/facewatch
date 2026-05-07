from fastapi import APIRouter, HTTPException

from app.core.state import app_state

router = APIRouter(
    prefix="/video",
    tags=["video"],
)


@router.get("/latest")
async def get_latest_video():
    if app_state.latest_processed_frame is None:
        raise HTTPException(
            status_code=404,
            detail="No processed frame available",
        )

    return {
        "frame": app_state.latest_processed_frame,
    }
