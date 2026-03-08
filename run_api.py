#!/usr/bin/env python3
"""
PlugMind Backend API - Start the FastAPI server
Frontend syncs with this when running. Run frontend: python run_app.py
"""
import os
import sys

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    backend_dir = os.path.join(project_root, 'Backend')
    os.chdir(backend_dir)
    sys.path.insert(0, backend_dir)
    
    print(">> Starting PlugMind Backend API...")
    print("   API: http://localhost:8000")
    print("   Docs: http://localhost:8000/docs")
    print("   Then run: python run_app.py (frontend)")
    print("   Press Ctrl+C to stop\n")
    
    import uvicorn
    uvicorn.run("main_api:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
