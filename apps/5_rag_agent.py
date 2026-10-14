from dotenv import load_dotenv
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader , PyPDFDirectoryLoader
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter
# pyrefly: ignore [missing-import]
from langchain_huggingface import HuggingFaceEmbeddings
# pyrefly: ignore [missing-import]
from langchain_community.vectorstores import InMemoryVectorStore
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
from langchain.agents import create_agent
from langchain_core.tools import tool
from langgraph.checkpoint.memory import InMemorySaver
import streamlit as st 

load_dotenv()

## Data in st session
if "document_uploaded" not in st.session_state:
    st.session_state.document_uploaded = False

if "agent" not in st.session_state:
    st.session_state.agent = None

if "vector_store" not in st.session_state:
    st.session_state.vector_store = None

if "messages" not in st.session_state:
    st.session_state.messages = []

def process_document(path):
    ## 1 - PDF Document Load
    loader = PyPDFDirectoryLoader(path)
    doc_load = loader.load()

    ## 2 - Chunk the PDF Document
    chunk_data = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
    doc_chunk = chunk_data.split_documents(doc_load)

    ## 3 - Embedding Model
    embedding = HuggingFaceEmbeddings(model="sentence-transformers/all-MiniLM-L6-v2")

    ## 4 Vector store 
    vector_store = InMemoryVectorStore.from_documents(
        documents = doc_chunk,
        embedding = embedding
    )

    ### Create agent = llm | tools | prompt | memory

    llm = ChatGroq(model ="openai/gpt-oss-120b")

    @tool
    def get_context(query:str):
        """Retrieve documents relevant to a query from the knowledge base."""

        context = ""
        response = vector_store.similarity_search(query = query, k=4)

        for doc in response:
            context = doc.page_content + "\n\n"

        return context 

    prompt = """
            You are a helpful assistant that answers questions using retrieved context. 
            My knowledge base consists of the details from the uploaded document. 
            ALWAYS use the `retrieve_context` tool for questions requiring external knowledge.
        """

    memory = InMemorySaver()

    agent = create_agent(
        model = llm,
        tools = [get_context],
        checkpointer= memory,
        system_prompt= prompt
    )

    st.session_state.agent = agent
    st.session_state.document_uploaded = True


## Upload Ui
if not st.session_state.document_uploaded:
    uploaded = st.file_uploader(label= "Upload PDF file", type=["pdf"], accept_multiple_files= True)
    if uploaded:
        with st.spinner("Processing..."):
            path = "./docs_files/"
            for file in uploaded:
                with open(path + file.name, "wb") as f:
                    f.write(file.getvalue())

            process_document(path)
            st.rerun()

## Chat Ui

st.subheader("Welcome to the RAG Agent. Upload PDF flies and ask Questions...")

if st.session_state.document_uploaded and st.session_state.agent:

    for message in st.session_state.messages:
        st.chat_message(message["role"]).markdown(message["content"])

    query = st.chat_input("Ask Anything about the Documents...")
    if query:
        st.chat_message("user").markdown(query)
        st.session_state.messages.append({"role":"user","content": query})
        
        response = st.session_state.agent.invoke({"messages": [{"role":"user", "content": query}]}, {"configurable": {"thread_id": "1"}})
        result = response["messages"][-1].content
        st.chat_message("ai").markdown(result)
        st.session_state.messages.append({"role":"ai","content": result})

