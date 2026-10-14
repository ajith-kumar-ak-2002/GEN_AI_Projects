import encodings
from dotenv import load_dotenv
load_dotenv()

### Text Document Loader
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import TextLoader
loader = TextLoader("../data/speech.txt", encoding = ("utf-8"))
text = loader.load()
print(len(text))
print(text[0].page_content)
print(text[0].metadata)

### PDF Document Loader
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import PyPDFLoader
loader = PyPDFLoader("../data/medical_report.pdf")
docs = loader.load()
print(len(docs))
print(docs[1].page_content)
print(docs[0].metadata)

### CSV Loader
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import CSVLoader
loader = CSVLoader("../data/employee_records.csv")
csv = loader.load()
print(len(csv))
print(csv[:5])


### Web Page Loader
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import WebBaseLoader
loader = WebBaseLoader(web_path = "https://techsimplus.com/programs/data-science-and-machine-learning-with-python?mode=online")
web = loader.load()
print(web[0].page_content)


### Wikipedia Loader
# pyrefly: ignore [missing-import]
from langchain_community.document_loaders import WikipediaLoader
loader = WikipediaLoader(query = "GEN AI", load_max_docs = 2)
docs = loader.load()
print(len(docs))
print(docs[0].page_content)