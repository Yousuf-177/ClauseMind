"""
Gemini API Hello-World Test Script

Validates that both the embedding and generation endpoints of the Gemini API
work correctly through the google-genai SDK.

Usage:
    python scripts/test_gemini.py

Prerequisites:
    1. Create a .env file from .env.example
    2. Add your GEMINI_API_KEY to the .env file
    3. Install dependencies: pip install -r requirements.txt
"""

import sys
from pathlib import Path

# Add project root to path so we can import config
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from config.settings import GEMINI_API_KEY, EMBEDDING_MODEL, GENERATION_MODEL, validate_config
from google import genai


def test_embedding():
    """Test the Gemini embedding endpoint with a sample legal text."""
    print("\n" + "=" * 60)
    print("TEST 1: Embedding API (text-embedding-004)")
    print("=" * 60)

    sample_text = (
        "This Non-Disclosure Agreement ('Agreement') is entered into as of "
        "January 1, 2025, by and between Party A ('Disclosing Party') and "
        "Party B ('Receiving Party'). The Receiving Party agrees to hold all "
        "Confidential Information in strict confidence and not to disclose it "
        "to any third party without prior written consent."
    )

    print(f"\n  Input text ({len(sample_text)} chars):")
    print(f"  '{sample_text[:80]}...'")

    client = genai.Client(api_key=GEMINI_API_KEY)
    result = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=sample_text,
    )

    embedding = result.embeddings[0].values
    print(f"\n  [OK] Embedding returned successfully!")
    print(f"  Dimension: {len(embedding)}")
    print(f"  First 5 values: {embedding[:5]}")
    print(f"  Type: {type(embedding[0]).__name__}")

    assert len(embedding) > 0, "Embedding should not be empty"
    assert isinstance(embedding[0], float), "Embedding values should be floats"

    return True


def test_generation():
    """Test the Gemini generation endpoint with a sample legal question."""
    print("\n" + "=" * 60)
    print(f"TEST 2: Generation API ({GENERATION_MODEL})")
    print("=" * 60)

    prompt = (
        "You are a legal assistant. Answer the following question concisely:\n\n"
        "What are the three essential elements of a valid contract under common law?"
    )

    print(f"\n  Prompt: '{prompt[:80]}...'")

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )

    answer = response.text
    print(f"\n  [OK] Generation returned successfully!")
    print(f"  Response length: {len(answer)} chars")
    print(f"\n  Response:\n  {'-' * 56}")
    for line in answer.strip().split("\n"):
        print(f"  {line}")
    print(f"  {'-' * 56}")

    assert len(answer) > 0, "Response should not be empty"

    return True


def main():
    """Run all Gemini API tests."""
    print("=" * 60)
    print("Gemini API Hello-World Test")
    print("=" * 60)

    # Validate config first
    try:
        validate_config()
        print("[OK] Configuration validated -- API key is set.")
    except EnvironmentError as e:
        print(f"[FAIL] {e}")
        print("\nPlease create a .env file with your GEMINI_API_KEY.")
        sys.exit(1)

    results = {}

    # Test 1: Embedding
    try:
        results["embedding"] = test_embedding()
    except Exception as e:
        print(f"\n  [FAIL] Embedding test FAILED: {e}")
        results["embedding"] = False

    # Test 2: Generation
    try:
        results["generation"] = test_generation()
    except Exception as e:
        print(f"\n  [FAIL] Generation test FAILED: {e}")
        results["generation"] = False

    # Summary
    print("\n" + "=" * 60)
    print("RESULTS SUMMARY")
    print("=" * 60)
    for test_name, passed in results.items():
        status = "[PASS]" if passed else "[FAIL]"
        print(f"  {status}  {test_name}")

    all_passed = all(results.values())
    print(f"\n{'[OK] All tests passed!' if all_passed else '[FAIL] Some tests failed.'}")
    print("=" * 60)

    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())
