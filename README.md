# GEN_AI_Projects

A comprehensive repository containing Generative AI projects, experiments, and applications built with **LangChain**, **LangGraph**, **OpenAI**, **Anthropic**, **Google Gemini**, **Groq**, **Ollama**, and **Streamlit**.

---

## 📂 Repository Structure

- **`apps/`**: Interactive applications (Streamlit chatbots, SQL agents, RAG systems, and LangGraph assistants).
  - `1_qna_chat_bot.py`: Basic Q&A chatbot.
  - `2_google_search_agent.py`: Agent with Google search integration.
  - `3_qna_chatbot_with_groq.py`: Fast Q&A chatbot using Groq.
  - `4_sql_agent.py`: SQL Database querying AI agent.
  - `5_rag_agent.py`: Retrieval-Augmented Generation agent.
  - `6_langgrapg_chatbot.py`: Stateful graph-based chatbot using LangGraph.
- **`notebooks/`**: Step-by-step modular Python scripts and tutorial workflows:
  - `1_Basics_langchain_with_openai.py` to `9_google_search_agent.py`: Core LangChain fundamentals (prompt chains, memory, structured outputs, streaming, agents).
  - `10_rag_load_document.py` to `15_pydantic_data_validation.py`: RAG pipeline (document loading, text splitting, vector embeddings, vector stores, validation).
  - `16_basics_langgraph.py` to `19_rag_with_langgraph.py`: Multi-agent workflows, state management, and RAG with LangGraph.
- **`data/`**: Sample documents (PDFs, CSVs, text) used for document loading and RAG experiments.

---

## 🚀 Getting Started

### 1. Clone the Repository
```bash
git clone https://github.com/ajith-kumar-ak-2002/GEN_AI_Projects.git
cd GEN_AI_Projects
```

### 2. Set Up Virtual Environment
```bash
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure API Keys
Copy `.env.example` to `.env` and fill in your API credentials:
```bash
cp .env.example .env
```
Ensure your `.env` contains:
- `OPENAI_API_KEY`
- `GOOGLE_API_KEY`
- `ANTHROPIC_API_KEY`
- `GROQ_API_KEY`
- (Optional: `HUGGINGFACEHUB_API_KEY`, `SERPER_API_KEY`, `OPENWEATHER_API_KEY`)

---

## 💻 Running the Applications

To launch any Streamlit app in `apps/`:
```bash
streamlit run apps/1_qna_chat_bot.py
```
Or run any individual workflow script:
```bash
python notebooks/19_rag_with_langgraph.py
```
