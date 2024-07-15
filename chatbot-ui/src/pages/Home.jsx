import React, { useEffect, useState } from "react";
import { TextField, Button, Container, Typography, Box } from "@mui/material";
import { styled } from "@mui/system";
import { postData } from "../api";
import { isFalsy } from "../util";
import { useNavigate } from "react-router-dom";

const RootHome = styled("div")({
  height: "80vh",
  width: "100%",
  display: "flex",
  flexDirection: "column",
  justifyContent: "flex-start",
  alignItems: "center",
  backgroundImage: `url("./background2.avif")`,
  backgroundSize: "cover",
  backgroundPosition: "center",
  backgroundRepeat: "no-repeat",
});

const FormContainer = styled(Container)(({ theme }) => ({
  background: "rgb(138 183 219 / 20%)",
  padding: theme.spacing(4),
  borderRadius: theme.spacing(1),
  width: "100%",
  // boxShadow: theme.shadows[5],
  display: "flex",
  flexDirection: "column",
  justifyContent: "center",
  alignItems: "center",
}));

const Home = ({ callBack }) => {
  const username = localStorage.getItem("user_name");
  const [nameForm, setNameForm] = useState("");
  const [nameUser, setNameUser] = useState(username);

  const navigate = useNavigate();

  const handleButtonClick = () => {
    navigate("/chat");
  };

  const handleNameChange = (event) => {
    setNameForm(event.target.value);
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    console.log("User name:", nameForm);
    // Add your submit logic here
    if (isFalsy(nameForm)) {
      alert("Not emplty please");
    } else {
      await handleAddUser(nameForm);
    }
  };

  const handleAddUser = async (name) => {
    try {
      // Call the addUser function from api.js
      let data = {
        username: name,
        created_at: new Date().toLocaleString(),
      };
      const addedUser = await postData("/users", data);
      console.log("User added:", addedUser);
      localStorage.setItem("user_id", addedUser.user_id);
      localStorage.setItem("user_name", addedUser.username);
      setNameUser(name);
      await callBack(addedUser.user_id);
    } catch (error) {
      console.error("Error adding user:", error);
    }
  };

  return (
    <RootHome>
      <FormContainer>
        <Typography variant="h4" align="center" gutterBottom>
          {isFalsy(nameUser)
            ? `Welcome to the Chatbot, What's your name?`
            : `Welcome to the Chatbot, ${nameUser}`}
        </Typography>

        {isFalsy(nameUser) ? (
          <Box sx={{ width: "50%" }}>
            <form onSubmit={handleSubmit}>
              <TextField
                label="Enter your name"
                variant="outlined"
                fullWidth
                sx={{ marginBottom: 2 }}
                value={nameForm}
                onChange={handleNameChange}
              />
              <Button
                type="submit"
                variant="contained"
                color="primary"
                fullWidth
              >
                Start Chat
              </Button>
            </form>
          </Box>
        ) : (
          <Button
            type="submit"
            variant="contained"
            color="primary"
            onClick={handleButtonClick}
          >
            Go to Chat
          </Button>
        )}
      </FormContainer>
    </RootHome>
  );
};

export default Home;
