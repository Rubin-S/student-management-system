// frontend/src/pages/LoginPage.jsx
import React, { useState } from 'react';
import api from '../api'; // Import our new api client
import { Button, TextField, Box, Typography } from '@mui/material';

function LoginPage({ onLoginSuccess }) {
  // State to hold the user's input
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  // Function to handle form submission
  const handleLogin = async (event) => {
    event.preventDefault(); // Prevent the form from reloading the page

    try {
      // Our backend's /token endpoint expects form data, not JSON
      const formData = new URLSearchParams();
      formData.append('username', email);
      formData.append('password', password);

      // Send the request to the backend
      const response = await api.post('/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      // Call the function passed from App.jsx with the new token
      onLoginSuccess(response.data.access_token); 

      // For now, just log the token to the console
      console.log('Login successful:', response.data);
      alert('Login successful! Check the console for the token.');

    } catch (error) {
      console.error('Login failed:', error);
      alert('Login failed. Check the console for details.');
    }
  };

  return (
  <Box component="form" onSubmit={handleLogin} sx={{ mt: 1, maxWidth: '400px', margin: 'auto' }}>
    <Typography component="h1" variant="h5">
      Login
    </Typography>
    <TextField
      margin="normal"
      required
      fullWidth
      id="email"
      label="Email Address"
      name="email"
      autoComplete="email"
      autoFocus
      value={email}
      onChange={(e) => setEmail(e.target.value)}
    />
    <TextField
      margin="normal"
      required
      fullWidth
      name="password"
      label="Password"
      type="password"
      id="password"
      autoComplete="current-password"
      value={password}
      onChange={(e) => setPassword(e.target.value)}
    />
    <Button
      type="submit"
      fullWidth
      variant="contained"
      sx={{ mt: 3, mb: 2 }}
    >
      Sign In
    </Button>
  </Box>
  );
}

export default LoginPage;