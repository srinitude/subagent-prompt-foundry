#!/usr/bin/env python3

from __future__ import annotations

import difflib
import json
import sys
from pathlib import Path

def main() -> int:
    if len(sys.argv) != 3:
        print("Usage: diff_prompt_versions.py old.txt new.txt", file=sys.stderr)
        return 1

    old_path = Path(sys.argv[1])
    new_path = Path(sys.argv[2])

    if not old_path.exists() or not new_path.exists():
        print("Both files must exist.", file=sys.stderr)
        return 1

    old_lines = old_path.read_text(encoding="utf-8").splitlines()
    new_lines = new_path.read_text(encoding="utf-8").splitlines()

    diff = list(
        difflib.unified_diff(
            old_lines,
            new_lines,
            fromfile=str(old_path),
            tofile=str(new_path),
            lineterm="",
        )
    )

    print(json.dumps({"diff": diff}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
