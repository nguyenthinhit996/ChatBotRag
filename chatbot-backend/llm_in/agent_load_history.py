

from langchain.agents import Tool, initialize_agent, AgentType, tool, create_json_chat_agent
from langchain.tools.retriever import create_retriever_tool
from langchain.memory import ConversationBufferWindowMemory
from langchain.agents.agent import AgentExecutor
from langchain.schema import AgentAction, AgentFinish
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS

from dotenv import load_dotenv
import os

from langchain.memory import SQLChatMessageHistory
from sqlalchemy import create_engine, Table, Column, Integer, String, Text, ForeignKey, MetaData, TIMESTAMP
from sqlalchemy.orm import sessionmaker
# from langchain.storage import SQLAlchemyStore
from langchain.agents import AgentExecutor, create_react_agent

load_dotenv()  # Load environment variables from .env file

# Access environment variables
SUPABASE_CONNECT = os.getenv("SUPABASE_CONNECT")

# Supabase PostgreSQL connection string
db_url = SUPABASE_CONNECT

# Create SQLAlchemy engine
# engine = create_engine(db_url)
# Create the SQLAlchemy engine with client encoding set
engine = create_engine(db_url)


# Define your database schema
metadata = MetaData()

users = Table('users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('username', String(50), unique=True),
    Column('created_at', TIMESTAMP)
)

sessions = Table('sessions', metadata,
    Column('id', Integer, primary_key=True),
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('session_start', TIMESTAMP),
    Column('session_end', TIMESTAMP),
    Column('title', Text)
)

messages = Table('messages', metadata,
    Column('id', Integer, primary_key=True),
    Column('session_id', Integer, ForeignKey('sessions.id')),
    Column('sender_role', Text),
    Column('message_text', Text),
    Column('message_timestamp', Text),
    Column('created_at', TIMESTAMP)
)

# Create tables if they don't exist
metadata.create_all(engine)

# Create a session factory
Session = sessionmaker(bind=engine)

# Custom SQLChatMessageHistory class to work with your schema
class CustomSQLChatMessageHistory(SQLChatMessageHistory):
    def __init__(self, session_id, connection_string):
        super().__init__(session_id=session_id, connection_string=connection_string)

    def add_message(self, message):
        with Session() as session:
            new_message = messages.insert().values(
                session_id=self.session_id,
                sender_role='human' if message.type == 'human' else 'ai',
                message_text=message.content,
                message_timestamp=datetime.now().isoformat(),
                created_at=datetime.now()
            )
            session.execute(new_message)
            session.commit()

    def clear(self):
        with Session() as session:
            delete_query = messages.delete().where(messages.c.session_id == self.session_id)
            session.execute(delete_query)
            session.commit()

    @property
    def messages(self):
        with Session() as session:
            query = messages.select().where(messages.c.session_id == self.session_id).order_by(messages.c.id)
            result = session.execute(query)
            return [self._create_message(row.sender_role, row.message_text) for row in result]

# Function to create a new user
def create_user(username):
    with Session() as session:
        new_user = users.insert().values(
            username=username,
            created_at=datetime.now()
        )
        result = session.execute(new_user)
        session.commit()
        return result.inserted_primary_key[0]

# Function to create a new session
def create_session(user_id, title):
    with Session() as session:
        new_session = sessions.insert().values(
            user_id=user_id,
            session_start=datetime.now(),
            title=title
        )
        result = session.execute(new_session)
        session.commit()
        return result.inserted_primary_key[0]

# Create a CustomSQLChatMessageHistory instance
def get_message_history(session_id):
    return CustomSQLChatMessageHistory(
        session_id=session_id,
        connection_string=db_url
    )

# Create a SQLAlchemyStore instance for the agent's state
# state_store = SQLAlchemyStore(engine=engine, table_name="agent_states")

# Function to create an agent executor
def create_agent_executor(session_id, llm, tools):
    message_history = get_message_history(session_id)
    return AgentExecutor.from_agent_and_tools(
        agent=create_react_agent(llm, tools),
        tools=tools,
        memory=message_history,
        verbose=True
    )

def function():
    vector_db_path = "/home/peter/Desktop/project/AI/ChatBotRag/chatbot-backend/data/db_faiss"
    # vector_db_path = "../data/db_faiss"

      
    # Embeding
    model_name = "all-MiniLM-L6-v2.gguf2.f16.gguf"
    gpt4all_kwargs = {'allow_download': 'True'}
    embedding_model = GPT4AllEmbeddings(
            model_name=model_name,
            gpt4all_kwargs=gpt4all_kwargs
    )
    # embedding_model = GPT4AllEmbeddings(model_name="all-MiniLM-L6-v2.gguf2.f16.gguf", {'allow_download': 'True'})
    db = FAISS.load_local(vector_db_path, embedding_model,  allow_dangerous_deserialization=True)
    
    retriever = db.as_retriever(search_kwargs = {"k": 2}, max_tokens_limit=4096)
    # Retrieval tool
    tool = create_retriever_tool(
        retriever,
        "Resvu-Company-Document-Retriever",
        "Useful for retrieving specific information, person from a collection of documents related to Resvu company",
    )
    return tool
tool = function()

tools = [tool]

llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
user_id = create_user("example_user")
session_id = create_session(user_id, "Chat about AI")

# agent_executor = create_agent_executor(session_id, llm, tools)

# query = "who is Thinh"

# for s in agent_executor.stream(
#     {"messages": [HumanMessage(content=query)]},
# ):
#     print(s)
#     print("----")

# Example usage:
# user_id = create_user("example_user")
# session_id = create_session(user_id, "Chat about AI")
# agent_executor = create_agent_executor(session_id, llm, tools)

# To save agent state:
# state_store.store(str(session_id), agent_executor.agent.state)

# To load a previous session:
# message_history = get_message_history(previous_session_id)
# loaded_state = state_store.load(str(previous_session_id))
# recovered_agent_executor = create_agent_executor(previous_session_id, llm, tools)
# recovered_agent_executor.agent.state = loaded_state