# ADR 0015: Use Explicit Protocol Version Handshake

## Status

Accepted

## Context

The TUI and server communicate through an internal protocol that can change during development. When a development reload updates one side but not the other, protocol mismatches can cause unpredictable failures, confusing errors, or stale behavior.

## Decision

The TUI and server will perform an explicit protocol compatibility handshake when establishing communication. Each side will report its supported protocol version, and communication will continue only when the versions are compatible.

If the handshake detects an incompatible protocol after a development reload, the TUI will prompt the user to perform a full restart instead of continuing and failing unpredictably.

## Consequences

- Protocol incompatibility is detected early and reported clearly.
- Development reloads become safer because partial reload mismatches fail predictably.
- Users may need to perform a full restart after changes that alter the protocol.
- Protocol changes must update the advertised protocol version intentionally.

## Alternatives Considered

- Allow mismatched TUI and server versions to continue communicating: rejected because failures would remain unpredictable and harder to diagnose.
- Attempt automatic recovery or restart: rejected for now because it adds complexity and may hide important development-state problems.
- Rely on implicit compatibility through message parsing errors: rejected because parse failures do not reliably identify protocol incompatibility or provide useful guidance.
