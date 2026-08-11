"""
Centralized configuration loader for the Multi-Document RAG Legal Assistant.

Loads settings from environment variables (via .env file) and provides
typed, validated access to all configuration values.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# Load .env from project root
# ---------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")


# ---------------------------------------------------------------------------
# API Keys
# ---------------------------------------------------------------------------
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

# ---------------------------------------------------------------------------
# Model Configuration
# ---------------------------------------------------------------------------
EMBEDDING_MODEL: str = os.getenv("EMBEDDING_MODEL", "text-embedding-004")
GENERATION_MODEL: str = os.getenv("GENERATION_MODEL", "gemini-2.5-flash")

# ---------------------------------------------------------------------------
# ChromaDB Configuration
# ---------------------------------------------------------------------------
CHROMA_PERSIST_DIR: str = os.getenv("CHROMA_PERSIST_DIR", str(PROJECT_ROOT / "chroma_data"))
CHROMA_COLLECTION_NAME: str = os.getenv("CHROMA_COLLECTION_NAME", "legal_docs")

# ---------------------------------------------------------------------------
# Chunking Configuration
# ---------------------------------------------------------------------------
CHUNK_SIZE: int = int(os.getenv("CHUNK_SIZE", "1000"))
CHUNK_OVERLAP: int = int(os.getenv("CHUNK_OVERLAP", "200"))

# ---------------------------------------------------------------------------
# Retrieval Configuration
# ---------------------------------------------------------------------------
TOP_K_RESULTS: int = int(os.getenv("TOP_K_RESULTS", "10"))
RERANK_TOP_K: int = int(os.getenv("RERANK_TOP_K", "5"))

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
DATA_RAW_DIR: Path = PROJECT_ROOT / "data" / "raw"
DOCS_DIR: Path = PROJECT_ROOT / "docs"
EVAL_DIR: Path = PROJECT_ROOT / "eval"

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


def validate_config() -> None:
    """Validate that all required configuration values are present."""
    errors = []

    if not GEMINI_API_KEY:
        errors.append("GEMINI_API_KEY is not set. Create a .env file from .env.example.")

    if errors:
        raise EnvironmentError(
            "Configuration validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
        )


if __name__ == "__main__":
    # Quick config check
    print("=" * 60)
    print("Configuration Summary")
    print("=" * 60)
    print(f"  Project Root:      {PROJECT_ROOT}")
    print(f"  Gemini API Key:    {'***' + GEMINI_API_KEY[-4:] if len(GEMINI_API_KEY) > 4 else '(not set)'}")
    print(f"  Embedding Model:   {EMBEDDING_MODEL}")
    print(f"  Generation Model:  {GENERATION_MODEL}")
    print(f"  Chroma Dir:        {CHROMA_PERSIST_DIR}")
    print(f"  Chunk Size:        {CHUNK_SIZE}")
    print(f"  Chunk Overlap:     {CHUNK_OVERLAP}")
    print(f"  Top-K Results:     {TOP_K_RESULTS}")
    print(f"  Re-rank Top-K:     {RERANK_TOP_K}")
    print(f"  Data Raw Dir:      {DATA_RAW_DIR}")
    print(f"  Log Level:         {LOG_LEVEL}")
    print("=" * 60)

    try:
        validate_config()
        print("[OK] Configuration is valid.")
    except EnvironmentError as e:
        print(f"[FAIL] {e}")
