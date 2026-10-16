#!/usr/bin/env python3
"""Detect the <TOOL> version(s) used by a project.

Usage: python detect_version.py [project_root]

Output is deliberately tiny (token cost). Example:
    runtime 1.2.3 docker-compose.yml
    lib 1.2.0 requirements.txt
    line 1.x
Prints `UNKNOWN` when nothing is found. Never guess in that case.

How to adapt:
- Fill PROBES with (kind, filename regex, content regex). First capture group is the version.
- Set PRIORITY to the order of kinds that decide the version line (for example the
  runtime or server wins over a client library).
- Change line_of() if lines are not just the major version (for example "1.20" style lines).
- Add probes as you meet new project layouts. Test each one on a fixture.
"""
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "target", "build", "dist", "__pycache__"}

# (kind, filename regex, content regex). First capture group = version.
PROBES = [
    ("lib", r"requirements.*\.txt$", r"<package-name>==(\d+\.\d+(?:\.\d+)?)"),
]

PRIORITY = ["runtime", "lib"]


def line_of(version: str) -> str:
    return f"{version.split('.')[0]}.x"


def walk(root: Path):
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield Path(dirpath) / name


def detect(root: Path):
    found = []
    for path in walk(root):
        for kind, name_re, content_re in PROBES:
            if not re.search(name_re, path.name):
                continue
            try:
                text = path.read_text(errors="ignore")
            except OSError:
                continue
            m = re.search(content_re, text)
            if m:
                found.append((kind, m.group(1), str(path.relative_to(root))))
    return found


def resolve_line(found):
    for want in PRIORITY:
        for kind, version, _ in found:
            if kind == want:
                return line_of(version)
    return None


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    found = detect(root)
    if not found:
        print("UNKNOWN")
        return
    seen = set()
    for kind, version, source in found:
        if (kind, version) in seen:
            continue
        seen.add((kind, version))
        print(f"{kind} {version} {source}")
    line = resolve_line(found)
    print(f"line {line}" if line else "line UNKNOWN")


if __name__ == "__main__":
    main()
