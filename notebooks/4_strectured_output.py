import os 
from dotenv import load_dotenv 
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(model ="gemini-3.5-flash-lite")


## Problem Statement
text = ("Hello , My Name is AJith Kumar, My email is ajithkumaraj0206@gmail.com and age is 26")

res = llm.invoke(f"Please Extract Name , email and age for this Text: {text}")

print(res.content[0]["text"])
print(type(res.content[0]["text"]))

### Solution: Structured Output 
from pydantic import BaseModel, Field
from typing import List

class structured_output(BaseModel):
    """Extract text from the text and return it."""
    name : str = Field(description = "Full Name ")
    email : str = Field(description = "Email Address")
    age : int = Field(description = "Age")

structure_llm = llm.with_structured_output(structured_output)
res = structure_llm.invoke(f"please Extract the name , email and age from the Text: {text}")

print(res)
print(res.name)
print(res.email)
print(res.age)
print(res.model_dump())



### Movies recommendation
class movies(BaseModel):
    movie: str = Field(description = "Movie Name")
    reason : str = Field(description = "Reason for recommendation")
    year : int = Field(description = "Year of release")

class movie_list(BaseModel):
    movies : list[movies]

movie_llm = llm.with_structured_output(movie_list)
movie_res = movie_llm.invoke("Give me three recent Telugu Sci-Fi Movies")

for i, movie in enumerate(movie_res.movies, start=1):
    print(f"Movie {i}")
    print(f"Name   : {movie.movie}")
    print(f"Reason : {movie.reason}")
    print(f"Year   : {movie.year}")
    print()


