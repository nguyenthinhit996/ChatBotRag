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

def startLLMInitial(link: str):
    if link is not None:
        # Initialize the session manager
        mistral_llm = Ollama(base_url=link, model="mistral")
        session_manager = SessionManager(mistral_llm)
        return session_manager

class UserSession:
    def __init__(self, user_id, local_llm):
        self.user_id = user_id
        self.llm = local_llm
        self.memory = ConversationBufferWindowMemory(k=5, memory_key="chat_history", return_messages=True)
        self.retrieval_tool = self.create_retrieval_tool()
        self.tools = [self.retrieval_tool]
        self.agent = self.create_agent()

    def read_vectors_db(self):
      vector_db_path = "/Volumes/data/peter/project/ChatBotRag/chatbot-backend/data/db_faiss"
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
        retriever = db.as_retriever(search_kwargs = {"k": 10}, max_tokens_limit=4096)
        # Retrieval tool
        tool = create_retriever_tool(
            retriever,
            "Resvu Company Document Retriever",
            "Useful for retrieving specific information, person from a collection of documents related to Resvu company",
        )
        return tool

    def create_agent(self):
        agent = initialize_agent(
            tools=[self.retrieval_tool],
            llm=self.llm,
            agent=AgentType.CONVERSATIONAL_REACT_DESCRIPTION,
            verbose=True,
            memory=self.memory,
            handle_parsing_errors=False,
            max_iterations=3,
            early_stopping_method="generate"
        )
        return agent

    def chat(self, user_input):
        try:
            response = self.agent.run(user_input)
            return response
        except Exception as e:
            print(f"Agent encountered an error: {str(e)}")
            return self.fallback_response(user_input)

    def fallback_response(self, user_input):
        # Direct LLM call as a fallback
        prompt = f"As an AI assistant for Resvu company, please respond to this user query: {user_input}"
        return self.llm(prompt)

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

    def get_or_create_session(self, user_id):
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession(user_id, self.llm)
        return self.sessions[user_id]

    def chat(self, user_id, user_input):
        session = self.get_or_create_session(user_id)
        return session.chat(user_input)