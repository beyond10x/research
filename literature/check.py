"""Check literature/DISTILLATION.md and QUEUE.md against the paper files.

Usage, from the repository root: python3 -I literature/check.py
Exit 0 when everything agrees, 1 with one line per disagreement otherwise. No model calls.
"""

import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
KINDS = ("practice", "observation")
EFFECTS = ("helps", "hurts", "none", "mixed")
GRADES = ("E4", "E3", "E2", "E1", "E0")
DESIGNS = (
    "rct", "benchmark-eval", "repo-mining", "user-study", "case-study",
    "experience-report", "literature-review", "position",
)
FRONT = (
    "schema", "id", "version", "title", "authors", "affiliation", "submitted", "categories", "url",
    "read", "design", "subjects", "agents", "period", "controlled", "independent", "artifacts",
)
SECTIONS = ["Question", "Findings", "Limits stated by the authors", "Reader's notes", "Discrepancies", "Leads"]
FIELDS = ["practice", "claim", "evidence", "effect", "reader"]
HEAD = re.compile(r"^### F(\d+) · (\S+) · ([a-z0-9-]+) · (E\d)$")
EVID = re.compile(r"^- (E\d) · (\S+) · (\S+) F(\d+) · \S")

errors = []
INDEPENDENT = set()


def err(where, message):
    errors.append(f"{where}: {message}")


def read_paper(path):
    """Return {n: (kind, slug, grade, effect)} for one paper file, recording shape errors."""
    name = path.name
    text = path.read_text()
    parts = text.split("---\n", 2)
    if len(parts) != 3 or parts[0] != "":
        err(name, "no front matter")
        return {}
    front, body = parts[1], parts[2]
    keys = {m.group(1): m.group(2).strip() for m in re.finditer(r"^([a-z]+):(.*)$", front, re.M)}
    for key in FRONT:
        if key not in keys:
            err(name, f"front matter lacks `{key}`")
    if keys.get("schema") != "1":
        err(name, f"schema is {keys.get('schema')}, expected 1")
    if keys.get("id") != f"arxiv:{path.stem}":
        err(name, f"id {keys.get('id')} does not match the file name")
    if keys.get("design") not in DESIGNS:
        err(name, f"design `{keys.get('design')}` is not in the closed set")
    for key in ("controlled", "independent"):
        if keys.get(key) not in ("true", "false"):
            err(name, f"`{key}` is not true or false")
    for key in ("by", "on", "coverage"):
        if not re.search(rf"^  {key}: \S", front, re.M):
            err(name, f"read.{key} missing")
    if [m.group(1) for m in re.finditer(r"^## (.+)$", body, re.M)] != SECTIONS:
        err(name, "body sections differ from the schema's list or order")

    findings = {}
    block = body.split("## Findings\n", 1)[-1].split("\n## ", 1)[0]
    for chunk in re.split(r"^(?=### )", block, flags=re.M):
        lines = [l for l in chunk.split("\n") if l.strip()]
        if not lines or not lines[0].startswith("### "):
            continue
        m = HEAD.match(lines[0])
        if not m:
            err(name, f"bad finding heading: {lines[0]}")
            continue
        n, kind, slug, grade = int(m.group(1)), m.group(2), m.group(3), m.group(4)
        fields = [l[2:].split(":", 1)[0] for l in lines[1:] if l.startswith("- ")]
        if fields != FIELDS:
            err(name, f"F{n} fields are {fields}")
        effect = next((l.split(":", 1)[1].strip() for l in lines if l.startswith("- effect:")), None)
        if kind not in KINDS:
            err(name, f"F{n} kind `{kind}`")
        if grade not in GRADES:
            err(name, f"F{n} grade `{grade}`")
        if effect not in EFFECTS:
            err(name, f"F{n} effect `{effect}`")
        if n in findings:
            err(name, f"F{n} appears twice")
        findings[n] = (kind, slug, grade, effect)
    if sorted(findings) != list(range(1, len(findings) + 1)):
        err(name, f"finding numbers are {sorted(findings)}")
    if keys.get("independent") == "true":
        INDEPENDENT.add(path.stem)
    has_e4 = any(f[2] == "E4" for f in findings.values())
    if keys.get("controlled") in ("true", "false") and (keys["controlled"] == "true") != has_e4:
        err(name, f"controlled is {keys['controlled']} but an E4 finding {'exists' if has_e4 else 'does not exist'}")
    return findings


def count_line(counter, names):
    return " · ".join(f"{n} {counter.get(n, 0)}" for n in names)


