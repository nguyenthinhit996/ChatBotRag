from fastapi import FastAPI, HTTPException, APIRouter, Query, Header
from typing import List
from supabase_in import (
    create_user, get_user, update_user, delete_user,
    create_session, get_session, update_session, delete_session,
    create_message, get_message, update_message, delete_message,
    get_session_by_user_id, get_messages_by_session_id, get_user_by_name
)
from models import User, Session, Message, MessageResponse, Messages, SessionDB, UserDB
from fastapi.middleware.cors import CORSMiddleware
from util import (parse_messages_to_responses, generateMesages, addNewSession)
from llm_in.core_llm import (startLLMInitial, UserSession, SessionManager)
from datetime import date

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

prefix_router = APIRouter(prefix="/api")
session_manager = startLLMInitial()

@prefix_router.get("/")
def read_root():
    return {"Hello": "World"}

# Endpoint to receive user messages
@prefix_router.post("/chatbot/message", response_model=MessageResponse)
async def receive_message(message: Message,  session: int = Header(None)):
    await generateMesages('user', message.message, session)
    response_message = session_manager.chat(session, message.message)
    await generateMesages('bot', response_message, session)
    return MessageResponse(text=response_message, role="bot")

# Endpoint to fetch chat history
@prefix_router.get("/chatbot/history", response_model=List[Message])
async def get_chat_history():
    return chat_history

# Endpoint to reset chat history
@prefix_router.delete("/chatbot/history", response_model=Message)
async def reset_chat_history():
    chat_history.clear()
    return {"message": "Chat history cleared."}
# Z9p553.uunNrr5M

@prefix_router.post("/users", response_model=User, status_code=201)
async def create_new_user(userInput: UserDB):
    user = await get_user_by_name(userInput.username)
    if user is None:
        await create_user(userInput)
        user = await get_user_by_name(userInput.username)

        session_start= str(date.today())
        title= "New Chat" + str(date.today())  

        newSession = SessionDB(user_id= user.user_id, session_start=session_start, title=title )
        await addNewSession(newSession)

    return user

@prefix_router.get("/users/{user_id}", response_model=User)
async def read_user(user_id: int):
    user = await get_user(user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@prefix_router.put("/users/{user_id}", response_model=User)
async def update_existing_user(user_id: int, user: User):
    user.id = user_id
    await update_user(user)
    return user

@prefix_router.delete("/users/{user_id}", status_code=204)
async def delete_existing_user(user_id: int):
    await delete_user(user_id)

@prefix_router.get("/users/{user_id}/sessions", response_model=List[Session])
async def get_session_by_user(user_id: int):
    data = await get_session_by_user_id(user_id)
    return data

@prefix_router.post("/sessions", response_model=Session, status_code=201)
async def create_new_session(session: SessionDB):
    data = await addNewSession(session)
    print(data)
    return data

@prefix_router.get("/sessions/{session_id}", response_model=Session)
async def read_session(session_id: int):
    return await get_session(session_id)

@prefix_router.get("/sessions/{session_id}/messages",response_model=List[MessageResponse])
async def read_message_from_session(session_id: int):
    data = await get_messages_by_session_id(session_id)    
    return parse_messages_to_responses(data)

@prefix_router.put("/sessions/{session_id}", response_model=Session)
async def update_existing_session(session_id: int, session: Session):
    session.id = session_id


# Now add the router to the app
app.include_router(prefix_router)    