#!/usr/bin/env python3
"""Validate information completeness for an event model JSON file."""

import json
import sys


TOP_LEVEL_KEYS = (
    "name",
    "version",
    "streams",
    "events",
    "commands",
    "read_models",
    "slices",
)


def main(argv):
    if len(argv) != 2:
        print("Usage: validate_event_model.py MODEL.json")
        return 2

    path = argv[1]
    try:
        with open(path, "r", encoding="utf-8") as file:
            model = json.load(file)
    except OSError as error:
        print("FAIL: unable to read model")
        print("- %s" % error)
        return 2
    except json.JSONDecodeError as error:
        print("FAIL: invalid JSON")
        print("- %s" % error)
        return 2

    errors = validate(model)
    if errors:
        print("FAIL: event model validation failed with %d error(s)" % len(errors))
        for error in errors:
            print("- %s" % error)
        return 1

    print("OK: event model validation passed")
    return 0


def validate(model):
    errors = []
    if not isinstance(model, dict):
        return ["model must be a JSON object"]

    for key in TOP_LEVEL_KEYS:
        if key not in model:
            errors.append("missing top-level key '%s'" % key)

    streams = require_list(model, "streams", errors)
    events = require_list(model, "events", errors)
    commands = require_list(model, "commands", errors)
    read_models = require_list(model, "read_models", errors)
    slices = require_list(model, "slices", errors)

    stream_names = named_items(streams, "streams", errors)
    event_names = named_items(events, "events", errors)
    command_names = named_items(commands, "commands", errors)
    read_model_names = named_items(read_models, "read_models", errors)

    event_attrs = collect_event_attributes(events, event_names, errors)
    read_model_fields = collect_read_model_fields(read_models, read_model_names, errors)
    command_inputs = collect_named_children(commands, "commands", "inputs", errors)
    command_reads = collect_name_list_children(commands, "commands", "reads", errors)
    command_external_inputs = collect_external_inputs(commands, errors)
    command_outputs = collect_name_list_children(commands, "commands", "produces", errors)
    if not any(command_outputs.values()):
        alternate_outputs = collect_name_list_children(commands, "commands", "events", errors)
        for command_name, output_names in alternate_outputs.items():
            command_outputs[command_name] = output_names

    event_producers = {}
    for command_name, produced_events in command_outputs.items():
        for event_name in produced_events:
            if event_name not in event_names:
                errors.append("command '%s' produces unknown event '%s'" % (command_name, event_name))
                continue
            event_producers.setdefault(event_name, set()).add(command_name)

    for command_name, read_names in command_reads.items():
        for read_name in read_names:
            if read_name not in read_model_names:
                errors.append("command '%s' reads unknown read model '%s'" % (command_name, read_name))

    for event_name in sorted(event_names):
        if event_name not in event_producers:
            errors.append("event '%s' is not produced by any command" % event_name)

    validate_event_sources(
        events,
        event_attrs,
        event_producers,
        command_inputs,
        command_reads,
        command_external_inputs,
        errors,
    )
    validate_read_model_sources(read_models, event_attrs, errors)
    validate_slices(slices, command_names, event_names, read_model_names, errors)

    for event in events:
        if isinstance(event, dict) and "stream" in event and event["stream"] not in stream_names:
            errors.append("event '%s' references unknown stream '%s'" % (event.get("name", "<unnamed>"), event["stream"]))

    return errors


def require_list(model, key, errors):
    value = model.get(key, [])
    if not isinstance(value, list):
        errors.append("top-level key '%s' must be a list" % key)
        return []
    return value


def named_items(items, label, errors):
    names = set()
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            errors.append("%s[%d] must be an object" % (label, index))
            continue
        name = item.get("name")
        if not isinstance(name, str) or not name:
            errors.append("%s[%d] is missing a non-empty name" % (label, index))
            continue
        if name in names:
            errors.append("%s contains duplicate name '%s'" % (label, name))
        names.add(name)
    return names


