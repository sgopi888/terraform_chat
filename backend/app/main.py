# backend/app/main.py

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import asyncio
import os
from dotenv import load_dotenv

# Import the agent logic
from app.agents.root import run_agent

load_dotenv()

app = FastAPI(title="AI Backend - Real RAG")

class QueryRequest(BaseModel):
    text: str

@app.get("/")
async def root():
    return {"status": "healthy", "service": "Agentic RAG Backend"}

@app.post("/api/v1/query")
async def query(payload: QueryRequest):
    """
    The main entry point for the Agentic RAG service.
    It calls the ADK Agent (root_agent) which uses our GCS PDFs.
    """
    try:
        # Run the async agent workflow
        result = await run_agent(payload.text)
        return {"response": result}
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": f"Agent Execution Error: {str(e)}"}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
