import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter

# --- Choice B: Pure OpenAI Ingestion ---
# We use OpenAI for embeddings and FAISS for local indexing.
# This gives you total control over the RAG logic without GCP billing risks.

load_dotenv()

DATASET_DIR = "dataset/"
INDEX_SAVE_DIR = "dataset/faiss_index"

def ingest_pdfs():
    print("🚀 Starting OpenAI PDF Ingestion...")
    
    # 1. Load PDFs
    documents = []
    for file in os.listdir(DATASET_DIR):
        if file.endswith(".pdf"):
            print(f"📄 Loading {file}...")
            loader = PyPDFLoader(os.path.join(DATASET_DIR, file))
            documents.extend(loader.load())

    if not documents:
        print("❌ No PDFs found in dataset/ folder!")
        return

    # 2. Split into chunks
    # FDE TIP: Small chunks (500-1000) are better for "Small" embedding models.
    print("✂️ Splitting documents into chunks...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
    docs = text_splitter.split_documents(documents)

    # 3. Create Embeddings & Index
    # We use text-embedding-3-small as requested.
    print(f"🧠 Generating OpenAI Embeddings (text-embedding-3-small) for {len(docs)} chunks...")
    embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
    
    vectorstore = FAISS.from_documents(docs, embeddings)

    # 4. Save Local Index
    print(f"💾 Saving index to {INDEX_SAVE_DIR}...")
    vectorstore.save_local(INDEX_SAVE_DIR)
    print("✅ Ingestion Complete! Your knowledge base is ready.")

if __name__ == "__main__":
    ingest_pdfs()
