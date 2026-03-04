#!/usr/bin/env python3
"""
Redirect to the correct API server
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

# Import and run the correct server
from api_server import app
import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
