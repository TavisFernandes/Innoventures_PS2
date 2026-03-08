# PlugMind
HackX 4.0 project by team Innoventures.

## Overview
PlugMind is an AI-powered Subject Matter Expert (SME) platform designed to provide comprehensive, high-confidence, and properly cited answers across specialized domains. Built originally with a strong focus on Finance and Stock Market analysis, PlugMind's modular architecture allows it to integrate with various AI agents and frameworks to prevent hallucinations and ensure accurate responses in high-stakes environments.

## Architecture
The platform is divided into two main components:
- **Frontend**: A modern web application built with Next.js, React, TypeScript, and Tailwind CSS.
- **Backend**: A robust Python FastAPI server that manages the SME plugins, handles Large Language Model (LLM) communications (e.g., Claude-3-Haiku via OpenRouter), Retrieval-Augmented Generation (RAG), and data adapters.

## Key Features
- 🤖 **AI-Powered SME Plugins**: Specialized experts (e.g., Finance, Stock Market, Loan Approval) that provide detailed analysis, predictions, and recommendations.
- 📚 **Citations & Sourcing**: All answers include proper citations to authoritative sources, enhancing trust and reliability.
- 📊 **Confidence Ratings**: The system evaluates its own responses and provides a confidence score alongside the methodology used.
- 🧩 **Modular Design**: Easy integration of new subject matter experts through the `sme_plugin` architecture.
- ⚡ **Fast & Responsive UI**: A sleek, real-time chat interface built with Next.js and Tailwind CSS.

## Getting Started

### Prerequisites
- Node.js (for Next.js frontend)
- Python 3.7+ (for FastAPI backend)

### Backend Setup
1. Navigate to the `Backend` directory:
   ```bash
   cd Backend
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the API server:
   ```bash
   python api_server.py
   ```
   *(Alternatively, run `python run_api.py` from the root project directory).*

### Frontend Setup
1. Navigate to the `Frontend` directory:
   ```bash
   cd Frontend
   ```
2. Install the frontend dependencies (if using npm):
   ```bash
   npm install
   ```
3. Start the Next.js development server:
   ```bash
   npm run dev
   ```
4. Open your browser and navigate to `http://localhost:3000`.

## Project Structure
```text
PlugMind/
├── Backend/                 # Python FastAPI server and SME logic
│   ├── core/                # Core strategy and plugin classes
│   ├── llms/                # LLM factory and integration
│   ├── rag/                 # Retrieval-Augmented Generation module
│   └── docs/                # Sample knowledge base documents
├── Frontend/                # Next.js web application
│   ├── src/components/      # React UI components (Chat panels, inputs, etc.)
│   └── src/lib/             # Frontend interfaces and API logic (`api.ts`)
├── sme_plugin/              # Custom SME plugin definitions 
└── sme_plugin_api/          # API interfaces for the plugins
```

## License
MIT License
