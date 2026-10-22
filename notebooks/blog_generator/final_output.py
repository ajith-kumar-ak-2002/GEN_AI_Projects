from dotenv import load_dotenv

from state import BlogState
from agents import get_llm , reseach_agent , writter_agent , editor_agent 

load_dotenv()
import os
os.getenv("GROQ_API_KEY")


# llm = get_llm()

# outline = reseach_agent(
#     llm = llm,
#     topic = "What is LLM?",
#     audience= "Beginners"
# )

# print(outline)

from graphs import build_blog_graph
from langgraph.types import Command

graph = build_blog_graph(BlogState)


# from IPython.display import Image
# Image(graph.get_graph().draw_mermaid_png())


config = {"configurable": {"thread_id": "123"}}

state = graph.invoke({
    "topic" : "What is LLM?",
    "audience" : "Ai and Agentic Ai Developers"
}, config = config
)

snap = graph.get_state(config)


#### Stage 1 Research Blog
interrupt_payload = snap.Interrupts[0].value
print("stage: ", interrupt_payload.get("stage"))
print("\n ----------------- Research outline for your Review ------------------ \n")
print("Research: " , interrupt_payload.get("research"))
print("instruction: ", interrupt_payload.get("instruction"))

#### Stage 2 Draft Blog 
state = graph.invoke(Command(resume={"action": "approve", "feedback": ""}), config = config)

snap = graph.get_state(config)
interrupt_payload = snap.Interrupts[0].value
print("\n ----------------- Draft blog for your Review ------------------ \n")
print("Draft: " , interrupt_payload.get("draft"))
print("instruction: ", interrupt_payload.get("instruction"))


### Approve the Darft Blog
state = graph.invoke(Command(resume={"action": "approve", "feedback": ""}), config = config)

print("------------- Final Published Blog -------------------- \n")
print(state["final_blog"])