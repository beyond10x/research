"""Reflow every bullet of a notes file to at most 100 columns. Usage: python3 -I rewrap.py FILE"""
import re
import sys
import textwrap
from pathlib import Path

path = Path(sys.argv[1])
blocks, current = [], []
for line in path.read_text().split("\n"):
    if re.match(r"^\s*- ", line) or not line.strip():
        if current:
            blocks.append(current)
        current = [line]
        if not line.strip():
            blocks.append(current)
            current = []
    else:
        current.append(line)
if current:
    blocks.append(current)

out = []
for block in blocks:
    if not block[0].strip() or not re.match(r"^\s*- ", block[0]):
        out.extend(block)
        continue
    if all(len(line) <= 100 for line in block):
        out.extend(block)
        continue
    indent = re.match(r"^(\s*)- ", block[0]).group(1)
    text = " ".join(line.strip() for line in block)
    out.extend(
        textwrap.wrap(
            text,
            width=100,
            initial_indent=indent,
            subsequent_indent=indent + "  ",
            break_long_words=False,
            break_on_hyphens=False,
        )
    )
path.write_text("\n".join(out))
