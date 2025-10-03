// frontend/src/pages/AttendancePage.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import toast from 'react-hot-toast';
import { Box, Button, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Radio, RadioGroup, FormControlLabel, CircularProgress } from '@mui/material';

function AttendancePage() {
  const { sessionId } = useParams();
  const [attendanceData, setAttendanceData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAttendanceData = async () => {
      try {
        const response = await api.get(`/sessions/${sessionId}/attendance/`);
        const formattedData = response.data.map(item => ({
          ...item,
          status: item.status || 'absent'
        }));
        setAttendanceData(formattedData);
      } catch (error) {
        toast.error("Failed to fetch attendance data.");
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
    const payload = {
      attendances: attendanceData.map(item => ({
        student_id: item.student.id,
        status: item.status
      }))
    };
    const promise = api.post(`/sessions/${sessionId}/attendance/`, payload);

    toast.promise(promise, {
        loading: 'Saving attendance...',
        success: 'Attendance saved successfully!',
        error: 'Failed to save attendance.',
    });
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4">Take Attendance</Typography>
        <Button variant="contained" onClick={handleSaveAttendance}>Save Attendance</Button>
      </Box>
      <Paper>
        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold' }}>Student Name</TableCell>
                <TableCell sx={{ fontWeight: 'bold' }}>Status</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {attendanceData.map(({ student, status }) => (
                <TableRow key={student.id}>
                  <TableCell>{student.first_name} {student.last_name}</TableCell>
                  <TableCell>
                    <RadioGroup row value={status} onChange={(e) => handleStatusChange(student.id, e.target.value)}>
                      <FormControlLabel value="present" control={<Radio />} label="Present" />
                      <FormControlLabel value="absent" control={<Radio />} label="Absent" />
                      <FormControlLabel value="late" control={<Radio />} label="Late" />
                    </RadioGroup>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
}

export default AttendancePage;