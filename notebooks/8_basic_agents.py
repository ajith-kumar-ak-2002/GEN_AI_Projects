from dotenv import load_dotenv
from langchain_core.tools import tool

load_dotenv()

@tool
def add_numbers(a:int, b:int):
    """
        its will return sum of the 2 numbers 

    agrs:
        a is one number
        b is two number
    """
    return a + b

add_numbers.invoke({"a": 13, "b": 10})

@tool 
def multiple_numbers(a: int , b: int):
    """
        This will multiple the two Numbers

    agrs:
        a is one number
        b is two number
    """
    return a * b

multiple_numbers.invoke({"a": 15,"b": 12})


from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import create_agent

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

agent = create_agent(
    model = llm,
    tools = [add_numbers, multiple_numbers],
    system_prompt = "You a Math Teacher, Always use tool for the calculation."
)

response = agent.invoke({"messages":[{"role": "user", "content": "What is 14 * 10"}]})

for chunk in response ["messages"]:
    print(chunk)

print(response["messages"][-1].content[0]["text"])
