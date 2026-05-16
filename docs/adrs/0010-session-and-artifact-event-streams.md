# ADR 0010: Model Session and Artifacts as Separate Event Streams

## Status

Accepted

## Context

Eddy records collaborative learning sessions, assistant turns, tool calls, reload facts, and filesystem artifacts through EventCore. These records need clear stream boundaries so the system can replay conversation state, reason about lessons, and track artifacts without coupling unrelated histories.

EventCore uses dynamic consistency boundaries, not traditional aggregates. A stream boundary should reflect the consistency needed for a decision at write time, rather than a fixed domain object hierarchy.

Filesystem artifacts are different from session conversation state. They may be created, edited, deleted, or replaced outside Eddy, so their histories cannot be assumed to be fully controlled by a session stream.

## Decision

Use `session-{session_id}` as the primary event stream for session-scoped behavior, including conversation events, lesson events, assistant turn events, tool-call events, and reload facts.

Use separate `artifact-{artifact_id}` event streams for filesystem artifact histories. Artifact streams represent Eddy's observations and decisions about a specific artifact, while acknowledging that the underlying file may change outside Eddy.

When an operation needs consistency across session state and artifact state, EventCore should establish the necessary dynamic consistency boundary for that operation instead of treating session or artifact streams as traditional aggregates.

## Consequences

Session replay remains focused on the collaborative conversation and learning flow.

Artifact histories can evolve independently from sessions and can represent external filesystem changes without polluting the session stream.

Cross-stream workflows must explicitly define the consistency boundary they require at write time.

Queries that need a full view of a session plus artifacts must project from both `session-{session_id}` and relevant `artifact-{artifact_id}` streams.

This avoids overloading the session stream with artifact lifecycle details while preserving traceability between sessions and artifacts through events that reference artifact identifiers.

## Alternatives Considered

Store all events in `session-{session_id}`. This would make session replay simple, but it would incorrectly imply that artifact state is fully owned by the session and would mix external filesystem changes into conversation history.

Store all artifact-related events only in artifact streams. This would keep artifacts isolated, but it would make the session stream incomplete for understanding assistant behavior, tool calls, and lesson context.

Model sessions and artifacts as traditional aggregates. This was rejected because EventCore's model is based on dynamic consistency boundaries, and fixed aggregate boundaries would be too rigid for operations that span session context and filesystem artifacts.
