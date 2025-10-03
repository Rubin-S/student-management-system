// frontend/src/main.jsx
import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';

// 1. Import MUI components
import { ThemeProvider, createTheme, CssBaseline } from '@mui/material';

// 2. Create a simple dark theme (or 'light')
const darkTheme = createTheme({
  palette: {
    mode: 'dark',
  },
});

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    {/* 3. Wrap your App in the ThemeProvider */}
    <ThemeProvider theme={darkTheme}>
      <CssBaseline /> {/* A reset for CSS consistency */}
      <App />
    </ThemeProvider>
  </React.StrictMode>
);