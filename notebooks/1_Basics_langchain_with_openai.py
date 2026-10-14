import os
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv
load_dotenv()

# ---------------------------------------------------------------
## Google Gemini Chat Model
#----------------------------------------------------------------

# 1. Import the Google Gemini Chat Model class
# pyrefly: ignore [missing-import]
from langchain_google_genai import ChatGoogleGenerativeAI

# 2. Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

# 3. Invoke the model
response = llm.invoke("What is GENAI? Explain in simple terms.")

# 4. Extract and print ONLY the clean text response
print(response.content[0]['text'])

#----------------------------------------------------------------
## Google Gemini Chat Model with System and User prompts
#----------------------------------------------------------------

# 1. Import the Google Gemini Chat Model class
# pyrefly: ignore [missing-import]
from langchain_google_genai import ChatGoogleGenerativeAI

# 2. Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

prompts = [
    ("system", "you are a Python Developer"),
    ("user", "How to sort the array in Python?")
]

res = llm.invoke(prompts)
print(res.content)


#----------------------------------------------------------------
## OpenAI Chat Model
#----------------------------------------------------------------

# 1. Import the OpenAI Chat Model class
# pyrefly: ignore [missing-import]
from langchain_openai import ChatOpenAI

# 2. Initialize OpenAI
llm = ChatOpenAI(model="gpt-6-astra")

# 3. Invoke the model
response = llm.invoke("what is largest number in python?")

# 4. Extract and print ONLY the clean text response
print(response.content[0]['text'])

#----------------------------------------------------------------
## Anthropic Claude Model
#----------------------------------------------------------------

# 1. Import the Anthropic Claude Model class
# pyrefly: ignore [missing-import]
from langchain_anthropic import ChatAnthropic

# 2. Initialize Claude
llm = ChatAnthropic(model="claude-opus-5")

# 3. Invoke the model
response = llm.invoke("Who is PM of India?")

# 4. Extract and print ONLY the clean text response
print(response.content)


