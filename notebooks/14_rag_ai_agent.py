from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_core.vectorstores import InMemoryVectorStore
from langchain.tools import tool
from langchain.agents import create_agent

load_dotenv()

## 1 - PDF Loader 
loader = PyPDFLoader("../data/medical_report.pdf")
doc_load = loader.load()

## 2 - Chunk the Data
splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=200)
split_data = splitter.split_documents(doc_load)

## 3 - Embedding
embedding = GoogleGenerativeAIEmbeddings(model="gemini-embedding-2")

## 4 - Vector_store
vector_store = InMemoryVectorStore.from_documents(
    documents= split_data,
    embedding= embedding
)

## tool | llm | prompt

@tool 
def get_info(query=str):
    """
        This tool can help you to retrieve the relevant data of the PDF Documents, and these pdf
        documents have details about medical reports.
    """
    print("Called Tool: ", query)
    res = vector_store.similarity_search(query=query, k=4)
    context = ""
    for doc in res:
        context = doc.page_content

    return context

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

prompt = """
    You are a helpful assistant that answers questions using retrieved context.
	ALWAYS use the `retriever_tool` tool for questions requiring external knowledge.
"""

agent = create_agent(
    model = llm,
    tools = [get_info],
    system_prompt= prompt
)

query = "Patient Name"
response = agent.invoke({"messages":[{"role": "user", "content": query}]})

result = response["messages"][-1].content
print(result)

