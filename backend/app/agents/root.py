# backend/app/agents/root.py
# Architecture: Vertex AI RAG (retrieval) + Native OpenAI SDK (reasoning)
# NO litellm, NO ADK model wrappers — maximum simplicity & reliability

import os
import vertexai
from vertexai import rag
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# ── Config ────────────────────────────────────────────────────────────────────
PROJECT_ID  = "summarize-398910"
LOCATION    = "europe-west4"
CORPUS_PATH = "projects/493443117630/locations/europe-west4/ragCorpora/6917529027641081856"
OPENAI_MODEL = "gpt-4.1-mini"

# ── Lazy-initialised singletons ───────────────────────────────────────────────
_vertex_initialised = False
_openai_client: OpenAI | None = None


def _init_vertex():
    global _vertex_initialised
    if not _vertex_initialised:
        vertexai.init(project=PROJECT_ID, location=LOCATION)
        _vertex_initialised = True


def _get_openai() -> OpenAI:
    global _openai_client
    if _openai_client is None:
        _openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _openai_client


# ── Core pipeline ─────────────────────────────────────────────────────────────

def retrieve_context(query: str) -> str:
    """Step 1 — pull relevant chunks from Vertex AI RAG."""
    _init_vertex()
    try:
        response = rag.retrieval_query(
            rag_resources=[rag.RagResource(rag_corpus=CORPUS_PATH)],
            text=query,
            similarity_top_k=5,
        )
        chunks = []
        for ctx in response.contexts.contexts:
            chunks.append(ctx.text)
        return "\n\n---\n\n".join(chunks) if chunks else ""
    except Exception as e:
        print(f"[RAG] retrieval failed: {e}")
        return ""


def call_openai(query: str, context: str) -> str:
    """Step 2 — send query + retrieved context to OpenAI."""
    client = _get_openai()

    system_prompt = (
        "You are a professional AI Interview Expert specialising in machine learning research.\n"
        "When context is provided, ground your answer in it and cite it.\n"
        "If no context is available, answer from your general knowledge."
    )

    user_message = query
    if context:
        user_message = f"{query}\n\n[Retrieved Context]\n{context}"

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user",   "content": user_message},
        ],
        temperature=0.3,
    )
    return response.choices[0].message.content


# ── Public entry-point called by main.py ─────────────────────────────────────

async def run_agent(query: str) -> str:
    """Hybrid RAG pipeline: Vertex retrieve → OpenAI reason."""
    context = retrieve_context(query)
    return call_openai(query, context)