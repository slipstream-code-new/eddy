# ADR 0005: Use One Active Managed Server Per Workspace Initially

## Status

Accepted

## Context

Eddy manages development servers associated with workspaces. Early support needs a simple ownership and discovery model so clients can find the correct managed server without ambiguity. The server descriptor and discovery mechanism already need a stable scope, and the workspace is the natural boundary for project-local behavior.

Supporting multiple active managed servers within a single workspace would require additional selection rules, UI/API semantics, lifecycle coordination, and conflict handling before those needs are proven.

## Decision

Initially, Eddy will support one active managed server per workspace.

The managed server descriptor and discovery process will be keyed by workspace. Clients that need to connect to a managed server will resolve the workspace first, then use that workspace-scoped descriptor to discover the active server.

Session switching, if needed, can be introduced later as a domain-level concept rather than by allowing multiple concurrently active managed servers in the same workspace from the start.

## Consequences

This keeps initial behavior predictable and reduces coordination complexity. There is a single authoritative active server for a workspace, which simplifies discovery, cleanup, error handling, and client expectations.

This also means workflows requiring multiple simultaneous managed servers in one workspace are not supported initially. If those workflows become important, Eddy will need an explicit domain model for selecting or switching sessions.

## Alternatives Considered

Allowing multiple active managed servers per workspace was considered, but rejected for the initial implementation because it adds selection and lifecycle complexity without a clear immediate requirement.

Keying discovery by session was considered, but rejected initially because sessions are not yet the primary boundary for server ownership. Session switching can be added later at the domain level if the product needs it.
