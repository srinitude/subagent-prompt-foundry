#!/usr/bin/env python3

from __future__ import annotations

import json
import sys
from pathlib import Path

def clamp(value: float, key: str = "") -> float:
    clamped = max(0.0, min(1.0, value))
    if clamped != value:
        print(f"WARNING: {key} value {value} was clamped to {clamped}", file=sys.stderr)
    return clamped

def score_determinism(
    structure_stability: float,
    constraint_preservation: float,
    research_completeness: float,
    protocol_clarity: float,
) -> float:
    values = [
        clamp(structure_stability, "structure_stability"),
        clamp(constraint_preservation, "constraint_preservation"),
        clamp(research_completeness, "research_completeness"),
        clamp(protocol_clarity, "protocol_clarity"),
    ]
    return round(sum(values) / len(values), 3)

def main() -> int:
    if len(sys.argv) != 2:
        print("Usage: score_determinism.py metrics.json", file=sys.stderr)
        return 1

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Metrics file not found: {path}", file=sys.stderr)
        return 1

    data = json.loads(path.read_text(encoding="utf-8"))
    score = score_determinism(
        float(data["structure_stability"]),
        float(data["constraint_preservation"]),
        float(data["research_completeness"]),
        float(data["protocol_clarity"]),
    )

    print(json.dumps({"determinism_score": score}, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
