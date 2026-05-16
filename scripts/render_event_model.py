#!/usr/bin/env python3
"""Render an event model JSON document as human-readable HTML."""

import json
import sys
from html import escape


def text(value):
    if value is None:
        return ""
    if isinstance(value, (dict, list)):
        return json.dumps(value, sort_keys=True)
    return str(value)


def html_text(value):
    return escape(text(value), quote=True)


def as_list(value):
    if value is None:
        return []
    if isinstance(value, list):
        return value
    return [value]


def get_any(mapping, *keys, default=None):
    if not isinstance(mapping, dict):
        return default
    for key in keys:
        if key in mapping:
            return mapping[key]
    return default


def title_of(item, fallback="Untitled"):
    if isinstance(item, dict):
        return get_any(item, "name", "title", "id", "event", "command", default=fallback)
    return item if item is not None else fallback


def render_list(items):
    values = as_list(items)
    if not values:
        return '<p class="muted">None.</p>'
    out = ["<ul>"]
    for item in values:
        out.append(f"<li>{html_text(item)}</li>")
    out.append("</ul>")
    return "\n".join(out)


def render_key_values(mapping, skip=()):
    if not isinstance(mapping, dict):
        return f"<p>{html_text(mapping)}</p>" if mapping is not None else ""
    rows = []
    for key in sorted(mapping):
        if key in skip:
            continue
        value = mapping[key]
        if isinstance(value, (dict, list)):
            value = json.dumps(value, indent=2, sort_keys=True)
            rows.append(
                "<tr>"
                f"<th>{html_text(key)}</th>"
                f"<td><pre>{html_text(value)}</pre></td>"
                "</tr>"
            )
        else:
            rows.append(
                "<tr>"
                f"<th>{html_text(key)}</th>"
                f"<td>{html_text(value)}</td>"
                "</tr>"
            )
    if not rows:
        return ""
    return '<table class="kv"><tbody>' + "\n".join(rows) + "</tbody></table>"


def render_overview(model):
    overview = get_any(model, "overview", "summary", "description", default=None)
    parts = ['<section id="overview"><h2>Overview</h2>']
    if isinstance(overview, dict):
        parts.append(render_key_values(overview))
    elif overview:
        parts.append(f"<p>{html_text(overview)}</p>")
    else:
        parts.append('<p class="muted">No overview provided.</p>')

    metadata = get_any(model, "metadata", "meta", default=None)
    if metadata:
        parts.append("<h3>Metadata</h3>")
        parts.append(render_key_values(metadata))
    parts.append("</section>")
    return "\n".join(parts)


def render_streams(model):
    streams = as_list(get_any(model, "streams", "event_streams", default=[]))
    parts = ['<section id="streams"><h2>Streams</h2>']
    if not streams:
        parts.append('<p class="muted">No streams provided.</p>')
    for stream in streams:
        parts.append('<article class="card">')
        parts.append(f"<h3>{html_text(title_of(stream, 'Stream'))}</h3>")
        if isinstance(stream, dict):
            parts.append(render_key_values(stream, skip=("name", "title", "id", "events", "commands")))
            events = get_any(stream, "events", default=[])
            commands = get_any(stream, "commands", default=[])
            if events:
                parts.append("<h4>Events</h4>")
                parts.append(render_list(events))
            if commands:
                parts.append("<h4>Commands</h4>")
                parts.append(render_list(commands))
        else:
            parts.append(f"<p>{html_text(stream)}</p>")
        parts.append("</article>")
    parts.append("</section>")
    return "\n".join(parts)


def render_timeline(model):
    timeline = as_list(get_any(model, "timeline", "slices", "time_slices", default=[]))
    parts = ['<section id="timeline"><h2>Timeline / Slices</h2>']
    if not timeline:
        parts.append('<p class="muted">No timeline or slices provided.</p>')
    for index, item in enumerate(timeline, 1):
        parts.append('<article class="card slice">')
        parts.append(f"<h3>{index}. {html_text(title_of(item, 'Slice'))}</h3>")
        if isinstance(item, dict):
            parts.append(render_key_values(item, skip=("name", "title", "id", "commands", "events", "read_models")))
            for label, key in (("Commands", "commands"), ("Events", "events"), ("Read Models", "read_models")):
                values = get_any(item, key, default=[])
                if values:
                    parts.append(f"<h4>{label}</h4>")
                    parts.append(render_list(values))
        else:
            parts.append(f"<p>{html_text(item)}</p>")
        parts.append("</article>")
    parts.append("</section>")
    return "\n".join(parts)


