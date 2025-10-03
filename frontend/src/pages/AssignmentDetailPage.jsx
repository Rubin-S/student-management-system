// frontend/src/pages/AssignmentDetailPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

function AssignmentDetailPage() {
  const { assignmentId } = useParams();
  const [assignment, setAssignment] = useState(null);
  const [submissions, setSubmissions] = useState([]);
  const [loading, setLoading] = useState(true);

  // State for the upload form
  const [selectedFile, setSelectedFile] = useState(null);
  const [studentId, setStudentId] = useState(''); // Simulating student selection

  useEffect(() => {
    fetchData();
  }, [assignmentId]);

  const fetchData = async () => {
    setLoading(true);
    try {
      const [assignmentRes, submissionsRes] = await Promise.all([
        api.get(`/assignments/${assignmentId}`),
        api.get(`/assignments/${assignmentId}/submissions/`)
      ]);
      setAssignment(assignmentRes.data);
      setSubmissions(submissionsRes.data);
    } catch (error) {
      console.error("Failed to fetch assignment data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
  };

  const handleUpload = async (event) => {
    event.preventDefault();
    if (!selectedFile || !studentId) {
      alert("Please select a file and enter a student ID.");
      return;
    }

    // FormData is required for file uploads
    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('student_id', studentId);

    try {
      await api.post(`/assignments/${assignmentId}/submissions/`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      alert('Submission successful!');
      // Reset form and refetch submissions to show the new one
      setSelectedFile(null);
      setStudentId('');
      fetchData(); 
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Upload failed.");
    }
  };

  if (loading) return <div>Loading...</div>;
  if (!assignment) return <div>Assignment not found.</div>;

  return (
    <div>
      <h2>{assignment.title}</h2>
      <p>Due: {new Date(assignment.due_date).toLocaleString()}</p>
      <a href={`${api.defaults.baseURL}/assignments/${assignmentId}/ics`}>
        Add to Calendar
      </a>
      <p>{assignment.description}</p>

      <hr />

      <h3>Upload Submission</h3>
      <form onSubmit={handleUpload}>
        <input 
          type="number" 
          value={studentId} 
          onChange={(e) => setStudentId(e.target.value)}
          placeholder="Enter Student ID"
          required
        />
        <input type="file" onChange={handleFileChange} required />
        <button type="submit">Upload</button>
      </form>

      <hr />

      <h3>Submissions</h3>
      {submissions.length > 0 ? (
        <ul>
          {submissions.map(sub => (
            <li key={sub.id}>
              Student ID: {sub.student.id} ({sub.student.first_name} {sub.student.last_name})
              - Submitted on: {new Date(sub.submission_date).toLocaleString()}
              - File: {sub.file_path}
            </li>
          ))}
        </ul>
      ) : (
        <p>No submissions yet.</p>
      )}
    </div>
  );
}

export default AssignmentDetailPage;