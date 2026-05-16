import os
from dotenv import load_dotenv
from pydantic import BaseModel
from langchain_groq import ChatGroq
load_dotenv()
llm=ChatGroq(model='llama-3.1-8b-instant')
class Blog(BaseModel):
    title: str
    content: str
prompt='Translate this: Title: Hello, Content: World. to German'
print(llm.with_structured_output(Blog).invoke(prompt))
