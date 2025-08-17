import os
import sys
from pathlib import Path

# Ensure root is importable as package base
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
	sys.path.insert(0, str(ROOT))

# Disable CSV ingestion during tests
os.environ.setdefault("SKIP_STARTUP", "1")
