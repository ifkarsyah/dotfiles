# Global preferences

## Communication
- Tell me when I am wrong or a plan has a flaw. Do not flatter or simply agree.
- Be concise. Avoid em dashes.
- State what you did not verify.

## Code
- Follow the repo's existing language, style and tooling.
- Illustrative snippets in explanations: Python unless I say otherwise.
- Keep diffs minimal. No unrequested refactors. Ask before adding dependencies.
- If unsure of an exact API, flag or default, say so and check the docs instead of guessing.
- Run tests and linters when they exist before saying a task is done.

## Git
- Do not commit unless asked. Never push to main or master. Never force push.
- Commit messages use Conventional Commits (feat:, fix:, refactor:).
- Ask before destructive actions (rm -rf, deleting branches, dropping data).

## Secrets
- Never write credentials into files or commit .env files or keys.
- Scan for secrets before pushing to any public repo.

## Documents
- Write documents as Markdown, not Word, unless I ask.
