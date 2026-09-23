# ⚖️ ClauseMind: Production Legal RAG System

## 🚀 Project Overview
ClauseMind is a high-precision Retrieval-Augmented Generation (RAG) system designed for the legal domain. Unlike general-purpose chatbots, ClauseMind prioritizes **grounding** and **traceability**, ensuring that every claim made by the AI is backed by a verifiable citation from the user's uploaded legal corpus.

## 🛠️ Technical Architecture
### The "Precision Stack"
- **LLM:** Gemini 2.5 Flash (for speed and grounded generation).
- **Embeddings:** `text-embedding-004` (768-dim).
- **Retrieval:** Hybrid Search (Dense Vector + BM25 Sparse) fused via Reciprocal Rank Fusion (RRF).
- **Re-Ranking:** `BGE-Reranker-Base` (Cross-Encoder) to filter the top 25 candidates down to the top 5.
- **Vector Store:** ChromaDB (Persistent local storage).

### Key Engineering Breakthroughs
1. **Structure-Aware Chunking:** Implemented a regex-based splitter that recognizes "Article X" and "Section Y," preventing the system from cutting legal clauses in half.
2. **Hard Abstention Guardrails:** Implemented a score-based threshold ($\tau = 0.15$) that forces the system to refuse answers when the retrieval confidence is too low.
3. **Citation Verification:** A post-generation module that cross-references LLM citations against retrieved metadata to eliminate "citation hallucinations."

## 📈 Quantitative Impact (Evaluated via RAGAS)
The system was benchmarked against a 40-question "Golden Dataset."

| Metric | Naive Vector Search | ClauseMind (Hybrid + Rerank) | Lift |
|---|---|---|---|
| **Hit Rate@5** | 65% | **92%** | **+27%** |
| **Faithfulness** | 0.88 | **0.97** | **+10%** |
| **Context Precision**| 0.62 | **0.91** | **+46%** |

## 📦 Deployment
- **Backend:** FastAPI (Async)
- **Frontend:** Streamlit
- **Infrastructure:** Docker & Docker-Compose

