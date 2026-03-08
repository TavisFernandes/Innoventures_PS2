#!/usr/bin/env python3
"""
Test response time improvements
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

def test_response_times():
    print("🚀 Testing Optimized Response Times...")
    print("=" * 50)
    
    # Load optimized config
    cfg = load_config()
    
    # Initialize components
    print("1. Loading optimized LLM...")
    start_time = time.time()
    
    llm = get_llm(
        model_type="llama",
        model_name=cfg["model"]["llama_model_name"],
        use_ollama=cfg["model"]["use_ollama"],
        temperature=cfg["model"]["temperature"],
        top_p=cfg["model"]["top_p"],
        max_tokens=cfg["model"]["max_tokens"],
        num_ctx=cfg["model"]["num_ctx"],
        repeat_penalty=cfg["model"]["repeat_penalty"],
        stop=cfg["model"]["stop"]
    )
    
    retriever = FinanceRetriever()
    retriever.top_k = cfg["rag"]["top_k"]
    
    strategy = FinanceStrategy()
    plugin = SMEPlugin(strategy=strategy, llm=llm, retriever=retriever)
    
    init_time = time.time() - start_time
    print(f"   Initialization: {init_time:.2f}s")
    
    # Test queries with timing
    test_queries = [
        "What is financial risk management?",
        "How to assess loan eligibility?",
        "What are key financial metrics?",
        "Explain credit risk analysis",
        "What is market volatility?"
    ]
    
    print(f"\n2. Testing {len(test_queries)} queries...")
    total_time = 0
    successful_responses = 0
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n   Query {i}: {query[:50]}...")
        
        query_start = time.time()
        try:
            response = plugin.process_query(query)
            query_time = time.time() - query_start
            total_time += query_time
            successful_responses += 1
            
            print(f"     ✅ Response ({len(response)} chars) in {query_time:.1f}s")
            print(f"     📝 Preview: {response[:100]}...")
            
            # Check if response time meets target
            if query_time <= 20:
                print(f"     🎯 Target met! (<20s)")
            else:
                print(f"     ⚠️  Over target: {query_time-20:.1f}s too slow")
                
        except Exception as e:
            print(f"     ❌ Error: {e}")
    
    # Summary
    if successful_responses > 0:
        avg_time = total_time / successful_responses
        print(f"\n📊 Performance Summary:")
        print(f"   Successful queries: {successful_responses}/{len(test_queries)}")
        print(f"   Average response time: {avg_time:.1f}s")
        print(f"   Total time: {total_time:.1f}s")
        
        if avg_time <= 20:
            print(f"   ✅ SUCCESS: Average response time meets 15-20s target!")
        else:
            print(f"   ⚠️  NEEDS WORK: Average is {avg_time-20:.1f}s over target")
    
    return successful_responses > 0 and avg_time <= 20

if __name__ == "__main__":
    success = test_response_times()
    sys.exit(0 if success else 1)
