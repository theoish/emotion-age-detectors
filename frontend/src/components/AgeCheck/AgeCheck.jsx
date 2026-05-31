import React, { useState, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import Webcam from 'react-webcam';
import { detectionService } from '../../services/detectionService';
import './AgeCheck.css';  // Import the CSS file

function AgeCheck() {
  const [mode, setMode] = useState('select');
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

  const detectAge = async () => {
    setLoading(true);
    setError(null);
    
    try {
      const blob = await (await fetch(image)).blob();
      const file = new File([blob], 'photo.jpg', { type: 'image/jpeg' });
      
      const result = await detectionService.detectAge(file);
      setResult(result);
    } catch (err) {
      setError('Failed to detect age. Please try again.');
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

  return (
    <div className="age-container">
      <button onClick={() => navigate('/')} className="back-btn">← Back to Dashboard</button>
      
      <div className="age-card">
        <h2 className="title">Age Detection</h2>
        
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
              <button onClick={detectAge} disabled={loading} className="detect-btn">
                {loading ? 'Detecting...' : 'Detect Age'}
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
              <div className="age-result">
                <div className="age-number">{Math.round(result.age)}</div>
                <div className="age-label">years old</div>
                <div className="age-group">{result.age_group}</div>
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

export default AgeCheck;