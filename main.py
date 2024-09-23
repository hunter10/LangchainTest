from typing import Any, Dict
from fastapi import Body, FastAPI, Form, Request
from fastapi.responses import HTMLResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from pinecone import Pinecone
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore

load_dotenv()

pc = Pinecone(api_key="PINECONE_API_KEY")

embeddings = OpenAIEmbeddings()

vector_store = PineconeVectorStore.from_existing_index(
    "recipes",
    embeddings,
)

app = FastAPI(
    title="ChefGPT. The best provider of Indian Recipes in the world.",
    description="Give ChefGPT a couple of ingredients and it will give you recipes in return.",
    servers=[
        {"url":"https://encouraging-amy-oasis-speakers.trycloudflare.com"}
    ]
)

class Document(BaseModel):
    page_content: str

@app.get(
    "/recipes", 
    summary="Returns a list of recipes.",
    description="Upon receiving an ingredient, this endpoint will return a list of recipes that contain that ingredient.",
    response_description="A Document object that contains the recipe and preparation instructions.",
    response_model=list[Document],
    # openapi_extra={
    #      "x-openai-isConsequential":True,
    # },
)

def get_recipes(ingredient: str):
    docs = vector_store.similarity_search(ingredient)
    return docs

# 가짜 DB
user_token_db = {
    "ABCDEF": "nico"
}

@app.get("/authorize", 
         response_class=HTMLResponse,
         include_in_schema=False,
)
def handle_authorize(client_id:str, redirect_uri:str, state:str):
    return f"""
    <html>
        <head>
            <title>Nicolacus Maximus Log In</title>
        </head>
        <body>
            <h1>Log Into Nicolacus Maximus</h1>
            <a href="{redirect_uri}?code=ABCDEF&state={state}">Authorize Nicolacus Maximus GPT</a>
        </body>
    </html>
    """

@app.post("/token", 
          include_in_schema=False,
)

def handle_token(code = Form(...)):
    print(code)
    return {
        "access_token": user_token_db[code]
    }