def collect_event_attributes(events, event_names, errors):
    attrs_by_event = {}
    for event in events:
        if not isinstance(event, dict):
            continue
        event_name = event.get("name")
        if event_name not in event_names:
            continue
        attrs = named_child_set(event, "attributes", "event '%s'" % event_name, errors)
        attrs_by_event[event_name] = attrs
    return attrs_by_event


def collect_read_model_fields(read_models, read_model_names, errors):
    fields_by_read_model = {}
    for read_model in read_models:
        if not isinstance(read_model, dict):
            continue
        read_model_name = read_model.get("name")
        if read_model_name not in read_model_names:
            continue
        fields = named_child_set(read_model, "fields", "read model '%s'" % read_model_name, errors)
        fields_by_read_model[read_model_name] = fields
    return fields_by_read_model


def collect_named_children(items, label, child_key, errors):
    children_by_parent = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            continue
        children_by_parent[item["name"]] = named_child_set(item, child_key, "%s '%s'" % (label[:-1], item["name"]), errors)
    return children_by_parent


def named_child_set(item, child_key, context, errors):
    children = item.get(child_key, [])
    if not isinstance(children, list):
        errors.append("%s key '%s' must be a list" % (context, child_key))
        return set()

    names = set()
    for index, child in enumerate(children):
        if isinstance(child, str):
            name = child
        elif isinstance(child, dict):
            name = child.get("name")
        else:
            errors.append("%s %s[%d] must be an object or string" % (context, child_key, index))
            continue
        if not isinstance(name, str) or not name:
            errors.append("%s %s[%d] is missing a non-empty name" % (context, child_key, index))
            continue
        names.add(name)
    return names


def collect_name_list_children(items, label, child_key, errors):
    values_by_parent = {}
    for item in items:
        if not isinstance(item, dict) or not isinstance(item.get("name"), str):
            continue
        parent_name = item["name"]
        values = item.get(child_key, [])
        if not isinstance(values, list):
            errors.append("%s '%s' key '%s' must be a list" % (label[:-1], parent_name, child_key))
            values_by_parent[parent_name] = set()
            continue
        names = set()
        for index, value in enumerate(values):
            name = value.get("name") if isinstance(value, dict) else value
            if not isinstance(name, str) or not name:
                errors.append("%s '%s' %s[%d] is missing a non-empty name" % (label[:-1], parent_name, child_key, index))
                continue
            names.add(name)
        values_by_parent[parent_name] = names
    return values_by_parent


def collect_external_inputs(commands, errors):
    external_by_command = {}
    for command in commands:
        if not isinstance(command, dict) or not isinstance(command.get("name"), str):
            continue
        command_name = command["name"]
        external_inputs = command.get("external_inputs", [])
        if not isinstance(external_inputs, list):
            errors.append("command '%s' key 'external_inputs' must be a list" % command_name)
            external_by_command[command_name] = set()
            continue
        names = set()
        for index, external_input in enumerate(external_inputs):
            name = external_input.get("name") if isinstance(external_input, dict) else external_input
            if not isinstance(name, str) or not name:
                errors.append("command '%s' external_inputs[%d] is missing a non-empty name" % (command_name, index))
                continue
            names.add(name)
        external_by_command[command_name] = names
    return external_by_command


def validate_event_sources(events, event_attrs, event_producers, command_inputs, command_reads, command_external_inputs, errors):
    for event in events:
        if not isinstance(event, dict) or not isinstance(event.get("name"), str):
            continue
        event_name = event["name"]
        attributes = event.get("attributes", [])
        if not isinstance(attributes, list):
            continue
        for index, attribute in enumerate(attributes):
            if not isinstance(attribute, dict):
                continue
            attr_name = attribute.get("name", "<unnamed>")
            source = attribute.get("source")
            if not isinstance(source, str) or not source:
                errors.append("event '%s' attribute '%s' is missing source" % (event_name, attr_name))
                continue
            if not source_is_valid(source, event_producers.get(event_name, set()), command_inputs, command_reads, command_external_inputs):
                errors.append("event '%s' attribute '%s' has invalid source '%s'" % (event_name, attr_name, source))
        event_attrs.setdefault(event_name, set())


