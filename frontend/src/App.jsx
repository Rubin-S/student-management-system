// frontend/src/App.jsx
import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import './App.css';
import LoginPage from './pages/LoginPage';
import StudentsPage from './pages/StudentsPage';
import CoursesPage from './pages/CoursesPage';
import CourseDetailPage from './pages/CourseDetailPage';
import AssignmentDetailPage from './pages/AssignmentDetailPage';
import GradebookPage from './pages/GradebookPage';
import AttendancePage from './pages/AttendancePage';
import Layout from './components/Layout';

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

  // A wrapper component to protect routes
  const ProtectedRoute = ({ children }) => {
    const token = localStorage.getItem('token');
    if (!token) {
      // If no token, redirect to login
      return <Navigate to="/login" replace />;
    }
    return children;
  };

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="/login"
          element={token ? <Navigate to="/" /> : <LoginPage onLoginSuccess={handleLoginSuccess} />}
        />

        {/* Main application routes wrapped in the Layout */}
        <Route 
          path="/" 
          element={
            <ProtectedRoute>
              <Layout handleLogout={handleLogout} />
            </ProtectedRoute>
          }
        >
          {/* These nested routes will render inside the Layout's <Outlet> */}
          <Route index element={<Navigate to="/students" replace />} />
          <Route path="students" element={<StudentsPage />} />
          <Route path="courses" element={<CoursesPage />} />
          <Route path="courses/:courseId" element={<CourseDetailPage />} />
          <Route path="courses/:courseId/gradebook" element={<GradebookPage />} />
          <Route path="assignments/:assignmentId" element={<AssignmentDetailPage />} />
          <Route path="sessions/:sessionId/attendance" element={<AttendancePage />} />
        </Route>

         {/* A catch-all route to redirect */}
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;