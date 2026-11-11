#!/usr/bin/env python3
"""Check a project JSON file against the Microsoft schema its '$schema' line names.

Usage:
    python scripts/json_schema.py <file or folder> [...]

Microsoft publishes a JSON schema for every report file of a Power BI project (page.json, visual.json,
report.json, bookmarks and so on) at https://github.com/microsoft/json-schemas (MIT licence). A copy of
every published version of each schema is kept in scripts/schemas/, so this check needs no network and gives
the same answer every time. maintenance/sources.md records the commit the copy was taken from.

A file whose '$schema' names a version that is not in scripts/schemas/ is not checked; the script says so.

This is a small validator for the parts of JSON Schema (draft-07) that Microsoft's schemas use:
type, properties, patternProperties, additionalProperties, required, items, maxItems, enum, const,
anyOf, oneOf, allOf, $ref (inside a file and to another schema), minLength, maxLength and pattern.

Needs Python 3.8 or later. Uses the standard library only. Reads files; never changes them.
Exit code: 0 = every file passes, 1 = at least one problem, 2 = wrong usage.
"""
import json
import os
import posixpath
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SCHEMA_FOLDER = os.path.join(HERE, "schemas")
ADDRESS_PREFIX = "https://developer.microsoft.com/json-schemas/"
CHECKED_ENDINGS = (".json", ".pbir", ".pbism", ".platform")
MAX_PROBLEMS = 5                    # per file: the first few say enough

_cache = {}


def schema_path(address):
    """Where the copy of a schema address is kept, or None when the address is not Microsoft's."""
    if not isinstance(address, str) or not address.startswith(ADDRESS_PREFIX):
        return None
    relative = address[len(ADDRESS_PREFIX):].split("#")[0]
    if ".." in relative.split("/"):
        return None
    return os.path.join(SCHEMA_FOLDER, *relative.split("/"))


def load_schema(address):
    """The schema for an address, or None when no copy is kept."""
    path = schema_path(address)
    if path is None:
        return None
    if path not in _cache:
        try:
            with open(path, encoding="utf-8-sig") as handle:
                _cache[path] = json.load(handle)
        except (OSError, ValueError):
            _cache[path] = None
    return _cache[path]


def _type_ok(value, name):
    if name == "object":
        return isinstance(value, dict)
    if name == "array":
        return isinstance(value, list)
    if name == "string":
        return isinstance(value, str)
    if name == "boolean":
        return isinstance(value, bool)
    if name == "null":
        return value is None
    if name == "integer":
        return (isinstance(value, int) and not isinstance(value, bool)) or (isinstance(value, float) and value.is_integer())
    if name == "number":
        return isinstance(value, (int, float)) and not isinstance(value, bool)
    return True


def _same(first, second):
    """JSON equality: true is not 1."""
    if isinstance(first, bool) or isinstance(second, bool):
        return isinstance(first, bool) and isinstance(second, bool) and first == second
    return first == second


def _resolve(reference, root, address):
    """(schema, root, address) that a '$ref' points to; schema is None when it cannot be found."""
    target, _, pointer = reference.partition("#")
    if target:
        if "://" not in target:                      # a path beside the schema that holds the reference
            folder = posixpath.dirname(address)
            target = folder.split("://")[0] + "://" + posixpath.normpath(posixpath.join(folder.split("://", 1)[1], target))
        address = target
        root = load_schema(target)
        if root is None:
            return None, None, address
    node = root
    for part in [p for p in pointer.split("/") if p]:
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(node, dict) and part in node:
            node = node[part]
        else:
            return None, root, address
    return node, root, address


