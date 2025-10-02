// frontend/src/pages/StudentsPage.jsx
import React, { useState, useEffect } from 'react';
import api from '../api';

function StudentsPage({ onLogout }) {
  const [students, setStudents] = useState([]);
  const [loading, setLoading] = useState(true);

  // State for the form fields
  const [newStudent, setNewStudent] = useState({ first_name: '', last_name: '', email: '' });
  const [editingStudentId, setEditingStudentId] = useState(null);

  // Fetch students when the component loads
  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await api.get('/students/');
      setStudents(response.data);
    } catch (error) {
      console.error("Failed to fetch students:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setNewStudent({ ...newStudent, [name]: value });
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (editingStudentId) {
        // Update existing student
        try {
            const response = await api.put(`/students/${editingStudentId}`, newStudent);
            setStudents(students.map(s => s.id === editingStudentId ? response.data : s));
        } catch (error) {
            console.error("Failed to update student:", error);
        }
    } else {
        // Add new student
        try {
            const response = await api.post('/students/', newStudent);
            setStudents([...students, response.data]); // Add new student to the list
        } catch (error) {
            console.error("Failed to add student:", error);
        }
    }
    // Reset form
    setNewStudent({ first_name: '', last_name: '', email: '' });
    setEditingStudentId(null);
  };

  const handleDelete = async (studentId) => {
    try {
      await api.delete(`/students/${studentId}`);
      setStudents(students.filter(s => s.id !== studentId)); // Remove student from the list
    } catch (error) {
      console.error("Failed to delete student:", error);
    }
  };

  const handleEdit = (student) => {
    setEditingStudentId(student.id);
    setNewStudent({ first_name: student.first_name, last_name: student.last_name, email: student.email });
  };


  if (loading) return <div>Loading students...</div>;

  return (
    <div>
      <h2>Students Management</h2>
      <button onClick={onLogout}>Logout</button>

      <form onSubmit={handleSubmit}>
        <h3>{editingStudentId ? 'Edit Student' : 'Add New Student'}</h3>
        <input name="first_name" value={newStudent.first_name} onChange={handleInputChange} placeholder="First Name" required />
        <input name="last_name" value={newStudent.last_name} onChange={handleInputChange} placeholder="Last Name" required />
        <input name="email" type="email" value={newStudent.email} onChange={handleInputChange} placeholder="Email" required />
        <button type="submit">{editingStudentId ? 'Update' : 'Add'}</button>
      </form>

      <h3>Students List</h3>
      <ul>
        {students.map((student) => (
          <li key={student.id}>
            {student.first_name} {student.last_name} ({student.email})
            <button onClick={() => handleEdit(student)}>Edit</button>
            <button onClick={() => handleDelete(student.id)}>Delete</button>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default StudentsPage;