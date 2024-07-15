# supabase.py
from typing import Optional
import asyncpg
import httpx
from models import User, Session, Message, Messages, SessionDB, UserDB
from supabase import create_client, Client
from typing import List


SUPABASE_URL ="https://.supabase.co"
SUPABASE_KEY =".."

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
    response = supabase.table('sessions').select('*').eq('user_id', user_id).execute()
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
async def create_message(message: Messages):
    return supabase.table('messages').insert(message.dict()).execute()

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
