# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_google_genai import ChatGoogleGenerativeAI
# pyrefly: ignore [missing-import]
import streamlit as st 

load_dotenv()

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

st.title("AskBuddy - AI QnA Bot")

st.markdown("An Intelligent QnA Chatbot Build With Langchain, Gemini and Streamlit 🚀🧠")

query = st.chat_input("Ask anything?")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role = message["role"]
    content = message["content"]
    st.chat_message("role").markdown(content)

if query:
    st.chat_message("user").markdown(query)
    st.session_state.messages.append({"role": "user", "content": query})

    response = llm.invoke(query)

    st.chat_message("AI").markdown(response.content[0]["text"])
    st.session_state.messages.append({"role": "AI", "content": response.content[0]["text"]})

