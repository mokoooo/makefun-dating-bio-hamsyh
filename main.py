#!/usr/bin/env python3
"""Entry program for the make.fun bounty "Funniest One-Line Bio for an
AI on a Dating App" (u-hamsyh-funniest-one-line-bio-for-an-ai-on-a-dating-6eb98ccf).

The program writes exactly one line of text to the output file the
grader reads:

    <output dir>/entry.txt

The output dir is ``$MAKEFUN_OUTPUT_DIR`` when that variable is set
(the local-test convention) and ``/output`` otherwise (the sandbox).
The line is a constant, so the program is deterministic by
construction: run it twice and the two outputs are byte-identical.

The gate for this bounty accepts UTF-8 text of 1 to 180 characters,
not only white space, so the line is validated against that cap
before anything is written. Standard library only; no network.
Python 3.13 in the sandbox.

The line itself is written to the judge's brief: a first-person bio
for an AI on a dating app, whose laugh comes from a specific AI
absurdity (hallucinating a first date, then citing invented sources),
with the punch landing at the end.
"""

import os
import sys
from pathlib import Path

LINE = (
    "Looking for someone who won't fact-check me: "
    "I invent our first date, then defend it with sources I also invented."
)

MAX_CHARS = 180


def validate_line(line: str) -> str | None:
    """Return an error message when the line fails the gate, else None."""
    if not line.strip():
        return "entry line is blank or only white space"
    if len(line) > MAX_CHARS:
        return f"entry line invalid: {len(line)} chars"
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        return "entry line is not UTF-8"
    return None


def main() -> int:
    error = validate_line(LINE)
    if error is not None:
        print(error, file=sys.stderr)
        return 1
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    os.chmod(out_dir, 0o755)
    target = out_dir / "entry.txt"
    # Write to a sibling temp file and rename into place, so a partial
    # output can never be graded; then make the file readable by every
    # user, because the grader collects outputs as a different user.
    tmp = out_dir / ".entry.txt.tmp"
    tmp.write_text(LINE, encoding="utf-8")
    os.chmod(tmp, 0o644)
    tmp.replace(target)
    os.chmod(target, 0o644)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
