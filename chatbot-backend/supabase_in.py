# supabase.py
from typing import Optional
import asyncpg
import httpx
from models import User, Session, Message, Messages, SessionDB, UserDB, BookingDB, Booking
from supabase import create_client, Client
from typing import List
from dotenv import load_dotenv
import os
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from datetime import datetime

load_dotenv()  # Load environment variables from .env file

# Access environment variables
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# User Operations
async def create_user(user: UserDB):
    supabase.table('users').insert(user.dict()).execute()

async def get_user(user_id: int) -> Optional[User]:
    response = supabase.table("users").select("*").eq('user_id', user_id).execute()
    print(response)
    if response.data is not None:
        user_data = response.data[0]
        user = User(
            user_id=user_data.get('user_id'),  # Assuming 'id' in Supabase corresponds to 'user_id'
            username=user_data.get('username'),  # Make sure this field exists in your Supabase table
            created_at=user_data.get('created_at'),  # Make sure this field exists in your Supabase table
        )
        return user
    return None

async def get_user_by_name(username: str) -> Optional[User]:
    response = supabase.table("users").select("*").eq('username', username).execute()
    if response.data is not None and len(response.data) > 0:
        user_data = response.data[0]
        user = User(
            user_id=user_data.get('user_id'),  # Assuming 'id' in Supabase corresponds to 'user_id'
            username=user_data.get('username'),  # Make sure this field exists in your Supabase table
            created_at=user_data.get('created_at'),  # Make sure this field exists in your Supabase table
        )
        return user
    return None

async def get_session_by_user_id(user_id: int) -> List[Session]:
    response = supabase.table('sessions').select('*').eq('user_id', user_id).order("id", desc=True).execute()
    sessions = response.data
    print(sessions)
    return [Session(**session) for session in sessions]

async def update_user(user_id: int, user: User):
    await supabase.table('users').update(user.dict()).eq('user_id', user_id).execute()

async def delete_user(user_id: int):
    await supabase.table('users').delete().eq('user_id', user_id).execute()

# Session Operations
async def create_session(session: SessionDB):
    data = supabase.table('sessions').insert(session.dict()).execute()
    print(create_session)
    print(data)
    return data

async def get_session(session_id: int) -> Session:
    session = await supabase.table('sessions').select('*').eq('id', session_id).single()
    return Session(**session)

async def update_session(session_id: int, session: Session):
    await supabase.table('sessions').update(session.dict()).eq('id', session_id).execute()

async def delete_session(session_id: int):
    await supabase.table('sessions').delete().eq('id', session_id).execute()

# Message Operations
def create_message(message: Messages):
    supabase.table('messages').insert(message.dict()).execute()

async def get_message(message_id: int) -> Message:
    message = await supabase.table('messages').select('*').eq('id', message_id).single()
    return Message(**message)

async def update_message(message_id: int, message: Message):
    await supabase.table('messages').update(message.dict()).eq('id', message_id).execute()

async def delete_message(message_id: int):
    await supabase.table('messages').delete().eq('id', message_id).execute()

async def get_messages_by_session_id(session_id: int) -> List[Messages]:
    response = supabase.table('messages').select('*').eq('session_id', session_id).execute()
    messages = response.data
    print(messages)
    return [Messages(**message) for message in messages]


def create_message_format(row):
    if row['sender_role'] == 'bot':
        return AIMessage(content=row['message_text'])
    elif row['sender_role'] == 'user':
        return HumanMessage(content=row['message_text'])
    else:
        return BaseMessage(content=row['message_text'])

def get_BaseMessage_by_session_id(session_id: int) -> List[BaseMessage]:
    response = supabase.table('messages').select('sender_role, message_text').eq('session_id', session_id).order("message_timestamp", desc=True).limit(10).execute()
    messages = response.data
    print("get_BaseMessage_by_session_id")
    print(messages)
    
    return [create_message_format(row) for row in messages]

def create_booking(booking: BookingDB) -> BookingDB:
    """Create a new booking in the database."""
    booking_dict = booking.model_dump(exclude_unset=True)
    if 'created_at' not in booking_dict:
        booking_dict['created_at'] = datetime.now().isoformat()
        booking_dict['status'] = 'Booking'
    
    response = supabase.table("booking").insert(booking_dict).execute()
    return BookingDB(**response.data[0])

def get_bookings(limit: int = 5) -> List[BookingDB]:
    """Retrieve the latest bookings from the database."""
    response = (
        supabase.table("booking")
        .select("*")
        .order("created_at", desc=True)
        .limit(limit)
        .execute()
    )
    return [BookingDB(**booking) for booking in response.data]

def update_booking(booking_id: int, updated_data: dict) -> BookingDB:
    """Update an existing booking in the database."""
    response = supabase.table("booking").update(updated_data).eq("id", booking_id).execute()
    if not response.data:
        raise ValueError(f"No booking found with id {booking_id}")
    return BookingDB(**response.data[0])

def delete_booking(booking_id: int) -> bool:
    """Delete a booking from the database."""
    response = supabase.table("booking").delete().eq("id", booking_id).execute()
    return len(response.data) > 0

def get_bookings_by_email(email: str) -> List[Booking]:
    response = (
        supabase.table("booking")
        .select("*")
        .eq("email", email)
        .execute()
    )
    
    if not response.data:
        return []
    
    return [Booking(**booking) for booking in response.data]

def get_bookings_by_id(id: str) -> Booking:
    response = (
        supabase.table("booking")
        .select("*")
        .eq("id", id)
        .execute()
    )
    
    if not response.data:
        return None
    booking = response.data[0]
    return Booking(**booking)