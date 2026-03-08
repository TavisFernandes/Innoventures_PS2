#!/usr/bin/env python3
"""
FastAPI Server for SME Plugin Backend
REST API for Frontend Integration with MongoDB Chat History
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Dict, List, Optional, Any
import uvicorn
import sys
import os
from datetime import datetime
import json
import requests
import yaml
import joblib
import numpy as np
from threading import Thread
from dataclasses import dataclass
from enum import Enum
import logging
import re
import base64
from firebase_admin import credentials, auth, db
from firebase_admin import firestore

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Firebase Admin SDK initialization
try:
    import firebase_admin
    from firebase_admin import credentials
    from firebase_admin import db as firestore_db
    from firebase_admin import auth as firebase_auth
    
    # Initialize Firebase Admin with service account
    cred = credentials.Certificate({
        "type": "service_account",
        "project_id": "echelon-99796",
        "private_key_id": "your-private-key-id",
        "private_key": "-----BEGIN PRIVATE KEY-----\nyour-private-key-content\n-----END PRIVATE KEY-----\n",
        "client_email": "firebase-adminsdk-xxxxx@echelon-99796.iam.gserviceaccount.com",
        "client_id": "your-client-id",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"
    })
    
    firebase_admin.initialize_app(cred)
    firebase_db = firestore_db.client()
    firebase_auth = firebase_auth
    print("✅ Firebase Admin initialized")
except Exception as e:
    print(f"⚠️ Firebase initialization failed: {e}")
    firebase_db = None
    firebase_auth = None

# Firebase chat storage functions
def save_chat_to_firebase(session_id: str, user_id: str, message: str, sender: str):
    """Save chat message to Firebase"""
    if not firebase_db:
        return
    
    try:
        # Create a reference to the user's chats
        chats_ref = firebase_db.collection('users').document(user_id).collection('chats')
        
        # Create a new chat document or update existing one
        chat_data = {
            'message': message,
            'sender': sender,
            'timestamp': datetime.now().isoformat(),
            'lastUpdated': datetime.now().isoformat()
        }
        
        # Use session_id as document ID
        chats_ref.document(session_id).set(chat_data)
        print(f"✅ Chat saved to Firebase: {session_id}")
    except Exception as e:
        print(f"❌ Error saving chat to Firebase: {e}")

def get_chat_history_from_firebase(user_id: str) -> List[dict]:
    """Get chat history from Firebase"""
    if not firebase_db:
        return []
    
    try:
        chats_ref = firebase_db.collection('users').document(user_id).collection('chats')
        chats_snapshot = chats_ref.get()
        
        if chats_snapshot.exists:
            chats = []
            for chat_doc in chats_snapshot.to_dict():
                # Get all messages for this chat
                messages_ref = firebase_db.collection('users').document(user_id).collection('chats').document(chat_doc['id']).collection('messages')
                messages_snapshot = messages_ref.get()
                
                chat_data = {
                    'id': chat_doc['id'],
                    'lastUpdated': chat_doc.get('lastUpdated', ''),
                    'messages': []
                }
                
                if messages_snapshot.exists:
                    for msg_doc in messages_snapshot.to_dict().values():
                        chat_data['messages'].append({
                            'text': msg_doc.get('message', ''),
                            'sender': msg_doc.get('sender', ''),
                            'timestamp': msg_doc.get('timestamp', '')
                        })
                
                chats.append(chat_data)
            
            # Sort by lastUpdated (newest first)
            chats.sort(key=lambda x: x.get('lastUpdated', ''), reverse=True)
            return chats
        else:
            return []
    except Exception as e:
        print(f"❌ Error getting chat history from Firebase: {e}")
        return []

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

# Add CORS middleware with more permissive settings
print("Setting up CORS middleware...")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # Explicitly include POST
    allow_headers=["*"],
    expose_headers=["*"]  # Expose all headers
)
print("CORS middleware configured with allow_origins=['*']")

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
    message: str
    session_id: str
    user_id: str
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

from dotenv import load_dotenv
load_dotenv()

@app.on_event("startup")
async def startup_event():
    """Initialize SME plugin and MongoDB on startup"""
    global sme_plugin
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            print("❌ ERROR: OPENROUTER_API_KEY not found in environment variables!")
            raise ValueError("OPENROUTER_API_KEY environment variable is required")
        print(f"🔑 Using API Key: {api_key[:20]}...")
        sme_plugin = HotSwappableSMEPlugin(api_key, ExpertiseDomain.FINANCE)
        print("✅ SME Plugin initialized successfully")
        
        # Connect to MongoDB
        connect_to_mongodb()
        
    except Exception as e:
        print(f"❌ Failed to initialize SME Plugin: {e}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "plugin": "SME Plugin API",
        "version": "1.0.1",
        "mongodb_connected": mongo_client is not None,
        "cors_enabled": True,
        "timestamp": str(datetime.now())
    }

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

@app.get("/test-ai")
async def test_ai():
    """Test AI endpoint to verify API is working"""
    try:
        api_key = os.getenv("OPENROUTER_API_KEY")
        print(f"🔑 Test API Key: {api_key[:20] if api_key else 'None'}...")
        
        if not api_key:
            return {"error": "No API key configured"}
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "anthropic/claude-3-haiku",
                "messages": [{"role": "user", "content": "Say hello in exactly 5 words"}],
                "max_tokens": 10,
                "temperature": 0.7
            },
            timeout=30
        )
        
        print(f"📡 Test API Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            ai_answer = result['choices'][0]['message']['content']
            print(f"✅ Test AI Response: {ai_answer}")
            return {"status": "success", "response": ai_answer}
        else:
            print(f"❌ Test API Error: {response.status_code} - {response.text}")
            return {"status": "error", "error": response.text}
            
    except Exception as e:
        print(f"❌ Test Error: {e}")
        return {"status": "error", "error": str(e)}

@app.get("/test-simple")
async def test_simple():
    """Simple test endpoint to verify basic functionality"""
    try:
        return JSONResponse(
            content={"message": "Test successful", "timestamp": str(datetime.now())},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "GET, POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )

@app.options("/chat")
async def chat_options():
    """Handle OPTIONS requests for /chat endpoint"""
    return {
        "status": "allowed",
        "methods": ["POST", "OPTIONS"],
        "headers": ["*"],
        "origins": ["*"]
    }

@app.post("/chat-simple")
async def chat_simple(request: dict):
    """Simple chat endpoint to test basic functionality"""
    try:
        message = request.get("message", "")
        return JSONResponse(
            content={"answer": f"You said: {message}", "confidence": 0.8},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )

@app.post("/chat-basic")
async def chat_basic(request: dict):
    """Basic chat endpoint with no dependencies"""
    try:
        message = request.get("message", "")
        return JSONResponse(
            content={
                "answer": f"I received your message: {message}. This is a basic response to test CORS.",
                "confidence": 0.9,
                "sources": ["Basic test"],
                "methodology": "Direct response",
                "domain": "test",
                "citations": [],
                "disclaimer": "This is a test response."
            },
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS",
                "Access-Control-Allow-Headers": "*"
            }
        )
    except Exception as e:
        return JSONResponse(
            content={"error": str(e)},
            headers={
                "Access-Control-Allow-Origin": "*",
                "Access-Control-Allow-Methods": "POST, OPTIONS", 
                "Access-Control-Allow-Headers": "*"
            }
        )

@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process a chat message using SME expertise with context"""
    print(f"🔍 Received message: {request.message[:50]}...")
    
    if not sme_plugin:
        return ChatResponse(
            answer="Backend service not properly initialized. Please try again.",
            confidence=0.0,
            sources=[],
            methodology="Error",
            domain="finance",
            citations=[],
            reasoning_steps=[],
            disclaimer="Server configuration error"
        )
    
    try:
        # Step 1: Detect the appropriate domain
        detected_domain = sme_plugin.detect_domain(request.message)
        print(f"🎯 Detected domain: {detected_domain.value}")
        
        # Step 2: Switch plugin to detected domain
        sme_plugin.domain = detected_domain
        
        # Step 3: Process query with full SME capabilities
        result = sme_plugin.process_query(
            query=request.message,
            query_type="general",
            context=request.context
        )
        
        # Remove duplicate numbered lists and paragraphs - ULTRA AGGRESSIVE
        print(f"🔍 Starting ultra-aggressive deduplication...")
        lines = result.answer.split('\n')
        seen_content = set()
        unique = []
        duplicates_removed = 0
        
        # First pass: detect if response has numbered lists
        has_numbered_lists = sum(1 for line in lines if re.match(r'^\d+\.\s', line)) > 3
        
        if has_numbered_lists:
            print("⚠️ Detected numbered list pattern - applying strict deduplication")
            # For numbered lists, keep only first occurrence of each item
            for line in lines:
                # Normalize: remove ALL numbers, citations, whitespace
                norm = re.sub(r'^\d+\.\s*', '', line)  # Remove leading numbers
                norm = re.sub(r'\[\d+\]', '', norm)  # Remove citations
                norm = re.sub(r'\d+\.', '', norm)  # Remove any other numbers
                norm = ' '.join(norm.lower().split())  # Normalize whitespace
                
                # Skip empty lines
                if not norm:
                    if len(unique) > 0 and unique[-1] != '':
                        unique.append(line)
                    continue
                
                # Skip if we've seen this content (exact match)
                if norm in seen_content:
                    duplicates_removed += 1
                    continue
                
                seen_content.add(norm)
                unique.append(line)
        else:
            # For paragraph responses, use similarity-based deduplication
            for line in lines:
                norm = re.sub(r'\[\d+\]', '', line)
                norm = ' '.join(norm.lower().split())
                
                if not norm:
                    unique.append(line)
                    continue
                
                if norm in seen_content:
                    duplicates_removed += 1
                    continue
                
                # Check 80% similarity for paragraphs
                is_duplicate = False
                for seen in seen_content:
                    if len(norm) > 20 and len(seen) > 20:
                        norm_words = set(norm.split())
                        seen_words = set(seen.split())
                        if len(norm_words) > 0:
                            similarity = len(norm_words & seen_words) / len(norm_words)
                            if similarity > 0.8:
                                is_duplicate = True
                                duplicates_removed += 1
                                break
                
                if not is_duplicate:
                    seen_content.add(norm)
                    unique.append(line)
        
        result.answer = '\n'.join(unique)
        print(f"📊 Removed {duplicates_removed} duplicate/similar lines from {len(lines)} total")
        
        print(f"✅ Generated response with {len(result.citations)} citations")
        print(f"📚 Citations: {result.citations}")

        # Return structured response with proper domain and citations
        return ChatResponse(
            answer=result.answer,
            confidence=result.confidence,
            sources=result.sources,
            methodology=result.methodology,
            domain=result.domain.value,
            citations=result.citations,
            reasoning_steps=result.reasoning_steps,
            disclaimer=result.disclaimer
        )
            
    except Exception as e:
        print(f"❌ Error processing query: {e}")
        import traceback
        traceback.print_exc()
        
        return ChatResponse(
            answer=f"I'm experiencing technical difficulties. Please try rephrasing your question or try again.",
            confidence=0.3,
            sources=[],
            methodology="Error handling",
            domain="finance",
            citations=[],
            reasoning_steps=[],
            disclaimer="Service temporarily unavailable"
        )

