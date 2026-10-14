import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model= "gemini-3.5-flash-lite")

prompt =[
    {"role": "user", "content": "My name is Ajith Kumar"},
    {"role": "ai", "content": "Hello Ajith Kumar, How are you?"},
    {"role": "user", "content": "What is my name?"}
]

res = llm.invoke(prompt)

print(res.content[0]["text"])


## History Management

history = []
while True:
    query = input("User: ")
    if query.lower() in ("bye", "exit", "see you!"):
        print("Good Bye 👋")
        break

    history.append({"role":"user", "content": query})

    print(query)

    res = llm.invoke(history)

    history.append({"role":"ai", "content":res.content[0]["text"]})

    print(res.content[0]["text"])


