#!/usr/bin/env python3
"""
Performance test for optimized document ingestion
"""
import sys
import os
import time
import tempfile
import shutil
sys.path.insert(0, os.path.dirname(__file__))

from rag.retriever import FinanceRetriever

def create_test_documents(num_docs: int = 5) -> list[str]:
    """Create test documents for performance testing"""
    temp_dir = tempfile.mkdtemp()
    doc_paths = []
    
    # Sample financial content
    content = """
    Financial Risk Management Report
    
    Executive Summary:
    This report outlines the key financial risks identified in Q3 2024.
    Market volatility has increased significantly due to geopolitical tensions.
    
    Risk Categories:
    1. Market Risk: Increased volatility in equity and bond markets
    2. Credit Risk: Deterioration in corporate credit ratings
    3. Operational Risk: System vulnerabilities in trading platforms
    
    Mitigation Strategies:
    - Diversification of investment portfolios
    - Enhanced credit scoring models
    - System upgrades and redundancy measures
    
    Financial Metrics:
    - VaR (95%): $2.5M
    - Expected Shortfall: $4.2M
    - Risk-Adjusted Return: 8.3%
    
    Conclusion:
    Proactive risk management is essential for maintaining financial stability.
    Regular monitoring and adjustment of risk mitigation strategies are recommended.
    """
    
    for i in range(num_docs):
        # Create both PDF and text files
        txt_path = os.path.join(temp_dir, f"test_report_{i+1}.txt")
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(f"Document {i+1}\n{content}")
        doc_paths.append(txt_path)
    
    return doc_paths, temp_dir

def test_ingestion_performance():
    """Test the performance of optimized document ingestion"""
    print("🚀 Testing Optimized Document Ingestion Performance")
    print("=" * 60)
    
    # Create test documents
    print("Creating test documents...")
    doc_paths, temp_dir = create_test_documents(5)
    
    try:
        # Test optimized retriever
        print("\n1. Testing Optimized FinanceRetriever...")
        retriever = FinanceRetriever()
        
        start_time = time.time()
        retriever.add_documents(doc_paths)
        ingestion_time = time.time() - start_time
        
        print(f"\n📊 Performance Results:")
        print(f"   Documents processed: {len(doc_paths)}")
        print(f"   Total chunks created: {len(retriever._documents)}")
        print(f"   Ingestion time: {ingestion_time:.3f} seconds")
        print(f"   Avg time per document: {ingestion_time/len(doc_paths):.3f} seconds")
        print(f"   Chunks per second: {len(retriever._documents)/ingestion_time:.1f}")
        
        # Test query performance
        print("\n2. Testing Query Performance...")
        test_queries = [
            "What is market risk?",
            "How to mitigate credit risk?",
            "What are the financial metrics?"
        ]
        
        query_start = time.time()
        for query in test_queries:
            results = retriever.invoke(query)
            print(f"   Query: '{query}' -> {len(results)} results")
        
        query_time = time.time() - query_start
        print(f"   Total query time: {query_time:.3f} seconds")
        print(f"   Avg time per query: {query_time/len(test_queries):.3f} seconds")
        
        print(f"\n✅ Performance test completed successfully!")
        
    finally:
        # Cleanup
        shutil.rmtree(temp_dir)
        print("🧹 Test documents cleaned up")

if __name__ == "__main__":
    test_ingestion_performance()
