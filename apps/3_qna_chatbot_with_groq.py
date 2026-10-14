from langchain_core.messages import message_chunk_to_message
from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import MemorySaver
import streamlit as st 

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b", streaming = True)
search = GoogleSerperAPIWrapper()
tools = [search.run]

if "memory" not in st.session_state:
    st.session_state.memory = MemorySaver()
if "history" not in st.session_state:
    st.session_state.history = []

agent = create_agent(
    model = llm,
    tools= tools,
    checkpointer= st.session_state.memory,
    system_prompt= "you are a helpful assistant, answer user questions accurately, use search tool when required"
)

### web Interface
st.title("⚡ Fast • Smart • Reliable Answers")
st.subheader("Powered by Groq + LangChain + Google Search")

query = st.chat_input("Ask anything, i am here to Help you..... ")

for message in st.session_state.history:
    role = message["role"]
    content = message["content"]
    st.chat_message(role).markdown(content)

if query:
    st.chat_message("user").markdown(query)
    st.session_state.history.append({"role":"user", "content": query})

    response = agent.stream({"messages":[{"role":"user", "content": query}]}, {"configurable": {"thread_id": "1"}}, stream_mode="messages")

    ai_container = st.chat_message("ai")
    with ai_container:
        space = st.empty()
        message = ""

        for chunk in response:
            message = message + chunk[0].content
            space.write(message)

    st.session_state.history.append({"role":"ai", "content":message})