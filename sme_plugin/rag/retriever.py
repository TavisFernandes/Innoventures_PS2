import os
import math
import time
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Set
from langchain_community.document_loaders import PyPDFLoader, TextLoader
from langchain_core.documents import Document

class FinanceRetriever:
    """Optimized RAG retriever using pure-Python TF-IDF with parallel processing"""

    def __init__(self, **kwargs):
        self._documents: list[Document] = []
        self._doc_words: list[Counter] = []   # word counts per doc
        self._idf: dict[str, float] = {}
        self._idf_cache: dict[str, float] = {}  # Cache for IDF calculations
        self.top_k = 5
        self._batch_size = 10  # Process documents in batches
        self._idf_dirty = False  # Track if IDF needs rebuild

    def invoke(self, query: str) -> list[Document]:
        if not self._documents:
            return []
        
        # Rebuild IDF only if needed (lazy evaluation)
        if self._idf_dirty:
            self._rebuild_idf()
            self._idf_dirty = False
            
        query_words = self._tokenize(query)
        scores = []
        for i, wc in enumerate(self._doc_words):
            score = sum(wc.get(w, 0) * self._idf.get(w, 0) for w in query_words)
            scores.append((score, i))
        scores.sort(reverse=True, key=lambda x: x[0])
        return [self._documents[i] for _, i in scores[: self.top_k] if _ > 0]

    def add_document(self, file_path: str):
        """Add a single document (kept for compatibility)"""
        self.add_documents([file_path])

    def add_documents(self, file_paths: List[str]):
        """Add multiple documents with parallel processing"""
        start_time = time.time()
        total_chunks = 0
        
        # Process documents in batches to avoid memory issues
        for i in range(0, len(file_paths), self._batch_size):
            batch = file_paths[i:i + self._batch_size]
            batch_chunks = self._process_document_batch(batch)
            total_chunks += batch_chunks
            
        # Rebuild IDF once after all documents are processed
        if self._idf_dirty:
            self._rebuild_idf()
            self._idf_dirty = False
            
        elapsed = time.time() - start_time
        print(f"  ✅ Processed {len(file_paths)} documents, {total_chunks} chunks in {elapsed:.2f}s")

    def _process_document_batch(self, file_paths: List[str]) -> int:
        """Process a batch of documents in parallel"""
        total_chunks = 0
        
        with ThreadPoolExecutor(max_workers=min(4, len(file_paths))) as executor:
            # Submit all document processing tasks
            future_to_path = {
                executor.submit(self._load_single_document, path): path 
                for path in file_paths
            }
            
            # Collect results as they complete
            for future in as_completed(future_to_path):
                path = future_to_path[future]
                try:
                    docs = future.result()
                    if docs:
                        self._documents.extend(docs)
                        for d in docs:
                            self._doc_words.append(Counter(self._tokenize(d.page_content)))
                        total_chunks += len(docs)
                        print(f"  Added {len(docs)} chunk(s) from {os.path.basename(path)}")
                    else:
                        print(f"  Skipped: {os.path.basename(path)} (unsupported format)")
                except Exception as e:
                    print(f"  Error processing {os.path.basename(path)}: {e}")
        
        if total_chunks > 0:
            self._idf_dirty = True
            
        return total_chunks

    def _load_single_document(self, file_path: str) -> List[Document]:
        """Load a single document (used by parallel processing)"""
        try:
            if file_path.endswith(".pdf"):
                loader = PyPDFLoader(file_path)
            elif file_path.endswith(".txt"):
                loader = TextLoader(file_path, encoding="utf-8")
            else:
                return []
            
            docs = loader.load_and_split()
            return docs if docs else []
        except Exception:
            return []

    # ── internal helpers ─────────────────────────────────────────
    @staticmethod
    def _tokenize(text: str) -> list[str]:
        """Optimized tokenization with better filtering"""
        # More efficient tokenization
        words = []
        for w in text.lower().split():
            # Remove punctuation and filter short words
            clean_word = w.strip(".,;:!?()[]{}\"'`~@#$%^&*+=|\\<>")
            if len(clean_word) > 2 and clean_word.isalnum():
                words.append(clean_word)
        return words

    def _rebuild_idf(self):
        """Optimized IDF calculation with caching"""
        start_time = time.time()
        n = len(self._doc_words)
        if n == 0:
            return
            
        # Get all unique words more efficiently
        all_words: Set[str] = set()
        for wc in self._doc_words:
            all_words.update(wc.keys())
        
        # Calculate IDF with caching
        self._idf = {}
        for w in all_words:
            # Check cache first
            if w in self._idf_cache:
                self._idf[w] = self._idf_cache[w]
                continue
                
            # Calculate document frequency
            df = sum(1 for wc in self._doc_words if w in wc)
            idf_value = math.log((n + 1) / (df + 1)) + 1
            
            self._idf[w] = idf_value
            self._idf_cache[w] = idf_value  # Cache for future use
        
        elapsed = time.time() - start_time
        print(f"  🔢 IDF rebuilt for {len(all_words)} terms in {elapsed:.3f}s")
