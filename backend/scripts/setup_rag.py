import vertexai
from vertexai import rag
from vertexai.generative_models import Tool
import os
from dotenv import load_dotenv

# --- Choice C: The Hybrid (Vertex RAG + OpenAI LLM) ---
# Goal: Learn Vertex AI RAG while using OpenAI for reasoning.

load_dotenv()

PROJECT_ID = "summarize-398910"
LOCATION = "europe-west4"
BUCKET_NAME = f"{PROJECT_ID}-dataset-bucket"
CORPUS_DISPLAY_NAME = "quiz-research-corpus"

# Initialize Vertex AI
print(f"Initializing Vertex AI in {LOCATION}...")
vertexai.init(project=PROJECT_ID, location=LOCATION)

def setup_managed_rag():
    print(f"🚀 Creating Managed Vertex RAG Corpus...")
    
    # 1. Configure the Embedding Model (Vertex Native)
    # Note: Managed RAG requires a Vertex embedding model for managed indexing.
    embedding_model_config = rag.RagEmbeddingModelConfig(
        vertex_prediction_endpoint=rag.VertexPredictionEndpoint(
            publisher_model="publishers/google/models/text-embedding-004"
        )
    )

    # 2. Create the Corpus
    rag_corpus = rag.create_corpus(
        display_name=CORPUS_DISPLAY_NAME,
        backend_config=rag.RagVectorDbConfig(
            rag_embedding_model_config=embedding_model_config
        ),
    )
    print(f"✅ Corpus Created: {rag_corpus.name}")

    # 3. Import Files from GCS
    print(f"📥 Importing PDFs from gs://{BUCKET_NAME}/dataset/ ...")
    rag.import_files(
        rag_corpus.name,
        [f"gs://{BUCKET_NAME}/dataset/"],
        transformation_config=rag.TransformationConfig(
            chunking_config=rag.ChunkingConfig(chunk_size=512, chunk_overlap=100)
        )
    )
    print("✅ Ingestion Triggered. Indexing will happen on GCP servers.")
    print(f"Save this CORPUS_PATH: {rag_corpus.name}")

if __name__ == "__main__":
    setup_managed_rag()
