# from langchain.agents import Tool, initialize_agent, AgentType, tool, create_json_chat_agent
from langchain.tools.retriever import create_retriever_tool
# from langchain.memory import ConversationBufferWindowMemory
# from langchain.agents.agent import AgentExecutor
# from langchain.schema import AgentAction, AgentFinish
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import FAISS

# from langchain_community.llms import Ollama
# from langchain.callbacks import StreamingStdOutCallbackHandler
# from langchain.tools import Tool
# from pydantic import BaseModel, Field
# from langchain.tools import StructuredTool
# from langchain import hub
# from langchain_mistralai import ChatMistralAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI

# from langgraph.checkpoint.sqlite import SqliteSaver

from typing import Literal
from langchain_core.runnables import ConfigurableField
from langchain_core.tools import tool
# from langchain_openai import ChatOpenAI
# from langgraph.prebuilt import create_react_agent


from psycopg_pool import ConnectionPool

import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""


load_dotenv() 

SUPABASE_CONNECT = os.getenv("SUPABASE_CONNECT")

# Supabase PostgreSQL connection string
db_url = SUPABASE_CONNECT



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
retriever_tool = function()


@tool
def get_weather(city: Literal["nyc", "sf"]):
    """Use this to get weather information."""
    if city == "nyc":
        return "It might be cloudy in nyc"
    elif city == "sf":
        return "It's always sunny in sf"
    else:
        raise AssertionError("Unknown city")


tools = [retriever_tool, get_weather]

pool = ConnectionPool(
    # Example configuration
    conninfo=db_url,
    max_size=20,
)

checkpointer = PostgresSaver(sync_connection=pool)
checkpointer.create_tables(pool)

# llm = ChatOpenAI(model="gpt-3.5-turbo-0125")
# agent_executor = create_react_agent(llm, tools)

# graph = create_react_agent(llm, tools=tools, checkpointer=checkpointer)
# config = {"configurable": {"thread_id": "1"}}
# res = graph.invoke({"messages": [("human", "what's the weather in sf")]}, config)

# query = "who is Thinh"

# for s in agent_executor.stream(
#     {"messages": [HumanMessage(content=query)]},
# ):
#     print(s)
#     print("----")