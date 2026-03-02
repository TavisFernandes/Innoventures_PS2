import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uvicorn

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

class ChatResponse(BaseModel):
    response: str
    domain: str = "finance"
    confidence: float = 0.8
    sources: list = []
    methodology: str = "RAG-based analysis"

@app.get("/")
async def root():
    return {"message": "PlugMind Backend API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.post("/chat")
async def chat(request: ChatRequest):
    # Mock response for now - integrate with your actual SME plugin
    response = f"This is a finance expert response to: {request.message}"
    
    return ChatResponse(
        response=response,
        domain="finance",
        confidence=0.85,
        sources=["Mock Source 1", "Mock Source 2"],
        methodology="RAG-based analysis with TF-IDF retrieval"
    )

@app.post("/answer")
async def answer_question(request: ChatRequest):
    # Alternative endpoint for frontend compatibility
    response = f"Finance expert answer: {request.message}"
    
    return {"answer": response}

# For Vercel serverless
handler = app

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
