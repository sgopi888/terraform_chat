from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="AI Backend - Agentic RAG")

class QueryRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"status": "healthy", "service": "Agentic RAG Backend"}

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/api/v1/query")
async def query(payload: QueryRequest):
    """
    Lazy-load the agent ONLY when a request comes in.
    This ensures the server always starts even if ADK has issues.
    """
    try:
        # Import inside the function so startup never crashes
        from app.agents.root import run_agent
        result = await run_agent(payload.text)
        return {"response": result}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": str(e)}
        )
