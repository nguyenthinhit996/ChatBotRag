from fastapi import FastAPI, HTTPException
from typing import List
from supabase_in import (
    create_user, get_user, update_user, delete_user,
    create_session, get_session, update_session, delete_session,
    create_message, get_message, update_message, delete_message,
)
from models import User, Session, Message, MessageResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

# Simulated chat history
chat_history = []

# Endpoint to receive user messages
@app.post("/chatbot/message", response_model=MessageResponse)
async def receive_message(message: Message):
    # Simulate processing and generate a response
    response_message = "Response from the chatbot."
    # Store message in chat history
    chat_history.append({"user": message.message, "chatbot": response_message})
    return MessageResponse(text=response_message)

# Endpoint to fetch chat history
@app.get("/chatbot/history", response_model=List[Message])
async def get_chat_history():
    return chat_history

# Endpoint to reset chat history
@app.delete("/chatbot/history", response_model=Message)
async def reset_chat_history():
    chat_history.clear()
    return {"message": "Chat history cleared."}
# Z9p553.uunNrr5M

@app.post("/users", response_model=User, status_code=201)
async def create_new_user(user: User):
    await create_user(user)
    return user

@app.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=User)
async def update_existing_user(user_id: int, user: User):
    user.id = user_id
    await update_user(user)
    return user

@app.delete("/users/{user_id}", status_code=204)
async def delete_existing_user(user_id: int):
    await delete_user(user_id)

@app.post("/sessions", response_model=Session, status_code=201)
async def create_new_session(session: Session):
    await create_session(session)
    return session

@app.get("/sessions/{session_id}", response_model=Session)
async def read_session(session_id: int):
    return await get_session(session_id)

@app.put("/sessions/{session_id}", response_model=Session)
async def update_existing_session(session_id: int, session: Session):
    session.id = session_id