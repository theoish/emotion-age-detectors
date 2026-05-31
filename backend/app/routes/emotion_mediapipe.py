from fastapi import APIRouter, UploadFile, File, HTTPException
import cv2
import numpy as np
from PIL import Image
import io

# Updated import for newer MediaPipe versions
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

router = APIRouter()

# Initialize MediaPipe Face Detection (newer API)
BaseOptions = mp.tasks.BaseOptions
FaceDetector = mp.tasks.vision.FaceDetector
FaceDetectorOptions = mp.tasks.vision.FaceDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

# Create face detector
options = FaceDetectorOptions(
    base_options=BaseOptions(model_asset_path='face_detector.task'),
    min_detection_confidence=0.5,
    running_mode=VisionRunningMode.IMAGE
)

# Note: You need to download the model file first
# For now, we'll use the simpler approach below

def analyze_facial_features_simple(image_np):
    """Simple emotion detection using OpenCV"""
    # Convert to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    
    # Detect faces using OpenCV
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    if len(faces) == 0:
        return "no_face"
    
    # For first face, analyze region
    x, y, w, h = faces[0]
    face_roi = gray[y:y+h, x:x+w]
    
    # Simple analysis based on average pixel intensity
    # (This is a placeholder - you can enhance this)
    avg_intensity = np.mean(face_roi)
    
    if avg_intensity > 150:
        emotion = "happy"
    elif avg_intensity > 100:
        emotion = "neutral"
    else:
        emotion = "sad"
    
    return emotion

@router.post("/emotion")
async def detect_emotion(file: UploadFile = File(...)):
    try:
        # Read image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        image_np = np.array(image)
        image_bgr = cv2.cvtColor(image_np, cv2.COLOR_RGB2BGR)
        
        # Detect emotion
        emotion = analyze_facial_features_simple(image_bgr)
        
        if emotion == "no_face":
            return {
                "success": False,
                "dominant_emotion": "unknown",
                "emotion_scores": {},
                "message": "No face detected in the image"
            }
        
        # Prepare emotion scores
        emotion_scores = {
            "happy": 0.9 if emotion == "happy" else 0.1,
            "sad": 0.9 if emotion == "sad" else 0.1,
            "angry": 0.1,
            "fear": 0.1,
            "surprise": 0.1,
            "neutral": 0.9 if emotion == "neutral" else 0.1
        }
        
        return {
            "success": True,
            "dominant_emotion": emotion,
            "emotion_scores": emotion_scores,
            "message": f"Detected emotion: {emotion}"
        }
        
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error: {str(e)}")