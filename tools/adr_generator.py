#!/usr/bin/env python3
"""
ADR Generator for Plantão 360.

Generates Architecture Decision Records.

Usage:
    python tools/adr_generator.py "Title of the ADR"
    python tools/adr_generator.py "Title" --status accepted
    python tools/adr_generator.py "Title" --template technical
"""

import argparse
import os
import re
import sys
import io
from datetime import datetime
from pathlib import Path

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


BACKEND_DIR = Path(__file__).parent.parent / "backend"
DOCS_DIR = Path(__file__).parent.parent / "docs"
ADR_DIR = DOCS_DIR / "adr"


def find_next_adr_number() -> int:
    if not ADR_DIR.exists():
        return 1
    existing = list(ADR_DIR.glob("ADR-*.md"))
    if not existing:
        return 1
    numbers = []
    for f in existing:
        match = re.match(r"ADR-(\d+)", f.name)
        if match:
            numbers.append(int(match.group(1)))
    return max(numbers, default=0) + 1


def to_kebab_case(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = re.sub(r"-+", "-", text)
    return text.strip("-")


def generate_adr(title: str, status: str = "proposed", template: str = "standard") -> str:
    number = find_next_adr_number()
    date = datetime.now().strftime("%Y-%m-%d")
    filename = f"ADR-{number:03d}-{to_kebab_case(title)}.md"

    if template == "technical":
        content = f"""# ADR-{number:03d}: {title}

**Date:** {date}

**Status:** {status}

**Deciders:** Plantão 360 Architecture Team

---

## Context

Describe the architectural context and problem that necessitated this decision.

## Decision

State the decision clearly and concisely.

## Consequences

### Positive

- [List positive consequences]

### Negative

- [List negative consequences]

### Neutral

- [List neutral consequences]

## Alternatives Considered

### Alternative 1: [Name]

**Pros:**
- [Pros]

**Cons:**
- [Cons]

**Reason for rejection:** [Why this was not chosen]

### Alternative 2: [Name]

**Pros:**
- [Pros]

**Cons:**
- [Cons]

**Reason for rejection:** [Why this was not chosen]

## Implementation

Describe how this decision will be implemented.

## References

- [Link to related ADRs]
- [Link to relevant documentation]
"""
    else:
        content = f"""# ADR-{number:03d}: {title}

**Date:** {date}

**Status:** {status}

**Deciders:** Plantão 360 Architecture Team

---

## Context

[Describe the context and problem]

## Decision

[State the decision]

## Rationale

[Explain why this decision was made]

## Consequences

### Positive
- [Positive consequences]

### Negative
- [Negative consequences]

## References
- [Related ADRs or documentation]
"""

    # Write the ADR
    ADR_DIR.mkdir(parents=True, exist_ok=True)
    filepath = ADR_DIR / filename
    filepath.write_text(content, encoding="utf-8")

    print(f"\n  ✓ ADR generated: {filepath.relative_to(DOCS_DIR.parent)}")
    print(f"    Number: {number:03d}")
    print(f"    Title: {title}")
    print(f"    Status: {status}")
    print()

    return str(filepath)


def main():
    parser = argparse.ArgumentParser(description="Generate Architecture Decision Record")
    parser.add_argument("title", help="ADR title")
    parser.add_argument("--status", default="proposed", choices=["proposed", "accepted", "deprecated", "superseded"],
                        help="ADR status (default: proposed)")
    parser.add_argument("--template", default="standard", choices=["standard", "technical"],
                        help="ADR template (default: standard)")

    args = parser.parse_args()
    generate_adr(args.title, status=args.status, template=args.template)


if __name__ == "__main__":
    main()
