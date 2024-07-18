
from typing import List
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.messages import BaseMessage, HumanMessage
from util import (generateMesages)
from supabase_in import (get_BaseMessage_by_session_id)

class CustomDBMessageHistoryGetting(BaseChatMessageHistory):
    def __init__(self, session_id: str):
        self.session_id = session_id

    def add_message(self, message: BaseMessage) -> None:
        print("adding message")
        print(message)
        generateMesages(role=message.type, text=message.content, session_id=self.session_id)    

    def clear(self) -> None:
        print("Clearing chat history")

    @property
    def messages(self) -> List[BaseMessage]:
        message = get_BaseMessage_by_session_id(self.session_id)
        return message

class CustomDBMessageHistoryUsing(BaseChatMessageHistory):
    def __init__(self, session_id: str):
        self.session_id = session_id
        self.messagesTem: List[BaseMessage] = []

    def add_message(self, message: BaseMessage) -> None:
        print("adding message")
        print(message)
        generateMesages(role=message.type, text=message.content, session_id=self.session_id)    

    def clear(self) -> None:
        print("Clearing chat history")
        self.messagesTem = []

    def customizePush(self, message: BaseMessage):
        self.messagesTem.append(message)

    @property
    def messages(self) -> List[BaseMessage]:
        return self.messagesTem