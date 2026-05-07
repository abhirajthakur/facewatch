from typing import Optional

import dlib
import numpy as np


class FaceDetectionService:
    def __init__(self) -> None:
        self.detector = dlib.get_frontal_face_detector()

    def detect_face(
        self,
        image: np.ndarray,
    ) -> Optional[dict]:
        faces = self.detector(image)

        if not faces:
            return None

        face = faces[0]

        x = face.left()
        y = face.top()

        width = face.right() - face.left()
        height = face.bottom() - face.top()

        return {
            "x": float(x),
            "y": float(y),
            "width": float(width),
            "height": float(height),
        }
