# ADR 0003: Treat the Server Subcommand as Internal Process Plumbing

## Status

Accepted

## Context

Eddy needs a long-running server process to support the TUI and related runtime behavior. A visible `eddy server` command can be useful for process supervision, diagnostics, and development, but presenting it as a normal end-user workflow would split lifecycle responsibility between users and the application.

## Decision

`eddy server` may exist for supervision and diagnostics, but it is not part of the normal user workflow. The TUI and supervisor own the server lifecycle, including starting, monitoring, and stopping the server as needed.

## Consequences

Users interact with Eddy through the intended top-level workflow instead of manually managing background processes. Server lifecycle behavior remains centralized, which reduces configuration ambiguity and makes failure handling more consistent. Documentation and help text should avoid implying that users normally need to run `eddy server` directly.

## Alternatives Considered

Expose `eddy server` as the primary way to start Eddy's runtime. This was rejected because it makes users responsible for lifecycle management and creates unnecessary operational steps.

Hide the server command entirely. This was rejected because an explicit command is still useful for supervisors, diagnostics, and development workflows.
