// frontend/src/pages/CoursesPage.jsx
import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom'; // For navigation
import api from '../api';

function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get('/courses/');
        setCourses(response.data);
      } catch (error) {
        console.error("Failed to fetch courses:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, []);

  if (loading) return <div>Loading courses...</div>;

  return (
    <div>
      <h2>Courses List</h2>
      <ul>
        {courses.map((course) => (
          <li key={course.id}>
            {/* We'll create this link target in the next step */}
            <Link to={`/courses/${course.id}`}>{course.title} ({course.code})</Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default CoursesPage;