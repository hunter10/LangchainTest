import time
import streamlit as st

from langchain.storage import LocalFileStore
from langchain.text_splitter import CharacterTextSplitter
from langchain.document_loaders import UnstructuredFileLoader
from langchain.embeddings import OpenAIEmbeddings, CacheBackedEmbeddings
from langchain.vectorstores import FAISS 


st.set_page_config(
    page_title="Document GPT",
    page_icon="📝",
)

def embed_file(file):
    file_content = file.read()
    file_path = f"./.cache/files/{file.name}"
    # st.write(file_content, file_path)
    with open(file_path, "wb") as f:
        f.write(file_content)

    cache_dir = LocalFileStore(f"./.cache/embeddings/{file.name}")

    splitter = CharacterTextSplitter.from_tiktoken_encoder(
        separator="\n",
        chunk_size=600,
        chunk_overlap=100,
    )

    loader = UnstructuredFileLoader("./files/chapter_one.docx")
    docs = loader.load_and_split(text_splitter=splitter)
    embeddings = OpenAIEmbeddings()
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)

    # 이부분에서 비용 발생 - 조심해야 함 (실행할때마다)
    vectorstore = FAISS.from_documents(docs, cached_embeddings) 
    retriever = vectorstore.as_retriever()
    return retriever

st.title("Document GPT")

st.markdown("""
Welcome!
            
Use this chatbot to ask questions to an AI About your files!


""")


file = st.file_uploader("Upload a .pdf .txt or .docx file", type=["pdf", "txt", ".docx"])

if file:
    retriever = embed_file(file)
    s = retriever.invoke("winston")
    s