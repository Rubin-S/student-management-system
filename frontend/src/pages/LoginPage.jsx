// frontend/src/pages/LoginPage.jsx
import React, { useState } from 'react';
import api from '../api'; // Import our new api client

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
    <div>
      <h2>Login</h2>
      <form onSubmit={handleLogin}>
        <div>
          <label>Email:</label>
          <input
            type="email"
            placeholder="user@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />
        </div>
        <div>
          <label>Password:</label>
          <input
            type="password"
            placeholder="********"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
          />
        </div>
        <button type="submit">Login</button>
      </form>
    </div>
  );
}

export default LoginPage;