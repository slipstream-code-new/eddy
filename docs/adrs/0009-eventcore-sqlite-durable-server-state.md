# ADR 0009: Store Durable Server State With EventCore on SQLite

## Status

Accepted

## Context

The server needs durable session and domain state that survives process restarts and can be resumed reliably by different front-end processes. Keeping this state in the TUI or supervisor would couple user-interface/process lifecycle concerns to authoritative application state and make recovery behavior harder to reason about.

The project also needs a state model that records changes explicitly and supports deterministic reconstruction of server state over time. EventCore provides command handling and stream-based persistence for this purpose, and SQLite provides a local durable storage backend that is simple to operate in development and deployment.

## Decision

The server owns durable session and domain state using EventCore with the SQLite adapter.

Server-side workflows will be modeled as EventCore commands that append to and read from EventCore streams. The persisted streams are the source of truth for durable state. The TUI and supervisor will store only lightweight resume and process metadata needed to reconnect to or restart server processes.

We will describe the domain in terms of commands and streams rather than traditional aggregate objects.

## Consequences

Durable state has a single owner: the server. This reduces ambiguity about which process is authoritative and keeps UI and supervision code focused on presentation, orchestration, and resume behavior.

SQLite keeps the operational footprint small while still providing durable local persistence. EventCore streams make history explicit, enabling reconstruction and audit of session/domain state.

The server must own schema/storage initialization, stream naming, command validation, and recovery behavior. Tests for durable behavior should exercise command handling and stream persistence rather than TUI or supervisor storage.

## Alternatives Considered

Keeping durable state in the TUI or supervisor was rejected because those processes are lifecycle and orchestration concerns, not authoritative domain-state owners.

Using ad hoc SQLite tables directly was rejected because it would spread persistence rules through application code and lose the explicit command/stream model provided by EventCore.

Using an external database service was rejected for now because it adds operational complexity that is not needed for the current local durable-state requirements.
