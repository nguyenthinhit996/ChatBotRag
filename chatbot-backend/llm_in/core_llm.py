from datetime import datetime
from langchain.agents import Tool, initialize_agent, AgentType, tool, create_json_chat_agent
from langchain.tools.retriever import create_retriever_tool
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents.agent import AgentExecutor
from langchain.schema import AgentAction, AgentFinish
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS

from langchain_community.llms import Ollama
from langchain.callbacks import StreamingStdOutCallbackHandler
from langchain.tools import Tool
from pydantic import BaseModel, Field
from langchain.tools import StructuredTool
from langchain import hub
from util import get_file_path
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent

from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, HumanMessage, trim_messages, SystemMessage
from llm_in.history import (CustomDBMessageHistoryGetting, CustomDBMessageHistoryUsing)
from supabase_in import create_booking, get_BaseMessage_by_session_id, get_bookings_by_id, get_bookings_by_email
from models import Booking, BookingDB
import json
from util import is_number
from typing import Optional
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.prompts import MessagesPlaceholder


@tool
def get_list_booking_facilities(id: Optional[str] = None, email:Optional[str] = None) -> str:
    "Allowing user retrieve booking facilities infomation by id (identify of booking as number) or email or both."
    
    if not id and not email:
        return "Please provide id or email to retrieve booking facilities infomation"
    if is_number(id):
        return "Please provide id as numberic"
    if id:
        booking = get_bookings_by_id(id)
        bookingstr = json.dumps(booking.model_dump())
        print(bookingstr)
        return bookingstr
    if email:
        bookings = get_bookings_by_email(email)
        bookingstr = json.dumps([booking.model_dump() for booking in bookings])
        print(bookingstr)
        return bookingstr

@tool
def add_new_booking_facilities(user_email: str, venue: str, time_start: str, time_end: str) -> str:
    "Allowing user book some facilities such as gym, hall, meeting room ... at Resvu system"
    
    if not user_email or not venue or not time_start or not time_end:
        return "Please provide all required information"
    
    booking = BookingDB(email=user_email, venue=venue, start=time_start, end=time_end)
    create_booking(booking)

    return """Booking facility at Resvu systems successfully {email} on {venues} with status Booking"""

print(add_new_booking_facilities.name)
print(add_new_booking_facilities.description)
print(add_new_booking_facilities.args)
print(add_new_booking_facilities.args_schema.schema())
print(get_list_booking_facilities.args_schema.schema())


def startLLMInitial():
    # Initialize the session manager
    # mistral_llm = Ollama(base_url="https://306b-34-16-161-126.ngrok-free.app/", model="mistral")
    llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
    session_manager = SessionManager(llm)
    return session_manager

store = {}

class UserSession:
    def __init__(self, session_id, local_llm, ini_message):
        self.session_id = session_id
        self.llm = local_llm
        self.ini_message = ini_message
        # self.memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
        self.retrieval_tool = self.create_retrieval_tool()
        self.tools = [self.retrieval_tool, get_list_booking_facilities, add_new_booking_facilities]
        self.agent = self.create_agent()

    def get_session_history(self, session_id: str) -> BaseChatMessageHistory:
        try:
            if session_id not in store:
                chatMessageHistory = ChatMessageHistory()
                [chatMessageHistory.add_message(row) for row in self.ini_message]
                store[session_id] = chatMessageHistory

            history = store[session_id]

            # Apply the trimmer to the chat history
            trimmed_messages = trim_messages(
                messages=history.messages,
                max_tokens=1046,
                strategy="last",
                token_counter=self.llm,  # Make sure 'model' is defined and can count tokens
                include_system=False,
                allow_partial=False,
                start_on="human"
            )

            # Update the history with trimmed messages
            history.clear()
            for message in trimmed_messages:
                history.add_message(message)

            store[session_id] = history
            return store[session_id]
        except Exception as e:
            print(f"Error in get_session_history: {e}")
            print(e)
            return None

    def read_vectors_db(self):
      vector_db_path = get_file_path("data/db_faiss")
      # Embeding
      model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf"
      gpt4all_kwargs = {'allow_download': 'True'}
      embedding_model = GPT4AllEmbeddings(
        model_name=model_name,
        gpt4all_kwargs=gpt4all_kwargs
      )
      # embedding_model = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf", {'allow_download': 'True'})
      db = FAISS.load_local(vector_db_path, embedding_model,  allow_dangerous_deserialization=True)
      return db

    def create_retrieval_tool(self):
        # Bat dau thu nghiem
        db = self.read_vectors_db()
        retriever = db.as_retriever(search_kwargs = {"k": 5}, max_tokens_limit=4096)
        # Retrieval tool
        tool = create_retriever_tool(
            retriever,
            "Resvu-Company-Document-Retriever",
            "Useful for retrieving specific information, person from a collection of documents related to Resvu company",
        )
        return tool

    def create_agent(self):
        # prompt = hub.pull("hwchase17/openai-tools-agent")
        template = ChatPromptTemplate.from_messages([
            ("system", "You are a helpful assistant at Resvu System."),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder("agent_scratchpad"),
        ])

        agent = create_tool_calling_agent(self.llm, self.tools, template)
        # Create an agent executor by passing in the agent and tools
        agent_executor = AgentExecutor(agent=agent, tools=self.tools, verbose=True)

        agent_with_chat_history = RunnableWithMessageHistory(
            agent_executor,
            self.get_session_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
                
        return agent_with_chat_history

    def chat(self, user_input):
        try:
            # response = self.agent.run(user_input)
            response = self.agent.invoke(
               {
                   "input": user_input
               },
                config={"configurable": {"session_id": self.session_id}},
            )
            print("response")
            print(response)

            return response
        except Exception as e:
            print(e)
            print(f"Agent encountered an error: {str(e)}")
            return self.fallback_response(user_input)

    def fallback_response(self, user_input):
        # Direct LLM call as a fallback
        # prompt = f"As an AI assistant for Resvu company, please respond to this user query: {user_input}"
        # return self.llm(prompt)
        return "I'm sorry, I'm unable to handle your request at the moment. Please try again later."

    def print_conversation_history(self):
        print(f"Conversation history for user {self.user_id}:")
        for i, message in enumerate(self.memory.chat_memory.messages):
            if message.type == 'human':
                print(f"Human: {message.content}")
            elif message.type == 'ai':
                print(f"AI: {message.content}")
            print("-" * 40)
    def reset_memory(self):
        self.memory.clear()
        print(f"Conversation memory for user {self.user_id} has been reset.")

class SessionManager:
    def __init__(self, llm):
        self.sessions = {}
        self.llm = llm

    def get_or_create_session(self, session_id):
        if session_id not in self.sessions:
            # get data from session
            ini_message = get_BaseMessage_by_session_id(session_id)
            self.sessions[session_id] = UserSession(session_id, self.llm, ini_message)
        return self.sessions[session_id]

    def chat(self, session_id, user_input):
        session = self.get_or_create_session(session_id)
        return session.chat(user_input)