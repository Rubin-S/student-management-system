// frontend/src/pages/GradebookPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import api from '../api';
import toast from 'react-hot-toast';
import { Box, Button, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, TextField } from '@mui/material';

function GradebookPage() {
  const { courseId } = useParams();
  const [gradebookData, setGradebookData] = useState({ students: [], assignments: [], grades: [] });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchGradebookData();
  }, [courseId]);

  const fetchGradebookData = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/courses/${courseId}/gradebook/`);
      setGradebookData(response.data);
    } catch (error) {
      toast.error("Failed to fetch gradebook data.");
    } finally {
      setLoading(false);
    }
  };

  const handleGradeChange = (studentId, assignmentId, score) => {
    const newGrades = [...gradebookData.grades];
    const gradeIndex = newGrades.findIndex(g => g.student_id === studentId && g.assignment_id === assignmentId);

    const newScore = score === '' ? null : parseFloat(score);

    if (gradeIndex > -1) {
      newGrades[gradeIndex].score = newScore;
    } else {
      newGrades.push({ student_id: studentId, assignment_id: assignmentId, score: newScore, comments: "" });
    }
    setGradebookData({ ...gradebookData, grades: newGrades });
  };

  const handleSaveGrades = async () => {
    const gradesToUpdate = gradebookData.grades.filter(g => typeof g.score === 'number');
    const promise = api.post('/grades/', { grades: gradesToUpdate });

    toast.promise(promise, {
        loading: 'Saving grades...',
        success: 'Grades saved successfully!',
        error: 'Failed to save grades.',
    });
  };

  const getGrade = (studentId, assignmentId) => {
    const grade = gradebookData.grades.find(g => g.student_id === studentId && g.assignment_id === assignmentId);
    return grade && typeof grade.score === 'number' ? grade.score : '';
  };

  if (loading) return <div>Loading gradebook...</div>;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4">Gradebook</Typography>
        <Button variant="contained" onClick={handleSaveGrades}>Save All Grades</Button>
      </Box>
      <Paper>
        <TableContainer>
          <Table stickyHeader>
            <TableHead>
              <TableRow>
                <TableCell sx={{ fontWeight: 'bold' }}>Student Name</TableCell>
                {gradebookData.assignments.map(assignment => (
                  <TableCell key={assignment.id} align="center" sx={{ fontWeight: 'bold' }}>
                    {assignment.title}
                  </TableCell>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {gradebookData.students.map(student => (
                <TableRow key={student.id}>
                  <TableCell component="th" scope="row">
                    {student.first_name} {student.last_name}
                  </TableCell>
                  {gradebookData.assignments.map(assignment => (
                    <TableCell key={assignment.id} align="center">
                      <TextField
                        type="number"
                        size="small"
                        sx={{ width: '80px' }}
                        value={getGrade(student.id, assignment.id)}
                        onChange={(e) => handleGradeChange(student.id, assignment.id, e.target.value)}
                        inputProps={{ min: 0, max: 100 }}
                      />
                    </TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>
    </Box>
  );
}

export default GradebookPage;