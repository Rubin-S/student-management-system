// frontend/src/pages/CourseDetailPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import api from '../api';

function CourseDetailPage() {
  const { courseId } = useParams(); // Get the courseId from the URL
  const [course, setCourse] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourseData = async () => {
      try {
        // Fetch both course details and sessions in parallel
        const [courseRes, sessionsRes] = await Promise.all([
          api.get(`/courses/${courseId}`),
          api.get(`/courses/${courseId}/sessions/`)
        ]);
        setCourse(courseRes.data);
        setSessions(sessionsRes.data);
      } catch (error) {
        console.error("Failed to fetch course data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchCourseData();
  }, [courseId]); // Re-run effect if courseId changes

  if (loading) return <div>Loading course details...</div>;
  if (!course) return <div>Course not found.</div>;

  return (
    <div>
      <h2>{course.title} ({course.code})</h2>
      <p>{course.description}</p>

      <h3>Scheduled Sessions</h3>
      {sessions.length > 0 ? (
        <ul>
          {sessions.map(session => (
            <li key={session.id}>
              Session on {session.date}: {session.topic}
              {/* Link to the future attendance page */}
              <Link to={`/sessions/${session.id}/attendance`} style={{ marginLeft: '10px' }}>
                Take Attendance
              </Link>
            </li>
          ))}
        </ul>
      ) : (
        <p>No sessions scheduled for this course yet.</p>
      )}
    </div>
  );
}

export default CourseDetailPage;