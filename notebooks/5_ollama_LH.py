import os

from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_ollama import ChatOllama

load_dotenv()

llm = ChatOllama(model="gemma:latest")

response = llm.invoke("Hello")

print(response.content)

