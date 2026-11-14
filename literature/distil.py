"""Re-render literature/DISTILLATION.md from the paper files plus hand-written lines. No model calls.

Usage, from the repository root: python3 -I literature/distil.py [ADDITIONS]

Kinds, slugs, grades and effects are read from papers/*.md. The description and `reading:` line of
each slug and the one-line text of each evidence line are kept from the existing DISTILLATION.md.
ADDITIONS is a text file that adds or replaces them, one entry per line:

    slug <slug> | <description> | <reading>
    <paper-id> F<n> | <one-line evidence text>

The script recomputes the header counts, every count line, the order of the sections and their
place under Practices or Observations. The intro, the notes after the counts and the Contradictions
section are kept as they are. It stops without writing when a finding has no text or a slug has no
description.
"""

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EFFECTS = ("helps", "hurts", "none", "mixed")
GRADES = ("E4", "E3", "E2", "E1", "E0")
KINDS = ("practice", "observation")
HEAD = re.compile(r"^### F(\d+) · (\S+) · ([a-z0-9-]+) · (E\d)$")
EVID = re.compile(r"^- E\d · \S+ · (\S+) F(\d+) · (.*)$")
COUNT_KEYS = (
    "papers read", "findings", "by grade", "by kind", "by effect", "at E4 by effect",
    "at E4, independent papers", "at E4, other papers",
)
INDEPENDENT = set()


def findings():
    out = {}
    for path in sorted((ROOT / "papers").glob("*.md")):
        current = None
        text = path.read_text()
        if re.search(r"^independent: true$", text, re.M):
            INDEPENDENT.add(path.stem)
        for line in text.split("\n"):
            m = HEAD.match(line)
            if m:
                current = (path.stem, int(m.group(1)))
                out[current] = [m.group(2), m.group(3), m.group(4), None]
            elif line.startswith("- effect:") and current:
                out[current][3] = line.split(":", 1)[1].strip()
    return out


def count_line(counter, names):
    return " · ".join(f"{n} {counter.get(n, 0)}" for n in names)


def main():
    every = findings()
    dist = (ROOT / "DISTILLATION.md").read_text()
    head, rest = dist.split("## Practices\n", 1)
    contradictions = rest.split("## Contradictions\n", 1)[1]
    body = rest.split("## Contradictions\n", 1)[0].replace("## Observations\n", "")

    slugs, texts = {}, {}
    for chunk in re.split(r"^### ", body, flags=re.M)[1:]:
        lines = [l for l in chunk.split("\n") if l.strip()]
        slugs[lines[0].strip()] = (lines[1], lines[2][len("- reading:"):].strip())
        for line in lines[3:]:
            m = EVID.match(line)
            if m:
                texts[(m.group(1), int(m.group(2)))] = m.group(3)

    if len(sys.argv) > 1:
        for number, line in enumerate(Path(sys.argv[1]).read_text().split("\n"), 1):
            if not line.strip() or line.startswith("#"):
                continue
            parts = [p.strip() for p in line.split(" | ")]
            if parts[0].startswith("slug ") and len(parts) == 3:
                slugs[parts[0][5:].strip()] = (parts[1], parts[2])
                continue
            m = re.match(r"^(\S+) F(\d+)$", parts[0])
            if m and len(parts) == 2:
                texts[(m.group(1), int(m.group(2)))] = parts[1]
                continue
            sys.exit(f"{sys.argv[1]}:{number}: not an entry: {line[:70]}")

    problems = [f"{p} F{n} has no evidence text" for (p, n) in every if (p, n) not in texts]
    problems += [f"slug {f[1]} has no description" for f in every.values() if f[1] not in slugs]
    problems += [f"{p} F{n} has text and is not in a paper file" for (p, n) in texts if (p, n) not in every]
    if problems:
        sys.exit("\n".join(sorted(set(problems))))

    by_slug = {}
    for key, (kind, slug, grade, effect) in every.items():
        by_slug.setdefault(slug, []).append((GRADES.index(grade), key, kind, grade, effect))

    def render(slug):
        rows = sorted(by_slug[slug])
        desc, reading = slugs[slug]
        out = [
            f"### {slug}",
            desc,
            f"- reading: {reading}",
            f"- best grade: {rows[0][3]} · papers: {len({r[1][0] for r in rows})} · "
            + count_line(Counter(r[4] for r in rows), EFFECTS),
        ]
        out += [f"- {grade} · {effect} · {key[0]} F{key[1]} · {texts[key]}" for _, key, _, grade, effect in rows]
        return "\n".join(out) + "\n"

    order = sorted(by_slug, key=lambda s: (min(r[0] for r in by_slug[s]), s))
    observations = [s for s in order if all(r[2] == "observation" for r in by_slug[s])]
    practices = [s for s in order if s not in observations]

    values = every.values()
    counts = {
        "papers read": str(len({k[0] for k in every})),
        "findings": str(len(every)),
        "by grade": " · ".join(f"{g} {sum(1 for f in values if f[2] == g)}" for g in GRADES),
        "by kind": count_line(Counter(f[0] for f in values), KINDS),
        "by effect": count_line(Counter(f[3] for f in values), EFFECTS),
        "at E4 by effect": count_line(Counter(f[3] for f in values if f[2] == "E4"), EFFECTS),
        "at E4, independent papers": count_line(
            Counter(f[3] for k, f in every.items() if f[2] == "E4" and k[0] in INDEPENDENT), EFFECTS),
        "at E4, other papers": count_line(
            Counter(f[3] for k, f in every.items() if f[2] == "E4" and k[0] not in INDEPENDENT), EFFECTS),
    }
    for key in COUNT_KEYS:
        head, n = re.subn(rf"^- {re.escape(key)}: .*$", f"- {key}: {counts[key]}", head, flags=re.M)
        if n != 1:
            sys.exit(f"header has {n} `{key}` lines")

    out = [head + "## Practices\n"] + [render(s) for s in practices]
    out += ["## Observations\n"] + [render(s) for s in observations]
    out += ["## Contradictions\n" + contradictions]
    (ROOT / "DISTILLATION.md").write_text("\n".join(out))
    print(f"{counts['papers read']} papers, {counts['findings']} findings, "
          f"{len(practices)} practice slugs, {len(observations)} observation slugs")


if __name__ == "__main__":
    main()
