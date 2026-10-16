#!/usr/bin/env python3
"""PreToolUse hook (matcher: Write|Edit|MultiEdit|NotebookEdit).

Blocks writes whose NEW content contains a high-confidence secret pattern.
Only the text being written is scanned, not the text being replaced, so
removing a leaked secret from a file is still allowed.

Exit code 2 blocks the call and sends stderr to Claude. The matched value is
never printed, only the kind of secret and the line number.

Limits: this only catches well-known formats. It misses generic passwords and
anything it has no pattern for. Keep a real scanner such as gitleaks in your
pre-commit hook too. A match containing "EXAMPLE" is ignored so documentation
samples (like AWS's own) do not trigger it.
"""
import json
import re
import sys

PATTERNS = [
    ("AWS access key ID", r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"),
    ("AWS secret access key", r"(?i)aws_secret_access_key\s*[:=]\s*[\"']?[A-Za-z0-9/+=]{40}\b"),
    ("GitHub token", r"\bgh[pousr]_[A-Za-z0-9]{36,}\b"),
    ("GitHub fine-grained token", r"\bgithub_pat_[A-Za-z0-9_]{22,}"),
    ("Anthropic API key", r"\bsk-ant-[A-Za-z0-9_-]{20,}"),
    ("OpenAI-style API key", r"\bsk-(?:proj-)?[A-Za-z0-9_-]{40,}"),
    ("ElevenLabs API key", r"\bsk_[a-f0-9]{40,}\b"),
    ("Stripe live key", r"\b[sr]k_live_[A-Za-z0-9]{20,}"),
    ("Slack token", r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    ("Google API key", r"\bAIza[0-9A-Za-z_-]{35}\b"),
    ("Private key block", r"-----BEGIN (?:[A-Z]+ )*PRIVATE KEY-----"),
]
COMPILED = [(name, re.compile(rx)) for name, rx in PATTERNS]


def new_content(tool_input):
    """Return the text being written: Write.content, Edit.new_string, etc."""
    chunks = []
    for key in ("content", "new_string", "new_source"):
        value = tool_input.get(key)
        if isinstance(value, str):
            chunks.append(value)
    for edit in tool_input.get("edits") or []:
        if isinstance(edit, dict) and isinstance(edit.get("new_string"), str):
            chunks.append(edit["new_string"])
    return chunks


def find_secret(text):
    for lineno, line in enumerate(text.splitlines(), start=1):
        for name, rx in COMPILED:
            match = rx.search(line)
            if match and "EXAMPLE" not in match.group(0).upper():
                return name, lineno
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    tool_input = data.get("tool_input") or {}
    for text in new_content(tool_input):
        found = find_secret(text)
        if found:
            name, lineno = found
            print(
                f"Blocked: the content looks like it contains a secret ({name}, line {lineno} "
                "of the text being written). Use an environment variable or a secret manager "
                "and write a placeholder instead.",
                file=sys.stderr,
            )
            sys.exit(2)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # fail open; SystemExit from sys.exit(2) is not caught here
        print(f"block_secrets.py error (write allowed): {exc}", file=sys.stderr)
