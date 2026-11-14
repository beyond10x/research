"""Replace the notes block of DISTILLATION.md. Usage: python3 -I replace_notes.py DISTILLATION NOTES"""
import sys
from pathlib import Path

target = Path(sys.argv[1])
text = target.read_text()
start = text.index("Notes on the set at ")
end = text.index("## Practices\n")
target.write_text(text[:start] + Path(sys.argv[2]).read_text() + text[end:])
print("replaced", end - start, "characters")
