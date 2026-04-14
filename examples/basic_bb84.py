"""Legacy wrapper kept for continuity. Prefer examples/bb84_protocol.py."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "examples"))

from bb84_protocol import main


if __name__ == "__main__":
    main()
