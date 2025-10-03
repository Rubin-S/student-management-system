// frontend/src/pages/CoursesPage.jsx
import React, { useState, useEffect } from 'react';
import { Link as RouterLink } from 'react-router-dom';
import api from '../api';
import toast from 'react-hot-toast';
import { Box, Typography, Grid, Card, CardContent, CardActions, Button, CircularProgress } from '@mui/material';

function CoursesPage() {
  const [courses, setCourses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchCourses = async () => {
      try {
        const response = await api.get('/courses/');
        setCourses(response.data);
      } catch (error) {
        toast.error("Failed to fetch courses.");
      } finally {
        setLoading(false);
      }
    };
    fetchCourses();
  }, []);

  if (loading) return <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}><CircularProgress /></Box>;

  return (
    <Box>
      <Typography variant="h4" gutterBottom>Courses</Typography>
      <Grid container spacing={3}>
        {courses.map((course) => (
          <Grid item key={course.id} xs={12} sm={6} md={4}>
            <Card>
              <CardContent>
                <Typography variant="h5" component="div">
                  {course.title}
                </Typography>
                <Typography sx={{ mb: 1.5 }} color="text.secondary">
                  {course.code}
                </Typography>
                <Typography variant="body2">
                  {course.description}
                </Typography>
              </CardContent>
              <CardActions>
                <Button component={RouterLink} to={`/courses/${course.id}`} size="small">View Details</Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
}

export default CoursesPage;