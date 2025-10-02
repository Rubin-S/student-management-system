// frontend/src/pages/AttendancePage.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';

function AttendancePage() {
  const { sessionId } = useParams();
  const [attendanceData, setAttendanceData] = useState([]);
  const [session, setSession] = useState(null); // Optional: to display session info
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAttendanceData = async () => {
      try {
        const response = await api.get(`/sessions/${sessionId}/attendance/`);
        // Initialize status to 'absent' if it's null (not yet marked)
        const formattedData = response.data.map(item => ({
          ...item,
          status: item.status || 'absent'
        }));
        setAttendanceData(formattedData);
      } catch (error) {
        console.error("Failed to fetch attendance data:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchAttendanceData();
  }, [sessionId]);

  const handleStatusChange = (studentId, newStatus) => {
    setAttendanceData(attendanceData.map(item =>
      item.student.id === studentId ? { ...item, status: newStatus } : item
    ));
  };

  const handleSaveAttendance = async () => {
    try {
      const payload = {
        attendances: attendanceData.map(item => ({
          student_id: item.student.id,
          status: item.status
        }))
      };
      await api.post(`/sessions/${sessionId}/attendance/`, payload);
      alert('Attendance saved successfully!');
    } catch (error) {
      console.error('Failed to save attendance:', error);
      alert('Failed to save attendance.');
    }
  };

  if (loading) return <div>Loading attendance...</div>;

  return (
    <div>
      <h2>Attendance for Session on {session ? session.date : sessionId}</h2>
      <table>
        <thead>
          <tr>
            <th>Student Name</th>
            <th>Status</th>
          </tr>
        </thead>
        <tbody>
          {attendanceData.map(({ student, status }) => (
            <tr key={student.id}>
              <td>{student.first_name} {student.last_name}</td>
              <td>
                <label><input type="radio" name={`status-${student.id}`} value="present" checked={status === 'present'} onChange={() => handleStatusChange(student.id, 'present')} /> Present</label>
                <label><input type="radio" name={`status-${student.id}`} value="absent" checked={status === 'absent'} onChange={() => handleStatusChange(student.id, 'absent')} /> Absent</label>
                <label><input type="radio" name={`status-${student.id}`} value="late" checked={status === 'late'} onChange={() => handleStatusChange(student.id, 'late')} /> Late</label>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <button onClick={handleSaveAttendance} style={{ marginTop: '20px' }}>Save Attendance</button>
    </div>
  );
}

export default AttendancePage;