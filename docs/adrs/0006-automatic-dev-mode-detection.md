# ADR 0006: Use Debug-Build Source-Tree Detection for Automatic Dev Mode

## Status

Accepted

## Context

Eddy needs a development mode that is convenient for contributors while remaining predictable for normal users. Development mode should be enabled automatically during local development, but it must not accidentally affect release builds, installed binaries, or other execution environments.

The project also needs explicit control for cases where automatic detection is not desired, such as testing production behavior from a source checkout or forcing development behavior in a controlled environment.

## Decision

Automatic development mode is enabled only when Eddy is running as a debug build from Eddy's own source tree.

Eddy also supports explicit command-line overrides:

- `--dev` forces development mode on.
- `--no-dev` forces development mode off.

Explicit overrides take precedence over automatic detection.

## Consequences

Contributors get development behavior by default when running a debug build from the project checkout. Release builds and binaries run outside Eddy's source tree do not enter development mode automatically.

The behavior is conservative and reduces the chance of development-only functionality leaking into normal usage. Tests and troubleshooting can still force either mode through explicit flags.

The detection logic depends on being able to identify both a debug build and Eddy's own source tree. If either signal is unavailable or ambiguous, automatic development mode remains disabled unless `--dev` is provided.

## Alternatives Considered

### Always Enable Development Mode for Debug Builds

This was rejected because debug builds can be run outside the source tree or distributed for diagnostics, where development behavior may be surprising.

### Enable Development Mode Based Only on Source-Tree Location

This was rejected because release builds may be executed from the source tree during packaging or verification and should retain production behavior by default.

### Require Development Mode to Be Explicit Only

This was rejected because it adds friction to the common contributor workflow and makes local development less convenient.
