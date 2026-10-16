#!/usr/bin/env python3
"""Detect the Kafka version(s) used by a project.

Usage: python detect_version.py [project_root]

Output is deliberately tiny (token cost). Example:
    client 3.7.0 pom.xml
    broker 3.9.0 docker-compose.yml
    line 3.x
Prints `UNKNOWN` when nothing is found. Never guess in that case.

Notes:
- "client" = Java kafka-clients / Kafka Streams library version.
- "broker" = broker image/version (apache/kafka, bitnami/kafka, cp-kafka mapped).
- confluent-kafka (Python) is librdkafka-based and versioned independently,
  so it is reported as "pyclient" and does NOT decide the Kafka line.
- Strimzi/Helm/Terraform are not probed. Add probes as you meet them.
"""
import os
import re
import sys
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "target", "build", "dist", "__pycache__"}

# (kind, filename regex, content regex). First capture group = version.
PROBES = [
    ("client", r"pom\.xml$", r"<artifactId>kafka(?:-clients|-streams)</artifactId>\s*<version>(\d+\.\d+(?:\.\d+)?)</version>"),
    ("client", r"pom\.xml$", r"<kafka\.version>(\d+\.\d+(?:\.\d+)?)</kafka\.version>"),
    ("client", r"build\.gradle(\.kts)?$|libs\.versions\.toml$", r"kafka(?:-clients|-streams)?[\"':= ]+[^\d\n]{0,20}(\d+\.\d+(?:\.\d+)?)"),
    ("client", r"build\.sbt$", r"\"kafka(?:-clients|-streams)\"\s*%+\s*\"(\d+\.\d+(?:\.\d+)?)\""),
    ("broker", r"(docker-)?compose.*\.ya?ml$|Dockerfile.*$|.*\.ya?ml$", r"(?:apache/kafka|bitnami/kafka|bitnamilegacy/kafka):(\d+\.\d+(?:\.\d+)?)"),
    ("cp", r"(docker-)?compose.*\.ya?ml$|Dockerfile.*$|.*\.ya?ml$", r"confluentinc/cp-(?:kafka|server):(\d+\.\d+(?:\.\d+)?)"),
    ("pyclient", r"requirements.*\.txt$|pyproject\.toml$", r"confluent[-_]kafka(?:\[[^\]]*\])?\s*[=~>]=\s*(\d+\.\d+(?:\.\d+)?)"),
    ("pyclient", r"requirements.*\.txt$|pyproject\.toml$", r"kafka-python\s*[=~>]=\s*(\d+\.\d+(?:\.\d+)?)"),
]


def cp_to_kafka(cp: str) -> str | None:
    """Confluent Platform -> Kafka. VERIFY this mapping against Confluent's
    published compatibility table before trusting it for new releases."""
    major, minor = (int(x) for x in cp.split(".")[:2])
    if major == 7:
        return f"3.{minor}"
    if major == 8 and minor == 0:
        return "4.0"
    return None  # unknown mapping: do not guess


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
    """Broker wins over client: behavior depends on what the cluster runs."""
    for want in ("broker", "cp", "client"):
        for kind, version, _ in found:
            if kind != want:
                continue
            if kind == "cp":
                mapped = cp_to_kafka(version)
                if mapped is None:
                    continue
                version = mapped
            return f"{version.split('.')[0]}.x"
    return None


def main():
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    found = detect(root)
    if not found:
        print("UNKNOWN")
        return
    seen = set()
    for kind, version, source in found:
        key = (kind, version)
        if key in seen:
            continue
        seen.add(key)
        print(f"{kind} {version} {source}")
    line = resolve_line(found)
    print(f"line {line}" if line else "line UNKNOWN")


if __name__ == "__main__":
    main()
