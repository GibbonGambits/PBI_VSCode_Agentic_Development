#!/usr/bin/env python3
"""Set one property of a model object in its .tmdl file. Nothing else in the file changes.

Usage:
    python scripts/set_model_properties.py <folder> [--dry-run] --set "<object>.<property>=<value>" [--set ...]
    python scripts/set_model_properties.py <folder> [--dry-run] --from-findings M102,M103 [--only "<object>" ...]

<object>    Table[Column], [Measure] or Table, as the project check prints them.
<property>  displayFolder      any object with folders: a measure, a column or a hierarchy
            formatString       a measure or a column
            isHidden           a column, a measure or a table; the only value is true
            summarizeBy        a column; the only value is none
            CalculatedReason   a calculated column or a calculated table: the annotation that says why it is
                               calculated in the model and cannot come from the source

--from-findings takes its changes from the project check: M102 and M103 (hide the column). Add --only to keep
the change to the objects the developer approved.

The script never chooses a folder, a format or a reason: you give the value. It never renames, moves or deletes,
and it does not change data types. It changes one line, or adds one, and writes the file as UTF-8 without BOM
with the line endings it had. A value it cannot place safely is refused and nothing is written.

Save in Power BI Desktop before running this. Afterwards reload the project in Desktop.
Needs Python 3.8 or later. Uses the standard library only.
Exit code: 0 = done, 1 = a change was refused (then no file is written), 2 = wrong usage.
"""
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp  # noqa: E402

PROPERTIES = {"displayfolder": "displayFolder", "formatstring": "formatString", "ishidden": "isHidden",
              "summarizeby": "summarizeBy", cp.REASON_ANNOTATION.lower(): cp.REASON_ANNOTATION}
KINDS = {"displayFolder": ("measure", "column", "hierarchy"), "formatString": ("measure", "column"),
         "isHidden": ("measure", "column", "table"), "summarizeBy": ("column",),
         cp.REASON_ANNOTATION: ("column", "table")}
FROM_FINDINGS = ("M102", "M103")


class Refused(Exception):
    pass


class Files:
    """The .tmdl files of the models under a folder, held in memory so that a dry run changes nothing."""

    def __init__(self, root):
        self.lines = {}
        self.newline = {}
        self.changed = set()
        self.models = cp.find_models(root)
        for model in self.models:
            for folder, dirs, files in os.walk(os.path.join(model, "definition")):
                dirs.sort()
                for name in sorted(files):
                    if name.lower().endswith(".tmdl"):
                        path = os.path.join(folder, name)
                        with open(path, "rb") as fh:
                            text = fh.read().decode("utf-8-sig")
                        self.newline[path] = "\r\n" if "\r\n" in text else "\n"
                        self.lines[path] = text.splitlines()

    def model(self):
        objects = []
        for path in sorted(self.lines):
            objects.extend(cp.check_tmdl_lines(path, self.lines[path], cp.Findings()) or [])
        return cp.build_model(objects)

    def write(self):
        for path in sorted(self.changed):
            newline = self.newline[path]
            payload = (newline.join(self.lines[path]) + newline).encode("utf-8")
            temporary = path + ".tmp"
            with open(temporary, "wb") as fh:
                fh.write(payload)
            os.replace(temporary, path)


def find_object(model, name):
    """The object a name such as Sales[Amount], [Total Sales] or Sales stands for. Raises Refused."""
    m = re.match(r"\s*(.*?)\s*\[(.+)\]\s*\Z", name)
    found = []
    if m:
        table_name, field = cp._unquote(m.group(1)), m.group(2)
        for table in model["tables"].values():
            if table_name and table["name"] != table_name:
                continue
            found.extend(o for o in table["columns"] + table["measures"] + table["hierarchies"] if o["name"] == field
                         and (table_name or o["kind"] == "measure"))
    else:
        table = model["tables"].get(cp._unquote(name.strip()))
        found = table["objects"][:1] if table else []
    if not found:
        raise Refused("object not found: %s (write a column as Table[Column], a measure as [Measure], a table by its name)" % name)
    if len(found) > 1:
        raise Refused("more than one object is called %s" % name)
    return found[0]


def _written(value):
    """A text value as TMDL needs it: in double quotes only when it starts or ends with a space or a quote."""
    if value != value.strip() or value.startswith('"') or value.endswith('"'):
        return '"%s"' % value.replace('"', '""')
    return value


