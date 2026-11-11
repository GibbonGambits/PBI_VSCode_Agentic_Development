#!/usr/bin/env python3
"""Find every place in this project that refers to one table, column or measure.

Usage:
    python scripts/find_references.py <folder> "<object>"

    <object>:  "[Total Sales]"          a measure
               "Sales[Amount]"          a column
               "Sales"                  a table

Use it before a rename or a move. A rename or a move always needs the developer's yes. After the yes,
Copilot does the work itself when this script can confirm every reference: it changes each place in the
first list, and then runs the project check, which fails on any reference that was missed (M901 to M903 and
M908 in the model, B001 in the report). When the second list is not empty, Copilot shows it to the developer:
those places need a person's eye.

Three lists are printed:
    1. References it recognises: the definition; DAX that names the object (read with the formula scanner);
       model properties that name it (relationships, sort column, hierarchy level, group-by column,
       aggregation, perspective, translation, security role); report files that use the field.
    2. Text it cannot classify: the same name inside Power Query, a description, an annotation or a report
       text. It may be a reference; it may be a coincidence.
    3. What no file here can show: other reports that use this model once it is published.

Needs Python 3.8 or later. Uses the standard library only. Reads files; never changes them.
Exit code: 0 = listed, 1 = the object is not in the model, 2 = wrong usage.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp  # noqa: E402
import formula_scanner as fs  # noqa: E402
import model_rules  # noqa: E402

REFERENCE_PROPERTIES = (("relationship", "fromcolumn"), ("relationship", "tocolumn"), ("column", "sortbycolumn"),
                        ("level", "column"), ("relatedcolumndetails", "groupbycolumn"),
                        ("alternateof", "basecolumn"), ("alternateof", "basetable"))
NAMED_KINDS = {"perspectivetable": "table", "perspectivecolumn": "column", "perspectivemeasure": "measure",
               "tablepermission": "table", "columnpermission": "column"}


def parse_target(text):
    """('measure', None, name), ('column', table, name) or ('table', table, None)."""
    text = text.strip()
    match = re.match(r"\[(.+)\]\Z", text)
    if match:
        return "measure", None, match.group(1).replace("]]", "]")
    match = re.match(r"(?:'((?:[^']|'')+)'|([^\[\]']+))\[(.+)\]\Z", text)
    if match:
        return "column", (match.group(1) or match.group(2)).replace("''", "'").strip(), match.group(3).replace("]]", "]")
    return "table", text.strip("'").replace("''", "'"), None


def where(path, line, root):
    return "%s:%d" % (os.path.relpath(path, root).replace(os.sep, "/"), line)


def model_references(root, model_dir, objects, kind, table, name):
    """(recognised, definition lines) for one model."""
    found = []
    model = cp.build_model(objects)
    tables = model["tables"]
    measure_names = {m["name"].lower() for t in tables.values() for m in t["measures"]}
    column_owners = {}
    for t in tables.values():
        for c in t["columns"]:
            column_owners.setdefault(c["name"].lower(), set()).add(t["name"])
    for obj in objects:
        if obj["translation"]:
            parent_table = obj["parent"]["name"] if obj["parent"] is not None and obj["parent"]["kind"] == "table" else None
            if (obj["kind"] == kind and obj["name"] == (name or table)
                    and (kind != "column" or parent_table == table)):
                found.append((obj["file"], obj["line"], "a translation of it"))
            continue
        owner = obj["table"]["name"] if obj["table"] is not None else None
        if kind == "table" and obj["kind"] == "table" and obj["top"] and obj["name"] == table:
            found.append((obj["file"], obj["line"], "DEFINITION of the table (its file is named after it)"))
        elif kind == obj["kind"] and obj["name"] == name and (kind == "measure" or owner == table):
            found.append((obj["file"], obj["line"], "DEFINITION of the %s" % kind))
        for object_kind, key in REFERENCE_PROPERTIES:
            if obj["kind"] != object_kind or key not in obj["props"]:
                continue
            target = model_rules._reference(obj["props"][key])
            if target is None:
                continue
            if target[1] is None and key != "basetable":             # a column of the object's own table
                target = (owner or (obj["parent"]["table"]["name"] if obj["parent"] and obj["parent"]["table"] else None), target[0])
            hit = (kind == "table" and target[0] == table) or (kind == "column" and target == (table, name))
            if hit:
                found.append((obj["file"], obj["prop_lines"].get(key, obj["line"]), "%s of %s '%s'" % (key, obj["kind"], obj["name"])))
        if obj["kind"] in NAMED_KINDS:
            parent = obj["parent"]["name"] if obj["parent"] is not None else None
            hit = ((kind == "table" and NAMED_KINDS[obj["kind"]] == "table" and obj["name"] == table)
                   or (kind == NAMED_KINDS[obj["kind"]] and kind != "table" and obj["name"] == name
                       and (kind == "measure" or parent == table)))
            if hit:
                found.append((obj["file"], obj["line"], "%s '%s'" % (obj["kind"], obj["name"])))
    for owner, text in model["expressions"]:
        stream = fs.tokens(text or "", fs.DAX)
        owner_table = owner["table"]["name"] if owner["table"] is not None else (
            owner["name"] if owner["kind"] == "tablepermission" else None)
        hits = set()
        for table_name, reference, _ in fs.dax_references(stream):
            if kind == "measure" and reference.lower() == name.lower():
                if table_name is None and len(column_owners.get(name.lower(), ())) > 0:
                    hits.add("[%s] (a column has the same name: check which one is meant)" % reference)
                else:
                    hits.add("%s[%s]" % (table_name, reference) if table_name else "[%s]" % reference)
            elif kind == "column" and reference.lower() == name.lower():
                if table_name is not None and table_name.lower() == table.lower():
                    hits.add("%s[%s]" % (table_name, reference))
                elif table_name is None and reference.lower() not in measure_names and owner_table == table:
                    hits.add("[%s] (written without its table)" % reference)
                elif table_name is None and reference.lower() not in measure_names and len(column_owners.get(name.lower(), ())) > 1:
                    hits.add("[%s] (written without its table; several tables have this column)" % reference)
            elif kind == "table" and table_name is not None and table_name.lower() == table.lower():
                hits.add("%s[%s]" % (table_name, reference))
        if kind == "table":
            for position, token in enumerate(stream):
                after = stream[position + 1] if position + 1 < len(stream) else None
                if (token.kind in ("word", fs.QUOTED_NAME) and token.value.lower() == table.lower()
                        and (after is None or after.kind != fs.BRACKET_NAME)
                        and not (token.kind == "word" and fs.is_symbol(after, "("))):
                    hits.add("the table by itself")
        if hits:
            found.append((owner["file"], owner["line"], "DAX of %s names %s" % (model_rules._label(owner), ", ".join(sorted(hits)))))
    return found


def report_references(report, kind, table, name):
    """(recognised, unclassified) for one report: (file, text) pairs."""
    recognised, loose = [], []
    wanted = "%s.%s" % (table, name) if kind == "column" else None
    by_file = {}
    for path, entity, prop in cp.report_fields(report):
        by_file.setdefault(path, []).append((entity, prop))
    for folder, dirs, files in os.walk(report):
        dirs[:] = sorted(d for d in dirs if d != ".pbi")
        for file_name in sorted(files):
            if not file_name.lower().endswith(".json"):
                continue
            path = os.path.join(folder, file_name)
            uses = by_file.get(path, [])
            count = 0
            for entity, prop in uses:
                if kind == "table":
                    count += entity == table
                elif kind == "column":
                    count += entity == table and prop == name
                else:
                    count += prop == name
            strings = []
            data = cp.load_json(path)

            def walk(node):
                if isinstance(node, dict):
                    for value in node.values():
                        walk(value)
                elif isinstance(node, list):
                    for value in node:
                        walk(value)
                elif isinstance(node, str):
                    strings.append(node)
            if data is not cp.FAILED:
                walk(data)
            dotted = 0
            other = []
            for text in strings:
                if kind == "table":
                    if text.startswith(table + "."):
                        dotted += 1
                    elif text != table and re.search(r"(?<![\w.])%s(?![\w])" % re.escape(table), text):
                        other.append(text)
                else:
                    short = name
                    if (wanted and text == wanted) or (kind == "measure" and text.endswith("." + short) and "(" not in text):
                        dotted += 1
                    elif text != short and short in text and text != wanted:
                        other.append(text)
            if count or dotted:
                recognised.append((path, "%d field reference(s), %d query name(s) of the form Table.Field" % (count, dotted)))
            for text in other[:5]:
                loose.append((path, "text %s" % json.dumps(text[:90])))
    return recognised, loose


def unclassified_model_text(model_dir, kind, table, name, known_lines):
    """Lines of .tmdl files that hold the name as plain text and were not recognised above."""
    out = []
    needle = name if name is not None else table
    pattern = re.compile(r"(?<![\w])%s(?![\w])" % re.escape(needle))
    for folder, dirs, files in os.walk(os.path.join(model_dir, "definition")):
        dirs.sort()
        for file_name in sorted(files):
            if not file_name.lower().endswith(".tmdl"):
                continue
            path = os.path.join(folder, file_name)
            try:
                with open(path, encoding="utf-8-sig") as handle:
                    lines = cp.split_lines(handle.read())
            except (OSError, UnicodeDecodeError):
                continue
            for number, line in enumerate(lines, 1):
                if (path, number) not in known_lines and pattern.search(line):
                    out.append((path, number, line.strip()[:100]))
    return out


def main(argv):
    cp.safe_output()
    if len(argv) != 3 or argv[1].startswith("-"):
        print(__doc__)
        return 2
    root = os.path.abspath(argv[1])
    kind, table, name = parse_target(argv[2])
    models = cp.find_models(root)
    if not os.path.isdir(root) or not models:
        print("No semantic model found under %s." % argv[1])
        return 2
    recognised, loose, defined = [], [], False
    for model_dir in models:
        objects = cp.check_model(model_dir, cp.Findings())
        found = model_references(root, model_dir, objects, kind, table, name)
        defined = defined or any(text.startswith("DEFINITION") for _, _, text in found)
        recognised.extend((where(path, line, root), text) for path, line, text in found)
        known = set()
        for path, line, text in found:
            known.add((path, line))
        expression_lines = set()
        for obj in objects:
            if obj["has_expr"] or obj["kind"] in ("measure", "column", "tablepermission", "calculationitem", "function"):
                for line in range(obj["line"], obj.get("expr_end", obj["line"]) + 1):
                    expression_lines.add((obj["file"], line))
        dax_owners = {(path, line) for path, line, text in found if text.startswith("DAX of")}
        for path, line, text in unclassified_model_text(model_dir, kind, table, name, known):
            if (path, line) in expression_lines and any(p == path for p, _ in dax_owners):
                continue                                 # a line of a formula already listed above
            loose.append((where(path, line, root), text))
    if not defined:
        print("The model has no %s %s. Write a measure as \"[Name]\", a column as \"Table[Name]\", a table as \"Table\"."
              % (kind, argv[2]))
        return 1
    for report in cp.find_reports(root):
        found, text = report_references(report, kind, table, name)
        recognised.extend((os.path.relpath(path, root).replace(os.sep, "/"), what) for path, what in found)
        loose.extend((os.path.relpath(path, root).replace(os.sep, "/"), what) for path, what in text)
    print("1. References recognised (%d). A rename or a move changes every one of these:" % len(recognised))
    for place, text in recognised:
        print("   %s  %s" % (place, text))
    print("2. Text that cannot be classified (%d)%s" % (len(loose), ": a person looks at each before the change:" if loose else "."))
    for place, text in loose:
        print("   %s  %s" % (place, text))
    print("3. Not in this repository: other reports that use this model after it is published. A rename or a move can "
          "break them, and no file here can show it. Say so to the developer every time.")
    print("After the change: python scripts/check_project.py %s  (M901-M903, M908 and B001 fail on a reference that was missed)."
          % argv[1])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
