#!/usr/bin/env python3
"""
PlugMind - Start the Finance Expert web app
Uses direct Backend import (default). For API mode: set PLUGMIND_API=1 and run python run_api.py first.
"""
import os
import subprocess
import sys

def main():
    project_root = os.path.dirname(os.path.abspath(__file__))
    frontend_app = os.path.join(project_root, 'Frontend', 'app.py')
    
    if not os.path.exists(frontend_app):
        print("❌ Frontend app not found. Expected:", frontend_app)
        sys.exit(1)
    
    os.chdir(project_root)
    print(">> Starting PlugMind Finance Expert...")
    print("   Open http://localhost:8501 in your browser")
    print("   Press Ctrl+C to stop\n")
    
    subprocess.run(
        [sys.executable, "-m", "streamlit", "run", frontend_app, "--server.headless", "true"],
        cwd=project_root
    )

if __name__ == "__main__":
    main()
