# models.py
# supabase.py
from typing import Optional
from pydantic import BaseModel

class Message(BaseModel):
    message: str

class MessageResponse(BaseModel):
    text: Optional[str] = None
    role: Optional[str] = None

class User(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    created_at: Optional[str] = None
    # Add other fields as needed
class Session(BaseModel):
    id: int
    user_id: int
    session_start: Optional[str] = None
    session_end: Optional[str] = None
    title: Optional[str] = None

class Messages(BaseModel):
    session_id: int
    sender_role: Optional[str] = None
    message_text: Optional[str] = None
    created_at: Optional[str] = None
    message_timestamp: Optional[str] = None

class SessionDB(BaseModel):
    user_id: int
    session_start: Optional[str] = None
    session_end: Optional[str] = None
    title: Optional[str] = None    


class UserDB(BaseModel):
    username: Optional[str] = None
    created_at: Optional[str] = None    