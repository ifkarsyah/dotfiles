## Git Hooks

Git hooks are scripts that run automatically at specific points in Git's workflow. They let you customize Git's behavior without modifying Git itself.

### How They Work

```
Git Command → Git checks hooks directory → Runs matching hook script → Proceeds or aborts
```

When you run `git commit`, Git looks for `.git/hooks/pre-commit` and executes it before actually committing. If the script exits with non-zero status, the commit is aborted.

### Hook Types

#### Client-Side Hooks (Local)

| Hook | When it runs |
|------|--------------|
| **pre-commit** | Before commit is created |
| **prepare-commit-msg** | Before commit message editor opens |
| **commit-msg** | After commit message is written  |
| **post-commit** | After commit is created |
| **pre-push** | Before pushing to remote |
| **pre-rebase** | Before rebasing |

#### Server-Side Hooks (Remote)

| Hook | When it runs |
|------|--------------|
| **pre-receive** | Before receiving pushed commits |
| **post-receive** | After receiving pushed commits |
| **update** | Before updating each ref |

### Naming Convention

- Files named `hook-name.sample` are **disabled** (templates)
- Files named `hook-name` (no `.sample`) are **active**
- Must be executable (`chmod +x`)

### Common Use Cases

```bash
# pre-commit: Run linters, format code, run tests
npm run lint
npm test

# commit-msg: Enforce commit message format 
PATTERN="^(feat|fix|refactor)(\(.+\))?: .+"

# pre-push: Run full test suite before pushing
npm run test:integration

# pre-commit: Check for secrets/API keys
grep -r "API_KEY" .
```

### The Hook We Created

Your `commit-msg` hook validates conventional commit format:

```bash
# .git/hooks/commit-msg

# Pattern: feat|fix|refactor with optional scope
PATTERN="^(feat|fix|refactor)(\(.+\))?: .+"

# If message doesn't match → exit 1 (abort commit)
# If message matches → exit 0 (allow commit)
```

### Sharing Hooks

Since `.git/hooks/` isn't tracked by Git, teams typically:
1. Store hooks in a folder like `git/hooks/` (tracked)
2. Use a setup script to copy them to `.git/hooks/`
3. Or use tools like **Husky** (for Node.js) or **pre-commit** framework

### Important Note

Client-side hooks are **not enforced** — developers can skip them with `--no-verify`. For enforcement, you need server-side hooks or CI/CD checks.