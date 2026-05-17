---
description: Prepare a scoped Forgejo PR with explicit-path staging and conventional commit checks.
agent: build
---

Prepare a Forgejo PR for: $ARGUMENTS

Workflow:

1. Audit scope with `git status` and diffs.
2. Stage only explicit paths; do not use `git add .`, `git add -A`, `git add -u`, or `git commit -a`.
3. Check commit titles follow conventional commits; the release PR generates changelog notes from conventional commits.
4. Verify relevant gates.
5. Push the branch with `git`, then create the PR with Forgejo MCP `forgejo_create_pull_request` using owner `Slipstream`, repo `eddy`, head `<branch>`, base `main`, title, and body.

Use Forgejo MCP for supported Forgejo operations. Do not use `tea` or `gh` for PR creation in this repo.
