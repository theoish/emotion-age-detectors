from fastapi import APIRouter, UploadFile, File, HTTPException
import cv2
import numpy as np
from PIL import Image
import io

router = APIRouter()

def estimate_age_simple(image_np):
    """Simple age estimation using face proportions"""
    # Convert to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    
    # Detect faces using OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 0:
        return None, "No face detected"
    
    # Get face dimensions
    x, y, w, h = faces[0]
    face_area = w * h
    image_area = image_np.shape[0] * image_np.shape[1]
    face_ratio = face_area / image_area
    
    # Estimate age based on face ratio
    # This is a very basic heuristic - for demo only
    if face_ratio > 0.25:
        age = 25  # Child/Young adult
        age_group = "Young Adult"
    elif face_ratio > 0.18:
        age = 35  # Adult
        age_group = "Adult"
    elif face_ratio > 0.12:
        age = 50  # Middle age
        age_group = "Middle Aged"
    else:
        age = 65  # Senior
        age_group = "Senior"
    
    return age, age_group

@router.post("/age")
async def detect_age(file: UploadFile = File(...)):
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_np = np.array(image)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Estimate age
        age, age_group = estimate_age_simple(image_bgr)
        
        if age is None:
            return {
                "success": False,
                "message": "No face detected in the image"
            }
        
        return {
            "success": True,
            "age": age,
            "age_group": age_group,
            "message": f"Estimated age: {age} years ({age_group})"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")