def apply(files, name, prop, value):
    """Change the lines held in 'files'. Returns a text that says what changed, or None when nothing had to."""
    prop = PROPERTIES.get(prop.lower())
    if prop is None:
        raise Refused("property not allowed: only %s" % ", ".join(sorted(PROPERTIES.values())))
    if "\n" in value or "\r" in value:
        raise Refused("the value must be one line")
    model = files.model()
    obj = find_object(model, name)
    if obj["kind"] not in KINDS[prop]:
        raise Refused("%s cannot be set on a %s (%s)" % (prop, obj["kind"], name))
    lines = files.lines[obj["file"]]
    unit = "\t" if any(line.startswith("\t") for line in lines) or not obj["indent"] else "    "
    inner = obj["indent"] + unit
    key = prop.lower()
    if prop == "isHidden":
        if value.strip().lower() != "true":
            raise Refused("isHidden can only be set to true here; to show an object again, edit the file with the developer")
        if obj["hidden"]:
            return None
        lines.insert(obj["expr_end"], inner + "isHidden")
        before = "visible"
    elif prop == cp.REASON_ANNOTATION:
        calculated = obj.get("calculated") if obj["kind"] == "column" else model["tables"][obj["name"]]["calculated"]
        if not calculated:
            raise Refused("%s is not a calculated column or a calculated table" % name)
        if not re.search(r"[^\W_]", value):
            raise Refused("the reason is empty")
        text = "%sannotation %s = %s" % (inner, prop, value.strip())
        before = obj["annotations"].get(prop)
        if before is not None and before.strip() == value.strip():
            return None
        if prop in obj["annotation_lines"]:
            lines[obj["annotation_lines"][prop] - 1] = text
        else:
            lines[obj["last_line"]:obj["last_line"]] = ["", text]
    else:
        if prop == "summarizeBy" and value.strip().lower() != "none":
            raise Refused("summarizeBy can only be set to none here")
        if not value.strip():
            raise Refused("%s needs a value" % prop)
        value = "none" if prop == "summarizeBy" else value
        before = obj["props"].get(key)
        if before == value:
            return None
        text = "%s%s: %s" % (inner, prop, _written(value))
        if key in obj["prop_lines"]:
            lines[obj["prop_lines"][key] - 1] = text
        else:
            lines.insert(obj["expr_end"], text)
    after = find_object(files.model(), name)             # read the result back before it counts
    seen = (("true" if after["hidden"] else None) if prop == "isHidden"
            else after["annotations"].get(prop) if prop == cp.REASON_ANNOTATION else after["props"].get(key))
    wanted = "true" if prop == "isHidden" else value.strip() if prop == cp.REASON_ANNOTATION else value
    if seen != wanted:
        raise Refused("could not place %s on %s safely; change this one in Power BI Desktop" % (prop, name))
    files.changed.add(obj["file"])
    return "%s: %s %s -> %s" % (name, prop, "not set" if before in (None, "") else "'%s'" % before, "'%s'" % wanted)


def main(argv):
    cp.safe_output()
    args = argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    changes, only, codes = [], [], []
    try:
        while len(args) > 1:
            if args[-2] == "--set":
                target, value = args[-1].split("=", 1)
                name, prop = target.rsplit(".", 1)
                changes.insert(0, (name.strip(), prop.strip(), value))
            elif args[-2] == "--only":
                only.append(args[-1].strip())
            elif args[-2] == "--from-findings":
                codes = [c.strip() for c in args[-1].split(",") if c.strip()]
            else:
                break
            del args[-2:]
    except ValueError:
        print(__doc__)
        return 2
    if len(args) != 1 or args[0].startswith("-") or not (changes or codes) or any(c not in FROM_FINDINGS for c in codes):
        print(__doc__)
        return 2
    root = os.path.abspath(args[0])
    files = Files(root)
    if not files.models:
        print("No *.SemanticModel folder with TMDL files found under %s." % args[0])
        return 2
    if codes:
        findings, _, _ = cp.run(root)
        for code, name, prop, value in findings.fixes:
            if code in codes and (not only or name in only) and (name, prop, value) not in changes:
                changes.append((name, prop, value))
    done = 0
    try:
        for name, prop, value in changes:
            message = apply(files, name, prop, value)
            if message:
                done += 1
                print("%s  %s" % ("would change" if dry_run else "changed", message))
            else:
                print("no change  %s: %s is already as asked" % (name, prop))
    except Refused as exc:
        print("refused  %s" % exc)
        print("Nothing was written.")
        return 1
    if not dry_run:
        files.write()
    print("%d change(s) %s in %d file(s)." % (done, "would be made" if dry_run else "made", len(files.changed)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
