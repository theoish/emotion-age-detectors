import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../../context/AuthContext';
import './Dashboard.css';

function Dashboard() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h1>Welcome, {user?.name}!</h1>
        <button onClick={handleLogout} className="logout-btn">Logout</button>
      </div>
      
      <div className="features-grid">
        <div className="feature-card" onClick={() => navigate('/emotion')}>
          <div className="feature-icon">😊</div>
          <h3>Detect Emotion</h3>
          <p>Upload or capture a photo to detect your current emotion</p>
        </div>
        
        <div className="feature-card" onClick={() => navigate('/age')}>
          <div className="feature-icon">🎂</div>
          <h3>Detect Age</h3>
          <p>Upload or capture a photo to estimate your age</p>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;