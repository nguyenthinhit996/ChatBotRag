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

import MovingImage from "./pages/Moving";

const drawerWidth = 240;
// const navItems = ['Home', 'About', 'Contact'];

const navItems = [
  // { text: "Home", path: "/" },
  { text: "Chat", path: "/chat" },
  { text: "Contact", path: "/contact" },
];

const App = (props) => {
  const [sessionChat, setSessionChat] = React.useState([]);

  const handleGetAllSessionByUseId = async (userId) => {
    try {
      let url = "users/" + userId + "/sessions";
      let data = await getData(url);
      if (data && data.length > 0) {
        data[0] = {
          ...data[0],
          isSelected: true,
        };
      }
      console.log("call data api:", data);
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
        <AppBar component="nav" sx={{ backgroundColor: "#0077cbb5" }}>
          <Toolbar>
            <Typography
              variant="h6"
              component="div"
              sx={{ flexGrow: 1, display: { xs: "none", sm: "block" } }}
              onClick={() => (window.location.href = "/")}
            >
              <MovingImage
                imageUrl="https://cdn3d.iconscout.com/3d/premium/thumb/chatbot-6899426-5627910.png"
                containerWidth={screen.width - 150}
                containerHeight={50}
                imageSize={60}
              />
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
                    fontWeight: "bold",
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
            <Route
              path="/"
              element={<Home callBack={handleGetAllSessionByUseId} />}
            />
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