def validate(value, schema, root, address, path="", problems=None, depth=0):
    """Add to 'problems' one line for each place where value does not fit schema. Returns problems."""
    if problems is None:
        problems = []
    if len(problems) >= MAX_PROBLEMS or depth > 200 or schema is True or not isinstance(schema, dict):
        if schema is False:
            problems.append("%s: nothing is allowed here" % (path or "(top)"))
        return problems
    where = path or "(top)"
    reference = schema.get("$ref")
    if isinstance(reference, str):
        target, target_root, target_address = _resolve(reference, root, address)
        if target is None:
            problems.append("%s: the schema refers to %s, which is not in scripts/schemas" % (where, reference))
        else:
            validate(value, target, target_root, target_address, path, problems, depth + 1)
    kinds = schema.get("type")
    if kinds is not None:
        kinds = kinds if isinstance(kinds, list) else [kinds]
        if not any(_type_ok(value, kind) for kind in kinds):
            problems.append("%s: must be %s" % (where, " or ".join(str(k) for k in kinds)))
            return problems
    if "const" in schema and not _same(value, schema["const"]):
        problems.append("%s: must be %s" % (where, json.dumps(schema["const"])))
    if isinstance(schema.get("enum"), list) and not any(_same(value, option) for option in schema["enum"]):
        shown = ", ".join(json.dumps(option) for option in schema["enum"][:12])
        problems.append("%s: %s is not one of the allowed values (%s%s)"
                        % (where, json.dumps(value)[:60], shown, ", ..." if len(schema["enum"]) > 12 else ""))
    if isinstance(value, str):
        if isinstance(schema.get("maxLength"), int) and len(value) > schema["maxLength"]:
            problems.append("%s: longer than %d characters" % (where, schema["maxLength"]))
        if isinstance(schema.get("minLength"), int) and len(value) < schema["minLength"]:
            problems.append("%s: shorter than %d characters" % (where, schema["minLength"]))
        if isinstance(schema.get("pattern"), str):
            try:
                if re.search(schema["pattern"], value) is None:
                    problems.append("%s: does not match the pattern %s" % (where, schema["pattern"]))
            except re.error:
                pass
    if isinstance(value, dict):
        properties = schema.get("properties") if isinstance(schema.get("properties"), dict) else {}
        patterns = schema.get("patternProperties") if isinstance(schema.get("patternProperties"), dict) else {}
        for name in schema.get("required") if isinstance(schema.get("required"), list) else []:
            if name not in value:
                problems.append("%s: the required property '%s' is missing" % (where, name))
        extra = schema.get("additionalProperties")
        for name, item in value.items():
            known = False
            if name in properties:
                known = True
                validate(item, properties[name], root, address, "%s/%s" % (path, name), problems, depth + 1)
            for pattern, sub in patterns.items():
                try:
                    hit = re.search(pattern, name) is not None
                except re.error:
                    hit = False
                if hit:
                    known = True
                    validate(item, sub, root, address, "%s/%s" % (path, name), problems, depth + 1)
            if not known:
                if extra is False:
                    problems.append("%s: the property '%s' is not in Microsoft's schema" % (where, name))
                elif isinstance(extra, dict):
                    validate(item, extra, root, address, "%s/%s" % (path, name), problems, depth + 1)
    if isinstance(value, list):
        if isinstance(schema.get("maxItems"), int) and len(value) > schema["maxItems"]:
            problems.append("%s: more than %d entries" % (where, schema["maxItems"]))
        if isinstance(schema.get("minItems"), int) and len(value) < schema["minItems"]:
            problems.append("%s: fewer than %d entries" % (where, schema["minItems"]))
        items = schema.get("items")
        if isinstance(items, dict):
            for index, item in enumerate(value):
                validate(item, items, root, address, "%s/%d" % (path, index), problems, depth + 1)
    for key in ("allOf",):
        for sub in schema.get(key) if isinstance(schema.get(key), list) else []:
            validate(value, sub, root, address, path, problems, depth + 1)
    for key in ("anyOf", "oneOf"):
        options = schema.get(key)
        if not isinstance(options, list) or not options:
            continue
        results = [validate(value, sub, root, address, path, [], depth + 1) for sub in options]
        passed = sum(1 for result in results if not result)
        if passed == 0:
            best = min(results, key=len)
            problems.append("%s: fits none of the %d allowed forms (closest: %s)"
                            % (where, len(options), best[0] if best else "?"))
        elif key == "oneOf" and passed > 1:
            problems.append("%s: fits %d forms where exactly one is allowed" % (where, passed))
    return problems


def check_value(data):
    """(state, problems) for one parsed JSON file.

    state: 'ok', 'failed', 'no schema line' (nothing to check against), 'not microsoft' or 'not shipped'.
    """
    address = data.get("$schema") if isinstance(data, dict) else None
    if not isinstance(address, str):
        return "no schema line", []
    if schema_path(address) is None:
        return "not microsoft", []
    schema = load_schema(address)
    if schema is None:
        return "not shipped", []
    problems = validate(data, schema, schema, address)[:MAX_PROBLEMS]
    return ("failed" if problems else "ok"), problems


def shipped_versions():
    """{schema name: [versions kept in scripts/schemas]}, for messages."""
    out = {}
    for folder, _, files in os.walk(SCHEMA_FOLDER):
        if "schema.json" in files:
            parts = os.path.relpath(folder, SCHEMA_FOLDER).split(os.sep)
            out.setdefault("/".join(parts[:-1]), []).append(parts[-1])
    return out


def main(argv):
    if len(argv) < 2 or argv[1].startswith("-"):
        print(__doc__)
        return 2
    files = []
    for target in argv[1:]:
        if os.path.isdir(target):
            for folder, dirs, names in os.walk(target):
                dirs[:] = sorted(d for d in dirs if d not in (".git", ".pbi", "node_modules", "schemas"))
                files.extend(os.path.join(folder, n) for n in sorted(names) if n.lower().endswith(CHECKED_ENDINGS))
        else:
            files.append(target)
    bad = checked = skipped = 0
    for path in files:
        try:
            with open(path, encoding="utf-8-sig") as handle:
                data = json.load(handle)
        except (OSError, ValueError) as exc:
            print("%s  cannot be read as JSON: %s" % (path, str(exc)[:120]))
            bad += 1
            continue
        state, problems = check_value(data)
        if state == "failed":
            bad += 1
            for line in problems:
                print("%s  %s" % (path, line))
        elif state == "ok":
            checked += 1
        else:
            skipped += 1
            if state == "not shipped":
                print("%s  not checked: no copy of %s in scripts/schemas" % (path, data.get("$schema")))
    print("Schema check: %d file(s) pass, %d with problems, %d not checked." % (checked, bad, skipped))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
