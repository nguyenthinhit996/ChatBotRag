from models import User, Session, MessageResponse, Messages, SessionDB
from typing import List
from datetime import date
from supabase_in import (
    create_user, get_user, update_user, delete_user,
    create_session, get_session, update_session, delete_session,
    create_message, get_message, update_message, delete_message,
    get_session_by_user_id, get_messages_by_session_id
)
import os
import pandas as pd

def get_file_path(relative_path: str) -> str:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print("script_dir")
    print(script_dir)
    return os.path.join(script_dir, relative_path)

def parse_messages_to_responses(messages: List[Messages]) -> List[MessageResponse]:
    return [MessageResponse(text=message.message_text, role=message.sender_role) for message in messages if message.message_text is not None]

def generateMesages(role, text, session_id):
    session_id = str(session_id)
    sender_role = role  
    message_text = text
    created_at = str(date.today())  
    message_time = str(date.today())
    message = Messages(session_id=session_id, sender_role=sender_role, message_text= message_text, created_at=created_at, message_timestamp=message_time)
    print(message)
    create_message(message)

async def addNewSession(session: SessionDB):
    await create_session(session)
def is_number(string):
    return pd.api.types.is_number(string)    