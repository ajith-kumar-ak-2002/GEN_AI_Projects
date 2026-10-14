from pydantic import BaseModel
from langgraph.graph import StateGraph , START , END

class GreetState(BaseModel):
    message : str = ""

graph = StateGraph(GreetState)


## Nodes -- Python Functions

def Greet(state:GreetState):
    state.message = f"{state.message} All good !"
    return state

def UpperCase(state:GreetState):
    state.message = state.message.upper()
    return state

graph.add_node("greet", Greet)
graph.add_node("upper_case" , UpperCase)

graph.add_edge(START, "greet")
graph.add_edge("greet", "upper_case")
graph.add_edge("upper_case", END)

final_graph = graph.compile()

res = final_graph.invoke({"message" : "Hello"})
print(res)


# pyrefly: ignore [missing-import]
from IPython.display import Image
Image(final_graph.get_graph().draw_mermaid_png())