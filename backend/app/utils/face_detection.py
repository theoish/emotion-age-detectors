import cv2
import numpy as np

def detect_faces(image_np):
    """Detect faces in the image using Haar Cascade"""
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    return faces

def get_face_count(image_np):
    """Get number of faces in the image"""
    faces = detect_faces(image_np)
    return len(faces)