// frontend/src/components/Layout.jsx
import React from 'react';
import { Outlet, useNavigate } from 'react-router-dom';
import { Box, Drawer, AppBar, Toolbar, List, ListItem, ListItemButton, ListItemIcon, ListItemText, Typography, Button } from '@mui/material';
import PeopleIcon from '@mui/icons-material/People';
import SchoolIcon from '@mui/icons-material/School';
import { Toaster } from 'react-hot-toast';

const drawerWidth = 240;

function Layout({ handleLogout }) {
  const navigate = useNavigate();

  const menuItems = [
    { text: 'Students', icon: <PeopleIcon />, path: '/students' },
    { text: 'Courses', icon: <SchoolIcon />, path: '/courses' },
  ];

  return (
    <Box sx={{ display: 'flex' }}>
        <Toaster position="top-center" reverseOrder={false} />
      <AppBar position="fixed" sx={{ zIndex: (theme) => theme.zIndex.drawer + 1 }}>
        <Toolbar>
          <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
            Student Information System
          </Typography>
          <Button color="inherit" onClick={handleLogout}>Logout</Button>
        </Toolbar>
      </AppBar>
      <Drawer
        variant="permanent"
        sx={{
          width: drawerWidth,
          flexShrink: 0,
          [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
        }}
      >
        <Toolbar />
        <Box sx={{ overflow: 'auto' }}>
          <List>
            {menuItems.map((item) => (
              <ListItem key={item.text} disablePadding>
                <ListItemButton onClick={() => navigate(item.path)}>
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText primary={item.text} />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      </Drawer>
      <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
        <Toolbar />
        {/* This is where the page content will be rendered */}
        <Outlet />
      </Box>
    </Box>
  );
}

export default Layout;