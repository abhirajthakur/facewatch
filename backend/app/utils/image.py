import base64
import io

import numpy as np
from PIL import Image


def decode_base64_image(image_data: str) -> Image.Image:
    image_bytes = base64.b64decode(image_data)

    image = Image.open(io.BytesIO(image_bytes))

    return image.convert("RGB")


def pil_to_numpy(image: Image.Image) -> np.ndarray:
    return np.array(image)


def encode_image_to_base64(image: Image.Image) -> str:
    buffer = io.BytesIO()

    image.save(buffer, format="JPEG")

    return base64.b64encode(buffer.getvalue()).decode("utf-8")
