from dotenv import load_dotenv
load_dotenv()

documents = [
    "Machine Learning is a subset of artificial intelligence.",
    "Deep Learning uses neural networks with multiple layers.",
    "Python is a programming language popular for data science.",
    "India won the cricket world cup in 2011.",
    "AI models can understand and generate human language."
]

from langchain_google_genai import GoogleGenerativeAIEmbeddings

embeddings = GoogleGenerativeAIEmbeddings(model = "gemini-embedding-2")

vector = embeddings.embed_documents(documents)

print(len(vector[0]))


### Store Embedding Data into Chroma DataBase
# pyrefly: ignore [missing-import]
from langchain_chroma import Chroma

vector_store = Chroma.from_texts(
    texts = documents,
    embedding = embeddings,
    persist_directory = "/data/vector_db"
)


query = "Data science"
result = vector_store.similarity_search(query = query, k=2)
result

