from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="PlugMind Backend API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default"

@app.get("/")
async def root():
    return {"message": "PlugMind Backend API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/answer")
async def answer_question(request: ChatRequest):
    response = f"Finance expert answer: {request.message}"
    return {"answer": response}

# Vercel serverless handler
handler = app
