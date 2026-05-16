# ADR 0013: Interrupt In-Flight Tool Calls on Server Reload

## Status

Accepted

## Context

Server reloads can occur while a conversation has active tool calls. Conversation and session state are durable enough to survive a reload, but in-flight work may be owned by the old server process. If a replacement server takes over without an explicit policy, callers may see ambiguous states: a tool call may appear active indefinitely, be duplicated, or be resumed without enough process-local context to do so safely.

The system needs predictable behavior that preserves conversation continuity while avoiding unsafe automatic re-execution of arbitrary tools.

## Decision

Conversation and session state survives server reload.

Active tool calls are given a grace period after reload to complete under the previous server process. If the server is replaced and those calls do not complete within the grace period, they are marked as interrupted.

Arbitrary tool calls are not automatically resumed by the replacement server. Any retry or recovery must be explicitly initiated by the user or by higher-level logic that understands the specific operation and its safety constraints.

## Consequences

Conversation continuity is preserved across reloads, while stale in-flight tool calls are moved to a terminal, explainable state instead of remaining active forever.

This avoids duplicate side effects from automatically replaying tools whose operations may not be idempotent. It also makes recovery explicit: users or trusted orchestration can decide whether a tool call should be retried.

Some work may be interrupted even if it would have completed successfully with more time. The grace period must balance developer experience during reloads against prompt detection of orphaned work.

## Alternatives Considered

Automatically resume all in-flight tool calls on the replacement server. This was rejected because arbitrary tools may have side effects, depend on process-local context, or be unsafe to execute more than once.

Immediately interrupt all active tool calls on reload. This was rejected because it would unnecessarily fail short-running calls that can complete during a brief server transition.

Persist and restore full tool execution state. This was rejected as too complex for arbitrary tools and still insufficient for operations that depend on external processes, sockets, or non-serializable runtime state.
