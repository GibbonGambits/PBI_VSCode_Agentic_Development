#!/usr/bin/env python3
"""The lessons file: record a mistake and its correction, and check the file.

Usage:
    python scripts/lessons.py add --trigger developer|check --key <key> --mistake "<text>" --correction "<text>"
                                  [--fix <where the fix went>] [--approved "<pull request>"]
    python scripts/lessons.py check

The file is docs/lessons.md. It holds one table row per lesson:
    No | Date | Trigger | Key | Mistake | Correction | Fix went to | Approved in

  Trigger      'developer' (a person pointed the problem out) or 'check' (a script check failed).
  Key          what kind of mistake it was. For a failed check use the finding code, for example D001.
               Otherwise a short name in lower-case words joined by hyphens, for example
               measure-in-wrong-table. Use the same key again when the same kind of mistake comes back.
  Fix went to  'report'            the mistake was put right in the project only (report, model, brief);
               template file(s)    one or more files of the template, separated by commas, when the
                                   lesson was built into the template: files under .github/, scripts/,
                                   tests/ or evals/, or a root file such as README.md;
               'declined: reason'  the developer decided not to change the template.
  Approved in  the pull request that approved a template change: its number or address
               (required with a template file), else '-'.

'add' checks the new row first and writes nothing when it is not valid (exit 2).

'check' fails when:
    X001  the table or a row is not in the form above
    X002  'Fix went to' names the checklist or the theme (they are never changed this way),
          or something that is not a file of the template
    X003  a mistake has come back: the same key has two lessons fixed only in the project, counted
          from the start or from the last time that key was built into the template or declined.
          It must then be built into the template, or the developer must decline
    X004  a row with a template file has no pull request number or address in 'Approved in'

What a lesson may reach: every template file, which includes the model standard, the layout standard, their
checks in check_project.py, the fix scripts and the skill pbi-improve. A failed check of those standards
(a code that starts with M, P, G, B, V or A) is a trigger like any other failed check. Copilot asks first and a
person approves by pull request. The checklist and the theme stay outside: X002 refuses them.

The check cannot see a lesson that was deleted from the end of the table or reworded; the pull request
diff shows that. Needs Python 3.8 or later. Uses the standard library only.
Exit code: 0 = no errors, 1 = at least one error, 2 = wrong usage or a row that is not valid.
"""
import datetime
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LESSONS = "docs/lessons.md"
HEADER = ["No", "Date", "Trigger", "Key", "Mistake", "Correction", "Fix went to", "Approved in"]
TRIGGERS = ("developer", "check")
KEY_OK = re.compile(r"(?:[A-Z][0-9]{3}|[a-z0-9]+(?:-[a-z0-9]+)*)\Z")
TEMPLATE_AREAS = (".github/", "scripts/", "tests/", "evals/", "maintenance/")
TEMPLATE_FILES = ("README.md", "LICENSE", "THIRD_PARTY_NOTICES.md", ".gitignore", ".gitattributes")
NEVER = ("checklist", "theme")
REPEAT_AT = 2


def _cells(line):
    """Cells of one Markdown table row. '\\|' inside a cell stands for a real bar."""
    parts = re.split(r"(?<!\\)\|", line.strip().strip("|"))
    return [p.replace("\\|", "|").strip() for p in parts]


def _is_rule(cells):
    return all(c and set(c) <= set("-: ") for c in cells)


def read_rows(text):
    """Return (rows, problems) for the text of a lessons file. rows: list of (line_number, dict)."""
    rows, problems = [], []
    state = "before"                 # before the table, in it, or after it
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if not stripped.startswith("|"):
            if state == "in":
                state = "after"
            continue
        cells = _cells(stripped)
        if state == "before":
            if cells == HEADER:
                state = "in"
            continue
        if state == "after":
            problems.append((number, "table row outside the lessons table: keep every lesson in one table with no gaps"))
            continue
        if _is_rule(cells):
            continue
        if len(cells) != len(HEADER):
            problems.append((number, "row has %d cells, expected %d" % (len(cells), len(HEADER))))
            continue
        rows.append((number, dict(zip(HEADER, cells))))
    if state == "before":
        problems.append((0, "no table with the header | %s |" % " | ".join(HEADER)))
    return rows, problems


