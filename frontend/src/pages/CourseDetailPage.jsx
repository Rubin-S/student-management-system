// frontend/src/pages/CourseDetailPage.jsx
import React, { useState, useEffect } from 'react';
import { useParams, Link as RouterLink } from 'react-router-dom';
import api from '../api';
import toast from 'react-hot-toast';
import { Box, Typography, Grid, Paper, List, ListItem, ListItemText, ListItemIcon, Button, Divider, TextField, CircularProgress } from '@mui/material';
import EventIcon from '@mui/icons-material/Event';
import AssignmentIcon from '@mui/icons-material/Assignment';

function CourseDetailPage() {
  const { courseId } = useParams();
  const [course, setCourse] = useState(null);
  const [sessions, setSessions] = useState([]);
  const [assignments, setAssignments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [newAssignment, setNewAssignment] = useState({ title: '', description: '', due_date: '' });

  useEffect(() => {
    fetchCourseData();
  }, [courseId]);

  const fetchCourseData = async () => {
    setLoading(true);
    try {
      const [courseRes, sessionsRes, assignmentsRes] = await Promise.all([
        api.get(`/courses/${courseId}`),
        api.get(`/courses/${courseId}/sessions/`),
        api.get(`/courses/${courseId}/assignments/`)
      ]);
      setCourse(courseRes.data);
      setSessions(sessionsRes.data);
      setAssignments(assignmentsRes.data);
    } catch (error) {
      toast.error("Failed to fetch course data.");
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => setNewAssignment({ ...newAssignment, [e.target.name]: e.target.value });

  const handleCreateAssignment = async (e) => {
    e.preventDefault();
    const promise = api.post(`/courses/${courseId}/assignments/`, newAssignment).then(response => {
      setAssignments([...assignments, response.data]);
      setNewAssignment({ title: '', description: '', due_date: '' });
    });
    toast.promise(promise, {
        loading: 'Creating assignment...',
        success: 'Assignment created!',
        error: 'Failed to create assignment.',
    });
  };

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;
  if (!course) return <Typography variant="h5">Course not found.</Typography>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>{course.title} ({course.code})</Typography>
      <Button component={RouterLink} to={`/courses/${courseId}/gradebook`} variant="contained" sx={{ mb: 2 }}>
        View Gradebook
      </Button>
      <Typography variant="body1" paragraph>{course.description}</Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 2 }}>
            <Typography variant="h6">Scheduled Sessions</Typography>
            <List>
              {sessions.length > 0 ? sessions.map(session => (
                <ListItem key={session.id} secondaryAction={
                  <Button component={RouterLink} to={`/sessions/${session.id}/attendance`}>Take Attendance</Button>
                }>
                  <ListItemIcon><EventIcon /></ListItemIcon>
                  <ListItemText primary={session.topic} secondary={`Date: ${session.date}`} />
                </ListItem>
              )) : <ListItem><ListItemText primary="No sessions scheduled." /></ListItem>}
            </List>
          </Paper>
        </Grid>
        <Grid item xs={12} md={6}>
          <Paper elevation={2} sx={{ p: 2 }}>
            <Typography variant="h6">Assignments</Typography>
            <List>
              {assignments.map(assignment => (
                <ListItem key={assignment.id} secondaryAction={
                  <Button component={RouterLink} to={`/assignments/${assignment.id}`}>View Submissions</Button>
                }>
                  <ListItemIcon><AssignmentIcon /></ListItemIcon>
                  <ListItemText primary={assignment.title} secondary={`Due: ${new Date(assignment.due_date).toLocaleString()}`} />
                </ListItem>
              ))}
            </List>
            <Divider sx={{ my: 2 }} />
            <Box component="form" onSubmit={handleCreateAssignment} sx={{ p: 2 }}>
                <Typography variant="subtitle1">Create New Assignment</Typography>
                <TextField name="title" label="Title" value={newAssignment.title} onChange={handleInputChange} fullWidth margin="normal" required size="small" />
                <TextField name="description" label="Description" value={newAssignment.description} onChange={handleInputChange} fullWidth margin="normal" size="small" multiline rows={2} />
                <TextField name="due_date" type="datetime-local" value={newAssignment.due_date} onChange={handleInputChange} fullWidth margin="normal" required size="small" InputLabelProps={{ shrink: true }} />
                <Button type="submit" variant="outlined" sx={{ mt: 1 }}>Create Assignment</Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
}

export default CourseDetailPage;