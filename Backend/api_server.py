#!/usr/bin/env python3
"""
FastAPI Server for SME Plugin Backend
REST API for Frontend Integration with MongoDB Chat History
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import uvicorn
import sys
import os
from datetime import datetime
import json

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

from complete_system import HotSwappableSMEPlugin, ExpertiseDomain

# MongoDB imports
try:
    from pymongo import MongoClient
    from bson import ObjectId
    MONGODB_AVAILABLE = True
except ImportError:
    print("⚠️ MongoDB not available. Install with: pip install pymongo")
    MONGODB_AVAILABLE = False

# Initialize FastAPI app
app = FastAPI(
    title="SME Plugin API",
    description="Hot-Swappable Subject Matter Expert Plugin API with Chat History",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# MongoDB Configuration
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb://localhost:27017/')
DB_NAME = 'plugmind_chat'
MESSAGES_COLLECTION = 'messages'
SESSIONS_COLLECTION = 'sessions'

# MongoDB Client
mongo_client = None
mongo_db = None
messages_collection = None
sessions_collection = None

def connect_to_mongodb():
    """Connect to MongoDB"""
    global mongo_client, mongo_db, messages_collection, sessions_collection
    
    if not MONGODB_AVAILABLE:
        return False
        
    try:
        mongo_client = MongoClient(MONGODB_URI)
        mongo_db = mongo_client[DB_NAME]
        messages_collection = mongo_db[MESSAGES_COLLECTION]
        sessions_collection = mongo_db[SESSIONS_COLLECTION]
        print("✅ Connected to MongoDB")
        return True
    except Exception as e:
        print(f"❌ MongoDB connection error: {e}")
        return False

def disconnect_from_mongodb():
    """Disconnect from MongoDB"""
    global mongo_client
    if mongo_client:
        mongo_client.close()
        print("✅ Disconnected from MongoDB")

# Initialize SME Plugin
sme_plugin = None

class SwitchDomainRequest(BaseModel):
    domain: str

class ChatRequest(BaseModel):
    message: str
    user_id: Optional[str] = "frontend_user"
    session_id: Optional[str] = "frontend_session"
    context: Optional[str] = ""

class SaveMessageRequest(BaseModel):
    session_id: str
    user_id: str
    message: str
    sender: str
    domain: Optional[str] = None
    confidence: Optional[float] = None
    sources: Optional[List[str]] = None
    methodology: Optional[str] = None
    citations: Optional[List[str]] = None
    disclaimer: Optional[str] = None

class ChatResponse(BaseModel):
    answer: str
    confidence: float
    sources: List[str]
    methodology: str
    domain: str
    citations: List[str]
    reasoning_steps: List[str]
    disclaimer: str

class HealthResponse(BaseModel):
    status: str
    plugin: str
    version: str
    mongodb_connected: bool

@app.on_event("startup")
async def startup_event():
    """Initialize SME plugin and MongoDB on startup"""
    global sme_plugin
    try:
        api_key = "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"
        sme_plugin = HotSwappableSMEPlugin(api_key, ExpertiseDomain.FINANCE)
        print("✅ SME Plugin initialized successfully")
        
        # Connect to MongoDB
        connect_to_mongodb()
        
    except Exception as e:
        print(f"❌ Failed to initialize SME Plugin: {e}")

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        plugin="SME Plugin API",
        version="1.0.0",
        mongodb_connected=mongo_client is not None
    )

@app.get("/plugin/info")
async def get_plugin_info():
    """Get plugin information and capabilities"""
    if not sme_plugin:
        raise HTTPException(status_code=500, detail="Plugin not initialized")
    
    return sme_plugin.get_plugin_info()

@app.get("/plugin/domains")
async def get_available_domains():
    """Get list of available expertise domains"""
    if not sme_plugin:
        raise HTTPException(status_code=500, detail="Plugin not initialized")
    
    return {
        "available_domains": sme_plugin.get_available_domains(),
        "current_domain": sme_plugin.domain.value
    }

@app.post("/plugin/switch_domain")
async def switch_domain(request: SwitchDomainRequest):
    """Switch to a different expertise domain"""
    if not sme_plugin:
        raise HTTPException(status_code=500, detail="Plugin not initialized")
    
    try:
        new_domain = ExpertiseDomain(request.domain)
        success = sme_plugin.switch_domain(new_domain)
        
        if success:
            return {
                "message": f"Successfully switched to {new_domain.value} domain",
                "current_domain": sme_plugin.domain.value
            }
        else:
            raise HTTPException(status_code=500, detail="Domain switch failed")
            
    except ValueError:
        available_domains = [d.value for d in ExpertiseDomain]
        raise HTTPException(
            status_code=400, 
            detail=f"Invalid domain. Available: {available_domains}"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message using SME expertise with context"""
    if not sme_plugin:
        raise HTTPException(status_code=500, detail="Plugin not initialized")
    
    try:
        # Get context from MongoDB if available
        context = request.context or ""
        if not context and mongo_client:
            context = get_context_from_mongodb(request.session_id)
        
        # Combine context with current message
        full_message = context + request.message
        
        # Automatically detect domain and switch if needed
        detected_domain = sme_plugin.detect_domain(request.message)
        
        # Switch domain if different from current
        if detected_domain != sme_plugin.domain:
            old_domain = sme_plugin.domain.value
            sme_plugin.switch_domain(detected_domain)
            print(f"🔄 Auto-switched from {old_domain} to {detected_domain.value} domain")
        
        # Process query with context
        query_type = "loan_analysis" if "loan" in request.message.lower() else "general"
        sme_response = sme_plugin.process_query(request.message, query_type, context)
        
        # Save messages to MongoDB
        if mongo_client:
            save_message_to_mongodb(
                request.session_id,
                request.user_id,
                request.message,
                "user"
            )
            save_message_to_mongodb(
                request.session_id,
                request.user_id,
                sme_response.answer,
                "ai",
                {
                    "domain": sme_response.domain.value,
                    "confidence": sme_response.confidence,
                    "sources": sme_response.sources,
                    "methodology": sme_response.methodology,
                    "citations": sme_response.citations,
                    "disclaimer": sme_response.disclaimer
                }
            )
        
        return ChatResponse(
            answer=sme_response.answer,
            confidence=sme_response.confidence,
            sources=sme_response.sources,
            methodology=sme_response.methodology,
            domain=sme_response.domain.value,
            citations=sme_response.citations,
            reasoning_steps=sme_response.reasoning_steps,
            disclaimer=sme_response.disclaimer
        )
        
    except Exception as e:
        print(f"Error processing chat message: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/context/{session_id}")
