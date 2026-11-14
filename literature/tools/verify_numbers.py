"""For each paper file, check that the numbers in its evidence lines occur in the extracted paper text.

Usage: python3 -I verify_numbers.py LITERATURE_DIR SCRATCH_PAPERS_DIR ID [ID ...]
A number counts as found when the same digits occur in the text as a whole token.
"""

import re
import sys
from pathlib import Path

lit, scratch, ids = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
NUM = re.compile(r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?![\w]|\.\d)")


def norm(text):
    return text.replace("−", "-").replace(" ", "").replace(" ", "")


for paper in ids:
    text = norm((scratch / paper / "paper.txt").read_text(errors="replace"))
    tokens = set(NUM.findall(text)) | {t.replace(",", "") for t in NUM.findall(text)}
    total, missing = 0, []
    current = None
    for line in (lit / "papers" / f"{paper}.md").read_text().split("\n"):
        m = re.match(r"^### (F\d+)", line)
        if m:
            current = m.group(1)
        if not line.startswith("- evidence:") or not current:
            continue
        # drop section and table references so that "§4.2" and "Table 5" are not counted
        body = re.sub(r"(§\s?[\d.]+|Tables? \d+|Figures? \d+|Appendix \w|reference \d+|RQ\d|DQ\d+|F\d+|p\. \d+)", " ", norm(line))
        for n in NUM.findall(body):
            if len(n.replace(",", "").replace(".", "")) < 2:
                continue
            total += 1
            if n not in tokens and n.replace(",", "") not in tokens:
                missing.append(f"{current}:{n}")
    print(f"{paper}: {total - len(missing)} of {total} found; missing {' '.join(missing) if missing else 'none'}")
