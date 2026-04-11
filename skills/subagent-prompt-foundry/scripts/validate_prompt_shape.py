#!/usr/bin/env python3

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_SECTIONS = [
    r"roles?",
    r"scopes?",
    r"inputs?",
    r"tasks?",
    r"methodolog(?:y|ies)",
    r"outputs?",
]

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: validate_prompt_shape.py prompt.md", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Prompt file not found: {path}", file=sys.stderr)
        return 1

    text = path.read_text(encoding="utf-8")
    missing = [pattern for pattern in REQUIRED_SECTIONS if not re.search(pattern, text, re.IGNORECASE)]
    print(json.dumps({"valid": len(missing) == 0, "missing_sections": missing}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
