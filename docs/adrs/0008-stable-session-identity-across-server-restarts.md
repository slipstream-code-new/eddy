# ADR 0008: Preserve Logical Session Identity Across Server Restarts

## Status

Accepted

## Context

Eddy maintains durable course and conversation state that must survive server process restarts. The TUI and server both need to refer to the same logical session after reconnecting, but a running server process has its own transient identity and lifecycle.

If clients treat server process identity as session identity, restarting the server can make an existing course or conversation appear lost, duplicated, or unrelated to the prior interaction.

## Decision

Server process identity is transient and must not define durable session identity.

A stable `session_id` identifies the logical course/conversation state. The TUI and server share this `session_id`, and the server uses it to load or continue the durable session state after restart. Reconnecting to a restarted server with the same `session_id` resumes the same logical session.

## Consequences

The TUI can reconnect across server restarts without losing the user's course or conversation context.

Server restarts no longer imply new logical sessions. Multiple server processes over time may serve the same durable session, while each process remains operationally distinct.

Session state management must consistently key durable course/conversation data by `session_id`, and code must avoid conflating process-scoped identifiers with durable logical identity.

## Alternatives Considered

Use server process identity as session identity: rejected because restarts would break continuity and make durable state difficult to resume reliably.

Create a new session on every reconnect: rejected because it would discard or fragment course/conversation continuity after expected restarts.

Have only the server generate session identity: rejected because the TUI must retain and present a stable identifier when reconnecting to a restarted server.
