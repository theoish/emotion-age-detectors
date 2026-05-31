import cv2
import numpy as np

def detect_emotion_simple(face_roi):
    """
    Simple geometric emotion detection
    Works offline with only OpenCV
    """
    # Convert to grayscale
    gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    
    # Detect mouth region
    mouth_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_smile.xml')
    mouths = mouth_cascade.detectMultiScale(gray, 1.3, 25)
    
    # Detect eyes
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(gray, 1.3, 25)
    
    # Simple heuristic
    if len(mouths) > 0:
        return "happy"
    elif len(eyes) < 2:
        return "sad"
    else:
        return "neutral"