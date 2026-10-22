from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
from langgraph.graph import StateGraph , START , END 
from langgraph.types import interrupt , Command
from pydantic import BaseModel 
from langgraph.checkpoint.memory import InMemorySaver
from typing import Literal

load_dotenv()

llm = ChatGroq(model="openai/gpt-oss-120b")

class EmailState(BaseModel):
    query : str = ""
    draft : str = ""
    human_feedback : str = ""
    final_answer : str = ""

def draft_mail_node(state: EmailState) -> EmailState:
    if state.human_feedback:
        draft = llm.invoke(f""" 
                Rewrite this Email for {state.query}
                you generated this email :{state.draft}
                Human Feedback to apply : {state.human_feedback}
        """).content
    else:
        draft = llm.invoke(state.query).content

    state.draft = draft
    return state

def approval_node(state: EmailState) -> EmailState:
    feedback = interrupt({
        "human_feedback" : state.draft,
        "question" : "Do you want to continue or re-write the email"
    })
    fb = (feedback or "").strip().lower()
    if fb in ("Approved", "ok" , "Yes"):
        state.human_feedback = ""
        return state
    else:
        state.human_feedback = feedback
        return state


def final_answer_node(state:EmailState) -> EmailState:
    if state.human_feedback:
        state.human_feedback = state.human_feedback
        return state
    else:
        print("Email Sent Sucessfully...")
    state.final_answer = "Email Sent Sucessfully..."
    return state

def conditional_node(state: EmailState) -> Literal["final" , "email"]:
    if state.human_feedback:
        return "email"
    else:
        return "final"


graph_builder = StateGraph(EmailState)

graph_builder.add_node("email", draft_mail_node)
graph_builder.add_node("approval", approval_node)
graph_builder.add_node("final", final_answer_node)

graph_builder.add_edge(START, "email")
graph_builder.add_edge("email", "approval")
graph_builder.add_conditional_edges("approval", conditional_node)
graph_builder.add_edge("final", END)

graph = graph_builder.compile(checkpointer=InMemorySaver())

# pyrefly: ignore [missing-import]
from IPython.display import Image
Image(graph.get_graph().draw_mermaid_png())

config = {"configurable":{"thread_id":"1"}}

res = graph.invoke({"query": "Write an email to my manager requesting a leave for 2 days"}, config)

print(res["draft"])

res = graph.invoke(Command(resume="I want to make the email more professional and dates are sep 25 and 26 and reason is Marriage "), config=config)
print(res["draft"])

res = graph.invoke(Command(resume="Yes"), config=config)

print(res["draft"])