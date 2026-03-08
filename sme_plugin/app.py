"""
SME-Plug: Finance Expert Module — Main Entry Point
Reads config.yaml, sets up the RAG pipeline, starts the directory watcher,
and runs an interactive chat loop.
"""
import os
import sys
import yaml
from threading import Thread
from dotenv import load_dotenv

# Auto-load .env (picks up GOOGLE_API_KEY)
load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

sys.path.insert(0, os.path.dirname(__file__))

from core.plugin import SMEPlugin
from core.strategy import FinanceStrategy
from rag.retriever import FinanceRetriever
from rag.watcher import DocumentWatcher
from llms.factory import get_llm
from adapters.langchain_tool import SMEPluginTool


def load_config(path: str = None) -> dict:
    if path is None:
        path = os.path.join(os.path.dirname(__file__), "config.yaml")
    with open(path, "r") as f:
        return yaml.safe_load(f)


def ingest_existing_docs(retriever: FinanceRetriever, docs_dir: str):
    """Ingest any documents already present in docs_dir on startup using optimized batch processing."""
    if not os.path.exists(docs_dir):
        os.makedirs(docs_dir)
        return
    
    # Collect all document files
    doc_files = []
    for fname in os.listdir(docs_dir):
        fpath = os.path.join(docs_dir, fname)
        if os.path.isfile(fpath) and (fname.endswith(".pdf") or fname.endswith(".txt")):
            doc_files.append(fpath)
    
    if doc_files:
        print(f"  Found {len(doc_files)} documents to ingest...")
        # Use optimized batch processing
        retriever.add_documents(doc_files)
    else:
        print("  No existing documents found.")


def start_watcher(watch_dir: str, retriever: FinanceRetriever) -> DocumentWatcher:
    watcher = DocumentWatcher(watch_dir=watch_dir, retriever=retriever)
    watcher_thread = Thread(target=watcher.start, daemon=True)
    watcher_thread.start()
    return watcher


def main():
    print("=" * 60)
    print("  SME-Plug: Finance Expert Module")
    print("=" * 60)

    cfg = load_config()
    model_type = cfg["model"]["type"]
    docs_dir = os.path.join(os.path.dirname(__file__), cfg["rag"]["docs_dir"])
    top_k = cfg["rag"].get("top_k", 5)

    # ── Step 1: Lightweight RAG retriever (TF-IDF, no API needed) ─
    print("\n[1/4] Initializing RAG Retriever (TF-IDF)...")
    retriever = FinanceRetriever()
    retriever.top_k = top_k

    # ── Step 2: Ingest existing docs ────────────────────────────
    print("[2/4] Ingesting existing documents...")
    ingest_existing_docs(retriever, docs_dir)

    # ── Step 3: Start live directory watcher ────────────────────
    print("[3/4] Starting live document watcher...")
    watcher = start_watcher(docs_dir, retriever)

    # ── Step 4: Load LLM ────────────────────────────────────────
    print(f"[4/4] Loading LLM backend ({model_type})...")
    try:
        if model_type == "llama":
            llm = get_llm(
                model_type="llama",
                model_name=cfg["model"].get("llama_model_name", "llama3.2:3b"),
                use_ollama=cfg["model"].get("use_ollama", True),
                temperature=cfg["model"].get("temperature", 0.01),
                top_p=cfg["model"].get("top_p", 0.5),
                max_tokens=cfg["model"].get("max_tokens", 150),
                num_ctx=cfg["model"].get("num_ctx", 512),
                repeat_penalty=cfg["model"].get("repeat_penalty", 1.2),
                stop=cfg["model"].get("stop", ["\n\n", "###", "--", "•", "1.", "2."]),
                mirostat=cfg["model"].get("mirostat", 2),
                mirostat_eta=cfg["model"].get("mirostat_eta", 0.1),
                mirostat_tau=cfg["model"].get("mirostat_tau", 5.0)
            )
        else:
            llm = get_llm(
                model_type="gemini",
                model_name=cfg["model"].get("gemini_model_name", "gemini-2.0-flash"),
            )
    except Exception as e:
        print(f"\n✖ Failed to load {model_type}: {e}")
        print("  Make sure your API key / Ollama server is configured.")
        sys.exit(1)

    # ── Assemble plugin ─────────────────────────────────────────
    strategy = FinanceStrategy()
    plugin = SMEPlugin(strategy=strategy, llm=llm, retriever=retriever)
    tool = SMEPluginTool(plugin=plugin)

    print("\n" + "=" * 60)
    print("  ✔ Plugin ready!")
    print(f"  Tool name : {tool.name}")
    print(f"  Model     : {model_type}")
    print(f"  Docs dir  : {docs_dir}")
    print("  Drop new PDF/TXT files into the docs folder — they")
    print("  will be auto-ingested into the knowledge base.")
    print("  Type 'exit' to quit.")
    print("=" * 60 + "\n")

    while True:
        try:
            user_input = input("You > ")
            if user_input.strip().lower() in ("exit", "quit"):
                break
            if not user_input.strip():
                continue

            print("\nThinking like a Financial Analyst...\n")
            response = plugin.process_query(user_input)
            print(f"Expert >\n{response}\n")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}\n")

    watcher.stop()
    print("Goodbye!")


if __name__ == "__main__":
    main()
