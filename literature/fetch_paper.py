"""Download arXiv papers for reading: metadata, PDF and extracted text. No model calls.

Usage: python3 -I literature/fetch_paper.py OUTDIR ID [ID ...]

Writes OUTDIR/<id>/meta.json, paper.pdf and paper.txt (pdftotext -layout). OUTDIR belongs in the
session scratch directory; the files are untrusted data and are not stored in the repository.
"""

import json
import subprocess
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

AGENT = "arxiv-literature-search/0.1 (python-urllib)"
ATOM = "{http://www.w3.org/2005/Atom}"
ARXIV = "{http://arxiv.org/schemas/atom}"
PAUSE = 3.5


def get(url):
    request = urllib.request.Request(url, headers={"User-Agent": AGENT})
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def squeeze(value):
    return " ".join((value or "").split())


def metadata(ids):
    feed = ET.fromstring(get("http://export.arxiv.org/api/query?max_results=100&id_list=" + ",".join(ids)))
    found = {}
    for entry in feed.findall(f"{ATOM}entry"):
        full = entry.findtext(f"{ATOM}id", "").rsplit("/", 1)[-1]
        base, _, version = full.partition("v")
        found[base] = {
            "id": base,
            "version": "v" + version,
            "title": squeeze(entry.findtext(f"{ATOM}title")),
            "authors": [squeeze(a.findtext(f"{ATOM}name")) for a in entry.findall(f"{ATOM}author")],
            "affiliations": sorted({squeeze(x.text) for x in entry.iter(f"{ARXIV}affiliation")}),
            "published": entry.findtext(f"{ATOM}published", "")[:10],
            "updated": entry.findtext(f"{ATOM}updated", "")[:10],
            "categories": [c.get("term") for c in entry.findall(f"{ATOM}category")],
            "comment": squeeze(entry.findtext(f"{ARXIV}comment")),
            "url": f"https://arxiv.org/abs/{full}",
        }
    return found


def main():
    out, ids = Path(sys.argv[1]), sys.argv[2:]
    meta = metadata(ids)
    for paper in ids:
        if paper not in meta:
            print(f"{paper}: no metadata")
            continue
        folder = out / paper
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "meta.json").write_text(json.dumps(meta[paper], indent=1, ensure_ascii=False) + "\n")
        pdf = folder / "paper.pdf"
        if not pdf.exists():
            time.sleep(PAUSE)
            pdf.write_bytes(get(f"https://arxiv.org/pdf/{paper}{meta[paper]['version']}"))
        subprocess.run(["pdftotext", "-layout", str(pdf), str(folder / "paper.txt")], check=True)
        info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
        pages = next((l.split()[-1] for l in info.splitlines() if l.startswith("Pages:")), "?")
        text = folder / "paper.txt"
        lines = sum(1 for _ in text.open(errors="replace"))
        print(f"{paper} {meta[paper]['version']} · {pages} pages · {text.stat().st_size} bytes · {lines} lines")


if __name__ == "__main__":
    main()
