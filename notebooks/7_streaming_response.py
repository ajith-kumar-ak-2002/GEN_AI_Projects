from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", streaming = True)

question = "What is GENAI?"

res = llm.stream(question)

for chunk in res:
    print(chunk.content, "\n")


# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq

llm = ChatGroq(model="openai/gpt-oss-120b", streaming = True)

q = "How many Libraries in Python?"

res = llm.stream(q)

for chunk in res:
    print(chunk.content, end = "")


