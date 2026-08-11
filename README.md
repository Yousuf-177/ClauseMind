# Multi-Document RAG Legal Assistant

A production-quality Retrieval-Augmented Generation (RAG) system for legal document analysis. Upload multiple legal documents — contracts, case law, SEC filings, EULAs, statutes — and ask natural-language questions to get accurate, citation-backed answers referencing specific documents, clauses, and page numbers.

---

## Features

- **Multi-Document Ingestion** — Parse PDFs with page-number preservation using PyMuPDF
- **Intelligent Chunking** — Recursive character splitting + regex-based legal clause segmentation
- **Hybrid Retrieval** — Dense (Gemini embeddings + ChromaDB) + Sparse (BM25) search with re-ranking
- **Grounded Generation** — Gemini-powered answers with inline citations (document, section, page)
- **Citation Verification** — Automated checks that cited text actually supports the claim
- **Hallucination Guardrails** — Abstains when evidence is insufficient
- **Cross-Document Analysis** — Compare clauses, terms, and provisions across multiple documents
- **Evaluation Harness** — RAGAS-based metrics: faithfulness, relevance, precision, recall

## Tech Stack

| Layer | Technology |
|-------|------------|
| PDF Parsing | PyMuPDF (fitz) |
| Chunking | RecursiveCharacterTextSplitter + Regex Clause Splitter |
| Embeddings | Gemini `text-embedding-004` |
| Vector DB | ChromaDB (local) |
| Sparse Retrieval | BM25 (`rank_bm25`) |
| Re-ranker | `bge-reranker-base` (HuggingFace) |
| LLM | Gemini 2.5 Pro/Flash (`google-genai`) |
| Backend | FastAPI |
| Frontend | Streamlit |
| Evaluation | RAGAS |
| Deployment | Docker → Render + Streamlit Community Cloud |

## Project Structure

```
Legal_Assistant/
├── ingestion/          # PDF parsing and chunking
├── retrieval/          # Vector search, BM25, hybrid scoring, re-ranking
├── generation/         # LLM prompts, citation logic, guardrails
├── eval/               # RAGAS evaluation harness
├── api/                # FastAPI backend
├── ui/                 # Streamlit frontend
├── config/             # Centralized configuration
├── data/raw/           # Test corpus (legal documents)
├── docs/               # Project documentation
├── scripts/            # Utility scripts
└── tests/              # Unit and integration tests
```

## Quick Start

### Prerequisites

- Python 3.10+
- Gemini API key ([Get one here](https://aistudio.google.com/apikey))

### Setup

```bash
# Clone the repository
git clone <repo-url>
cd Legal_Assistant

# Create virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Verify setup
python scripts/test_gemini.py
```

## License

This project is for educational and portfolio purposes.

## Disclaimer

This system provides information retrieval and text-based analysis. It does **not** provide legal advice. Outputs should not be treated as legal counsel.
