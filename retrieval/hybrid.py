"""
Hybrid retrieval combining dense (Chroma) and sparse (BM25) search.

Includes weighted score merging, deduplication, and re-ranking via bge-reranker-base.
Implemented in Phase 3.
"""
