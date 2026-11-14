"""Move one queued line of QUEUE.md to the Read section.

    python3 -I literature/mark_read.py literature/QUEUE.md 2609.17598 2026-11-13
"""

import sys


def main() -> int:
    path, arxiv_id, read_on = sys.argv[1:4]
    lines = open(path).read().split("\n")
    hits = [i for i, line in enumerate(lines) if line.startswith(f"- [ ] {arxiv_id} ")]
    if len(hits) != 1:
        print(f"expected one queued line for {arxiv_id}, found {len(hits)}", file=sys.stderr)
        return 1
    queued = lines.pop(hits[0])
    fields = queued.replace("- [ ]", "- [x]", 1).split(" · ")[:3]
    done = " · ".join(fields) + f" · read {read_on}"

    start = lines.index("## Read") + 2
    end = lines.index("## Skipped")
    block = [line for line in lines[start:end] if line.startswith("- [x]")] + [done]
    block.sort(key=lambda line: line.split(" · ")[1], reverse=True)
    lines[start:end] = block + [""]
    open(path, "w").write("\n".join(lines))
    print(done)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
