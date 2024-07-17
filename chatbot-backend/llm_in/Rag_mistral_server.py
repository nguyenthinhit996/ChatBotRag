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
from langchain_mistralai import ChatMistralAI
from langgraph.prebuilt import create_react_agent
from langchain_core.messages import AIMessage, HumanMessage
from dotenv import load_dotenv

import os
os.environ["CUDA_VISIBLE_DEVICES"] = ""


load_dotenv() 

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
    
    retriever = db.as_retriever(search_kwargs = {"k": 5}, max_tokens_limit=4096)
    # Retrieval tool
    tool = create_retriever_tool(
        retriever,
        "Resvu-Company-Document-Retriever",
        "Useful for retrieving specific information, person from a collection of documents related to Resvu company",
    )
    return tool
tool = function()

awnser = tool.invoke("Resvu")
print("awnser")
print(awnser)

# tools = [tool]

# mistral_llm_server = ChatMistralAI(model="mistral-large-latest")
# agent_executor = create_react_agent(mistral_llm_server, tools)

# query = "tell me more about Resvu?"

# for s in agent_executor.stream(
#     {"messages": [HumanMessage(content=query)]},
# ):
#     print(s)
#     print("----")