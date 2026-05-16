# ADR 0016: Use Ratatui and Prefer Prebuilt TUI Components

## Status

Accepted

## Context

Eddy needs a terminal user interface that can support agent-oriented workflows such as conversation transcripts, multiline prompts, progress and reload status, logs, command discovery, selection lists, modals, and eventually richer rendered content. Building those behaviors directly from low-level terminal primitives is costly and easy to underestimate. Ratatui provides a Rust-native TUI foundation, but its built-in widget set is intentionally limited to general-purpose primitives.

The Ratatui ecosystem includes third-party crates for higher-level widgets and interaction patterns. Some of those crates are mature and actively maintained; others are promising but new or narrow. Eddy should be able to reach for existing components when implementation needs arise without committing to unnecessary dependencies before those needs are concrete.

## Decision

Eddy will use Ratatui as its TUI framework.

When implementing TUI features, Eddy will prefer suitable prebuilt Ratatui-compatible components over building the same behavior directly from primitives. This preference applies especially to complex interactive widgets such as multiline text editing, scrollable views, overlays, trees, rich lists, logging panes, markdown rendering, spinners, and command/menu affordances.

Eddy will maintain a living research catalog at `docs/research/tui-component-libraries.md`. The catalog records actively maintained Ratatui-compatible component libraries, the kinds of components they provide, and cautions discovered during research.

The catalog is not an approved dependency list. Component crates should be added only when an implementation needs them. Before adding a component dependency, the implementation work should check fit, maintenance status, license, dependency impact, testability, and integration risk. Most component choices are implementation-level decisions and do not need their own ADR. A separate ADR is needed only if a component or framework choice materially constrains the architecture.

## Consequences

- The TUI direction is Rust-native and aligned with the existing Rust-centered architecture.
- The team has a default bias toward proven TUI components instead of hand-building complex widgets from primitives.
- The repository gains a maintained place to record component research without rewriting accepted ADRs.
- Dependencies are still introduced lazily, which keeps the dependency graph smaller while Eddy's UI needs are still emerging.
- Each adopted component may bring its own interaction model, state model, styling conventions, and Ratatui version constraints, so integration must be evaluated at adoption time.
- Some needed agent UI elements, such as command palettes or markdown chat rendering, may not have a mature single-purpose crate and may still require composition from smaller components.

## Alternatives Considered

- Build the TUI directly from Ratatui primitives only: rejected because complex terminal UI behavior is harder than it appears and would create avoidable implementation risk.
- Adopt a larger alternate TUI framework instead of Ratatui: rejected because Ratatui is the desired Rust-native framework and has an active ecosystem of compatible widgets.
- Add a broad set of component dependencies immediately: rejected because many needs are not concrete yet, and speculative dependencies would increase maintenance burden.
- Record component research only in this ADR: rejected because ADRs are historical decision records, while component availability and maintenance status change over time.
