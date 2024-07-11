// src/App.jsx
import React from "react";
import Toolbar from "@mui/material/Toolbar";

import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";
import List from "@mui/material/List";
import ListItem from "@mui/material/ListItem";
import ListItemButton from "@mui/material/ListItemButton";
import ListItemText from "@mui/material/ListItemText";
import MenuIcon from "@mui/icons-material/Menu";
import Typography from "@mui/material/Typography";
import Button from "@mui/material/Button";
import AppBar from "@mui/material/AppBar";

import { Route, Routes, Link } from "react-router-dom";
import Contact from "./pages/Contact";
import Chat from "./pages/Chat";
import Home from "./pages/Home";

const drawerWidth = 240;
// const navItems = ['Home', 'About', 'Contact'];

const navItems = [
  { text: "Home", path: "/" },
  { text: "Chat", path: "/chat" },
  { text: "Contact", path: "/contact" },
];

const App = (props) => {
  const { window } = props;
  const [mobileOpen, setMobileOpen] = React.useState(false);

  const [list, setList] = React.useState([
    { title: "Hello world", id: Date.now().toString() },
  ]);

  const handleDrawerToggle = () => {
    setMobileOpen((prevState) => !prevState);
  };

  const drawer = (
    <Box onClick={handleDrawerToggle} sx={{ textAlign: "center" }}>
      <Typography variant="h6" sx={{ my: 2 }}>
        MUI
      </Typography>
      <Divider />
      {navItems.map((item) => (
        // eslint-disable-next-line react/jsx-key
        <Link
          to={item.path}
          style={{
            textDecoration: "none",
            color: "inherit",
            width: "100%",
            display: "block",
            textAlign: "center",
            padding: "8px 0",
          }}
        >
          {item.text}
        </Link>
      ))}
    </Box>
  );

  const container =
    window !== undefined ? () => window().document.body : undefined;

  return (
    <Box>
      <Box sx={{ display: "flex", flexDirection: "column", gap: "3em" }}>
        <CssBaseline />
        <AppBar component="nav">
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
              onClick={handleDrawerToggle}
              sx={{ mr: 2, display: { sm: "none" } }}
            >
              <MenuIcon />
            </IconButton>
            <Typography
              variant="h6"
              component="div"
              sx={{ flexGrow: 1, display: { xs: "none", sm: "block" } }}
            >
              MUI
            </Typography>
            <Box sx={{ display: "flex", gap: 2 }}>
              {navItems.map((item) => (
                // eslint-disable-next-line react/jsx-key
                <Link
                  to={item.path}
                  style={{
                    textDecoration: "none",
                    color: "inherit",
                    width: "100%",
                    display: "block",
                    textAlign: "center",
                    padding: "8px 0",
                  }}
                >
                  {item.text}
                </Link>
              ))}
            </Box>
          </Toolbar>
        </AppBar>
        <nav>
          <Drawer
            container={container}
            variant="temporary"
            open={mobileOpen}
            onClose={handleDrawerToggle}
            ModalProps={{
              keepMounted: true, // Better open performance on mobile.
            }}
            sx={{
              display: { xs: "block", sm: "none" },
              "& .MuiDrawer-paper": {
                boxSizing: "border-box",
                width: drawerWidth,
              },
            }}
          >
            {drawer}
          </Drawer>
        </nav>
        <Box
          component="main"
          sx={{
            mt: "2em",
            display: "flex",
          }}
        >
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/contact" element={<Contact />} />
            <Route
              path="/Chat"
              element={<Chat list={list} setList={setList} />}
            />
          </Routes>
        </Box>
      </Box>
    </Box>
  );
};

export default App;
