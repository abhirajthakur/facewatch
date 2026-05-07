from PIL import ImageDraw
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.face_detector import FaceDetectionService
from app.services.roi_service import ROIService
from app.utils.image import (
    encode_image_to_base64,
    pil_to_numpy,
)

face_detector = FaceDetectionService()


class FrameProcessor:
    @staticmethod
    async def process_frame(
        image,
        db: AsyncSession,
    ):
        numpy_image = pil_to_numpy(image)

        roi = face_detector.detect_face(numpy_image)

        if roi is None:
            return {
                "frame": encode_image_to_base64(image),
                "roi": None,
            }

        draw = ImageDraw.Draw(image)

        draw.rectangle(
            [
                (roi["x"], roi["y"]),
                (
                    roi["x"] + roi["width"],
                    roi["y"] + roi["height"],
                ),
            ],
            outline="red",
            width=3,
        )

        saved_roi = await ROIService.create_roi(
            db=db,
            roi_data=roi,
        )

        processed_frame = encode_image_to_base64(image)

        return {
            "frame": processed_frame,
            "roi": {
                "id": saved_roi.id,
                "x": saved_roi.x,
                "y": saved_roi.y,
                "width": saved_roi.width,
                "height": saved_roi.height,
            },
        }
