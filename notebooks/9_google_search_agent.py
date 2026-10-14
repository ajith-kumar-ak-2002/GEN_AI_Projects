from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_community.utilities import GoogleSerperAPIWrapper
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver  


load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")
search = GoogleSerperAPIWrapper()
memory = InMemorySaver

agent = create_agent(
    model = llm,
    tools = [search.run],
    checkpointer= InMemorySaver(),
    system_prompt = "You are a helpful assistant who can answer questions about the real world."

)

question = "what is his father name?"
response = agent.invoke({"messages":[{"role":"user", "content": question}]}, {"configurable": {"thread_id": "1"}})

for res in response["messages"]:
    print(res)


print(response["messages"][-1].content)