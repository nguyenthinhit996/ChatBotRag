import React, { useCallback, useEffect, useRef, useState } from "react";
import {
  Container,
  Typography,
  Grid,
  Box,
  Paper,
  List,
  ListItem,
  ListItemText,
  Divider,
  TextField,
  Button,
} from "@mui/material";
import { styled } from "@mui/system";
import { DeepChat } from "deep-chat-react";
import ListItemButton from "@mui/material/ListItemButton";
import IconButton from "@mui/material/IconButton";
import AddCircleIcon from "@mui/icons-material/AddCircle";
import { getRandomInt } from "../util";
import cloneDeep from "lodash/cloneDeep";
import { getData, postData } from "../api";

// import backgroundImage from './techBackground.svg'; // Ensure this path is correct

const Root = styled("div")({
  display: "flex",
  height: "80vh",
  width: "100%",
});

const ChatHistory = styled(Paper)({
  height: "70vh",
  overflowY: "auto",
});

const ChatContainer = styled(Grid)({
  height: "70vh",
});

const ChatPanel = styled(Paper)({
  height: "100%",
});

let introMessage = { text: "Hi I am your assistant, ask me anything!" };

const ChatbotPage = ({ setSessionChat, sessionChat, callBack }) => {
  const userId = localStorage.getItem("user_id");
  // Check if user_id exists
  if (!userId) {
    // Redirect to /home page
    window.location.href = "/";
    return;
  } else {
    // User ID exists, you can proceed with other actions
    console.log("User ID:", userId);
  }
  const [initialMessages, setInitialMessages] = useState([]);
  const sessionIdRef = useRef();

  const customizeRequestInterceptor = (requestDetails) => {
    console.log("requestDetails,", requestDetails); // printed above
    // requestDetails.body = { prompt: requestDetails.body.messages[0].text }; // custom body
    requestDetails.body = {
      message:
        requestDetails.body.messages[requestDetails.body.messages.length - 1]
          .text,
    };

    requestDetails.headers["session"] = sessionIdRef.current;
    return requestDetails;
  };

  const customizeResponseInterceptor = (response) => {
    console.log("response", response); // printed above
    return response;
  };

  const actionNewChat =  async() => {
    resetSelected();
    let dataNew = {
      user_id: userId,
      session_start: new Date().toUTCString(),
      title: "New Chat - " + new Date().getMilliseconds(),
      isSelected: true,
    };

    //call api get new chat
    try {
      await postData("/sessions", dataNew)
    }catch(e){
      console.log(e);
    }
    await callBack(userId)
    // dataNew = { ...dataNew, id: getRandomInt(100, 10000) };
    // let newSessionChat = cloneDeep(sessionChat);
    // newSessionChat.unshift(dataNew);
    // console.log(newSessionChat);
    // setSessionChat(newSessionChat);
  };

  const handleListItemClick = (id) => {
    let newSessionChat = sessionChat.map((item) => {
      if (item.id === id) item.isSelected = true;
      else item.isSelected = false;
      return item;
    });
    setSessionChat(newSessionChat);
  };

  const resetSelected = () => {
    let newSessionChat = sessionChat.map((item) => {
      item.isSelected = false;
      return item;
    });
    setSessionChat(newSessionChat);
  };

  const handleGetMessgesBySessionId = async (data = []) => {
    const idSessionChat = data.filter((item) => item.isSelected)[0]?.id;
    if (idSessionChat) {
      //the message of the first session
      let url = "/sessions/" + idSessionChat + "/messages";
      let data = await getData(url);
      setInitialMessages(data);
      url = "http://127.0.0.1:8080/api/chatbot/" + idSessionChat + "/message";
      sessionIdRef.current = idSessionChat;
    }
  };

  useEffect(() => {
    if (sessionChat && sessionChat.length) {
      handleGetMessgesBySessionId(sessionChat);
    }
  }, [sessionChat]);

  return (
    <Root>
      <Container sx={{ flexGrow: 1, display: "flex", flexDirection: "column" }}>
        <Box
          sx={{
            display: "flex",
            justifyContent: "flex-start",
            alignItems: "center",
            gap: "2em",
            padding: "0 1em",
          }}
        >
          <Typography variant="h5" align="center">
            History Session
          </Typography>
          <IconButton
            onClick={actionNewChat}
            aria-label="delete"
            size="large"
            color="primary"
            sx={{
              "&:focus": {
                outline: "none",
              },
            }}
          >
            <AddCircleIcon fontSize="large" color="primary" />
          </IconButton>
        </Box>

        <Grid container spacing={2} sx={{ flexGrow: 1 }}>
          <Grid item xs={3}>
            <ChatHistory component={ChatPanel} elevation={3}>
              <List>
                {sessionChat.map((session) => (
                  <React.Fragment key={session.id}>
                    <ListItemButton
                      selected={session.isSelected}
                      onClick={() => handleListItemClick(session.id)}
                      sx={{
                        "&.Mui-selected": {
                          backgroundColor: "rgba(25, 118, 210, 0.5)",
                        },
                        "&.Mui-hover": {
                          backgroundColor: "rgba(25, 118, 210, 0.5)",
                        },
                      }}
                    >
                      <ListItemText
                        primary={session.title}
                        secondary={session.session_start}
                      />
                    </ListItemButton>
                    <Divider />
                  </React.Fragment>
                ))}
              </List>
            </ChatHistory>
          </Grid>
          <Grid item xs={9}>
            <ChatContainer container>
              <DeepChat
                avatars="true"
                request={{
                  url: "http://192.168.18.23:8080/api/chatbot/message",
                  method: "POST",
                }}
                chatStyle={{
                  width: "100%",
                  height: "100%",
                  overflow: "auto",
                }}
                introMessage={introMessage}
                demo={true}
                style={{ borderRadius: "10px" }}
                textInput={{ placeholder: { text: "Welcome to the demo!" } }}
                initialMessages={initialMessages}
                requestInterceptor={customizeRequestInterceptor}
                responseInterceptor={customizeResponseInterceptor}
              />
            </ChatContainer>
          </Grid>
        </Grid>
      </Container>
    </Root>
  );
};

export default ChatbotPage;
