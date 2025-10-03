// frontend/src/pages/StudentsPage.jsx
import React, { useState, useEffect } from 'react';
import api from '../api';
import toast from 'react-hot-toast';
import { Box, Button, Typography, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, IconButton, Modal, TextField } from '@mui/material';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';

const modalStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)',
  width: 400,
  bgcolor: 'background.paper',
  border: '2px solid #000',
  boxShadow: 24,
  p: 4,
};

function StudentsPage() {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);
  const [open, setOpen] = useState(false); // Modal open/close state
  const [formData, setFormData] = useState({ first_name: '', last_name: '', email: '' });
  const [editingId, setEditingId] = useState(null);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    setLoading(true);
    try {
      const response = await api.get('/students/');
      setStudents(response.data);
    } catch (error) {
      toast.error("Failed to fetch students.");
      console.error("Failed to fetch students:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleOpen = (student = null) => {
    if (student) {
      setFormData({ first_name: student.first_name, last_name: student.last_name, email: student.email });
      setEditingId(student.id);
    } else {
      setFormData({ first_name: '', last_name: '', email: '' });
      setEditingId(null);
    }
    setOpen(true);
  };

  const handleClose = () => setOpen(false);

  const handleInputChange = (e) => setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    const apiCall = editingId
      ? api.put(`/students/${editingId}`, formData)
      : api.post('/students/', formData);

    const promise = apiCall.then(() => {
      handleClose();
      fetchStudents(); // Refresh the list
    });

    toast.promise(promise, {
       loading: editingId ? 'Updating student...' : 'Adding student...',
       success: `Student ${editingId ? 'updated' : 'added'} successfully!`,
       error: `Failed to ${editingId ? 'update' : 'add'} student.`,
    });
  };

  const handleDelete = async (studentId) => {
    if (window.confirm("Are you sure you want to delete this student?")) {
        const promise = api.delete(`/students/${studentId}`).then(() => {
            setStudents(students.filter(s => s.id !== studentId));
        });

        toast.promise(promise, {
            loading: 'Deleting student...',
            success: 'Student deleted successfully!',
            error: 'Failed to delete student.',
        });
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h4">Students</Typography>
        <Button variant="contained" onClick={() => handleOpen()}>Add Student</Button>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>First Name</TableCell>
              <TableCell>Last Name</TableCell>
              <TableCell>Email</TableCell>
              <TableCell align="right">Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {students.map((student) => (
              <TableRow key={student.id}>
                <TableCell>{student.first_name}</TableCell>
                <TableCell>{student.last_name}</TableCell>
                <TableCell>{student.email}</TableCell>
                <TableCell align="right">
                  <IconButton onClick={() => handleOpen(student)}><EditIcon /></IconButton>
                  <IconButton onClick={() => handleDelete(student.id)}><DeleteIcon /></IconButton>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      <Modal open={open} onClose={handleClose}>
        <Box sx={modalStyle} component="form" onSubmit={handleSubmit}>
          <Typography variant="h6">{editingId ? 'Edit Student' : 'Add New Student'}</Typography>
          <TextField name="first_name" label="First Name" value={formData.first_name} onChange={handleInputChange} fullWidth margin="normal" required />
          <TextField name="last_name" label="Last Name" value={formData.last_name} onChange={handleInputChange} fullWidth margin="normal" required />
          <TextField name="email" label="Email" type="email" value={formData.email} onChange={handleInputChange} fullWidth margin="normal" required />
          <Button type="submit" variant="contained" sx={{ mt: 2 }}>{editingId ? 'Update' : 'Create'}</Button>
        </Box>
      </Modal>
    </Box>
  );
}

export default StudentsPage;