async def get_context(session_id: str):
    """Get conversation context for a session"""
    if not mongo_client:
        return {"context": ""}
    
    context = get_context_from_mongodb(session_id)
    return {"context": context}

@app.post("/save_message")
async def save_message(request: SaveMessageRequest):
    """Save a message to MongoDB"""
    if messages_collection is None:
        return {"status": "error", "message": "MongoDB not connected"}
    
    try:
        save_message_to_mongodb(
            request.session_id,
            request.user_id,
            request.message,
            request.sender,
            {
                "domain": request.domain,
                "confidence": request.confidence,
                "sources": request.sources,
                "methodology": request.methodology,
                "citations": request.citations,
                "disclaimer": request.disclaimer
            }
        )
        return {"status": "success", "message": "Message saved"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/history/{session_id}")
async def get_chat_history(session_id: str, limit: int = 50):
    """Get chat history for a session"""
    if messages_collection is None:
        return {"messages": []}
    
    try:
        history = get_chat_history_from_mongodb(session_id, limit)
        return {"messages": history}
    except Exception as e:
        return {"messages": [], "error": str(e)}

@app.delete("/clear_history/{session_id}")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session"""
    if messages_collection is None:
        return {"status": "error", "message": "MongoDB not connected"}
    
    try:
        # Delete all messages for the session
        messages_collection.delete_many({"session_id": session_id})
        sessions_collection.delete_one({"session_id": session_id})
        return {"status": "success", "message": "History cleared"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def get_context_from_mongodb(session_id: str, max_messages: int = 8) -> str:
    """Get conversation context from MongoDB"""
    if messages_collection is None:
        return ""
    
    try:
        # Get recent messages for context
        context_messages = list(
            messages_collection.find({"session_id": session_id})
            .sort("timestamp", -1)
            .limit(max_messages)
        )
        
        if not context_messages:
            return ""
        
        # Build context prompt
        context_prompt = "Previous conversation context:\n\n"
        
        for msg in reversed(context_messages):  # Chronological order
            sender = "User" if msg["sender"] == "user" else "AI Assistant"
            timestamp = msg["timestamp"].strftime("%Y-%m-%d %H:%M:%S")
            
            context_prompt += f"[{timestamp}] {sender}: {msg['message']}\n"
            
            # Include domain info for AI messages
            if msg["sender"] == "ai" and msg.get("domain"):
                confidence = round((msg.get("confidence", 0) * 100))
                context_prompt += f"(Domain: {msg['domain']}, Confidence: {confidence}%)\n"
        
        context_prompt += "\nCurrent question: "
        return context_prompt
        
    except Exception as e:
        print(f"Error getting context: {e}")
        return ""

def save_message_to_mongodb(session_id: str, user_id: str, message: str, sender: str, metadata: dict = None):
    """Save a message to MongoDB"""
    if messages_collection is None:
        return
    
    try:
        # Create or update session
        sessions_collection.update_one(
            {"session_id": session_id},
            {
                "$set": {
                    "user_id": user_id,
                    "updated_at": datetime.utcnow(),
                    "last_message": message,
                    "$inc": {"message_count": 1}
                }
            },
            upsert=True
        )
        
        # Save message
        message_doc = {
            "session_id": session_id,
            "user_id": user_id,
            "message": message,
            "sender": sender,
            "timestamp": datetime.utcnow(),
            **(metadata or {})
        }
        
        messages_collection.insert_one(message_doc)
        
    except Exception as e:
        print(f"Error saving message: {e}")

def get_chat_history_from_mongodb(session_id: str, limit: int = 50) -> List[dict]:
    """Get chat history from MongoDB"""
    if messages_collection is None:
        return []
    
    try:
        history = list(
            messages_collection.find({"session_id": session_id})
            .sort("timestamp", 1)
            .limit(limit)
        )
        
        # Convert ObjectId to string for JSON serialization
        for msg in history:
            msg["_id"] = str(msg["_id"])
            if "timestamp" in msg:
                msg["timestamp"] = msg["timestamp"].isoformat()
        
        return history
        
    except Exception as e:
        print(f"Error getting chat history: {e}")
        return []

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "SME Plugin API Server with MongoDB Chat History",
        "version": "1.0.0",
        "mongodb_connected": mongo_client is not None,
        "endpoints": {
            "health": "/health",
            "plugin_info": "/plugin/info",
            "domains": "/plugin/domains",
            "switch_domain": "/plugin/switch_domain",
            "chat": "/chat",
            "context": "/context/{session_id}",
            "save_message": "/save_message",
            "history": "/history/{session_id}",
            "clear_history": "/clear_history/{session_id}"
        }
    }

if __name__ == "__main__":
    print("🚀 SME Plugin FastAPI Server Starting...")
    print("📍 Available endpoints:")
    print("  GET  / - Root endpoint")
    print("  GET  /health - Health check")
    print("  GET  /plugin/info - Plugin information")
    print("  GET  /plugin/domains - Available domains")
    print("  POST /plugin/switch_domain - Switch expertise domain")
    print("  POST /chat - Process chat message")
    print("  GET  /context/{session_id} - Get conversation context")
    print("  POST /save_message - Save message")
    print("  GET  /history/{session_id} - Get chat history")
    print("  DELETE /clear_history/{session_id} - Clear chat history")
    print("\n🔗 Server running on http://localhost:8001")
    print("🌐 CORS enabled for frontend on http://localhost:3000")
    print("🗄️ MongoDB integration for chat history")
    
    uvicorn.run(app, host="0.0.0.0", port=8001)
