# TUI Component Libraries

This catalog records Ratatui-compatible component and widget libraries that Eddy may reach for during implementation. Prefer prebuilt components from this catalog when they fit the feature rather than building complex TUI behavior directly from Ratatui primitives.

The catalog is research, not an approved dependency list. Add a crate only when an implementation needs it, and re-check fit, maintenance, license, dependency impact, testability, and integration risk before adoption.

## Research Criteria

- Compatible with Ratatui or the current Ratatui ecosystem.
- Actively maintained or showing recent release activity.
- Documented well enough to evaluate quickly through examples, docs, or source.
- Relevant to Eddy's agent UI needs.

## Built-In Ratatui Widgets

Ratatui includes general-purpose widgets such as `Block`, `Paragraph`, `List`, `Table`, `Tabs`, `Scrollbar`, `Gauge`, `LineGauge`, `Sparkline`, `BarChart`, `Chart`, `Canvas`, and `calendar::Monthly`.

Use these for simple layout, display, and selection needs. Reach for third-party components when the required behavior is interactive or stateful enough that primitive composition would become fragile.

## Strong Initial Candidates

| Crate | Component Types | Useful For | Notes |
| --- | --- | --- | --- |
| `ratatui-textarea` | Multiline text editor widget | Agent prompt input, editable notes, command argument entry | Strong direct candidate for multiline input; fork of `tui-textarea` focused on Ratatui. |
| `tui-textarea` | Multiline text editor widget | Prompt input and text editing | Mature and widely used; verify current Ratatui compatibility before adoption. |
| `tui-textarea-2` | Multiline text editor widget | Prompt input and text editing | Recent fork/continuation; verify API stability and maintainer intent. |
| `tui-scrollview` | Scrollable viewport/container | Chat transcripts, logs, long status panes | Good fit for content larger than the terminal area. |
| `tui-scrollbar` | Scrollbar helper | Scroll indicators for transcript and list panes | UI helper only; pair with explicit scroll state. |
| `tui-widget-list` | Stateful list of widgets | Command results, transcript item lists, selectable rich rows | Useful when list rows need to be widgets rather than plain text. |
| `tui-tree-widget` | Tree widget | File trees, artifact trees, context/source navigation | Check interaction model before adoption. |
| `tui-popup` | Popup/modal primitive | Simple dialogs and overlays | Basic overlay behavior; may not cover advanced drawers/popovers. |
| `tui-overlay` | Drawers, modals, popovers, toasts | More complex overlay patterns | Promising but newer; verify behavior and maintenance. |
| `throbber-widgets-tui` | Spinner/throbber | Assistant thinking state, background work, reload activity | Focused status indicator with visible ecosystem presence. |
| `ratatui-image` | Image widget | Future image attachments or previews | Only adopt when image rendering becomes a real product need. |

## Agent UI Essentials

| Need | Candidate Crates | Notes |
| --- | --- | --- |
| Multiline prompt input | `ratatui-textarea`, `tui-textarea`, `tui-textarea-2` | Prefer an existing textarea/editor rather than implementing editing, cursor movement, selection, and wrapping manually. |
| Chat transcript rendering | `tui-scrollview`, `tui-widget-list`, `tui-scrollbar` | No obvious mature chat transcript crate surfaced; compose scroll/list widgets before writing a bespoke viewport. |
| Markdown rendering | `ratatui-markdown`, `mdfrier`, `ratkit` | Promising but currently immature or low-adoption candidates; prototype before relying on them. |
| Command palette | `tui-popup`, `tui-overlay`, `tui-widget-list`, `rat-menu`, `tui-menu`, `ratatui-which-key` | No mature dedicated command-palette crate surfaced; likely compose a popup/list/input from smaller components. |
| Progress and activity status | Ratatui `Gauge`, Ratatui `LineGauge`, `throbber-widgets-tui`, `tui-spinner`, `tui-skeleton` | Prefer built-in gauges for determinate progress and spinner/skeleton crates for indeterminate loading states. |
| Logs and debug panes | `tui-logger`, `tui-tracing`, `tui-scrollview` | `tui-logger` is established; `tui-tracing` appears newer and should be evaluated before adoption. |
| Modals and overlays | `tui-popup`, `tui-overlay` | Start simple unless drawers/popovers/toasts need a richer overlay abstraction. |
| Lists, tables, and trees | Ratatui `List`, Ratatui `Table`, `tui-widget-list`, `tui-tree-widget`, `ratatui-explorer` | Built-ins are fine for simple rows; use third-party crates for widget rows, trees, and file exploration. |
| Tabs and panes | Ratatui `Tabs`, `ratatui-hypertile`, `panes-ratatui`, `rat-widget`, `rat-salsa` | Built-in tabs may be sufficient initially; pane/layout frameworks need deeper evaluation before adoption. |

## Additional Candidates To Re-Evaluate When Needed

| Crate | Component Types | Caution |
| --- | --- | --- |
| `ratkit` | Resizable splits, tree views, markdown, toasts, dialogs, terminal embedding | Broad and relevant, but very new; could become framework-like if adopted widely. |
| `rat-widget` | Data input widgets, split/tabbed/multi-page structure, table, file dialog, menus, status bar | Broad ecosystem tied to `rat-salsa`; evaluate as a larger implementation direction, not just a single widget. |
| `rat-salsa` | Event queue, tasks, timers, focus handling, dialog windows | Potentially framework-level; would likely require an ADR if adopted as a core UI architecture dependency. |
| `ratatui-interact` | Interactive components, focus management, mouse support | Newer/smaller ecosystem; useful if focus management becomes painful. |
| `rat-menu` | Menus | Candidate for command/menu UI; verify fit against command palette needs. |
| `tui-menu` | Nestable menus | Listed in the Ratatui third-party widget showcase. |
| `ratatui-which-key` | Which-key style keybinding popup | Good for discoverability, not a command palette replacement. |
| `ratatui-explorer` | File explorer widget | Useful for workspace/file navigation if needed. |
| `tui-file-explorer` | Keyboard-driven file browser | Newer/smaller alternative to `ratatui-explorer`. |
| `tui-checkbox` | Checkbox widget | Useful for settings and multi-select dialogs. |
| `ratatui-form` | Form builder | Low adoption; evaluate before using. |
| `tonkotsu` | Text input, select, confirm, number, textarea, file path forms | Very new; relevant but high caution. |
| `ratatui-toaster` | Toast notifications | Useful if non-blocking notifications become important. |
| `ratatui-notifications` | Animated notifications | Verify project legitimacy and maintenance before adoption. |
| `tui-term` | Pseudoterminal widget | Useful only if Eddy embeds terminal sessions. |
| `ansi-to-tui` | ANSI to Ratatui text conversion | Useful for rendering colored process output. |
| `tui-syntax-highlight` | Syntax highlighting | Candidate for code blocks or file previews. |
| `tachyonfx` | Effects and animations | Visual polish only; avoid until core UI works. |

## Research Sources

- Ratatui documentation and built-in widget showcase.
- Ratatui third-party widgets showcase.
- Awesome Ratatui library catalog.
- crates.io searches for Ratatui, TUI widgets, and agent-UI-relevant component names.