def render_commands(model):
    commands = as_list(get_any(model, "commands", default=[]))
    parts = ['<section id="commands"><h2>Commands</h2>']
    if not commands:
        parts.append('<p class="muted">No commands provided.</p>')
    for command in commands:
        parts.append('<article class="card">')
        parts.append(f"<h3>{html_text(title_of(command, 'Command'))}</h3>")
        if isinstance(command, dict):
            parts.append(render_key_values(command, skip=("name", "title", "id", "emits", "events", "attributes", "fields")))
            fields = get_any(command, "attributes", "fields", default=[])
            emits = get_any(command, "emits", "events", default=[])
            if fields:
                parts.append("<h4>Attributes</h4>")
                parts.append(render_list(fields))
            if emits:
                parts.append("<h4>Emits</h4>")
                parts.append(render_list(emits))
        else:
            parts.append(f"<p>{html_text(command)}</p>")
        parts.append("</article>")
    parts.append("</section>")
    return "\n".join(parts)


def render_attributes(attributes):
    values = as_list(attributes)
    if not values:
        return '<p class="muted">No attributes provided.</p>'
    rows = []
    for attr in values:
        if isinstance(attr, dict):
            name = title_of(attr, "Attribute")
            typ = get_any(attr, "type", "kind", default="")
            source = get_any(attr, "source", "from", "sources", default="")
            desc = get_any(attr, "description", "notes", default="")
            rows.append(
                "<tr>"
                f"<td>{html_text(name)}</td>"
                f"<td>{html_text(typ)}</td>"
                f"<td>{html_text(source)}</td>"
                f"<td>{html_text(desc)}</td>"
                "</tr>"
            )
        else:
            rows.append(f"<tr><td>{html_text(attr)}</td><td></td><td></td><td></td></tr>")
    return (
        '<table><thead><tr><th>Attribute</th><th>Type</th><th>Source</th><th>Description</th></tr></thead><tbody>'
        + "\n".join(rows)
        + "</tbody></table>"
    )


def render_events(model):
    events = as_list(get_any(model, "events", default=[]))
    parts = ['<section id="events"><h2>Events</h2>']
    if not events:
        parts.append('<p class="muted">No events provided.</p>')
    for event in events:
        parts.append('<article class="card">')
        parts.append(f"<h3>{html_text(title_of(event, 'Event'))}</h3>")
        if isinstance(event, dict):
            parts.append(render_key_values(event, skip=("name", "title", "id", "attributes", "fields", "sources", "source")))
            sources = get_any(event, "sources", "source", default=[])
            if sources:
                parts.append("<h4>Sources</h4>")
                parts.append(render_list(sources))
            parts.append("<h4>Attributes</h4>")
            parts.append(render_attributes(get_any(event, "attributes", "fields", default=[])))
        else:
            parts.append(f"<p>{html_text(event)}</p>")
        parts.append("</article>")
    parts.append("</section>")
    return "\n".join(parts)


def render_field_sources(fields):
    values = as_list(fields)
    if not values:
        return '<p class="muted">No fields provided.</p>'
    rows = []
    for field in values:
        if isinstance(field, dict):
            name = title_of(field, "Field")
            typ = get_any(field, "type", "kind", default="")
            source = get_any(field, "source", "from", "sources", default="")
            desc = get_any(field, "description", "notes", default="")
            rows.append(
                "<tr>"
                f"<td>{html_text(name)}</td>"
                f"<td>{html_text(typ)}</td>"
                f"<td>{html_text(source)}</td>"
                f"<td>{html_text(desc)}</td>"
                "</tr>"
            )
        else:
            rows.append(f"<tr><td>{html_text(field)}</td><td></td><td></td><td></td></tr>")
    return (
        '<table><thead><tr><th>Field</th><th>Type</th><th>Source</th><th>Description</th></tr></thead><tbody>'
        + "\n".join(rows)
        + "</tbody></table>"
    )


