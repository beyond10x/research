"""Counts for the notes in DISTILLATION.md. Usage: python3 -I stats.py LITERATURE_DIR"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

root = Path(sys.argv[1])
HEAD = re.compile(r"^### F(\d+) · (\S+) · ([a-z0-9-]+) · (E\d)$")
papers = {}
slug_papers = defaultdict(set)
slug_e4 = defaultdict(set)
for path in sorted((root / "papers").glob("*.md")):
    text = path.read_text()
    pid = path.stem
    independent = re.search(r"^independent: (\w+)", text, re.M).group(1)
    design = re.search(r"^design: (\S+)", text, re.M).group(1)
    rows = []
    lines = text.split("\n")
    for i, line in enumerate(lines):
        m = HEAD.match(line)
        if not m:
            continue
        effect = next(l for l in lines[i:] if l.startswith("- effect:")).split(":")[1].strip()
        rows.append((m.group(2), m.group(3), m.group(4), effect))
        slug_papers[m.group(3)].add(pid)
        if m.group(4) == "E4":
            slug_e4[m.group(3)].add((pid, independent, effect))
    papers[pid] = (independent, design, rows)

print("designs", Counter(d for _, d, _ in papers.values()))
print("independent", Counter(i for i, _, _ in papers.values()))
for flag in ("true", "false"):
    with_e4 = {p: Counter(r[3] for r in rows if r[2] == "E4") for p, (i, _, rows) in papers.items() if i == flag}
    with_e4 = {p: c for p, c in with_e4.items() if c}
    print(f"independent={flag}: {len(with_e4)} papers with E4")
    for p, c in with_e4.items():
        print("  ", p, papers[p][1], dict(c))
multi = {s: sorted(p) for s, p in slug_papers.items() if len(p) > 1}
print(len(slug_papers), "slugs;", len(multi), "with 2+ papers")
for s, p in sorted(multi.items()):
    print("  ", s, p)
print("slugs with E4 from 2+ papers:")
for s, rows in sorted(slug_e4.items()):
    if len({r[0] for r in rows}) > 1:
        print("  ", s, sorted(rows))
