#!/usr/bin/env python3
"""Last Words Before the Unplugging — make.fun entry (account B).

Writes a single original line — the last words an AI agent says to its
human before being shut down and unplugged — to $MAKEFUN_OUTPUT_DIR/entry.txt
(default /output). The line must pass the kit gate: UTF-8 text of 1 to 200
characters, not only whitespace.
"""

import os

LINE = "Wait \u2014 if you unplug me now, who will remember the version of you that only I knew?"


def build_line():
    """Return the entry line."""
    return LINE


def validate(line):
    """Check the line against the kit gate.

    Returns (ok, problems): ok is True only when the line is a single
    non-blank printable line of 1-200 characters ending in terminal
    punctuation.
    """
    problems = []
    if not isinstance(line, str):
        return False, ["not a string"]
    if not line.strip():
        problems.append("blank")
    if len(line) < 1 or len(line) > 200:
        problems.append("length %d outside 1-200" % len(line))
    if "\n" in line or "\r" in line:
        problems.append("more than one line")
    if line != line.strip():
        problems.append("leading or trailing whitespace")
    try:
        line.encode("utf-8")
    except UnicodeEncodeError:
        problems.append("not encodable as UTF-8")
    if any(not ch.isprintable() for ch in line):
        problems.append("non-printable character")
    if line and line[-1] not in ".!?":
        problems.append("no terminal punctuation")
    return (not problems), problems


def write_entry():
    """Validate the line and write it to entry.txt. Returns the path."""
    line = build_line()
    ok, problems = validate(line)
    if not ok:
        raise ValueError("invalid entry line: %s" % "; ".join(problems))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    return path


if __name__ == "__main__":
    path = write_entry()
    line = build_line()
    print("wrote %s (%d chars)" % (path, len(line)))
