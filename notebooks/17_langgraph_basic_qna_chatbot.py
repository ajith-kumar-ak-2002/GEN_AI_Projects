from dotenv import load_dotenv
from pydantic import BaseModel
from langgraph.graph import StateGraph , START , END 
from langgraph.graph.message import add_messages
from typing import Annotated
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

class ChatState(BaseModel):
    messages : Annotated[list , add_messages]

llm = ChatGroq(model ="openai/gpt-oss-120b")

def ChatBotNode(state : ChatState) -> ChatState:
    res = llm.invoke(state.messages)
    state.messages = [res]
    return state

memory = InMemorySaver()

graph = StateGraph(ChatState)
graph.add_node("bot" , ChatBotNode)

graph.add_edge(START , "bot")
graph.add_edge("bot", END)

graph = graph.compile(checkpointer= memory)

response = graph.invoke({"messages": [{"role": "user", "content": "What is his Age?"}]},
         {"configurable": {  "thread_id" : "1"}})

result = response["messages"][-1].content

print(f"Response: {result}")