from langgraph.graph import StateGraph , START , END 
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Interrupt , Command
from typing import Literal

from state import BlogState
from agents import get_llm , reseach_agent , writter_agent , editor_agent

MAX_REVISION  = 3

### Research Node
def researcher_node(state:BlogState):
    """Researcher agent generates or revises the researech outline"""
    llm = get_llm()
    research_data = reseach_agent(
        llm = llm,
        topic = state.topic,
        audience= state.audience,
        feedback = state.research_feedback
    )
    state.research = research_data

    return state

def human_review_research_node(state: BlogState):
    """Pause and ask the human to approve the research or send the feedback"""
    decision = Interrupt({
        "stage": "research_reviw",
        "research": state.research,
        "instruction":(
            "Replay with 'approve' to continue the writing"
            "or describe what to change to send it back to the researcher"
        )
    })
    if isinstance(decision, dict):
        action = decision.get("action", "approve")
        feedback = decision.get("feedback", "")
    else:
        text = str(decision)
        action = "approve" if text.lower() in ["approve", "approved", "ok", "yes", "process", ""] else "revise"
        feedback = "" if action == "approve" else text
    
    state.research_feedback = feedback
    return state
    


### writter Node
def writter_node(state:BlogState):
    """Writter agent produce the fill draft blog(or revise it)"""
    llm = get_llm()
    draft_data = writter_agent(
        llm = llm,
        topic = state.topic,
        audience= state.audience,
        feedback = state.draft_feedback
    )
    state.draft = draft_data
    state.feedback = state.draft_feedback

    return state

def human_review_writter_node(state:BlogState):
    """pause and ask the human to approve the draft or send the feedback to the writter"""
    decision = Interrupt({
        "state": "draft_review",
        "draft": state.draft,
        "instruction":(
            "Replay with 'approve' to continue to sent to the editor"
            "or describe what to change to send it back to the writter"
        )
    })
    if isinstance(decision, dict):
        action = decision.get("action", "approve")
        feedback = decision.get("feedback", "")
    else:
        text = str(decision)
        action = "approve" if text.lower() in ["approve", "approved", "ok", "yes", "process", ""] else "revise"
        feedback = "" if action == "approve" else text
    state.draft_feedback = feedback
    return state

### Editor Node
def editor_node(state:BlogState):
    llm = get_llm()
    final = editor_agent(
        llm = llm ,
        topic = state.topic,
        draft = state.draft

    )
    state.final_blog = final
    return state



#### Conditional Nodes

def route_after_research_review(state: BlogState) -> Literal["researcher", "writter"]:
    if state.research_feedback:
        return "researcher"
    else:
        return "writter"

def route_after_draft_review(state: BlogState) -> Literal["editor", "writter"]:
    if state.draft_feedback and state.revision_count < MAX_REVISION:
        return "writter"
    else:
        return "editor"



### Build and complie the Nodes
def build_blog_graph(BlogState):
    builder = StateGraph(BlogState)

    # Add your nodes
    builder.add_node("researcher", researcher_node)
    builder.add_node("review_research", human_review_research_node)
    builder.add_node("writter", writter_node)
    builder.add_node("draft_review", human_review_writter_node)
    builder.add_node("editor", editor_node)

    # Add your edges
    builder.add_edge(START, "researcher")
    builder.add_edge("researcher", "review_research")

    builder.add_conditional_edges(
        "review_research",
        route_after_research_review,
        {
            "researcher": "researcher",
            "writter": "writter",
        },
    )

    builder.add_edge("writter", "draft_review")

    builder.add_conditional_edges(
        "draft_review",
        route_after_draft_review,
        {
            "writter": "writter",
            "editor": "editor",
        },
    )

    builder.add_edge("editor", END)

    # IMPORTANT: Keep these lines inside the function
    graph = builder.compile(checkpointer=InMemorySaver())
    return graph

