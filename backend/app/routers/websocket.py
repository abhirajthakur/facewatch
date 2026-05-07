import json

from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.state import app_state
from app.services.frame_processor import FrameProcessor
from app.utils.image import decode_base64_image

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/video")
async def websocket_video_stream(
    websocket: WebSocket,
    db: AsyncSession = Depends(get_db),
):
    await websocket.accept()

    try:
        while True:
            data = await websocket.receive_text()
            payload = json.loads(data)
            frame_data = payload["frame"]
            image = decode_base64_image(frame_data)

            result = await FrameProcessor.process_frame(
                image=image,
                db=db,
            )

            app_state.latest_processed_frame = result["frame"]
            app_state.latest_roi = result["roi"]

            await websocket.send_json(result)

    except WebSocketDisconnect:
        print("Client disconnected")

    except Exception as e:
        await websocket.send_json(
            {
                "error": str(e),
            }
        )