@app.get("/context/{session_id}")
async def get_context(session_id: str):
    """Get conversation context for a session"""
    if not mongo_client:
        return {"context": ""}
    
    context = get_context_from_mongodb(session_id)
    return {"context": context}

@app.post("/save_message")
async def save_message(request: SaveMessageRequest):
    """Save a message to Firebase"""
    if not firebase_db:
        raise HTTPException(status_code=500, detail="Firebase not initialized")
    
    try:
        save_chat_to_firebase(
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
        return {"message": "Message saved successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/history/{session_id}")
async def get_chat_history(session_id: str, limit: int = 50):
    """Get chat history for a specific session"""
    try:
        history = get_chat_history_from_mongodb(session_id, limit)
        return {"messages": history}
    except Exception as e:
        return {"messages": [], "error": str(e)}

@app.get("/user-history/{user_id}")
async def get_user_chat_history(user_id: str, limit: int = 50):
    """Get all chat sessions for a specific user"""
    try:
        history = get_user_chat_sessions_from_mongodb(user_id, limit)
        return {"sessions": history}
    except Exception as e:
        return {"sessions": [], "error": str(e)}

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

def get_user_chat_sessions_from_mongodb(user_id: str, limit: int = 50) -> List[dict]:
    """Get all chat sessions for a specific user"""
    if sessions_collection is None:
        return []
    
    try:
        # Get all sessions for this user, sorted by most recent
        sessions = list(
            sessions_collection.find({"user_id": user_id})
            .sort("updated_at", -1)
            .limit(limit)
        )
        
        # Convert ObjectId to string and format
        for session in sessions:
            session["_id"] = str(session["_id"])
            if "updated_at" in session:
                session["updated_at"] = session["updated_at"].isoformat()
            if "created_at" in session:
                session["created_at"] = session["created_at"].isoformat()
        
        return sessions
        
    except Exception as e:
        print(f"Error getting user sessions: {e}")
        return []

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
        "cors_enabled": True,
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

@app.get("/test-cors")
async def test_cors():
    """Test CORS endpoint"""
    return {
        "message": "CORS test successful",
        "timestamp": str(datetime.now()),
        "origin": "any origin allowed"
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
