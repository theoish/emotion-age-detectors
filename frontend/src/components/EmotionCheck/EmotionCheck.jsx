import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Webcam from 'react-webcam';
import { detectionService } from '../../services/detectionService';
import './EmotionCheck.css';

function EmotionCheck() {
  const [mode, setMode] = useState('select'); // select, camera, upload
  const [image, setImage] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const webcamRef = useRef(null);
  const navigate = useNavigate();

  const capturePhoto = () => {
    const imageSrc = webcamRef.current.getScreenshot();
    setImage(imageSrc);
    setMode('preview');
  };

  const handleFileUpload = (event) => {
    const file = event.target.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result);
        setMode('preview');
      };
      reader.readAsDataURL(file);
    }
  };

  const detectEmotion = async () => {
    setLoading(true);
    setError(null);
    
    try {
      // Convert base64 to file
      const blob = await (await fetch(image)).blob();
      const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });
      
      const result = await detectionService.detectEmotion(file);
      setResult(result);
    } catch (err) {
      setError('Failed to detect emotion. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const resetDetection = () => {
    setMode('select');
    setImage(null);
    setResult(null);
    setError(null);
  };

  const getEmotionEmoji = (emotion) => {
    const emojis = {
      'happy': '😊',
      'sad': '😢',
      'angry': '😠',
      'fear': '😨',
      'surprise': '😲',
      'neutral': '😐',
      'disgust': '🤢'
    };
    return emojis[emotion.toLowerCase()] || '😐';
  };

  return (
    <div className="emotion-container">
      <button onClick={() => navigate('/')} className="back-btn">← Back to Dashboard</button>
      
      <div className="emotion-card">
        <h2 className="title">Emotion Detection</h2>
        
        {mode === 'select' && (
          <div className="mode-selector">
            <button onClick={() => setMode('camera')} className="mode-btn">
              📸 Use Camera
            </button>
            <button onClick={() => setMode('upload')} className="mode-btn">
              📁 Upload Photo
            </button>
          </div>
        )}
        
        {mode === 'camera' && (
          <div className="camera-section">
            <Webcam
              ref={webcamRef}
              screenshotFormat="image/jpeg"
              className="webcam"
            />
            <button onClick={capturePhoto} className="capture-btn">
              Capture Photo
            </button>
            <button onClick={() => setMode('select')} className="cancel-btn">
              Cancel
            </button>
          </div>
        )}
        
        {mode === 'upload' && (
          <div className="upload-section">
            <input
              type="file"
              accept="image/*"
              onChange={handleFileUpload}
              className="file-input"
            />
            <button onClick={() => setMode('select')} className="cancel-btn">
              Cancel
            </button>
          </div>
        )}
        
        {mode === 'preview' && image && !result && (
          <div className="preview-section">
            <img src={image} alt="Preview" className="preview-image" />
            <div className="action-buttons">
              <button onClick={detectEmotion} disabled={loading} className="detect-btn">
                {loading ? 'Detecting...' : 'Detect Emotion'}
              </button>
              <button onClick={resetDetection} className="retake-btn">
                Retake/Reupload
              </button>
            </div>
          </div>
        )}
        
        {error && (
          <div className="error-message">
            {error}
          </div>
        )}
        
        {result && (
          <div className="result-section">
            <img src={image} alt="Analyzed" className="result-image" />
            <div className="result-details">
              <div className="dominant-emotion">
                <span className="emotion-emoji">{getEmotionEmoji(result.dominant_emotion)}</span>
                <h3>Dominant Emotion: {result.dominant_emotion.toUpperCase()}</h3>
              </div>
              
              <div className="emotion-scores">
                <h4>Emotion Scores:</h4>
                {Object.entries(result.emotion_scores).map(([emotion, score]) => (
                  <div key={emotion} className="score-bar-container">
                    <span className="emotion-label">{emotion}</span>
                    <div className="score-bar">
                      <div 
                        className="score-fill"
                        style={{ width: `${score}%` }}
                      ></div>
                    </div>
                    <span className="score-value">{Math.round(score)}%</span>
                  </div>
                ))}
              </div>
              
              <button onClick={resetDetection} className="new-detection-btn">
                New Detection
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default EmotionCheck;