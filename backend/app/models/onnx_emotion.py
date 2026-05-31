import cv2
import numpy as np
import onnxruntime as ort

class EmotionDetector:
    def __init__(self):
        # Load ONNX model (download model file first)
        self.session = ort.InferenceSession("emotion-ferplus-8.onnx")
        self.emotions = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
    
    def detect_emotion(self, face_image):
        # Preprocess image
        face = cv2.resize(face_image, (64, 64))
        face = face.astype(np.float32)
        face = np.transpose(face, (2, 0, 1))
        face = np.expand_dims(face, axis=0)
        
        # Run inference
        outputs = self.session.run(None, {'input': face})
        
        # Get emotion with highest probability
        emotion_idx = np.argmax(outputs[0])
        return self.emotions[emotion_idx]