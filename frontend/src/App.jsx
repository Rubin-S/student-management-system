// frontend/src/App.jsx
import React, { useState, useEffect } from 'react';
import './App.css';
import LoginPage from './pages/LoginPage';
import StudentsPage from './pages/StudentsPage';

function App() {
  // Check for a token in localStorage when the app loads
  const [token, setToken] = useState(localStorage.getItem('token'));

  const handleLoginSuccess = (newToken) => {
    // Store the token in localStorage and in state
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    // Clear the token from localStorage and state
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <div>
      {token ? (
        // If the user is logged in, show the Students page
        <StudentsPage onLogout={handleLogout} />
      ) : (
        // Otherwise, show the Login page
        <LoginPage onLoginSuccess={handleLoginSuccess} />
      )}
    </div>
  );
}

export default App;