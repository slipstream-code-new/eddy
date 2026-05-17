# Verification

Run the narrow test that proves the current RGR cycle before broader gates. Use `just` recipes for local test commands; Rust test recipes must run through nextest.

For event-model slices, the narrow outer test is the focused Cucumber scenario against the compiled, running program. Run lower-level Rust tests only for drill-down cycles beneath that accepted outer RED, using a `just` recipe backed by nextest, then return to the Cucumber scenario before declaring the slice green.

Before handoff, run the strongest relevant gate feasible for the change: `just fmt`, `just clippy`, `just test`, `just deny`, `just build`, or `just ci`. If a gate is skipped, state why.
