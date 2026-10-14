from docutils.parsers.rst.directives import encoding
from dotenv import load_dotenv
load_dotenv()

# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter

text = "This makes RAG especially useful for applications involving private documents, company knowledge bases, FAQs, technical documentation, and domain-specific information."

chunk = RecursiveCharacterTextSplitter(chunk_size = 50, chunk_overlap = 10)

tx_chunk = chunk.split_text(text)
print(len(tx_chunk))


### Load And Chunk the Data (Text & PDF)
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader, TextLoader
# pyrefly: ignore [missing-import]
from langchain_text_splitters import RecursiveCharacterTextSplitter

tx_loader = TextLoader("../data/speech.txt", encoding = "utf=8")
tx_load = tx_loader.load()

print("Before Length of text: ", len(tx_load))

pd_loader = PyPDFLoader("../data/medical_report.pdf")
pd_load = pd_loader.load()

print("Before Length of PDF: ", len(pd_load))


chunks = RecursiveCharacterTextSplitter(chunk_size = 500, chunk_overlap= 100)

tx_chunk = chunks.split_documents(tx_load)
print("After length of the Text: ", len(tx_chunk))

pd_chunk = chunks.split_documents(pd_load)
print("After Length of PDF: ", len(pd_chunk))
