#!/usr/bin/env python3
"""
Test with actual documents
"""
import sys
import os
import time
sys.path.insert(0, os.path.dirname(__file__))

from rag.retriever import FinanceRetriever

print('🚀 Testing with actual documents...')
retriever = FinanceRetriever()

# Get actual docs
docs_dir = './docs'
doc_files = []
for fname in os.listdir(docs_dir):
    fpath = os.path.join(docs_dir, fname)
    if os.path.isfile(fpath) and (fname.endswith('.pdf') or fname.endswith('.txt')):
        doc_files.append(fpath)

print(f'Found {len(doc_files)} actual documents')

start_time = time.time()
retriever.add_documents(doc_files)
ingestion_time = time.time() - start_time

print(f'\n📊 Real Document Performance:')
print(f'   Documents: {len(doc_files)}')
print(f'   Chunks: {len(retriever._documents)}')
print(f'   Time: {ingestion_time:.3f}s')
print(f'   Speed: {len(doc_files)/ingestion_time:.1f} docs/sec')