def render_read_models(model):
    read_models = as_list(get_any(model, "read_models", "readModels", "projections", default=[]))
    parts = ['<section id="read-models"><h2>Read Models</h2>']
    if not read_models:
        parts.append('<p class="muted">No read models provided.</p>')
    for read_model in read_models:
        parts.append('<article class="card">')
        parts.append(f"<h3>{html_text(title_of(read_model, 'Read Model'))}</h3>")
        if isinstance(read_model, dict):
            parts.append(render_key_values(read_model, skip=("name", "title", "id", "fields", "attributes")))
            parts.append("<h4>Field Sources</h4>")
            parts.append(render_field_sources(get_any(read_model, "fields", "attributes", default=[])))
        else:
            parts.append(f"<p>{html_text(read_model)}</p>")
        parts.append("</article>")
    parts.append("</section>")
    return "\n".join(parts)


def render_scenarios(model):
    scenarios = as_list(get_any(model, "scenarios", "examples", default=[]))
    parts = ['<section id="scenarios"><h2>Scenarios</h2>']
    if not scenarios:
        parts.append('<p class="muted">No scenarios provided.</p>')
    for scenario in scenarios:
        parts.append('<article class="card">')
        parts.append(f"<h3>{html_text(title_of(scenario, 'Scenario'))}</h3>")
        if isinstance(scenario, dict):
            parts.append(render_key_values(scenario, skip=("name", "title", "id", "given", "when", "then")))
            for label, key in (("Given", "given"), ("When", "when"), ("Then", "then")):
                value = get_any(scenario, key, default=[])
                if value:
                    parts.append(f"<h4>{label}</h4>")
                    parts.append(render_list(value))
        else:
            parts.append(f"<p>{html_text(scenario)}</p>")
        parts.append("</article>")
    parts.append("</section>")
    return "\n".join(parts)


def render_document(model):
    title = get_any(model, "name", "title", default="Event Model") if isinstance(model, dict) else "Event Model"
    if not isinstance(model, dict):
        model = {"overview": model}
    body = "\n".join(
        [
            render_overview(model),
            render_streams(model),
            render_timeline(model),
            render_commands(model),
            render_events(model),
            render_read_models(model),
            render_scenarios(model),
        ]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{html_text(title)}</title>
<style>
:root {{ color-scheme: light; --bg: #f7f7f4; --card: #ffffff; --ink: #202124; --muted: #666b70; --line: #d8dadc; --accent: #345995; }}
body {{ margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.5 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }}
main {{ max-width: 1040px; margin: 0 auto; padding: 32px 20px 56px; }}
h1 {{ margin: 0 0 24px; font-size: 2.2rem; line-height: 1.1; }}
h2 {{ margin: 36px 0 12px; padding-bottom: 6px; border-bottom: 2px solid var(--line); color: var(--accent); }}
h3 {{ margin: 0 0 10px; }}
h4 {{ margin: 18px 0 8px; }}
.card {{ background: var(--card); border: 1px solid var(--line); border-radius: 10px; padding: 16px; margin: 12px 0; box-shadow: 0 1px 2px rgba(0, 0, 0, 0.04); }}
.slice {{ border-left: 5px solid var(--accent); }}
.muted {{ color: var(--muted); }}
table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
th, td {{ border: 1px solid var(--line); padding: 8px 10px; text-align: left; vertical-align: top; }}
th {{ background: #eef1f5; font-weight: 650; }}
.kv th {{ width: 190px; }}
pre {{ margin: 0; white-space: pre-wrap; word-break: break-word; font: 0.9rem/1.45 ui-monospace, SFMono-Regular, Consolas, "Liberation Mono", monospace; }}
ul {{ margin-top: 8px; }}
@media (max-width: 720px) {{ main {{ padding: 22px 12px 40px; }} table {{ display: block; overflow-x: auto; }} }}
</style>
</head>
<body>
<main>
<h1>{html_text(title)}</h1>
{body}
</main>
</body>
</html>
"""


def main(argv):
    if len(argv) != 2:
        print("usage: render_event_model.py MODEL.json", file=sys.stderr)
        return 2
    try:
        with open(argv[1], "r", encoding="utf-8") as source:
            model = json.load(source)
    except OSError as exc:
        print(f"error: cannot read {argv[1]}: {exc}", file=sys.stderr)
        return 1
    except json.JSONDecodeError as exc:
        print(f"error: invalid JSON in {argv[1]}: {exc}", file=sys.stderr)
        return 1
    sys.stdout.write(render_document(model))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
