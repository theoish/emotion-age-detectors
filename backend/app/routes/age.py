from fastapi import APIRouter, UploadFile, File, HTTPException
from deepface import DeepFace
import cv2
import numpy as np
from PIL import Image
import io

router = APIRouter()

@router.post("/age")
async def detect_age(file: UploadFile = File(...)):
    try:
        # Read the uploaded image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert PIL Image to numpy array
        image_np = np.array(image)
        
        # Convert RGB to BGR (OpenCV format)
        if len(image_np.shape) == 3:
            image_np = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Detect age using DeepFace
        result = DeepFace.analyze(img_path=image_np, actions=['age'], enforce_detection=False)
        
        # Extract age
        if isinstance(result, list):
            result = result[0]
        
        age = result['age']
        
        # Determine age group
        if age < 13:
            age_group = "Child"
        elif age < 20:
            age_group = "Teenager"
        elif age < 35:
            age_group = "Young Adult"
        elif age < 50:
            age_group = "Adult"
        elif age < 65:
            age_group = "Middle Aged"
        else:
            age_group = "Senior"
        
        return {
            "success": True,
            "age": round(age, 1),
            "age_group": age_group,
            "message": f"Detected age: {round(age, 1)} years ({age_group})"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error processing image: {str(e)}")