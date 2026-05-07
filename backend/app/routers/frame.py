import io

from fastapi import APIRouter, Depends, File, UploadFile
from PIL import Image
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.services.frame_processor import FrameProcessor

router = APIRouter(prefix="/frame", tags=["frame"])


@router.post("/process")
async def process_frame(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
):
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    result = await FrameProcessor.process_frame(
        image=image,
        db=db,
    )

    return result
