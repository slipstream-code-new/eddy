# ADR 0012: Generate and Validate Documentation From a Machine-Readable Event Model

## Status

Superseded by [ADR 0017: Store Event Models as Per-Workflow JSON Files](0017-per-workflow-event-model-files.md)

## Context

Eddy's event documentation must stay accurate, complete, and useful for both humans and automation. Manually maintained prose is easy to drift from implementation details, especially as event names, payload fields, descriptions, and usage guidance evolve.

We need a single source of truth that can be validated for completeness and rendered into readable documentation.

## Decision

Maintain a machine-readable JSON event model as the source of truth for documented events.

Provide scripts that:

- validate the event model for required information and completeness;
- fail when required documentation fields are missing or malformed;
- render the model into HTML documentation for human readers.

Generated documentation should be treated as an output of the event model, not as the authoritative source.

## Consequences

- Event documentation has a structured source that can be checked automatically.
- Missing or incomplete event metadata can be caught before documentation is published.
- HTML documentation can be regenerated consistently from the same model.
- Contributors must update the JSON model when event documentation changes.
- The validation and rendering scripts become part of the documentation maintenance workflow.

## Alternatives Considered

- Maintain documentation manually in Markdown or HTML. This is simple initially but allows drift and does not support completeness checks well.
- Document events only in source code comments. This keeps documentation near implementation but makes publishing and validation harder.
- Generate documentation directly from implementation code. This reduces duplication but can make it difficult to include human-oriented explanations, examples, and stability metadata that are not represented in code.
