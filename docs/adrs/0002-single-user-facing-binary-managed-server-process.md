# ADR 0002: Use a Single User-Facing Binary With Managed Server Process

## Status

Accepted

## Context

Eddy is used in a course workflow where the simplest path for students and instructors should remain the default. The normal entrypoint should be `eddy`, and the default development command should continue to be `cargo run` without requiring users to understand or invoke multiple binaries.

At the same time, Eddy needs a long-running server component that may need to be restarted independently from the terminal UI. Restarting the entire TUI to recover or reload server state would interrupt the user's workflow.

## Decision

Keep `eddy` as the single user-facing binary and normal entrypoint. Internally, `eddy` launches the TUI and also starts a separate managed server process.

The TUI is responsible for managing the server lifecycle, including starting it and restarting it when needed, without requiring the user to restart the TUI or invoke a separate command.

## Consequences

Users keep a simple invocation model: run `eddy`, or use the default `cargo run` during development.

The server can be restarted without restarting the TUI, preserving the interactive session and reducing disruption during the course workflow.

The implementation must include process management, health handling, and cleanup behavior so the managed server process does not become orphaned or stale.

Internal complexity increases because one user-facing binary now coordinates multiple runtime processes.

## Alternatives Considered

Use separate user-facing binaries for the TUI and server. This would make process boundaries explicit, but it would complicate the course workflow and make `cargo run` less obvious as the default path.

Run the server in-process with the TUI. This would simplify process management, but it would prevent restarting the server independently from the TUI.

Require users to manually start the server before launching the TUI. This would reduce internal orchestration, but it would add operational burden and increase the chance of setup mistakes.
