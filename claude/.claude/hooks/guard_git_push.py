#!/usr/bin/env python3
"""PreToolUse hook (matcher: Bash). Blocks risky `git push` commands.

Blocks:
  - pushes that target main or master, explicitly or by pushing while on it
  - force pushes: --force, --force-with-lease, -f, or a "+" before a refspec
  - --all and --mirror, which can push or overwrite every branch

Exit code 2 blocks the call and sends stderr to Claude. Any other exit lets
the command run, so an unexpected error in this script fails open.

This is a guardrail, not a security boundary. Enable GitHub branch protection
on main as the real protection.
"""
import json
import re
import shlex
import subprocess
import sys

PROTECTED = {"main", "master"}
SEGMENT_SPLIT = re.compile(r"&&|\|\||;|\||\n")
WRAPPERS = {"env", "command", "time", "nohup", "exec", "sudo", "nice", "xargs"}
SHELLS = {"bash", "sh", "zsh"}
FLAGS_WITH_VALUE = {"-o", "--push-option", "--repo", "--receive-pack", "--exec"}


def block(reason):
    print(f"Blocked: {reason}", file=sys.stderr)
    sys.exit(2)


def current_branch(cwd, repo_dir):
    cmd = ["git"] + (["-C", repo_dir] if repo_dir else []) + ["rev-parse", "--abbrev-ref", "HEAD"]
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=5)
    except (OSError, subprocess.SubprocessError):
        return None
    return out.stdout.strip() if out.returncode == 0 else None


def split_tokens(segment):
    try:
        return shlex.split(segment)
    except ValueError:
        return segment.split()


def check_tokens(tokens, cwd):
    # Skip env assignments and wrappers such as `FOO=1 env git push`.
    while tokens and (re.match(r"^\w+=", tokens[0]) or tokens[0] in WRAPPERS):
        tokens = tokens[1:]
    if not tokens:
        return

    # `bash -c "git push ..."`: look inside the quoted command.
    if tokens[0] in SHELLS and "-c" in tokens:
        idx = tokens.index("-c")
        if idx + 1 < len(tokens):
            check_command(tokens[idx + 1], cwd)
        return

    if tokens[0] != "git":
        return

    # Skip git's own options before the subcommand: -C <path>, -c <k=v>, --no-pager ...
    repo_dir = None
    i = 1
    while i < len(tokens) and tokens[i].startswith("-"):
        if tokens[i] == "-C" and i + 1 < len(tokens):
            repo_dir = tokens[i + 1]
            i += 2
        elif tokens[i] == "-c" and i + 1 < len(tokens):
            i += 2
        else:
            i += 1
    if i >= len(tokens) or tokens[i] != "push":
        return

    args = tokens[i + 1:]
    positionals = []
    skip_next = False
    for arg in args:
        if skip_next:
            skip_next = False
            continue
        if arg in FLAGS_WITH_VALUE:
            skip_next = True
            continue
        if arg.startswith("--"):
            if arg == "--force" or arg.startswith("--force-with-lease") or arg == "--force-if-includes":
                block("force push is not allowed.")
            if arg in ("--all", "--mirror"):
                block(f"`git push {arg}` can overwrite or push every branch.")
            continue
        if arg.startswith("-"):
            if re.fullmatch(r"-[A-Za-z]*f[A-Za-z]*", arg):
                block("force push is not allowed.")
            continue
        positionals.append(arg)

    refspecs = positionals[1:]  # positionals[0] is the remote
    branch = None
    if not refspecs:
        branch = current_branch(cwd, repo_dir)
        if branch in PROTECTED:
            block(f"you are on '{branch}'. Create a branch and push that instead.")
        return

    for refspec in refspecs:
        if refspec.startswith("+"):
            block("force push (leading '+' in refspec) is not allowed.")
        dst = refspec.split(":", 1)[1] if ":" in refspec else refspec
        dst = re.sub(r"^refs/heads/", "", dst)
        if dst == "HEAD":
            dst = current_branch(cwd, repo_dir) or dst
        if dst in PROTECTED:
            block(f"push to '{dst}' is not allowed. Push a branch and open a pull request.")


def check_command(command, cwd):
    if "push" not in command:
        return
    for segment in SEGMENT_SPLIT.split(command):
        if "push" in segment:
            check_tokens(split_tokens(segment), cwd)


def main():
    try:
        data = json.load(sys.stdin)
    except json.JSONDecodeError:
        return
    command = (data.get("tool_input") or {}).get("command", "")
    if isinstance(command, str):
        check_command(command, data.get("cwd"))


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # fail open; SystemExit from block() is not caught here
        print(f"guard_git_push.py error (command allowed): {exc}", file=sys.stderr)
