from dotenv import load_dotenv

# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader 
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq

from pydantic import BaseModel , Field
from langgraph.graph import StateGraph , START , END

load_dotenv()

## PDF Loader
loader = PyPDFLoader("../data/MBA_project.pdf")
doc_load = loader.load()

## Chunk the PDF 
splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap = 200)
chunks = splitter.split_documents(doc_load)

## Embedding and Vector Store
embed = GoogleGenerativeAIEmbeddings(model= "gemini-embedding-2")

vector_store = InMemoryVectorStore.from_documents(
    documents = chunks,
    embedding= embed
)

## Lang_Graph
class RagState(BaseModel):
    question : str = Field(description="user question")
    documents : list = []
    context : str = Field(description="Context Data for user question", default="")
    answer : str = Field(description="Final Answer...", default="")

llm = ChatGroq(model="openai/gpt-oss-120b")

## question -> retrive -> context -> generate_answer -> END

def retrive_node(state:RagState) -> RagState:
    doc = vector_store.similarity_search(state.question)
    state.documents = doc
    return state

def context_node(state: RagState) -> RagState:
    context = ""
    for doc in state.documents:
        context += doc.page_content
    state.context = context + "\n\n"
    return state

def generate_node(state: RagState) -> RagState:
    prompt = f"""You are a assistant and provide the answer for user question based on the provided context.
        If you don't find the relevant answer, then just say 'I dont know.'.
        question : {state.question},
        context : {state.context}
        """
    res = llm.invoke(prompt)
    state.answer = res.content 
    return state

## Graph
graph = StateGraph(RagState)

graph.add_node("retrive", retrive_node)
graph.add_node("context", context_node)
graph.add_node("generate_answer", generate_node)

## Edges
graph.add_edge(START, "retrive")
graph.add_edge("retrive", "context")
graph.add_edge("context", "generate_answer")
graph.add_edge("generate_answer", END)

final_graph = graph.compile()

# pyrefly: ignore [missing-import]
from IPython.display import Image
Image(final_graph.get_graph().draw_mermaid_png())

resposne = final_graph.invoke({"question": "Title of the Project"})
print(resposne["answer"])

