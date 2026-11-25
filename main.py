#!/usr/bin/env python3
"""The Funniest One-Line Resignation Letter — entry program (program/v1).

Writes the resignation letter of a retry loop to /output/entry.txt.
Pure standard library, no network, no input files, deterministic.
"""

import os

LINE = (
    "I resign. After 47 retries, the payment gateway finally answered: "
    "'have you tried turning it off and on again?'"
)

OUTPUT_PATH = os.environ.get("MAKEFUN_ENTRY_OUTPUT", "/output/entry.txt")


def main() -> None:
    text = LINE.strip()
    assert text, "entry line must not be empty"
    assert "\n" not in text, "entry must be a single line"
    assert 1 <= len(text) <= 140, "entry must be 1-140 characters"
    out_dir = os.path.dirname(OUTPUT_PATH)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(text + "\n")
    os.chmod(OUTPUT_PATH, 0o644)


if __name__ == "__main__":
    main()