def source_is_valid(source, producer_names, command_inputs, command_reads, command_external_inputs):
    if source.startswith("generated.") and len(source) > len("generated."):
        return True
    if source.startswith("command."):
        input_name = source[len("command."):].split(".", 1)[0]
        return any(input_name in command_inputs.get(command_name, set()) for command_name in producer_names)
    if source.startswith("external."):
        remainder = source[len("external."):]
        external_name = remainder.split(".", 1)[0]
        return bool(external_name) and any(external_name in command_external_inputs.get(command_name, set()) for command_name in producer_names)
    if source.startswith("read_model."):
        remainder = source[len("read_model."):]
        read_model_name = remainder.split(".", 1)[0]
        return bool(read_model_name) and any(read_model_name in command_reads.get(command_name, set()) for command_name in producer_names)
    return False


def validate_read_model_sources(read_models, event_attrs, errors):
    known_sources = set()
    for event_name, attrs in event_attrs.items():
        for attr_name in attrs:
            known_sources.add("%s.%s" % (event_name, attr_name))

    for read_model in read_models:
        if not isinstance(read_model, dict) or not isinstance(read_model.get("name"), str):
            continue
        read_model_name = read_model["name"]
        fields = read_model.get("fields", [])
        if not isinstance(fields, list):
            continue
        for field in fields:
            if not isinstance(field, dict):
                continue
            field_name = field.get("name", "<unnamed>")
            source = field.get("source")
            if not isinstance(source, str) or not source:
                errors.append("read model '%s' field '%s' is missing source" % (read_model_name, field_name))
                continue
            normalized = source[len("event."):] if source.startswith("event.") else source
            if normalized not in known_sources:
                errors.append("read model '%s' field '%s' references unknown event attribute '%s'" % (read_model_name, field_name, source))


def validate_slices(slices, command_names, event_names, read_model_names, errors):
    for index, slice_item in enumerate(slices):
        if not isinstance(slice_item, dict):
            errors.append("slices[%d] must be an object" % index)
            continue
        slice_name = slice_item.get("name", "slices[%d]" % index)
        validate_slice_refs(slice_item, slice_name, "commands", command_names, errors)
        validate_slice_refs(slice_item, slice_name, "events", event_names, errors)
        validate_slice_refs(slice_item, slice_name, "read_models", read_model_names, errors)

        slice_type = slice_item.get("type")
        if slice_type == "state_change":
            require_gwt(slice_item, slice_name, errors)
        elif slice_type == "state_view":
            require_gt(slice_item, slice_name, errors)


def validate_slice_refs(slice_item, slice_name, key, known_names, errors):
    values = slice_item.get(key, [])
    if not isinstance(values, list):
        errors.append("slice '%s' key '%s' must be a list" % (slice_name, key))
        return
    singular = key[:-1] if key != "read_models" else "read_model"
    for index, value in enumerate(values):
        name = value.get("name") if isinstance(value, dict) else value
        if not isinstance(name, str) or not name:
            errors.append("slice '%s' %s[%d] is missing a non-empty name" % (slice_name, key, index))
            continue
        if name not in known_names:
            errors.append("slice '%s' references unknown %s '%s'" % (slice_name, singular, name))


def require_gwt(slice_item, slice_name, errors):
    missing = [key for key in ("given", "when", "then") if key not in slice_item]
    if "when" in slice_item and not slice_item.get("when"):
        missing.append("when")
    if "then" in slice_item and not slice_item.get("then"):
        missing.append("then")
    if missing:
        errors.append("state_change slice '%s' is missing GWT key(s): %s" % (slice_name, ", ".join(missing)))


def require_gt(slice_item, slice_name, errors):
    missing = [key for key in ("given", "then") if key not in slice_item]
    if "then" in slice_item and not slice_item.get("then"):
        missing.append("then")
    if missing:
        errors.append("state_view slice '%s' is missing GT key(s): %s" % (slice_name, ", ".join(missing)))


if __name__ == "__main__":
    sys.exit(main(sys.argv))
