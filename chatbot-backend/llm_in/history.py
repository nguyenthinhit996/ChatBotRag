# export OLLAMA_HOST=https://f30f-34-168-55-128.ngrok-free.app/
from typing import List
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage
from utils import (generateMesages)

class CustomDBMessageHistory(BaseChatMessageHistory):
    def __init__(self, user_id: str, session_id: str, db_connection):
        self.user_id = user_id
        self.session_id = session_id
        self.db_connection = db_connection

    def add_message(self, message: BaseMessage) -> None:
        with self.db_connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO messages (user_id, session_id, role, content) VALUES (%s, %s, %s, %s)",
                (self.user_id, self.session_id, message.type, message.content)
            )
        self.db_connection.commit()

    def clear(self) -> None:
        with self.db_connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM messages WHERE user_id = %s AND session_id = %s",
                (self.user_id, self.session_id)
            )
        self.db_connection.commit()

    @property
    def messages(self) -> List[BaseMessage]:
        with self.db_connection.cursor() as cursor:
            cursor.execute(
                "SELECT role, content FROM messages WHERE user_id = %s AND session_id = %s ORDER BY created_at",
                (self.user_id, self.session_id)
            )
            return [BaseMessage(type=row[0], content=row[1]) for row in cursor.fetchall()]
