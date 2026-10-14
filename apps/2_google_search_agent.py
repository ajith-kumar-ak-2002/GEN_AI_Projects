from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
# pyrefly: ignore [missing-import]
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.agents import create_agent
from langgraph.checkpoint.memory import InMemorySaver

load_dotenv()

llm = ChatGroq(model= "openai/gpt-oss-120b")
search = GoogleSerperAPIWrapper()
memory = InMemorySaver()

agent = create_agent(
    model = llm,
    tools = [search.run],
    checkpointer = memory,
    system_prompt ="You are a Google Search Agent, Any Question User Ask Use Google Search Tool and give Answer."
)

while True:
    query = input("Ask Anything: ")
    if query.lower() in ("bye", "exit", "quit"):
        print("Good Bye! 👋")
        break

    response = agent.invoke({"messages": [{"role": "user","content": query}]}, {"configurable": {"thread_id": "1"}})
    print(response["messages"][-1].content)