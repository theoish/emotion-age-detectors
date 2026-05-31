import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Login from './components/Auth/Login';
import Dashboard from './components/Dashboard/Dashboard';
import EmotionCheck from './components/EmotionCheck/EmotionCheck';
import AgeCheck from './components/AgeCheck/AgeCheck';  // Fixed this line
import PrivateRoute from './components/Common/PrivateRoute';
import './App.css';

function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="App">
          <Routes>
            <Route path="/login" element={<Login />} />
            <Route path="/" element={<PrivateRoute><Dashboard /></PrivateRoute>} />
            <Route path="/emotion" element={<PrivateRoute><EmotionCheck /></PrivateRoute>} />
            <Route path="/age" element={<PrivateRoute><AgeCheck /></PrivateRoute>} />
          </Routes>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;