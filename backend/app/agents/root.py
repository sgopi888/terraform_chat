# backend/app/agents/root.py

import os
from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm  
from google.adk.tools.retrieval.vertex_ai_rag_retrieval import VertexAiRagRetrieval # 🔥 VERTEX SEARCH
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

load_dotenv()

# --- Choice C: The Hybrid Config ---
PROJECT_ID = "summarize-398910"
LOCATION = "europe-west4"

# ✅ UPDATED: Your specific Corpus Path
CORPUS_PATH = "projects/493443117630/locations/europe-west4/ragCorpora/6917529027641081856"

# THE VERTEX RETRIEVAL TOOL (Learned from Vertex AI)
rag_tool = VertexAiRagRetrieval(
    name="vertex_rag_tool",
    description="Retrieves relevant context from Vertex AI RAG corpus",
    rag_resources=[
        {
            "rag_corpus": CORPUS_PATH
        }
    ]
)

# THE OPENAI REASONER (Safe for your Gemini status)
root_agent = Agent(
    name="root_agent",
    model=LiteLlm(model="openai/gpt-5-nano"),
    tools=[rag_tool], 
    description="Hybrid AI Assistant (Vertex RAG + OpenAI LLM)",
    instruction="""You are a professional AI Interview Expert. 
    1. Use the 'VertexAiRagRetrieval' tool to find facts in the research PDFs.
    2. Synthesize those facts using your internal knowledge.
    3. Always cite the research findings when answering."""
)

session_service = InMemorySessionService()

APP_NAME = "app"
USER_ID = "user1"
SESSION_ID = "session1"

runner = Runner(
    agent=root_agent,
    app_name=APP_NAME,
    session_service=session_service
)

async def run_agent(query: str):
    """
    Executes the Hybrid RAG workflow.
    """
    try:
        await session_service.create_session(
            app_name=APP_NAME,
            user_id=USER_ID,
            session_id=SESSION_ID
        )
    except:
        pass 

    content = types.Content(role="user", parts=[types.Part(text=query)])

    async for event in runner.run_async(
        user_id=USER_ID,
        session_id=SESSION_ID,
        new_message=content
    ):
        if event.is_final_response():
            return event.content.parts[0].text

    return "No response"