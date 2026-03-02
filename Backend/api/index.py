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

@app.post("/chat")
async def chat(request: ChatRequest):
    response = f"This is a finance expert response to: {request.message}"
    
    return {
        "answer": response,
        "domain": "finance",
        "confidence": 0.85,
        "sources": ["Mock Source 1", "Mock Source 2"],
        "methodology": "RAG-based analysis with TF-IDF retrieval",
        "citations": ["[1]", "[2]"],
        "reasoning_steps": ["Analyzed query", "Retrieved documents", "Generated response"],
        "disclaimer": "This is for educational purposes only."
    }

@app.post("/answer")
async def answer_question(request: ChatRequest):
    response = f"Finance expert answer: {request.message}"
    return {"answer": response}

# Render handler
handler = app

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
