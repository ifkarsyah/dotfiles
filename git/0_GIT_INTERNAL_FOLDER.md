## Git Internal Folder Structure

Here's what each component does:

### Core Files

| File | Purpose |
|------|---------|
| **HEAD** | Points to your current branch (e.g., `ref: refs/heads/main`). Think of it as "where am I now?" |
| **config** | Repository-specific settings (remote URLs, user name/email for this repo, etc.) |
| **description** | Used by GitWeb (rarely used, mostly for Git servers) |
| **index** | The staging area. Tracks what changes are staged for the next commit |

### `hooks/` - Git Hooks
Scripts that run automatically at specific points:
- **commit-msg** ← After commit message is entered, but before commit is finalized
- **pre-commit** - Runs before a commit is made
- **pre-push** - Runs before pushing to remote
- Files with `.sample` are disabled templates (remove `.sample` to activate)

### `objects/` - The Object Database
Git's content-addressable storage. Everything is stored here:

| Directory | Purpose |
|-----------|---------|
| **pack/** | Compressed storage of all objects (blobs, trees, commits) |
| **info/** | Metadata about objects |

**Object types:**
- **Blob** - File contents (not filename, just data)
- **Tree** - Directory structure (maps names to blobs/trees)
- **Commit** - Snapshot metadata (author, message, parent commits)

### `refs/` - References
Human-readable pointers to commits:

```
refs/
├── heads/     → Local branches (main, feature-x)
├── remotes/   → Remote-tracking branches (origin/main)
└── tags/      → Release tags (v1.0.0)
```

### `logs/` - History Log
Records all ref changes. Powers `git reflog`:

```
logs/refs/heads/main  → History of where 'main' branch pointed
```

### `packed-refs`
When you have many refs, Git packs them into a single file for efficiency.

---

## How They Work Together

```
┌─────────────┐
│    HEAD     │ ──→ refs/heads/main ──→ commit object
└─────────────┘                           │
                                          ↓
                                    tree object ──→ blob (file content)
```

1. **HEAD** tells Git which branch you're on
2. **refs/heads/main** points to the latest commit SHA
3. **commit object** (in objects/) contains metadata + tree reference
4. **tree object** contains directory listing pointing to blobs
5. **blob** contains actual file content