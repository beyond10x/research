"""Query the arXiv API for every line of a query file and write one JSONL record per hit.

Deterministic fetch only: no model calls, no relevance judgement. Deciding which hits
enter QUEUE.md is a reader's judgement and happens after this script.

    python3 -I literature/arxiv_search.py literature/queries.txt OUT.jsonl [--max 40]

Query file: one arXiv `search_query` expression per line; blank lines and `#` lines are skipped.
A paper hit by several queries is written once, with every query that found it.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

API = "http://export.arxiv.org/api/query"
ATOM = "{http://www.w3.org/2005/Atom}"
PAUSE_SECONDS = 3.5
USER_AGENT = "arxiv-literature-search/0.1 (python-urllib)"


def fetch(query: str, max_results: int) -> bytes:
    params = urllib.parse.urlencode(
        {
            "search_query": query,
            "sortBy": "submittedDate",
            "sortOrder": "descending",
            "start": 0,
            "max_results": max_results,
        }
    )
    request = urllib.request.Request(f"{API}?{params}", headers={"User-Agent": USER_AGENT})
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except Exception as error:  # noqa: BLE001 - retried, then re-raised
            last_error = error
            time.sleep(PAUSE_SECONDS * (attempt + 2))
    raise RuntimeError(f"arXiv API failed for {query!r}: {last_error}")


def text(entry: ET.Element, tag: str) -> str:
    node = entry.find(f"{ATOM}{tag}")
    return " ".join((node.text or "").split()) if node is not None else ""


def parse(feed: bytes) -> list[dict]:
    records = []
    for entry in ET.fromstring(feed).iter(f"{ATOM}entry"):
        raw_id = text(entry, "id").rsplit("/abs/", 1)[-1]
        arxiv_id, _, version = raw_id.partition("v")
        if not arxiv_id:
            continue
        records.append(
            {
                "id": arxiv_id,
                "version": f"v{version}" if version else "",
                "published": text(entry, "published")[:10],
                "updated": text(entry, "updated")[:10],
                "title": text(entry, "title"),
                "authors": [text(a, "name") for a in entry.iter(f"{ATOM}author")][:4],
                "categories": [c.get("term", "") for c in entry.iter(f"{ATOM}category")],
                "summary": text(entry, "summary"),
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("queries", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--max", type=int, default=40)
    args = parser.parse_args()

    queries = [
        line.strip()
        for line in args.queries.read_text().splitlines()
        if line.strip() and not line.lstrip().startswith("#")
    ]
    seen: dict[str, dict] = {}
    for index, query in enumerate(queries):
        if index:
            time.sleep(PAUSE_SECONDS)
        hits = parse(fetch(query, args.max))
        print(f"{len(hits):3d} hits  {query}", file=sys.stderr, flush=True)
        for record in hits:
            seen.setdefault(record["id"], {**record, "queries": []})["queries"].append(query)

    ordered = sorted(seen.values(), key=lambda r: (r["published"], r["id"]), reverse=True)
    with args.out.open("w") as handle:
        for record in ordered:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
    print(f"{len(ordered)} unique papers -> {args.out}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
