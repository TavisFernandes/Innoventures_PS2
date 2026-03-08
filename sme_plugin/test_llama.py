#!/usr/bin/env python3
"""
Quick test script for SME Plugin with Llama 3.2 3B
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from core.plugin import SMEPlugin
from core.strategy import FinanceStrategy
from rag.retriever import FinanceRetriever
from llms.factory import get_llm
import yaml

def load_config():
    with open("config.yaml", "r") as f:
        return yaml.safe_load(f)

def main():
    print("Testing SME Plugin with Llama 3.2 3B...")
    
    # Load config
    cfg = load_config()
    
    # Initialize components
    print("1. Loading LLM...")
    llm = get_llm(
        model_type="llama",
        model_name=cfg["model"]["llama_model_name"],
        use_ollama=cfg["model"]["use_ollama"],
        temperature=cfg["model"]["temperature"],
        top_p=cfg["model"]["top_p"],
        max_tokens=cfg["model"]["max_tokens"],
        num_ctx=cfg["model"]["num_ctx"]
    )
    
    print("2. Loading retriever...")
    retriever = FinanceRetriever()
    retriever.top_k = cfg["rag"]["top_k"]
    
    print("3. Creating plugin...")
    strategy = FinanceStrategy()
    plugin = SMEPlugin(strategy=strategy, llm=llm, retriever=retriever)
    
    print("4. Testing query...")
    test_query = "What is financial risk management?"
    
    try:
        response = plugin.process_query(test_query)
        print(f"\n✅ Success! Response ({len(response)} chars):")
        print("-" * 50)
        print(response)
        print("-" * 50)
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
