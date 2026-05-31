import base64
import cv2
import numpy as np
from PIL import Image
import io

def decode_base64_image(base64_string):
    """Decode base64 image to numpy array"""
    # Remove header if present
    if ',' in base64_string:
        base64_string = base64_string.split(',')[1]
    
    # Decode base64
    image_bytes = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_bytes))
    image_np = np.array(image)
    
    # Convert to BGR for OpenCV
    if len(image_np.shape) == 3:
        image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
    
    return image_np

def encode_image_to_base64(image_np):
    """Encode numpy image to base64"""
    _, buffer = cv2.imencode('.jpg', image_np)
    return base64.b64encode(buffer).decode('utf-8')