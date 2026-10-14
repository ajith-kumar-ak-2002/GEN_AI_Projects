from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

res = llm.invoke("What is Python?")

print(res.content)

