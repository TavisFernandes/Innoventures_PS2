#!/usr/bin/env python3
"""
Quick test of actual application
"""
import sys
import os
import time
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
    print("🚀 Quick Test - Ultra-Optimized SME Plugin")
    print("=" * 50)
    
    cfg = load_config()
    
    # Initialize
    print("Loading components...")
    retriever = FinanceRetriever()
    retriever.top_k = cfg["rag"]["top_k"]
    
    llm = get_llm(
        model_type="llama",
        model_name=cfg["model"]["llama_model_name"],
        use_ollama=cfg["model"]["use_ollama"],
        temperature=cfg["model"]["temperature"],
        top_p=cfg["model"]["top_p"],
        max_tokens=cfg["model"]["max_tokens"],
        num_ctx=cfg["model"]["num_ctx"],
        repeat_penalty=cfg["model"]["repeat_penalty"],
        stop=cfg["model"]["stop"],
        mirostat=cfg["model"]["mirostat"],
        mirostat_eta=cfg["model"]["mirostat_eta"],
        mirostat_tau=cfg["model"]["mirostat_tau"]
    )
    
    strategy = FinanceStrategy()
    plugin = SMEPlugin(strategy=strategy, llm=llm, retriever=retriever)
    
    # Test single query
    query = "What is financial risk management?"
    print(f"\nTesting: {query}")
    
    start_time = time.time()
    response = plugin.process_query(query)
    elapsed = time.time() - start_time
    
    print(f"\nResponse time: {elapsed:.1f}s")
    print(f"Response length: {len(response)} chars")
    print(f"Target met: {'✅ YES' if elapsed <= 20 else '❌ NO'}")
    print(f"\nResponse:\n{response}")
    
    return elapsed <= 20

if __name__ == "__main__":
    success = main()
    print(f"\n{'✅ SUCCESS' if success else '❌ FAILED'}: Ultra-optimized test completed")
