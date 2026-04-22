# Mentor Guide: Building a GCP-Native Agentic RAG (Phase 2)

Hello fresher! You have now constructed a sophisticated multi-cloud hybrid agent. This is the exactly the kind of architecture expected in a Lead Deployment Engineer role.

---

## Phase 2.4: The RAG Librarian (Real RAG)

**Learning**: Uploading files is not enough. You need an automated system to read, chunk, and index those files so an LLM can find them. This is what the **Vertex AI RAG Engine** provides.

**FDE Rationale**: 
Using **ADK** as your orchestrator allows you to "mix and match" the best tools for the job. You are using **Vertex AI** for its professional document management (RAG Engine) and **OpenAI** for its flexible reasoning. This avoids vendor lock-in and optimizes for both performance and cost.

### [Step 2.4a] Provisioning the Engine
1. **Apply the Terraform**:
   ```bash
   cd terraform
   terraform apply
   ```
   **Why?** This creates the `google_vertex_ai_rag_corpus`. It's like building the bookshelf. It also creates the `google_vertex_ai_rag_data_source`, which is the worker that moves books from GCS to the bookshelf.

### [Step 2.4b] Attaching the Tool in Code
1. **Examine `backend/app/agents/root.py`**:
   - We imported `VertexAiRagRetrieval`.
   - we defined the `CORPUS_PATH`.
   - We added `tools=[rag_tool]` to the `Agent`.

### [Step 2.4c] Verify the Grounding
Run your server:
```bash
cd backend
PYTHONPATH=. uvicorn app.main:app --reload
```
And test the "Brain" on the specific PDF content:
```bash
curl -X POST http://localhost:8000/api/v1/query \
-d '{"text": "What does the 2025 Long Context paper say about quiz generation?"}'
```

---

## Terminology Recap:
*   **RAG Engine**: The managed service that handles the "Search" part of RAG.
*   **Corpus**: A logical collection of documents that have been vectorized.
*   **Data Source**: A connector that links a GCS bucket to a Corpus.
*   **Grounding**: The process of the LLM using the retrieved "facts" to answer, rather than guessing.
*   **Model Agnostic**: An architecture that doesn't care which LLM is used (GPT-4 vs Gemini), allowing you to swap them in seconds.
