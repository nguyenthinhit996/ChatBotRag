# supabase.py
from typing import Optional
import asyncpg
import httpx
from models import User, Session, Message
from supabase import create_client, Client

 

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# User Operations
async def create_user(user: User):
    await supabase.table('users').insert(user.dict()).execute()

async def get_user(user_id: int) -> Optional[User]:
    response = supabase.table("users").select("*").execute()

    user_data = response.data  # Assuming the query returns a single user


    print(user_data)
    return None
    # # Map the Supabase fields to your User model fields
    # try:
    #     user = User(
    #         user_id=user_data.get('user_id'),  # Assuming 'id' in Supabase corresponds to 'user_id'
    #         username=user_data.get('username'),  # Make sure this field exists in your Supabase table
    #         created_at=user_data.get('created_at'),  # Make sure this field exists in your Supabase table
    #         # Map other fields as necessary
    #     )
    #     return user
    # except ValueError as e:
    #     print(f"Error creating User object: {e}")
    #     return None

async def update_user(user_id: int, user: User):
    await supabase.table('users').update(user.dict()).eq('user_id', user_id).execute()

async def delete_user(user_id: int):
    await supabase.table('users').delete().eq('user_id', user_id).execute()

# Session Operations
async def create_session(session: Session):
    await supabase.table('sessions').insert(session.dict()).execute()

async def get_session(session_id: int) -> Session:
    session = await supabase.table('sessions').select('*').eq('id', session_id).single()
    return Session(**session)

async def update_session(session_id: int, session: Session):
    await supabase.table('sessions').update(session.dict()).eq('id', session_id).execute()

async def delete_session(session_id: int):
    await supabase.table('sessions').delete().eq('id', session_id).execute()

# Message Operations
async def create_message(message: Message):
    await supabase.table('messages').insert(message.dict()).execute()

async def get_message(message_id: int) -> Message:
    message = await supabase.table('messages').select('*').eq('id', message_id).single()
    return Message(**message)

async def update_message(message_id: int, message: Message):
    await supabase.table('messages').update(message.dict()).eq('id', message_id).execute()

async def delete_message(message_id: int):
    await supabase.table('messages').delete().eq('id', message_id).execute()