def main():
    papers = {}
    for path in sorted((ROOT / "papers").glob("*.md")):
        papers[path.stem] = read_paper(path)
    every = {(p, n): f for p, fs in papers.items() for n, f in fs.items()}

    dist = (ROOT / "DISTILLATION.md").read_text()
    head, rest = dist.split("## Practices\n", 1)
    practices, rest = rest.split("## Observations\n", 1)
    observations, _ = rest.split("## Contradictions\n", 1)

    e4 = Counter(f[3] for f in every.values() if f[2] == "E4")
    expected = {
        "papers read": str(len(papers)),
        "findings": str(len(every)),
        "by grade": " · ".join(f"{g} {sum(1 for f in every.values() if f[2] == g)}" for g in GRADES),
        "by kind": count_line(Counter(f[0] for f in every.values()), KINDS),
        "by effect": count_line(Counter(f[3] for f in every.values()), EFFECTS),
        "at E4 by effect": count_line(e4, EFFECTS),
        "at E4, independent papers": count_line(
            Counter(f[3] for k, f in every.items() if f[2] == "E4" and k[0] in INDEPENDENT), EFFECTS),
        "at E4, other papers": count_line(
            Counter(f[3] for k, f in every.items() if f[2] == "E4" and k[0] not in INDEPENDENT), EFFECTS),
    }
    for key, want in expected.items():
        m = re.search(rf"^- {re.escape(key)}: (.*)$", head, re.M)
        if not m:
            err("DISTILLATION header", f"no `{key}` line")
        elif m.group(1).strip() != want:
            err("DISTILLATION header", f"`{key}` is `{m.group(1).strip()}`, the paper files give `{want}`")

    cited = Counter()
    seen_slugs = set()
    for part, part_name in ((practices, "Practices"), (observations, "Observations")):
        for chunk in re.split(r"^### ", part, flags=re.M)[1:]:
            lines = [l for l in chunk.split("\n") if l.strip()]
            slug = lines[0].strip()
            where = f"DISTILLATION {slug}"
            if slug in seen_slugs:
                err(where, "section appears twice")
            seen_slugs.add(slug)
            if len(lines) < 5 or not lines[2].startswith("- reading:") or not lines[3].startswith("- best grade:"):
                err(where, "lines are not description, reading, best grade, evidence")
                continue
            rows = []
            for line in lines[4:]:
                m = EVID.match(line)
                if not m:
                    err(where, f"bad evidence line: {line[:60]}")
                    continue
                grade, effect, paper, n = m.group(1), m.group(2), m.group(3), int(m.group(4))
                found = every.get((paper, n))
                if not found:
                    err(where, f"{paper} F{n} is not in a paper file")
                    continue
                cited[(paper, n)] += 1
                if found[1] != slug:
                    err(where, f"{paper} F{n} has slug {found[1]}")
                if (grade, effect) != (found[2], found[3]):
                    err(where, f"{paper} F{n} is {found[2]} {found[3]} in the paper file, {grade} {effect} here")
                rows.append((paper, found))
            if not rows:
                continue
            best = min((r[1][2] for r in rows), key=GRADES.index)
            want = (
                f"- best grade: {best} · papers: {len({r[0] for r in rows})} · "
                + count_line(Counter(r[1][3] for r in rows), EFFECTS)
            )
            if lines[3].strip() != want:
                err(where, f"count line should be `{want}`")
            all_obs = all(r[1][0] == "observation" for r in rows)
            if all_obs != (part_name == "Observations"):
                err(where, f"is under {part_name}")
    for key in every:
        if cited[key] != 1:
            err("DISTILLATION", f"{key[0]} F{key[1]} is cited {cited[key]} times")

    queue = (ROOT / "QUEUE.md").read_text()
    read_ids = set(re.findall(r"^- \[x\] (\S+) ", queue, re.M))
    for paper in papers:
        if paper not in read_ids:
            err("QUEUE", f"{paper} has a paper file and no `[x]` line")
    for paper in read_ids - set(papers):
        err("QUEUE", f"{paper} is marked read and has no paper file")
    ids = re.findall(r"^- \[.\] (\S+) ", queue, re.M)
    for paper, count in Counter(ids).items():
        if count > 1:
            err("QUEUE", f"{paper} is listed {count} times")

    for line in errors:
        print(line)
    print(f"{len(papers)} papers, {len(every)} findings, {len(seen_slugs)} slugs, {len(errors)} errors")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
