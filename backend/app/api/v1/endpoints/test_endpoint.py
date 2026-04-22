from fastapi import APIRouter
from openai import OpenAI
import os

router = APIRouter()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@router.get("/test")
def test():
    return {"message": "Test endpoint is working!"}

@router.post("/chat")
def chat(payload: dict):
    q = payload.get("q")

    res = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": q}]
    )

    return {"response": res.choices[0].message.content}