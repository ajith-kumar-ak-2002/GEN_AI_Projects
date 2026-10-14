import os 
# pyrefly: ignore [missing-import]
from dotenv import load_dotenv 
load_dotenv

# pyrefly: ignore [missing-import]
from langchain_google_genai import ChatGoogleGenerativeAI

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite")

prompt = [
    {"role" :"system", "content":"You are a JavaScript Developer"},
    {"role" :"user", "content":"Difference B/W map and fliter"}
]

res = llm.invoke(prompt)
print(res.content[0]['text'])


prompt = [
    {"role" :"system", "content":"You are a Python Developer"},
    {"role" :"user", "content":"Difference B/W map and fliter"}
]

res = llm.invoke(prompt)
print(res.content[0]['text'])


prompt = [
    {"role" :"system", "content":"You are a Translater and translate input in Telugu"},
    {"role" :"user", "content":"I Love to Play Cricket?"}
]

res = llm.invoke(prompt)
print(res.content[0]['text'])


### Propmts Templetes - Dynamic Variables Input

# pyrefly: ignore [missing-import]
from langchain_google_genai import ChatGoogleGenerativeAI
# pyrefly: ignore [missing-import]
from langchain_core.prompts import ChatPromptTemplate
# pyrefly: ignore [missing-import]
from langchain_core.output_parsers import StrOutputParser

llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash")

prompt = ChatPromptTemplate.from_messages ([
    {"role": "system", "content": "You are a {language} Developer"},
    {"role": "user", "content": "Answer this {query}"}
])


# final_prompt = prompt.invoke({
#     "language": "Python",
#     "query": "Why Python is Important"
# })
 
# res = llm.invoke(final_prompt)
# print(res.content[0]["text"])


# res = llm.invoke(prompt.invoke({"language" : "Python", "query": "Create a Calcuator"}))
# print(res.content[0]["text"])

chains = prompt | llm | StrOutputParser()
res = chains.invoke({"language": "Python", "query": "What is Python?"})
print(res)
