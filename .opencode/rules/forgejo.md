# Forgejo

This repo uses Forgejo at `git.johnwilger.com`, not GitHub. Use the Forgejo MCP for supported issue, pull request, review, comment, label, branch, file, notification, workflow, and tracked-time operations. Do not use `tea` for workflows covered by the Forgejo MCP, and do not introduce `gh` workflows.

Before reaching for another Forgejo client, check whether the Forgejo MCP has the needed operation. If the MCP lacks a required operation, state the gap and use the narrowest Forgejo-compatible fallback for that operation only.

Inline review feedback must be answered on the inline thread first. Start each reply by @-tagging the user whose comment is being answered, using the comment author's Forgejo login. For Forgejo API replies, copy the original comment `position` into the reply payload as `new_position` and set `old_position` to `0`.
