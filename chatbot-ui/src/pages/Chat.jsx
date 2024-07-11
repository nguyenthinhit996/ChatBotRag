// src/pages/About.jsx
import React from "react";
// import {DeepChat as DeepChatCore} from 'deep-chat'; <- type
import { DeepChat } from "deep-chat-react";

import IconButton from "@mui/material/IconButton";
import AddCircleIcon from "@mui/icons-material/AddCircle";
import { Stack, Typography } from "@mui/material";
import Card from "@mui/material/Card";
import CardActions from "@mui/material/CardActions";
import CardContent from "@mui/material/CardContent";
import Button from "@mui/material/Button";
import DeleteIcon from "@mui/icons-material/Delete";

let introMessage = { text: "Hi I am your assistant, ask me anything!" };

// eslint-disable-next-line react/prop-types
const Chat = ({ list = [], setList = () => {} }) => {
  const initialMessages = [
    { role: "user", text: "Hey, how are you today?" },
    { role: "ai", text: "I am doing very well!" },
  ];

  const customizeRequestInterceptor = (requestDetails) => {
    console.log(requestDetails); // printed above
    // requestDetails.body = { prompt: requestDetails.body.messages[0].text }; // custom body

    requestDetails.body = {
      message:
        requestDetails.body.messages[requestDetails.body.messages.length - 1]
          .text,
    };
    return requestDetails;
  };

  const customizeResponseInterceptor = (response) => {
    console.log("response", response); // printed above
    return response;
  };

  const genegrateChat = (data) => {
    return (
      <Card variant="outlined">
        <CardActions sx={{ display: "flex", justifyContent: "space-between" }}>
          <Typography size="small">{data?.title + " - " + data?.id}</Typography>
          <Button size="small">
            <DeleteIcon
              color="error"
              onClick={() => actionRemoveChat(data.id)}
            />
          </Button>
        </CardActions>
        <CardContent>
          <DeepChat
            request={{
              url: "http://127.0.0.1:8080/chatbot/message",
              method: "POST",
            }}
            introMessage={introMessage}
            demo={true}
            style={{ borderRadius: "10px" }}
            textInput={{ placeholder: { text: "Welcome to the demo!" } }}
            // initialMessages={initialMessages}
            requestInterceptor={customizeRequestInterceptor}
            responseInterceptor={customizeResponseInterceptor}
          />
        </CardContent>
      </Card>
    );
  };

  const actionNewChat = () => {
    //call api get new chat
    let dataMock = {
      title: "Chat number ",
      id: Date.now().toString(),
    };
    setList([...list, dataMock]);
  };

  const actionRemoveChat = (idRemove) => {
    //remove by id
    let listNew = list.filter((item) => item.id !== idRemove);
    setList(listNew);
  };

  return (
    <div className="App">
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
      <Stack
        direction="row"
        spacing={2}
        useFlexGap
        flexWrap="wrap"
        sx={{ padding: "10px" }}
      >
        {list.map((item, index) => genegrateChat(item))}
      </Stack>
    </div>
  );
};

export default Chat;
