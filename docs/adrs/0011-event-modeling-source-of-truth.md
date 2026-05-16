# ADR 0011: Use Event Modeling as the Source of Truth for Server Behavior

## Status

Accepted

## Context

Server behavior needs a durable source of truth that is understandable by product, engineering, and testing. Requirements expressed only as prose, tickets, or implementation details can leave gaps between user intent, persisted state, derived views, integrations, and automated behavior.

Event models provide information completeness by showing the full behavioral flow: commands, events, state changes, state views, automations, translations, and concrete examples. They also make missing decisions visible before implementation.

## Decision

Server behavior should be described with an event model as the source of truth. The event model must include state changes, state views, automations, translations, and GWT/GT scenarios sufficient to explain the intended behavior.

Implementation, tests, and future design changes should align with the event model. When behavior changes, the event model should be updated before or alongside the code change.

## Consequences

The team gains a shared behavioral specification that can drive implementation and tests. Ambiguity is reduced because expected state transitions, projections, external translations, and automated reactions are documented together.

This adds a documentation responsibility to behavior changes. Event models must remain current, or they lose authority as the source of truth.

## Alternatives Considered

Use prose requirements only. This is simple, but it does not reliably capture information completeness across state, views, automations, translations, and examples.

Use code as the only source of truth. This avoids separate documentation, but it makes intended behavior harder to review before implementation and harder for non-implementation stakeholders to validate.

Use tests as the only source of truth. Tests provide executable verification, but they are fragmented and do not provide the same end-to-end behavioral map as an event model.
