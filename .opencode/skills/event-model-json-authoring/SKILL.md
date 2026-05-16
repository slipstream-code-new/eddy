---
name: event-model-json-authoring
description: Eddy event-model JSON authoring; use when creating or editing docs/event-model/workflows/*.eventmodel.json or event model schema-like content.
---

# Event Model JSON Authoring

Use this skill when creating or editing Eddy's machine-readable event model files.

## File Layout

Workflow event models live under:

`docs/event-model/workflows/<workflow-name>.eventmodel.json`

Generated HTML lives under:

`docs/event-model/generated/<workflow-name>.html`

Prefer one file per coherent workflow or use case. Do not create one file per tiny slice. Do not create one giant model for unrelated workflows.

## Top-Level Shape

Each workflow model is a JSON object with these required keys:

```json
{
  "name": "Human-readable workflow name",
  "version": "0.1.0",
  "description": "What this workflow model covers.",
  "scope": "Boundary of the workflow and what is intentionally out of scope.",
  "streams": [],
  "events": [],
  "commands": [],
  "read_models": [],
  "slices": []
}
```

The current validator requires `name`, `version`, `streams`, `events`, `commands`, `read_models`, and `slices`. `description` and `scope` are strongly recommended for human and agent understanding.

## Streams

Streams describe consistency boundaries and event sequences.

```json
{
  "name": "repair_ticket",
  "id_pattern": "repair-ticket-{repair_ticket_id}",
  "purpose": "History and consistency boundary for one repair ticket."
}
```

Fields:

- `name`: stable stream name used by events.
- `id_pattern`: how instances are identified.
- `purpose`: why this boundary exists.

## Events

Events are persisted facts. They must reference a known stream.

```json
{
  "name": "RepairTicketOpened",
  "stream": "repair_ticket",
  "description": "A repair ticket was opened for an item brought in by a customer.",
  "attributes": [
    { "name": "repair_ticket_id", "source": "generated.uuid" },
    { "name": "customer_name", "source": "command.customer_name" },
    { "name": "opened_at", "source": "generated.timestamp" }
  ]
}
```

Fields:

- `name`: past-tense fact in PascalCase.
- `stream`: stream that stores the event.
- `description`: what the fact means in business language.
- `attributes`: event payload fields.

Attribute fields:

- `name`: payload field name.
- `source`: where the value comes from.
- `description`: optional explanation when the field is not obvious.
- `type`: optional data type when useful.

Valid event attribute source prefixes:

- `command.<input>` for values supplied by the producing command.
- `generated.<kind>` for generated values like `generated.uuid` or `generated.timestamp`.
- `external.<external_input>.<field>` for values supplied by external inputs listed on the producing command.
- `read_model.<read_model>.<field>` for values read by the producing command.

## Commands

Commands are requests that can produce events.

```json
{
  "name": "OpenRepairTicket",
  "description": "Open a repair ticket for a customer's item.",
  "inputs": ["customer_name", "customer_phone", "item_description"],
  "reads": [],
  "external_inputs": [],
  "produces": ["RepairTicketOpened"]
}
```

Fields:

- `name`: imperative PascalCase action.
- `description`: what the command asks the system to do.
- `inputs`: values provided with the command.
- `reads`: read models needed to decide or enrich the command.
- `external_inputs`: outside data sources used by the command.
- `produces`: events recorded when the command succeeds.

Every event should be produced by at least one command.

## Read Models

Read models are queryable views built from event attributes.

```json
{
  "name": "repair_queue",
  "description": "Tickets staff need to work on.",
  "fields": [
    { "name": "repair_ticket_id", "source": "RepairTicketOpened.repair_ticket_id" },
    { "name": "customer_name", "source": "RepairTicketOpened.customer_name" }
  ]
}
```

Fields:

- `name`: snake_case noun phrase.
- `description`: who or what uses this view.
- `fields`: visible/queryable fields.

Read model field sources must reference known event attributes as `EventName.attribute_name`.

## Slices

Slices are the smallest useful modeled behavior units.

State-change slice:

```json
{
  "type": "state_change",
  "name": "Open a repair ticket",
  "commands": ["OpenRepairTicket"],
  "events": ["RepairTicketOpened"],
  "read_models": ["repair_queue"],
  "given": [],
  "when": "OpenRepairTicket",
  "then": ["RepairTicketOpened"]
}
```

State-view slice:

```json
{
  "type": "state_view",
  "name": "Show repair queue",
  "commands": [],
  "events": ["RepairTicketOpened"],
  "read_models": ["repair_queue"],
  "given": ["RepairTicketOpened"],
  "then": ["repair_queue shows open tickets"]
}
```

Automation slice:

```json
{
  "type": "automation",
  "name": "Notify staff when urgent repair is opened",
  "commands": ["NotifyStaff"],
  "events": ["RepairTicketOpened", "StaffNotificationRequested"],
  "read_models": ["repair_queue"],
  "trigger": "RepairTicketOpened"
}
```

Translation slice:

```json
{
  "type": "translation",
  "name": "Import manufacturer warranty status",
  "commands": ["RecordWarrantyStatus"],
  "events": ["WarrantyStatusRecorded"],
  "read_models": [],
  "external_event": "manufacturer_warranty_response"
}
```

Slice fields:

- `type`: one of `state_change`, `state_view`, `automation`, or `translation`.
- `name`: business-readable phrase.
- `commands`: command names involved in the slice.
- `events`: event names involved in the slice.
- `read_models`: read model names involved in the slice.
- `given`: prior facts for examples.
- `when`: command for state-change examples.
- `then`: expected events, read-model outcomes, or errors.
- `trigger`: event/timer/signal for automations.
- `external_event`: external input for translations.

## Authoring Rules

- Keep JSON valid and deterministic with two-space indentation.
- Do not add speculative behavior to make a model look complete.
- Prefer explicit `description` fields for business meaning, even when the validator does not require them.
- If a source is unknown, pause and ask. Do not invent a source.
- If a rule is unclear, add a scenario only after confirming it with the user.
- Use existing event names consistently across workflow files when they represent the same business fact.
