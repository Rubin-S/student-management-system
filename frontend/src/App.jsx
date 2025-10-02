// frontend/src/App.jsx
import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate, Link } from 'react-router-dom';
import './App.css';
import LoginPage from './pages/LoginPage';
import StudentsPage from './pages/StudentsPage';
import CoursesPage from './pages/CoursesPage'; // Import the new page
import CourseDetailPage from './pages/CourseDetailPage';
import AttendancePage from './pages/AttendancePage';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

  const handleLoginSuccess = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  return (
    <BrowserRouter>
      {token && (
        <nav>
          <Link to="/students">Students</Link> | <Link to="/courses">Courses</Link>
          <button onClick={handleLogout} style={{ marginLeft: '20px' }}>Logout</button>
        </nav>
      )}
      <Routes>
        <Route
          path="/login"
          element={
            token ? <Navigate to="/students" /> : <LoginPage onLoginSuccess={handleLoginSuccess} />
          }
        />
        <Route
          path="/students"
          element={token ? <StudentsPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/courses"
          element={token ? <CoursesPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/courses/:courseId"
          element={token ? <CourseDetailPage /> : <Navigate to="/login" />}
        />
        <Route
          path="/sessions/:sessionId/attendance"
          element={token ? <AttendancePage /> : <Navigate to="/login" />}
        />
        {/* Default route */}
        <Route
          path="*"
          element={<Navigate to={token ? "/students" : "/login"} />}
        />
      </Routes>
    </BrowserRouter>
  );
}

export default App;