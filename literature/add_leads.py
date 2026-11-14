"""Add leads to literature/QUEUE.md with title and date from the arXiv API. No model calls.

Usage, from the repository root: python3 -I literature/add_leads.py LEADS

LEADS has one lead per line: `<arxiv-id> | <topic heading of the Queued section> | <source paper id>`.
A lead whose id is already anywhere in QUEUE.md is left out. Each topic is kept newest first by id.
"""

import re
import sys
import time
import urllib.error
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AGENT = "arxiv-literature-search/0.1 (python-urllib)"
ATOM = "{http://www.w3.org/2005/Atom}"


def metadata(ids):
    url = "http://export.arxiv.org/api/query?max_results=200&id_list=" + ",".join(ids)
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    for attempt in range(6):
        try:
            with urllib.request.urlopen(request, timeout=120) as response:
                feed = ET.fromstring(response.read())
            break
        except urllib.error.HTTPError as error:
            if error.code not in (429, 503) or attempt == 5:
                raise
            time.sleep(30 * (attempt + 1))
    found = {}
    for entry in feed.findall(f"{ATOM}entry"):
        base = entry.findtext(f"{ATOM}id", "").rsplit("/", 1)[-1].partition("v")[0]
        title = " ".join((entry.findtext(f"{ATOM}title") or "").split())
        found[base] = (entry.findtext(f"{ATOM}published", "")[:10], title)
    return found


def main():
    queue_path = ROOT / "QUEUE.md"
    queue = queue_path.read_text()
    known = set(re.findall(r"^- \[.\] (\S+) ", queue, re.M))
    leads = []
    for line in Path(sys.argv[1]).read_text().split("\n"):
        if line.strip() and not line.startswith("#"):
            paper, topic, source = [p.strip() for p in line.split(" | ")]
            if paper not in known and paper not in {l[0] for l in leads}:
                leads.append((paper, topic, source))
    if not leads:
        print("no new leads")
        return
    meta = metadata([l[0] for l in leads])
    head, queued = queue.split("## Queued\n", 1)
    topics, order = {}, []
    for chunk in re.split(r"^### ", queued, flags=re.M)[1:]:
        lines = chunk.split("\n")
        order.append(lines[0].strip())
        topics[lines[0].strip()] = [l for l in lines[1:] if l.startswith("- [")]
    added = 0
    for paper, topic, source in leads:
        if paper not in meta or not meta[paper][1]:
            print(f"{paper}: no metadata, left out")
            continue
        if topic not in topics:
            sys.exit(f"{paper}: topic `{topic}` is not in QUEUE.md")
        date, title = meta[paper]
        topics[topic].append(f"- [ ] {paper} · {date} · {title} · lead from {source}")
        added += 1
    out = [head + "## Queued\n"]
    for topic in order:
        lines = sorted(topics[topic], key=lambda l: l.split()[3], reverse=True)
        out.append(f"### {topic}\n\n" + "\n".join(lines) + "\n")
    queue_path.write_text("\n".join(out))
    print(f"{added} leads added, {sum(len(v) for v in topics.values())} queued")


if __name__ == "__main__":
    main()
