# Bash Best Practices & Tricks

Here are essential bash best practices and tricks:

## Redirections

```bash
# File descriptors: 0=stdin, 1=stdout, 2=stderr

# Redirect stderr to stdout (combine them)
command 2>&1 | grep "error"

# Redirect stdout to file, stderr to another
command >out.log 2>err.log

# Discard output (/dev/null is black hole)
command >/dev/null 2>&1 # Silence everything

command >/dev/null  # Silence stdout, keep stderr
command 1>/dev/null # Same as above (stdout)
command 2>/dev/null # Silence stderr, keep stdout
```

## Parameter Expansion

```bash
name="file.txt"

# Default value if unset
${name:-default}          # "file.txt"
${undefined:-default}     # "default"

# Assign default (modifies variable)
${undefined:=default}     # Sets $undefined to "default"

# Error if unset
${required:?Error: not set}  # Exits with message if unset
```

## Safe Variables & Quoting

```bash
# Always quote variables
"$var"                    # Safe
$var                      # Unsafe (word splitting, glob expansion)

# Use [[ ]] instead of [ ]
[[ $name == "test" ]]     # No quotes needed inside [[ ]]
[ $name == "test" ]       # Fails if $name is empty or has spaces

# Check if variable is set
[[ -v VAR ]]              # True if VAR is declared
```

## Useful Tests

```bash
# File tests
[[ -f file ]]     # Exists and is regular file
[[ -d dir ]]     # Exists and is directory
[[ -e path ]]    # Exists (any type)
[[ -r file ]]     # Readable
[[ -w file ]]     # Writable
[[ -x file ]]     # Executable
[[ -s file ]]     # Non-empty
[[ file1 -nt file2 ]]  # Newer than

# String tests
[[ -z "$str" ]]   # Empty string
[[ -n "$str" ]]   # Non-empty string
[[ "$a" == "$b" ]] # String equality
[[ "$a" =~ regex ]]  # Regex match

# Numeric tests
(( x > 5 ))       # Numeric comparison
(( x++ ))         # Increment
(( x == y ))      # Numeric equality
```

## Process Substitution

```bash
# Compare outputs without temp files
diff <(sort file1) <(sort file2)

# Multiple inputs to a command
cat <(echo "header") <(echo "body")

# Capture both stdout and stderr separately
{ read out; read err; } < <(command 2>&1; echo "ERR:$?")
```

## Debugging

```bash
# Debug mode - print commands before executing
set -x              # Enable
set +x              # Disable

# Or run script with debug
bash -x script.sh

# Print each command with source info
PS4='+ ${BASH_SOURCE:-}:${LINENO}: ' 
set -x

# Trap errors for cleanup
trap 'echo "Error on line $LINENO"; exit 1' ERR
```

## Arrays

```bash
arr=(one two three)

echo "${arr[0]}"           # First element: "one"
echo "${arr[@]}"           # All elements
echo "${#arr[@]}"          # Array length: 3
echo "${arr[@]:1:2}"       # Slice: "two three"

# Iterate safely
for item in "${arr[@]}"; do
    echo "$item"
done

# Add element
arr+=("four")

# Check if element exists
[[ " ${arr[*]} " =~ " two " ]]
```

## Here Documents & Strings

```bash
# Multi-line string
cat <<EOF
Line 1
Line 2
EOF

# Preserve indentation (tabs only)
cat <<-EOF
	Indented content
	EOF

# Single line (here-string)
grep "pattern" <<< "search in this string"
```

## Practical Patterns

```bash
# Safe directory navigation
cd "$dir" || exit 1

# Cleanup on exit
cleanup() { rm -f "$tmpfile"; }
trap cleanup EXIT

# Check command exists
command -v jq >/dev/null || { echo "jq required"; exit 1; }

# Get script directory (reliable)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Timeout for commands
timeout 30s long_running_command

# Run in background, capture PID
command &
pid=$!
wait $pid  # Wait for it
```

## Quick Reference

| Pattern | Use |
|---------|-----|
| `2>&1` | Merge stderr to stdout |
| `&>/dev/null` | Silence all output |
| `${var:-default}` | Default value |
| `${var%.*}` | Remove extension |
| `[[ ]]` | Safer tests |
| `(( ))` | Arithmetic |
| `<()` | Process substitution |
| `trap ... EXIT` | Cleanup |
| `set -euo pipefail` | Strict mode |