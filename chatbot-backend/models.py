# models.py
# supabase.py
from typing import Optional
from pydantic import BaseModel

class Message(BaseModel):
    message: str

class MessageResponse(BaseModel):
    text: str

class User(BaseModel):
    user_id: Optional[int] = None
    username: Optional[str] = None
    created_at: Optional[str] = None
    # Add other fields as needed
class Session(BaseModel):
    id: int
    user_id: int
    session_start: str
    session_end: str
    title: str

class Messages(BaseModel):
    id: int
    session_id: int
    sender_role: str
    message_text: str
    created_at: str
    message_timestemp: str
