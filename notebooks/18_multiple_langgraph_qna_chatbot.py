from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph , START , END
from pydantic import BaseModel , Field
from typing import Literal

## Libs for agent
from langchain.agents import create_agent
# pyrefly: ignore [missing-import]
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain.tools import tool
import os
import requests

load_dotenv()

class FlowState(BaseModel):
    question: str = Field(description="User Question")

    category: Literal["coding", "google_search", "weather"] = Field(
        default="google_search",
        description="Category of the question"
    )

    answer: str = ""

class QuestionCategory(BaseModel):
    category: Literal["coding" , "google_search", "weather"] = Field(description="Category of the question")

llm = ChatGroq(model="openai/gpt-oss-120b")

## create Google Search agent
search = GoogleSerperAPIWrapper()
tools = [search.run]

google_agent = create_agent(
    model = llm,
    tools = tools,
    system_prompt= "You are a Google Search Agent, Any Question User Ask Use Google Search Tool and give Answer."
)

## create weather agent
@tool
def get_weather(city:str):
    """Get Weather Information for a City"""
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": os.getenv("OPENWEATHER_API_KEY"),
        "units": "metric"
    }

    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code != 200:
        return data.get("message", "Weather unavailable")

    return (
        f"City: {data['name']}\n"
        f"Temperature: {data['main']['temp']}°C\n"
        f"Weather: {data['weather'][0]['description']}\n"
        f"Humidity: {data['main']['humidity']}%"
    )

weather_agent = create_agent(
    model = llm,
    tools=[get_weather],
    system_prompt= "You are a weather expert, extract weather"
)

def check_question_category(state: FlowState) -> FlowState:
    prompt = f"""
    Classify the user's question into exactly one category.

    Categories:
    - coding: Python, programming, debugging, algorithms,
      software development, simple arithmetic or math.
    - google_search: General knowledge, company addresses,
      current events, and information requiring web search.
    - weather: Weather, temperature, humidity, and forecasts.
    User question: {state.question}
    """

    result = llm.invoke(prompt)

    category = result.content.strip().lower()

    # Validate the model's response
    if category not in ["coding", "google_search", "weather"]:
        raise ValueError(f"Invalid category returned by LLM: {category}")

    print("Detected category:", category)

    return state.model_copy(update={"category": category})

def route(state: FlowState) -> Literal["coding" , "google_search", "weather"]:
    return state.category

def coding_node(state: FlowState) -> FlowState:
    res = llm.invoke(f"You are a coding expert: {state.question}")
    state.answer = res.content
    return state

def google_search_node(state: FlowState) -> FlowState:
    res = google_agent.invoke({"messages":[{"role": "user", "content": state.question}]})
    state.answer = res["messages"][-1].content
    return state

def weather_node(state:FlowState) -> FlowState:
    res = weather_agent.invoke({"messages":[{"role":"user", "content": state.question}]})
    state.answer = res["messages"][-1].content
    return state

graph = StateGraph(FlowState)

graph.add_node("question_category", check_question_category)
graph.add_node("coding", coding_node)
graph.add_node("google_search", google_search_node)
graph.add_node("weather", weather_node)

graph.add_edge(START , "question_category")
graph.add_conditional_edges("question_category", route)
graph.add_edge("coding", END)
graph.add_edge("google_search", END)
graph.add_edge("weather", END)

graph = graph.compile()

response = graph.invoke({
    "question": "write a simple python code"
})

print(response["answer"])