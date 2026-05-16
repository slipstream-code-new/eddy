# ADR 0014: Use Server-Owned Read Models for TUI Query State

## Status

Accepted

## Context

The TUI needs query-oriented views of application state, including snapshots,
timelines, statuses, and lesson progress. The authoritative state is produced by
EventCore, but reconstructing that state directly inside the TUI would duplicate
domain logic, couple the interface to event storage details, and make protocol
boundaries unclear.

The server already owns the application state boundary and is responsible for
presenting stable protocol responses to clients. Keeping read/query state on the
server lets the TUI remain a client of explicit views rather than a second state
reconstruction implementation.

## Decision

The TUI does not reconstruct EventCore state directly.

The server exposes snapshots, timelines, statuses, and lesson progress through
read/query models over the protocol. The TUI requests those models and renders
the returned data without replaying events or depending on EventCore internals.

## Consequences

Server-owned read models keep state reconstruction logic centralized and make the
protocol the stable boundary between the TUI and domain state. This reduces
duplication, keeps UI code focused on interaction and rendering, and allows read
models to evolve with server-side domain logic.

The server must maintain query models that are complete enough for TUI needs.
Protocol changes are required when the TUI needs new derived views or additional
fields. The TUI may also depend on server availability for state inspection that
could otherwise have been computed locally.

## Alternatives Considered

### Reconstruct EventCore State in the TUI

Rejected because it would duplicate projection logic, expose EventCore details to
the client, and increase the risk of the TUI diverging from server behavior.

### Share Projection Code Between Server and TUI

Rejected because it would still couple the TUI to domain reconstruction concerns
and complicate the client boundary. The protocol should expose purpose-built read
models instead of shared internal projection mechanisms.

### Add Ad Hoc Query Endpoints per Screen

Rejected because screen-specific endpoints would make the protocol harder to
reason about and more tightly coupled to current UI layout. Stable read/query
models provide a clearer contract.
