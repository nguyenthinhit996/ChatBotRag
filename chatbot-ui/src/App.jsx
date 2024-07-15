// src/App.jsx
import Toolbar from "@mui/material/Toolbar";
import React, { useEffect } from "react";

import MenuIcon from "@mui/icons-material/Menu";
import AppBar from "@mui/material/AppBar";
import Box from "@mui/material/Box";
import CssBaseline from "@mui/material/CssBaseline";
import Divider from "@mui/material/Divider";
import Drawer from "@mui/material/Drawer";
import IconButton from "@mui/material/IconButton";
import Typography from "@mui/material/Typography";

import { Link, Route, Routes } from "react-router-dom";
import Chat from "./pages/Chat";
import ChatbotPage from "./pages/Chat";
import Contact from "./pages/Contact";
import Home from "./pages/Home";
import { getData } from "./api";

const drawerWidth = 240;
// const navItems = ['Home', 'About', 'Contact'];

const navItems = [
  { text: "Home", path: "/" },
  { text: "Chat", path: "/chat" },
  { text: "Contact", path: "/contact" },
];

const mockSesstion = [
  {
    id: 1,
    user_id: 101,
    session_start: "2024-07-13T09:00:00",
    session_end: "2024-07-13T10:00:00",
    title: "Initial Meeting",
    isSelected: false,
  },
  {
    id: 2,
    user_id: 102,
    session_start: "2024-07-14T14:00:00",
    session_end: "2024-07-14T15:30:00",
    title: "Project Planning",
    isSelected: true,
  },
  {
    id: 3,
    user_id: 103,
    session_start: "2024-07-15T11:00:00",
    session_end: "2024-07-15T12:00:00",
    title: "Training Session",
    isSelected: false,
  },
  {
    id: 4,
    user_id: 101,
    session_start: "2024-07-16T10:30:00",
    session_end: "2024-07-16T11:30:00",
    title: "Review Meeting",
    isSelected: false,
  },
  {
    id: 5,
    user_id: 104,
    session_start: "2024-07-17T13:00:00",
    session_end: "2024-07-17T14:30:00",
    title: "Client Presentation",
    isSelected: false,
  },
];

const App = (props) => {
  const [sessionChat, setSessionChat] = React.useState([]);

  const handleGetAllSessionByUseId = async (userId) => {
    try {
      let url = "users/" + userId + "/sessions";
      let data = await getData(url);
      if(data && data.length > 0) {
        data[0] = {
          ...data[0],
          isSelected: true
        }
      }
      console.log("call data api:" ,data);
      setSessionChat(data);
    } catch (e) {
      console.log(e);
    }
  };

  useEffect(() => {
    const userId = localStorage.getItem("user_id");
    if (userId) {
      handleGetAllSessionByUseId(userId);
      console.log("Calling handleGetAllSessionByUseId");
    }
  }, []);

  return (
    <Box sx={{ width: "100%" }}>
      <Box sx={{ display: "flex", flexDirection: "column", gap: "3em" }}>
        <CssBaseline />
        <AppBar component="nav">
          <Toolbar>
            <IconButton
              color="inherit"
              aria-label="open drawer"
              edge="start"
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
        <Box
          component="main"
          sx={{
            mt: "2em",
            display: "flex",
          }}
        >
          <Routes>
            <Route path="/" element={<Home  callBack={handleGetAllSessionByUseId} />} />
            <Route path="/contact" element={<Contact />} />
            {/* <Route
              path="/Chat"
              element={<Chat list={list} setList={setList} />}
            /> */}
            <Route
              path="/Chat"
              element={
                <ChatbotPage
                  sessionChat={sessionChat}
                  setSessionChat={setSessionChat}
                  callBack={handleGetAllSessionByUseId}
                />
              }
            />
          </Routes>
        </Box>
      </Box>
    </Box>
  );
};

export default App;
