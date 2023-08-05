from pathlib import Path

__version__ = "0.1.1"

CACHE_DIR = Path.home() / ".cache/sonorus"
CACHE_DIR.mkdir(parents=True, exist_ok=True)
