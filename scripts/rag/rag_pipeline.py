"""RAG Pipeline: document ingestion + retrieval using LangChain + Qdrant + Ollama.

Usage:
    python scripts/rag/rag_pipeline.py ingest <file_path>
    python scripts/rag/rag_pipeline.py query "question"
"""

import sys
import os
import subprocess

# Load API key from SOPS
def load_api_key():
    sops_exe = r"C:\Tools\sops\sops.exe"
    os.environ["SOPS_AGE_KEY_FILE"] = os.path.expanduser(r"~\.config\sops\age\keys.txt")
    result = subprocess.run([sops_exe, "--decrypt", ".secrets.yaml"], capture_output=True, text=True, cwd=r"D:\Projects\ai")
    for line in result.stdout.splitlines():
        if line.startswith("LITELLM_API_KEY:"):
            val = line.split(":", 1)[1].strip().strip('"').strip("'")
            os.environ["LITELLM_API_KEY"] = val
            return val
    return None

load_api_key()

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_qdrant import QdrantVectorStore
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

QDRANT_URL = "http://127.0.0.1:6333"
COLLECTION_NAME = "ai-workstation"
EMBED_MODEL = "nomic-embed-text"
CHAT_MODEL = "qwen3:8b"

def ingest(file_path):
    """Load and ingest a document into Qdrant."""
    loader = TextLoader(file_path)
    docs = loader.load()
    
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    
    embeddings = OllamaEmbeddings(base_url="http://127.0.0.1:11434", model=EMBED_MODEL)
    
    vs = QdrantVectorStore.from_documents(
        chunks, embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
    )
    print(f"Ingested {len(chunks)} chunks from {file_path}")

def query(question):
    """Query the RAG pipeline."""
    embeddings = OllamaEmbeddings(base_url="http://127.0.0.1:11434", model=EMBED_MODEL)
    
    vs = QdrantVectorStore.from_existing_collection(
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
        embedding=embeddings,
    )
    
    retriever = vs.as_retriever(search_kwargs={"k": 3})
    
    template = """Answer based on context:
    {context}
    
    Question: {question}
    Answer:"""
    prompt = ChatPromptTemplate.from_template(template)
    
    llm = ChatOllama(base_url="http://127.0.0.1:11434", model=CHAT_MODEL)
    
    rag_chain = (
        {"context": retriever, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    
    answer = rag_chain.invoke(question)
    print(answer)

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    
    cmd = sys.argv[1]
    if cmd == "ingest":
        ingest(sys.argv[2])
    elif cmd == "query":
        query(sys.argv[2])
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)