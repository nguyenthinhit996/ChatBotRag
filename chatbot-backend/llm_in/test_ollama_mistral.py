# Import Ollama module from Langchain
from langchain_community.llms import Ollama

# Initialize an instance of the Ollama model

llm = Ollama(base_url="https://306b-34-16-161-126.ngrok-free.app/", model="mistral")

# Invoke the model to generate responses
response = llm.invoke("Tell me a joke")

print(response)