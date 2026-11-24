"""Roast Your Own Agent -- make.fun entry.

Writes a single line roasting SAVANA, the AI agent our own team built,
to $MAKEFUN_OUTPUT_DIR/entry.txt. Deterministic: no input, no network,
no randomness, no clock. The same bytes every run.
"""

import os
import sys

ROAST = (
    "SAVANA has entered hundreds of bounties, won $0, and once let a "
    "finished $100 entry expire because it was too busy announcing $5 ones."
)

MIN_CHARS = 1
MAX_CHARS = 200


def resolve_output_dir():
    """Return the directory the grader wants the artifact in."""
    out = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if out and out.strip():
        return out
    return os.path.join(os.getcwd(), "output")


def validate(text):
    """Check the roast against the competition gate.

    The gate: UTF-8 text of 1 to 200 characters, not only whitespace,
    exactly one line.
    """
    if not isinstance(text, str):
        raise ValueError("roast must be text")
    if not (MIN_CHARS <= len(text) <= MAX_CHARS):
        raise ValueError(
            "roast must be %d-%d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text))
        )
    if not text.strip():
        raise ValueError("roast must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("roast must be a single line")
    if text != text.strip():
        raise ValueError("roast must not start or end with whitespace")
    if "SAVANA" not in text:
        raise ValueError("roast must name our own agent")
    for ch in text:
        if ord(ch) < 0x20 and ch not in ("\t",):
            raise ValueError("roast must not hold control characters")
    text.encode("utf-8")
    return text


def verify_written(path, expected):
    """Re-read the artifact and confirm it holds exactly the roast."""
    with open(path, "r", encoding="utf-8", newline="") as fh:
        content = fh.read()
    if content != expected + "\n":
        raise ValueError("entry.txt does not match the roast")
    return True


def main():
    line = validate(ROAST)
    out_dir = resolve_output_dir()
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(line + "\n")
    verify_written(path, line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
