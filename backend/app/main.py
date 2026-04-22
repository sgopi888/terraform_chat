from fastapi import FastAPI, Request, status
from fastapi.responses import RedirectResponse, JSONResponse
from pydantic import BaseModel
from openai import OpenAI
import os

app = FastAPI(title="AI Backend")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ✅ Request schema (fixes Swagger + 422 issues)
class ChatRequest(BaseModel):
    q: str


@app.get("/")
async def root(request: Request):
    return RedirectResponse(url="/docs", status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/metrics")
async def metrics():
    return JSONResponse(content={"message": "Metrics not implemented"})


@app.post("/api/v1/chat")
def chat(payload: ChatRequest):
    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": payload.q}]
    )
    return {"response": res.choices[0].message.content}