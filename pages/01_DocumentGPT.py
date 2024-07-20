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

@st.cache_data(show_spinner="Embedding file...")
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

    loader = UnstructuredFileLoader(file_path)
    docs = loader.load_and_split(text_splitter=splitter)
    embeddings = OpenAIEmbeddings()
    cached_embeddings = CacheBackedEmbeddings.from_bytes_store(embeddings, cache_dir)

    # 이부분에서 비용 발생 - 조심해야 함 (실행할때마다)
    vectorstore = FAISS.from_documents(docs, cached_embeddings) 
    retriever = vectorstore.as_retriever()
    return retriever

def send_message(message, role, save=True):
    with st.chat_message(role):
        st.markdown(message)
    if save:
        st.session_state["messages"].append({"message": message, "role": role})

def patin_history():
    for message in st.session_state["messages"]:
        send_message(message["message"], message["role"], save=False,)

st.title("Document GPT")

st.markdown("""
Welcome!
            
Use this chatbot to ask questions to an AI About your files!

Upload your files on the sidebar.
""")

with st.sidebar:
    file = st.file_uploader("Upload a .pdf .txt or .docx file", type=["pdf", "txt", ".docx"])

if file:
    retriever = embed_file(file)
    send_message("I'm ready! Ask away!", "ai", save=False)
    patin_history()
    message = st.chat_input("Ask anything about your file...")
    if message:
        send_message(message, "human")
        send_message("hahaha", "ai")
else:
    st.session_state["messages"] = []

