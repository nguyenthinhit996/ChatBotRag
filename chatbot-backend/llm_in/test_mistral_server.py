
from langchain_mistralai import ChatMistralAI

model = ChatMistralAI(model="mistral-large-latest")

# Initialize the session manager
mistral_llm_server = ChatMistralAI(model="open-mistral-7b")

from langchain_core.messages import HumanMessage

model.invoke([HumanMessage(content="Hi! Tell me a joke")])