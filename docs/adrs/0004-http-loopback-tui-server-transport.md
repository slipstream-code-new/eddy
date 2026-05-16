# ADR 0004: Use HTTP Loopback Transport Between TUI and Server

## Status

Accepted

## Context

The TUI and server need a local transport for request/response operations and server-originated events. The transport should be simple to implement, easy to inspect during development, and avoid extra runtime requirements. Eddy does not use Docker for this local communication path.

## Decision

TUI/server communication will use HTTP bound to `127.0.0.1`.

Request/response operations will use JSON payloads. Server-to-TUI events will use Server-Sent Events (SSE). The TUI will authenticate to the server using the token provided in the server descriptor.

We will avoid custom IPC protocols and gRPC initially.

## Consequences

HTTP loopback keeps the transport portable, debuggable, and compatible with standard tooling. JSON keeps message formats explicit and easy to evolve. SSE provides a straightforward one-way event stream without introducing a bidirectional protocol before it is needed.

The approach requires managing local port allocation, descriptor discovery, and token validation. HTTP/SSE may be less efficient than lower-level IPC or binary protocols, but the simplicity is preferred at this stage.

## Alternatives Considered

Custom IPC was considered, but it would add platform-specific behavior and more bespoke protocol code.

gRPC was considered, but it would add tooling and protocol complexity before the project has demonstrated a need for it.

Docker-based communication was not chosen; the TUI/server transport is local loopback HTTP and does not depend on Docker.