def _has_words(text):
    return re.search(r"[^\W_]", text) is not None


def _valid_date(text):
    if not re.match(r"[0-9]{4}-[0-9]{2}-[0-9]{2}\Z", text):
        return False
    try:
        datetime.date(int(text[:4]), int(text[5:7]), int(text[8:]))
    except ValueError:
        return False
    return True


def fix_kind(value, must_exist=False):
    """'report', 'declined', 'template', 'never', or a text saying what is wrong."""
    if value == "report":
        return "report"
    if value.lower().startswith("declined:"):
        return "declined" if _has_words(value.split(":", 1)[1]) else "'declined:' needs a reason"
    paths = [p.strip().strip("`").strip().replace("\\", "/") for p in value.split(",")]
    if not paths or not all(paths):
        return "must be 'report', 'declined: <reason>' or template files separated by commas"
    for path in paths:
        while path.startswith("./"):
            path = path[2:]
        parts = [p for p in path.split("/") if p]
        if any(p.lower() in NEVER or p.lower() in ("checklist.md", "theme.json") for p in parts):
            return "never"
        if ".." in parts or path.startswith("/") or re.match(r"[A-Za-z]:", path):
            return "'%s' must be a path inside the repository" % path
        if not (path in TEMPLATE_FILES or path.startswith(TEMPLATE_AREAS)):
            return ("'%s' is not a template file. Use 'report' for a fix in the project, 'declined: <reason>', "
                    "or files under %s or a root file such as README.md" % (path, ", ".join(TEMPLATE_AREAS)))
        if must_exist and not os.path.isfile(os.path.join(ROOT, path)):
            return "file does not exist: %s" % path
    return "template"


def row_problems(row, must_exist=False):
    """List of (code, text) for one lesson row, not counting its number or repeats."""
    out = []
    if not _valid_date(row["Date"]):
        out.append(("X001", "date must be a real date written as YYYY-MM-DD"))
    if row["Trigger"] not in TRIGGERS:
        out.append(("X001", "trigger must be one of: %s" % ", ".join(TRIGGERS)))
    if not KEY_OK.match(row["Key"]):
        out.append(("X001", "key must be a finding code such as D001, or lower-case words joined by hyphens"))
    for column in ("Mistake", "Correction"):
        if not _has_words(row[column]):
            out.append(("X001", "'%s' is empty" % column))
    kind = fix_kind(row["Fix went to"], must_exist)
    if kind == "never":
        out.append(("X002", "the checklist and the theme are never changed through a lesson"))
    elif kind not in ("report", "declined", "template"):
        out.append(("X002", "'Fix went to': %s" % kind))
    elif kind == "template" and not re.search(r"[1-9]", row["Approved in"]):
        out.append(("X004", "a template change needs the number or address of the pull request that approved it in 'Approved in'"))
    return out


def open_repeats(rows):
    """Keys whose mistake has come back and is not yet resolved: {key: (line_number, count)}."""
    counts, last = {}, {}
    for number, row in rows:
        key = row["Key"]
        kind = fix_kind(row["Fix went to"])
        if kind in ("template", "declined"):
            counts[key] = 0
        elif kind == "report":
            counts[key] = counts.get(key, 0) + 1
            last[key] = number
    return {key: (last[key], count) for key, count in counts.items() if count >= REPEAT_AT}


def repeat_text(key, count):
    advice = ("a check already catches it, so add the line of guidance that would have prevented it"
              if re.match(r"[A-Z][0-9]{3}\Z", key) else
              "a script check if a script can catch it, otherwise one line of guidance")
    return ("the mistake '%s' has come back (%d lessons fixed only in the project): build it into the template "
            "(%s), or record 'declined: <reason>'. Ask the developer first" % (key, count, advice))


def check_text(text, shown):
    rows, problems = read_rows(text)
    out = ["X001  %s%s  %s" % (shown, ":%d" % n if n else "", message) for n, message in problems]
    for expected, (number, row) in enumerate(rows, 1):
        where = "%s:%d" % (shown, number)
        if row["No"] != str(expected):
            out.append("X001  %s  lesson number is '%s', expected %d (lessons are numbered in order and never removed)"
                       % (where, row["No"], expected))
        out.extend("%s  %s  %s" % (code, where, message) for code, message in row_problems(row))
    for key, (number, count) in open_repeats(rows).items():
        out.append("X003  %s:%d  %s" % (shown, number, repeat_text(key, count)))
    return out


