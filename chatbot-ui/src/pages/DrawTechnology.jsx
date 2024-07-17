import React from "react";
import {
  Box,
  Typography,
  Paper,
  List,
  ListItem,
  ListItemText,
  Grid,
  Container,
  Chip,
  Divider,
} from "@mui/material";

const ChatbotTechnologies = () => {
  const technologies = {
    frontend: [
      { name: "Vite", category: "Build Tool" },
      { name: "React", category: "UI Library" },
      { name: "Material-UI 5", category: "UI Framework" },
    ],
    backend: [
      { name: "FastAPI", category: "Web Framework" },
      { name: "Uvicorn", category: "ASGI Server" },
      { name: "Pydantic", category: "Data Validation" },
      { name: "Supabase", category: "Database" },
      { name: "Asyncpg", category: "Database Driver" },
      { name: "Unstructured", category: "Document Processing" },
      { name: "Python-docx", category: "Document Processing" },
      { name: "Langgraph", category: "Graph Processing" },
      { name: "Langchain", category: "LLM Framework" },
      { name: "Langchain-huggingface", category: "LLM Integration" },
      { name: "Langchain-community", category: "LLM Ecosystem" },
      { name: "Mistral", category: "Language Model" },
      { name: "FAISS-cpu", category: "Vector Database" },
    ],
  };

  const diagram = `
  +-------------+     +-------------+
  |    Vite     |     |   React     |
  | (Build Tool)|     | (UI Library)|
  +------+------+     +------+------+
         |                   |
  +------v-------------------v------+
  |        Material-UI 5            |
  |        (UI Framework)           |
  +----------------+----------------+
                   |
  +----------------v----------------+
  |   FastAPI (Backend API)         |
  +----------------+----------------+
                   |
  +----------------v----------------+
  |         Langchain               |
  |   (Orchestration Layer)         |
  +----------------+----------------+
                   |
  +----------------v----------------+
  |           Mistral               |
  |      (Language Model)           |
  +----------------+----------------+
                   |
  +----------------v----------------+
  |   FAISS-cpu / Langgraph         |
  | (Vector Store / Graph Process)  |
  +----------------+----------------+
                   |
  +--------+---------------+--------+
  |        |               |        |
  |  Supabase (DB)  Unstructured    |
  | Asyncpg (Driver) Python-docx    |
  |        |               |        |
  +--------v---------------v--------+
  `;

  const TechList = ({ techs, title }) => (
    <Box>
      <Typography variant="h6" gutterBottom>
        {title}
      </Typography>
      <List dense>
        {techs.map((tech, index) => (
          <ListItem key={index}>
            <ListItemText
              primary={tech.name}
              secondary={
                <Chip
                  label={tech.category}
                  size="small"
                  color="primary"
                  variant="outlined"
                />
              }
            />
          </ListItem>
        ))}
      </List>
    </Box>
  );

  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h4" component="h1" gutterBottom>
          Our Chatbot Technologies
        </Typography>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Paper elevation={3}>
              <Box p={3}>
                <TechList
                  techs={technologies.frontend}
                  title="Frontend Technologies"
                />
                <Divider sx={{ my: 2 }} />
                <TechList
                  techs={technologies.backend}
                  title="Backend Technologies"
                />
              </Box>
            </Paper>
          </Grid>
          <Grid item xs={12} md={6}>
            <Paper elevation={3}>
              <Box p={3}>
                <Typography variant="h6" gutterBottom>
                  Architecture Diagram
                </Typography>
                <pre
                  style={{
                    whiteSpace: "pre-wrap",
                    wordWrap: "break-word",
                    fontFamily: "monospace",
                    fontSize: "0.7rem",
                  }}
                >
                  {diagram}
                </pre>
              </Box>
            </Paper>
          </Grid>
        </Grid>
      </Box>
    </Container>
  );
};

export default ChatbotTechnologies;
