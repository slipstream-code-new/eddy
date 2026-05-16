# ADR 0007: Support Managed Server Rebuild and Replacement in Dev Mode

## Status

Accepted

## Context

In dev mode, the TUI depends on a local server process that may change while the developer is working. Rebuilding and restarting that server manually interrupts the feedback loop, but replacing a running server with a failed or incomplete build would make the TUI unusable.

Dev mode needs a managed rebuild flow that keeps the current server available until a replacement has been built successfully.

## Decision

In dev mode, the TUI/supervisor will watch the server code for changes and run `cargo build` when a rebuild is needed.

If the build fails, the existing server process remains running and the TUI continues using it. The failed build is reported, but no server replacement occurs.

If the build succeeds, the supervisor replaces the running server with the newly built server and reconnects the TUI to it.

## Consequences

Developers get automatic server rebuilds without losing a working TUI session on build failure.

The running server may temporarily lag behind the source code when the latest build fails, so dev mode must make build failures visible.

The supervisor becomes responsible for coordinating file watching, build execution, server replacement, and TUI reconnection.

## Alternatives Considered

Always stop the old server before building: rejected because a build failure would leave dev mode without a usable server.

Restart the server on every file change without building first: rejected because it could launch stale or invalid artifacts and obscure build errors.

Require manual rebuild and restart: rejected because it slows the dev feedback loop and duplicates work the supervisor can handle reliably.
