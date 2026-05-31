# backend/app/routes/emotion_lightweight.py
import cv2
import numpy as np

def detect_emotion_geometric(face_roi):
    """
    Detect emotion using geometric analysis without TensorFlow
    Based on: mouth curvature, eye openness, brow position
    """
    # Convert to grayscale
    gray = cv2.cvtColor(face_roi, cv2.COLOR_BGR2GRAY)
    
    # Detect facial landmarks using dlib or OpenCV
    # Calculate mouth aspect ratio (smile detection)
    # Calculate eye aspect ratio
    # Return dominant emotion based on ratios
    
    return {
        "dominant_emotion": "happy",  # Example
        "emotion_scores": {"happy": 0.85, "neutral": 0.15}
    }