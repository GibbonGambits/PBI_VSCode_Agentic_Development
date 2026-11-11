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
import collections
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


Line = collections.namedtuple("Line", "text end")


class Files:
    """The .tmdl files of the models under a folder, held in memory so that a dry run changes nothing."""

    def __init__(self, root):
        self.lines = {}             # path -> list of Line: the text of a line and its own line ending
        self.newline = {}           # path -> the ending a new line gets
        self.changed = set()
        self.models = cp.find_models(root)
        for model in self.models:
            for folder, dirs, files in os.walk(os.path.join(model, "definition")):
                dirs.sort()
                for name in sorted(files):
                    if name.lower().endswith(".tmdl"):
                        path = os.path.join(folder, name)
                        with open(path, "rb") as fh:
                            raw = fh.read()
                        try:
                            text = raw.decode("utf-8-sig")
                        except UnicodeDecodeError:
                            raise Refused("%s is not UTF-8 text; save it as UTF-8 without BOM first" % path)
                        parts = re.split(r"(\r\n|\n)", text)         # only real line breaks; each line keeps its own
                        pairs = [Line(parts[i], parts[i + 1] if i + 1 < len(parts) else "") for i in range(0, len(parts), 2)]
                        if pairs and pairs[-1] == Line("", ""):
                            pairs.pop()
                        self.newline[path] = "\r\n" if text.count("\r\n") * 2 > text.count("\n") else "\n"
                        self.lines[path] = pairs

    def text_lines(self, path):
        return [line.text for line in self.lines[path]]

    def insert(self, path, index, texts):
        """Put new lines before position 'index' (0-based). The line before them gets an ending if it had none."""
        lines = self.lines[path]
        if 0 < index <= len(lines) and lines[index - 1].end == "":
            lines[index - 1] = Line(lines[index - 1].text, self.newline[path])
            lines[index:index] = [Line(t, self.newline[path]) for t in texts[:-1]] + [Line(texts[-1], "")]
        else:
            lines[index:index] = [Line(t, self.newline[path]) for t in texts]

    def replace(self, path, index, text):
        self.lines[path][index] = Line(text, self.lines[path][index].end)

    def model(self):
        objects = []
        for path in sorted(self.lines):
            objects.extend(cp.check_tmdl_lines(path, self.text_lines(path), cp.Findings()) or [])
        return cp.build_model(objects)

    def write(self):
        for path in sorted(self.changed):
            payload = "".join(line.text + line.end for line in self.lines[path]).encode("utf-8")
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


def _indent_unit(lines, obj):
    """One level of indentation, as this file writes it below this object: a tab, or the spaces it uses."""
    for line in lines[obj["line"]:]:
        if line.strip():
            lead = line[:len(line) - len(line.lstrip(" \t"))]
            if lead.startswith(obj["indent"]) and len(lead) > len(obj["indent"]) and not obj["has_expr"]:
                return lead[len(obj["indent"]):]
            break
    for line in lines:
        lead = line[:len(line) - len(line.lstrip(" \t"))]
        if lead and line.strip():
            return "\t" if lead[0] == "\t" else lead      # the first indented line of the file is one level deep
    return "\t"


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
    path = obj["file"]
    lines = files.text_lines(path)
    inner = obj["indent"] + _indent_unit(lines, obj)
    key = prop.lower()
    if prop == "isHidden":
        if value.strip().lower() != "true":
            raise Refused("isHidden can only be set to true here; to show an object again, edit the file with the developer")
        if obj["hidden"]:
            return None
        if "ishidden" in obj["prop_lines"]:                  # written as 'isHidden: false'
            files.replace(path, obj["prop_lines"]["ishidden"] - 1, inner + "isHidden")
        else:
            files.insert(path, obj["expr_end"], [inner + "isHidden"])
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
            at = obj["annotation_lines"][prop] - 1
            if lines[at].split("=", 1)[1].strip() in ("", "```"):
                raise Refused("the %s annotation of %s runs over several lines; change this one by hand" % (prop, name))
            files.replace(path, at, text)
        else:
            files.insert(path, obj["last_line"], ["", text])
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
            files.replace(path, obj["prop_lines"][key] - 1, text)
        else:
            files.insert(path, obj["expr_end"], [text])
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
                known = re.match(r"(.+?)\.(%s)=(.*)\Z" % "|".join(PROPERTIES.values()), args[-1], re.S | re.I)
                if known:
                    name, prop, value = known.groups()
                else:
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
    try:
        files = Files(root)
    except Refused as exc:
        print("refused  %s" % exc)
        print("Nothing was written.")
        return 1
    if not files.models:
        print("No *.SemanticModel folder with TMDL files found under %s." % args[0])
        return 2
    if len(files.models) > 1:
        print("refused  more than one model under %s; give the folder that holds one project" % args[0])
        print("Nothing was written.")
        return 1
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
