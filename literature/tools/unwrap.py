"""Join the continuation lines of each bullet into one line. Usage: python3 -I unwrap.py IN OUT"""
import sys
from pathlib import Path

out = []
for line in Path(sys.argv[1]).read_text().split("\n"):
    stripped = line.strip()
    if out and stripped and line.startswith(" ") and not stripped.startswith("- ") and out[-1].strip():
        out[-1] = out[-1] + " " + stripped
    else:
        out.append(line)
Path(sys.argv[2]).write_text("\n".join(out))
