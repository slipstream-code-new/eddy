# ADR 0017: Store Event Models as Per-Workflow JSON Files

## Status

Accepted

## Context

ADR 0012 established machine-readable JSON event models and generated HTML documentation. The initial repository model was a single speculative file created to explore architecture direction, not a behavior model derived from implemented features or a real Event Modeling session.

Keeping speculative behavior in a canonical event-model file creates risk. Future contributors and agents may treat invented events, commands, read models, and slices as authoritative. A single large model file also makes workflow-focused modeling harder for humans and LLM agents because unrelated behavior must be loaded and edited together.

Eddy is intended to use vertical slices. In that style, a workflow-sized event model is usually easier to facilitate, review, validate, and evolve. Shared event names and payload meanings still need to remain consistent across workflows, but they do not require every workflow to live in one JSON document from the start.

## Decision

Store machine-readable event models as per-workflow JSON files under `docs/event-model/workflows/` using the `*.eventmodel.json` suffix.

Each file should describe one coherent workflow or use case and should be created from an actual modeling session. Do not maintain placeholder workflows or speculative event vocabularies as source-of-truth artifacts.

Generated HTML documentation should live under `docs/event-model/generated/` and remain derived output.

The existing validation and rendering scripts continue to operate on one workflow model file at a time. Cross-workflow event cataloging or schema consistency checks can be added later when real modeled workflows create enough shared vocabulary to justify them.

## Consequences

Workflow models stay smaller and easier for humans and LLM agents to understand.

The source of truth is less likely to be polluted by invented behavior because absent workflows remain absent until modeled.

Validation remains simple because each workflow file can be checked independently with the existing scripts.

Shared event schemas may need additional tooling later if multiple workflows define the same event name or payload differently.

Documentation consumers must look at the set of workflow model files rather than one monolithic event-model file.

## Alternatives Considered

Keep one `eddy.eventmodel.json` file. This centralizes the model, but it encourages unrelated workflows to accumulate in one large document and makes speculative content harder to distinguish from modeled behavior.

Create one file per slice. This maximizes locality, but it fragments the story and makes workflow-level facilitation and review harder.

Create a shared event catalog immediately. This may become useful, but adding it before real workflows exist would risk prematurely standardizing invented event schemas.