def check_file(path):
    """Return a list of 'CODE  where  message' lines."""
    shown = os.path.relpath(path, ROOT).replace(os.sep, "/")
    try:
        with open(path, encoding="utf-8-sig") as fh:
            text = fh.read()
    except (OSError, UnicodeDecodeError) as exc:
        return ["X001  %s  cannot read the lessons file as UTF-8 text: %s" % (shown, exc)]
    return check_text(text, shown)


def _cell(text):
    return " ".join(str(text).split()).replace("|", "\\|")


def add(path, trigger, key, mistake, correction, fix="report", approved="-", today=None):
    """Append one lesson. Returns (number, lessons of this key still open as a repeat).

    Raises ValueError, and writes nothing, when the file or the new row is not valid.
    """
    level = cp.code_levels().get(key)
    if trigger == "check" and level in ("warn", "note"):
        raise ValueError("%s is a %s of the project check. Only a failed check starts the loop: a warning or a note "
                         "(a suggestion) is not a mistake to record" % (key, "warning" if level == "warn" else "note"))
    with open(path, "rb") as fh:
        raw = fh.read()
    text = raw.decode("utf-8-sig")
    rows, problems = read_rows(text)
    if problems:
        raise ValueError("%s is not in the expected form: %s" % (LESSONS, problems[0][1]))
    values = [str(len(rows) + 1), today or datetime.date.today().isoformat(), trigger, key,
              _cell(mistake), _cell(correction), _cell(fix), _cell(approved or "-")]
    row = dict(zip(HEADER, [v.replace("\\|", "|") for v in values]))
    found = row_problems(row, must_exist=True)
    if found:
        raise ValueError("; ".join(message for _, message in found))

    lines = text.splitlines(keepends=True)
    last = None
    in_table = False
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped.startswith("|"):
            if not in_table and _cells(stripped) == HEADER:
                in_table = True
            if in_table:
                last = index
        elif in_table:
            break
    newline = "\r\n" if lines[last].endswith("\r\n") or (not lines[last].endswith("\n") and "\r\n" in text) else "\n"
    if not lines[last].endswith("\n"):
        lines[last] += newline
    lines.insert(last + 1, "| %s |%s" % (" | ".join(values), newline))
    payload = "".join(lines).encode("utf-8")           # encode before touching the file
    temporary = path + ".tmp"
    with open(temporary, "wb") as fh:
        fh.write(payload)
    os.replace(temporary, path)
    repeats = open_repeats(rows + [(0, row)])
    return len(rows) + 1, repeats.get(key, (0, 0))[1]


def _options(args):
    values = {}
    while args:
        name = args.pop(0)
        if not name.startswith("--") or not args:
            return None
        values[name[2:]] = args.pop(0)
    return values


def main(argv):
    cp.safe_output()
    args = list(argv[1:])
    path = os.path.join(ROOT, LESSONS)
    if args == ["check"]:
        if not os.path.isfile(path):
            print("X001  %s  the lessons file is missing" % LESSONS)
            print("Lessons check: 1 error(s).")
            return 1
        found = check_file(path)
        for line in found:
            print(line)
        print("Lessons check: %d error(s)." % len(found))
        return 1 if found else 0
    if args[:1] == ["add"]:
        values = _options(args[1:])
        needed = ("trigger", "key", "mistake", "correction")
        allowed = needed + ("fix", "approved")
        if values is None or any(n not in values for n in needed) or any(n not in allowed for n in values):
            print(__doc__)
            return 2
        try:
            number, open_count = add(path, values["trigger"], values["key"], values["mistake"], values["correction"],
                                     values.get("fix", "report"), values.get("approved", "-"))
        except ValueError as exc:                       # includes text that cannot be written as UTF-8
            print("Nothing was written. The lesson is not valid: %s" % str(exc)[:500])
            return 2
        except OSError as exc:
            print("Nothing was written. Could not change %s: %s" % (LESSONS, exc))
            return 1
        print("Added lesson %d to %s." % (number, LESSONS))
        if open_count:
            print("X003  %s  %s" % (LESSONS, repeat_text(values["key"], open_count)))
            return 1
        return 0
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
