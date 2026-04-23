# GCP-Native Agentic RAG Service (Hybrid Architecture)

This repository implements a production-grade **Agentic RAG (Retrieval-Augmented Generation)** service designed for AI Interview Quiz Preparation. It showcases a modern, hybrid architecture combining **Google Cloud Platform (GCP)** managed infrastructure with **OpenAI's** reasoning capabilities.

## 🧠 Architecture Overview

This is not a toy demo. It is a dual-region, hybrid AI system built for scale and reliability:

- **Serving Layer**: FastAPI deployed on **Google Cloud Run** (Scalable, Serverless).
- **Data Layer**: **Vertex AI RAG Engine** (Managed Corpus, Indexing, and Retrieval).
- **Storage Layer**: **Google Cloud Storage (GCS)** for raw document (PDF) hosting.
- **Reasoning Layer**: **OpenAI GPT-4o-mini** via Native SDK for high-performance grounded generation.
- **Infrastructure**: Fully provisioned via **Terraform** (Infrastructure-as-Code).
- **Security**: **GCP Secret Manager** for sensitive API credentials.

## 💥 Key Vertex AI Implementations

The project leverages the power of Vertex AI as the core data engine:

1.  **Vertex AI RAG Engine**: 
    - Automated ingestion of research PDFs from GCS.
    - Managed chunking and high-performance embedding using `text-embedding-004`.
    - Native similarity-based retrieval API.
2.  **Hybrid Orchestration**:
    - Uses Vertex AI for **Managed Context Retrieval**.
    - Uses OpenAI for **Contextual Reasoning** and answer synthesis.
    - This pattern reflects real-world production setups where specific providers are chosen for their unique strengths (GCP for data infra, OpenAI for reasoning).

## 🚀 Technical Highlights

- **Infrastructure as Code (IaC)**: Terraform manages GCS buckets, Cloud Run services, IAM roles, and Project-level APIs.
- **Agentic Workflow**: Implements the "Retrieve-then-Reason" pattern.
- **Financial Guardrails**: Built-in cost-control variables in Terraform to prevent unauthorized resource scaling.
- **Secure Secrets**: Seamless integration between Cloud Run and Secret Manager for `OPENAI_API_KEY`.
- **European Region Hosting**: RAG Corpus hosted in `europe-west4` (Netherlands) for specialized compliance and latency testing.

## 🛠️ Getting Started

### Prerequisites

1.  **GCP Project**: Active project with billing enabled.
2.  **Terraform**: Installed locally.
3.  **GCloud CLI**: Authenticated to your project.
4.  **OpenAI API Key**: Stored in Secret Manager as `OPENAI_API_KEY`.

### Deployment

1.  **Provision Infrastructure**:
    ```bash
    cd terraform
    terraform init
    terraform apply
    ```
2.  **Setup RAG Corpus**:
    ```bash
    cd backend
    python scripts/setup_rag.py
    ```
3.  **Build & Deploy Backend**:
    ```bash
    gcloud builds submit . --tag gcr.io/YOUR_PROJECT_ID/fastapi-cloudrun
    gcloud run services update cloudrun-service-v2 \
      --image=gcr.io/YOUR_PROJECT_ID/fastapi-cloudrun \
      --region=us-central1
    ```

## 🧪 Usage

Interact with the Agentic RAG endpoint:

```bash
curl -X POST https://YOUR_SERVICE_URL/api/v1/query \
-H "Content-Type: application/json" \
-d '{"text": "What does the 2025 Long Context paper say about quiz generation accuracy?"}'
```

## 🧠 Knowledge Nuggets

- **Why Hybrid?**: Pivoting from Gemini to OpenAI while retaining Vertex RAG demonstrates an understanding of modular AI architecture—swapping the "Brain" while keeping the "Knowledge Base" intact.
- **ADK Insight**: Explored the Google Agent Development Kit (ADK) for tool abstraction and session management, gaining deep insight into Google's preferred agent patterns.

---
*Built by a Forward Deployed Engineer (AI/ML focus).*
