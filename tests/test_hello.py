"""
Smoke test to verify the project environment is set up correctly.
"""

import importlib
import sys
from pathlib import Path

# Ensure project root is on the import path
PROJECT_ROOT = str(Path(__file__).resolve().parent.parent)
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def test_python_version():
    """Ensure Python 3.10+ is being used."""
    assert sys.version_info >= (3, 10), (
        f"Python 3.10+ required, got {sys.version_info.major}.{sys.version_info.minor}"
    )


def test_config_imports():
    """Ensure the config module can be imported."""
    config = importlib.import_module("config.settings")
    assert hasattr(config, "GEMINI_API_KEY")
    assert hasattr(config, "EMBEDDING_MODEL")
    assert hasattr(config, "GENERATION_MODEL")
    assert hasattr(config, "PROJECT_ROOT")


def test_package_imports():
    """Ensure all package __init__.py files are importable."""
    packages = ["ingestion", "retrieval", "generation", "eval", "api"]
    for pkg in packages:
        mod = importlib.import_module(pkg)
        assert mod is not None, f"Failed to import {pkg}"


def test_google_genai_installed():
    """Ensure google-genai SDK is installed."""
    try:
        import google.genai  # noqa: F401
    except ImportError:
        raise AssertionError(
            "google-genai is not installed. Run: pip install google-genai"
        )


if __name__ == "__main__":
    test_python_version()
    print("[OK] Python version OK")

    test_config_imports()
    print("[OK] Config imports OK")

    test_package_imports()
    print("[OK] Package imports OK")

    test_google_genai_installed()
    print("[OK] google-genai installed OK")

    print("\n[OK] All smoke tests passed!")
