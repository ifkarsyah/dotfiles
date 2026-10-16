# `set -euo pipefail`

`set -euo pipefail` is a bash best practice that makes scripts more robust and fail-fast. Here's what each flag does:

## `set -e` (Exit on error)
Exit immediately when a command fails, instead of continuing.

```bash
# Without -e: continues even if cp fails
cp missing_file.txt /backup/
echo "This still runs"  # Runs even after error

# With -e: script exits on first error
set -e
cp missing_file.txt /backup/
echo "This won't run"   # Never reached
```

## `set -u` (Treat unset variables as error)
Fail when referencing undefined variables.

```bash
# Without -u: undefined variable expands to empty string
rm -rf $UNDEFINED_DIR/*  # Expands to: rm -rf /*  (DANGEROUS!)

# With -u: script exits with error
set -u
echo $UNDEFINED_VAR  # Error: UNDEFINED_VAR: unbound variable
```

## `set -o pipefail` (Pipe failure propagation)
A pipeline fails if *any* command in it fails, not just the last one.

```bash
# Without pipefail: only checks last command's exit code
false | echo "done"  # Returns 0 (success) because echo succeeded

# With pipefail: fails if any command in pipe fails
set -o pipefail
false | echo "done"  # Returns 1 (failure) from false
```

## Why combine them?

Together they catch errors early and prevent silent failures:

```bash
#!/bin/bash
set -euo pipefail

# If any command fails, undefined var is used, or pipe breaks → script exits
./build.sh | tee build.log
deploy_to_production  # Only runs if build succeeded
```

## Common gotcha

With `-e`, you sometimes need to handle expected failures explicitly:

```bash
# Allow command to fail without exiting script
if ! maybe_failing_command; then
    echo "Handled the failure"
fi

# Or capture exit code
maybe_failing_command || true
```