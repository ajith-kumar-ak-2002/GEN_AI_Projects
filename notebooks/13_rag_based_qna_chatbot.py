from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma 
from langchain_core.prompts import PromptTemplate

load_dotenv()

## 1 - Load Documents
loader = PyPDFLoader("../data/medical_report.pdf")
docs = loader.load()

## 2 - Chunk the Dataset
splitter = RecursiveCharacterTextSplitter(chunk_size = 1000, chunk_overlap=100)
chunk_data = splitter.split_documents(docs)

## 3 - Create Embedding 
embedding = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-2")

## 4 - Store Chunk_Data in Vector Store (Chorma)
vector_store = Chroma.from_documents(
    documents = chunk_data,
    embedding = embedding
)

query = "RBC"
res = vector_store.similarity_search(query = query)

context = ""
for doc in res:
    context += doc.page_content + "\n"

llm = ChatGoogleGenerativeAI(model="gemini-3.8-flash")

## chain -- contect_generator | Prompt | llm

def get_context(query=str):
    res = vector_store.similarity_search(query = query)
    context = ""
    for doc in res:
        context += doc.page_content + "\n"

    return {
        "context": context,
        "question": query
    }

prompt = PromptTemplate.from_template("""
        You are a helpful assistant and provide answerd based on the context for user question. and 
    if you don't know the answer, then you can say that 'I dont know.'

    context : {context},
    question :{question}
""")

rag_chain = get_context | prompt | llm

res = rag_chain.invoke("What is the value of RBC Count and is it in range ?")
print(res.text)
