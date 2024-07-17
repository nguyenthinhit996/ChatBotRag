import React from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  List,
  ListItem,
  ListItemText,
  Link,
  Divider,
} from "@mui/material";

import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";

import all_url from "./Link";
import ChatbotTechnologies from "./DrawTechnology";

const Contact = () => {
  return (
    <Container maxWidth="md">
      <Box my={4}>
        <Typography variant="h3" component="h1" gutterBottom>
          Our Chatbot
        </Typography>

        <Paper elevation={3}>
          <Box p={3}>
            <Box
              sx={{
                width: "100%",
                maxWidth: 800,
                maxHeight: "500px",
                margin: "auto",
              }}
            >
              <Typography variant="h4" component="h1" gutterBottom>
                Crawled URLs: {all_url.length} Links
              </Typography>
              <TableContainer component={Paper} sx={{ maxHeight: 400 }}>
                <Table stickyHeader aria-label="crawled urls table">
                  <TableHead>
                    <TableRow>
                      <TableCell>URL</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {all_url.map((url, index) => (
                      <TableRow key={index}>
                        <TableCell>
                          <Link
                            href={url}
                            target="_blank"
                            rel="noopener noreferrer"
                            sx={{
                              display: "block",
                              maxWidth: "100%",
                              overflow: "hidden",
                              textOverflow: "ellipsis",
                              whiteSpace: "nowrap",
                            }}
                          >
                            {url}
                          </Link>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Box>
          </Box>
        </Paper>

        <Box my={4}>
          <Paper elevation={3}>
            <Box p={3}>
              <ChatbotTechnologies />
            </Box>
          </Paper>
        </Box>

        <Box my={4}>
          <Paper elevation={3}>
            <Box p={3}>
              <Typography variant="h5" gutterBottom>
                Contact Us
              </Typography>
              <Typography paragraph>
                If you need assistance or have any questions, please don't
                hesitate to reach out:
              </Typography>
              <List>
                <ListItem>
                  <ListItemText
                    primary="Email"
                    secondary={
                      <Link href="mailto:thinh.n@resvu.io">
                        thinh.n@resvu.io
                      </Link>
                    }
                  />
                </ListItem>
                <ListItem>
                  <ListItemText primary="Phone" secondary="61411276342" />
                </ListItem>
                <ListItem>
                  <ListItemText
                    primary="TMA Tower address"
                    secondary="Street #10, Quality Tech Solution Complex (QTSC), 1 To Ky, District 12, Ho Chi Minh City (Map)"
                  />
                </ListItem>
              </List>
            </Box>
          </Paper>
        </Box>
      </Box>
    </Container>
  );
};

export default Contact;
