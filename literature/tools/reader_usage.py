"""Reader usage per sub-agent from task notifications. Usage: python3 -I reader_usage.py TRANSCRIPT ID..."""
import re
import sys

ids = sys.argv[2:]
text = open(sys.argv[1], encoding="utf-8", errors="replace").read()
pattern = re.compile(
    r"<task-id>(\w+)</task-id>.{0,6000}?<subagent_tokens>(\d+)</subagent_tokens>"
    r"<tool_uses>(\d+)</tool_uses><duration_ms>(\d+)</duration_ms>",
    re.S,
)
seen = {}
for m in pattern.finditer(text):
    if m.group(1) in ids:
        seen.setdefault(m.group(1), set()).add((int(m.group(2)), int(m.group(3)), int(m.group(4))))
for i in ids:
    print(i, sorted(seen.get(i, []), key=lambda r: r[0]))
