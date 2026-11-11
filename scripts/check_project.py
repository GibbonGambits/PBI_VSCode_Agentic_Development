#!/usr/bin/env python3
"""Machine checks for a Power BI project (PBIP: TMDL model + PBIR report).

Usage:
    python scripts/check_project.py <folder>            check every project found under <folder>
    python scripts/check_project.py --review <file>     check a finished 79-item review table

Needs Python 3.8 or later. Uses the standard library only. Reads files; never changes them.
Exit code: 0 = no errors, 1 = at least one error, 2 = wrong usage or nothing to check.

Finding codes (errors unless marked info):
    D001  visible table, column or measure has no '///' description
    D002  shared Power Query query or parameter ('expression') has no '///' description
    D003  '///' description is not directly above an object
    I001  (info) description still holds the placeholder TODO(owner)
    C001  '//' comment outside a Power Query (M) or DAX expression block
    P001  Power Query step has no '//' (or '/* */') description line directly above it (template convention)
    F001  a .Report or .SemanticModel folder is not in PBIR / TMDL format (no 'definition' folder)
    F002  a page folder has no page.json, or a visual folder has no visual.json
    F003  a model's 'definition' folder holds no .tmdl file
    J001  a project JSON file is not valid JSON or starts with a byte-order mark; or a .tmdl file is not UTF-8
    J002  a project JSON file does not have the structure Power BI expects
    S001  '$schema' is missing or is not a Microsoft Fabric schema address
    N001  page name or folder has characters other than letters, digits, underscore, hyphen; or the name is over 50
    N002  visual name or folder: same rule
    N003  visual has neither a Page_Type_Subject name nor a VisualLabel annotation
    N004  visual is named Page_Type_Subject but its folder has a different name
    N005  two visuals on one page share a name or a label
    H001  Header icons are on, or not set, on the visual itself (or on in its mobile layout)
    H002  Tooltips are on, or not set, on the visual itself (or on in its mobile layout)
    T001  report has no custom theme registered, or the registered theme file is missing or unreadable
    R0xx  problems in a review table (see --review)

A visual may keep Header icons or Tooltips on only with a HeaderTooltipException annotation whose value
names what stays on and why: "header: <reason>", "tooltip: <reason>" or "both: <reason>".
The Power Query step check reads the outer 'let' of each query; it is a plain text check, not a parser.
"""
import json
import os
import re
import sys

NAME_OK = re.compile(r"[A-Za-z0-9_-]+\Z")           # Microsoft Learn: PBIR naming convention
NAME_MAX = 50                                        # Microsoft schemas: page 2.1.0, visualContainer 2.13.0
LABEL_ANNOTATION = "VisualLabel"                     # template convention
EXCEPTION_ANNOTATION = "HeaderTooltipException"      # template convention
EXCEPTION_SCOPES = {"header": ("visualHeader",), "tooltip": ("visualTooltip",),
                    "both": ("visualHeader", "visualTooltip")}
PLACEHOLDER = "TODO(owner)"                          # template convention
SCHEMA_PREFIX = "https://developer.microsoft.com/json-schemas/fabric/"
REVIEW_STATUSES = ("Pass", "Fail", "Not applicable")
ITEM_COUNT = 79
FAILED = object()                                    # returned by load_json when a file cannot be parsed

DESCRIBED_KINDS = ("table", "column", "measure")
STEP_RE = re.compile(r'^(#"(?:[^"]|"")+"|[^\W\d][\w.]*)\s*=(?![=>])')
DECL_RE = re.compile(r"^([A-Za-z]+)\s+('(?:[^']|'')*'|[^\s=:]+)\s*(.*)$")
PROP_EQ_RE = re.compile(r"^([A-Za-z_]\w*)\s*=\s*(.*)$")
PROP_COLON_RE = re.compile(r"^([A-Za-z_]\w*)\s*:")
OBJECT_KEYWORDS = frozenset((
    "table", "column", "measure", "expression", "partition", "hierarchy", "level",
    "calculationgroup", "calculationitem", "function", "role", "tablepermission",
    "relationship", "perspective", "culture", "cultureinfo", "datasource", "model", "database",
    "annotation", "extendedproperty", "querygroup", "variation", "kpi"))
VALUE_ONLY = frozenset(("annotation", "extendedproperty"))       # 'name = value' lines, not real objects
PLAIN_VALUE_KEYS = frozenset(("changedproperty",))               # 'key = value' where the value is not an expression
FREE_TEXT_KEYS = frozenset(("sourcecolumn", "formatstring", "displayfolder", "sortbycolumn",
                            "sourcelineagetag", "description", "displayname", "caption"))
HIDING_FLAGS = frozenset(("ishidden", "ishidden:true", "isprivate", "isprivate:true"))
QUOTED = re.compile(r"'(?:[^']|'')*'|\"(?:[^\"]|\"\")*\"")
EMPTY_EVIDENCE = frozenset(("todo", "tbd", "na", "n/a", "none", "nbsp", "br", "x", "evidence"))


class Findings:
    def __init__(self):
        self.items = []

    def add(self, code, path, line, message, info=False):
        self.items.append((code, path, line, message, info))

    def errors(self):
        return [f for f in self.items if not f[4]]

    def print_all(self, base):
        for code, path, line, message, info in self.items:
            rel = os.path.relpath(path, base) if path else "-"
            where = "%s:%d" % (rel, line) if line else rel
            print("%s  %s  %s" % (code, where.replace(os.sep, "/"), message))


def safe_output():
    """Never stop on a character the console cannot show."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")


# ---------------------------------------------------------------- TMDL

def _width(line):
    return len(line) - len(line.lstrip(" \t"))


def _unquote(name):
    if len(name) >= 2 and name[0] == "'" and name[-1] == "'":
        return name[1:-1].replace("''", "'")
    return name


def _has_comment(text):
    """True when text holds '//' that is not '///', not inside quotes and not part of an address such as http://."""
    return re.search(r"(?<![:/])//(?!/)", QUOTED.sub("''", text)) is not None


def _m_code(text):
    """A line of Power Query with text values and a trailing '//' comment removed."""
    text = re.sub(r'#?"(?:[^"]|"")*"', '""', text)
    return text.split("//")[0]


def check_m_steps(block, path, owner, findings):
    """block: list of (line_number, text) of one Power Query expression.

    Finds the first 'let', then looks at every step of that 'let' (lines that start a 'name = ...'
    outside any bracket) and reports a step with no comment line directly above it.
    """
    start = None
    in_block_comment = False
    for idx, (n, t) in enumerate(block):
        s = t.strip()
        if in_block_comment:
            in_block_comment = "*/" not in s
            continue
        if s.startswith("/*") and "*/" not in s:
            in_block_comment = True
            continue
        code = _m_code(re.sub(r"/\*.*?\*/", " ", s)).strip()
        if not code:
            continue
        m = re.search(r"(?:^|[\s)>])let(?:\s+(.*))?$", code)
        if m:
            start = idx
            break
    if start is None:
        return

    depth = 0
    nested = []           # bracket depth at which each inner 'let' opened
    in_block_comment = False
    previous_is_comment = False
    first = True
    for n, t in block[start:]:
        s = t.strip()
        if first:
            first = False
            code = _m_code(s)
            m = re.search(r"(?:^|[\s)>])let(?:\s+(.*))?$", code.strip())
            rest = (m.group(1) or "").strip() if m else ""
            if rest and STEP_RE.match(rest):
                findings.add("P001", path, n,
                             "Power Query step %s in %s starts on the 'let' line; put it on its own line with a '//' description above"
                             % (STEP_RE.match(rest).group(1), owner))
            for ch in rest:
                depth += ch in "([{"
                depth -= ch in ")]}"
            continue
        if not s:
            previous_is_comment = False       # the description must sit directly above its step
            continue
        if in_block_comment:
            if "*/" in s:
                in_block_comment = False
                previous_is_comment = s.endswith("*/")
            continue
        if s.startswith("/*") and "*/" not in s:
            in_block_comment = True
            continue
        if s.startswith("//"):
            previous_is_comment = bool(s[2:].strip())
            continue
        if s.startswith("/*") and s.endswith("*/"):
            previous_is_comment = bool(s[2:-2].strip())
            continue
        code = _m_code(s).strip()
        if code == "in" or code.startswith("in "):
            if nested and nested[-1] == depth:
                nested.pop()
            elif depth == 0 and not nested:
                break
        elif depth == 0 and not nested:
            m = STEP_RE.match(s.lstrip(", "))
            if m and not previous_is_comment:
                findings.add("P001", path, n,
                             "Power Query step %s in %s has no '//' description line directly above it" % (m.group(1), owner))
        for ch in code:
            depth += ch in "([{"
            depth -= ch in ")]}"
        depth = max(depth, 0)
        if re.search(r"(?:^|[\s=(,>])let$", code):
            nested.append(depth)
        previous_is_comment = False


def check_tmdl_file(path, findings):
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        findings.add("J001", path, 0, "cannot read file: %s" % exc)
        return
    try:
        if b"\x00" in raw:
            raise UnicodeDecodeError("utf-8", raw, 0, 1, "the file looks like UTF-16")
        lines = raw.decode("utf-8-sig").splitlines()
    except UnicodeDecodeError:
        findings.add("J001", path, 0, "file is not UTF-8 text, so it cannot be checked; save it as UTF-8 without BOM")
        return
    uses_tabs = any(line.startswith("\t") for line in lines)

    objects = []          # dicts: kind, name, line, described, hidden, table, top, placeholder
    stack = []            # (indent width, object) for the objects the current line sits inside
    pending = []          # (line_number, text) of '///' lines waiting for their object
    block = None          # the expression block being read
    partition_is_m = False
    translations = False  # inside a cultureInfo file: names there are translations, not model objects

    def close_block():
        nonlocal block
        if block and block["is_m"]:
            check_m_steps(block["lines"], path, block["owner"], findings)
        block = None

    def comment(number):
        findings.add("C001", path, number, "'//' comment outside a Power Query or DAX expression block")

    for number, line in enumerate(lines, 1):
        stripped = line.strip()

        if block is not None:
            if block["fenced"]:
                if stripped == "```":
                    close_block()
                else:
                    block["lines"].append((number, line))
                continue
            if not stripped:
                block["lines"].append((number, line))
                continue
            width = _width(line)
            if block["limit"] is None:
                # Files indented with spaces: the indent step is unknown, so the first line sets the depth.
                block["limit"] = width if width > block["owner_width"] else block["owner_width"] + 1
            if width >= block["limit"]:
                block["lines"].append((number, line))
                continue
            close_block()

        if not stripped:
            if pending:
                findings.add("D003", path, pending[0][0],
                             "'///' description is followed by a blank line; it must sit directly above its object")
                pending = []
            continue

        width = _width(line)

        if stripped.startswith("///"):
            pending.append((number, stripped[3:].strip()))
            continue

        if stripped.startswith("//"):
            comment(number)
            continue

        description = " ".join(t for _, t in pending).strip()
        had_pending = bool(pending)
        pending_line = pending[0][0] if pending else 0
        pending = []

        while stack and stack[-1][0] >= width:
            stack.pop()

        decl = DECL_RE.match(stripped)
        keyword = decl.group(1).lower() if decl else ""
        is_object = bool(decl) and keyword in OBJECT_KEYWORDS
        opens_block = False
        fenced = False
        is_m = False
        owner = ""
        steps_deeper = 1      # tab levels between this line and the first line of its expression

        if is_object:
            raw_name = decl.group(2)
            rest = decl.group(3).strip()
            if not raw_name.startswith("'") and "//" in raw_name:
                comment(number)                       # a comment glued to the name: 'column A// note'
                raw_name = raw_name.split("//")[0]
                rest = ""
            name = _unquote(raw_name)
            tail = None
            if rest.startswith("="):
                tail = rest[1:].strip()
                if tail == "":
                    opens_block = True
                elif tail == "```":
                    opens_block = True
                    fenced = True
                elif keyword == "partition" and _has_comment(" " + tail):
                    comment(number)                   # 'partition X = m // note': 'm' is a type, not an expression
                elif keyword == "expression" and re.match(r"let\b", tail):
                    findings.add("P001", path, number,
                                 "query '%s' is written on one line; put 'let' and each step on its own line with a '//' description above each step" % name)
            elif rest and _has_comment(" " + rest):
                comment(number)
            if keyword in VALUE_ONLY:
                if had_pending:
                    findings.add("D003", path, pending_line, "'///' description is not directly above an object")
            else:
                if keyword == "cultureinfo":
                    translations = True
                table = None
                for _, enclosing in stack:
                    if enclosing["kind"] == "table":
                        table = enclosing
                obj = {"kind": keyword, "name": name, "line": number, "described": bool(description),
                       "hidden": False, "table": table, "top": not stack, "translation": translations,
                       "placeholder": PLACEHOLDER.lower() in description.lower()}
                objects.append(obj)
                stack.append((width, obj))
                if keyword == "partition":
                    partition_is_m = (tail or "").split("//")[0].strip().lower() == "m"
                is_m = keyword == "expression"
                owner = "query '%s'" % name
                steps_deeper = 2
        else:
            prop = PROP_EQ_RE.match(stripped)
            colon = PROP_COLON_RE.match(stripped)
            if had_pending and (prop or colon or stripped.replace(" ", "").lower() in HIDING_FLAGS):
                findings.add("D003", path, pending_line, "'///' description is not directly above an object")
            if prop:
                key = prop.group(1).lower()
                tail = prop.group(2).strip()
                if tail == "":
                    opens_block = True
                elif tail == "```":
                    opens_block = True
                    fenced = True
                elif key in PLAIN_VALUE_KEYS and _has_comment(" " + tail):
                    comment(number)
                is_m = key == "source" and partition_is_m
                if is_m and re.match(r"let\b", tail):
                    findings.add("P001", path, number,
                                 "this query is written on one line; put 'let' and each step on its own line with a '//' description above each step")
                table = None
                for _, enclosing in stack:
                    if enclosing["kind"] == "table":
                        table = enclosing
                owner = "table '%s'" % (table["name"] if table else "?")
            else:
                key = colon.group(1).lower() if colon else ""
                if key not in FREE_TEXT_KEYS and _has_comment(stripped):
                    comment(number)
                if stripped.replace(" ", "").lower() in HIDING_FLAGS and stack:
                    stack[-1][1]["hidden"] = True

        if opens_block:
            limit = width + steps_deeper if uses_tabs and line.startswith("\t") or (uses_tabs and width == 0) else None
            block = {"limit": limit, "owner_width": width, "fenced": fenced, "is_m": is_m,
                     "owner": owner, "lines": []}

    if block is not None:
        close_block()
    if pending:
        findings.add("D003", path, pending[0][0],
                     "'///' description at end of file is not above any object")

    for obj in objects:
        if obj["translation"]:
            continue
        kind = obj["kind"]
        if kind in DESCRIBED_KINDS:
            table = obj["table"]
            hidden = obj["hidden"] or (table is not None and table["hidden"])
            if not hidden and not obj["described"]:
                findings.add("D001", path, obj["line"],
                             "visible %s '%s' has no '///' description" % (kind, obj["name"]))
        elif kind == "expression" and obj["top"] and not obj["described"]:
            findings.add("D002", path, obj["line"],
                         "shared query or parameter '%s' has no '///' description" % obj["name"])
        if obj["placeholder"]:
            findings.add("I001", path, obj["line"],
                         "%s '%s' still has a %s placeholder as its description" % (kind, obj["name"], PLACEHOLDER),
                         info=True)


# ---------------------------------------------------------------- PBIR

def _no_constants(name):
    raise ValueError("%s is not valid JSON" % name)


def load_json(path, findings=None):
    """Return the parsed JSON value, or FAILED after recording J001."""
    try:
        with open(path, "rb") as fh:
            raw = fh.read()
    except OSError as exc:
        if findings is not None:
            findings.add("J001", path, 0, "cannot read file: %s" % exc)
        return FAILED
    has_mark = raw[:3] == b"\xef\xbb\xbf"
    if has_mark and findings is not None:
        findings.add("J001", path, 1, "file starts with a byte-order mark; save as UTF-8 without BOM")
    try:
        return json.loads(raw.decode("utf-8-sig"), parse_constant=_no_constants)
    except (UnicodeDecodeError, ValueError, RecursionError) as exc:
        if findings is not None:
            findings.add("J001", path, 0, "not valid JSON: %s" % str(exc)[:200])
        return FAILED


def load_object(path):
    """Parsed JSON if it is an object, else None. For callers that only need a dict or nothing."""
    data = load_json(path)
    return data if isinstance(data, dict) else None


def literal_bool(value):
    """Read {"expr": {"Literal": {"Value": "false"}}} -> False. Anything else -> None."""
    try:
        text = value["expr"]["Literal"]["Value"]
    except (TypeError, KeyError):
        return None
    if text == "true":
        return True
    if text == "false":
        return False
    return None


def show_state(container_json, card):
    """State of visual.visualContainerObjects.<card>[].properties.show.

    'off', 'on', 'missing' (no entry), 'other' (show is there but not the literal true/false form)
    or 'malformed' (the card is not a list of entries).
    """
    visual = container_json.get("visual") if isinstance(container_json, dict) else None
    if not isinstance(visual, dict):
        return "malformed"
    objects = visual.get("visualContainerObjects")
    if objects is None:
        return "missing"
    if not isinstance(objects, dict):
        return "malformed"
    entries = objects.get(card)
    if entries is None:
        return "missing"
    if not isinstance(entries, list):
        return "malformed"
    state = "missing"
    for entry in entries:
        if not isinstance(entry, dict) or not isinstance(entry.get("properties", {}), dict):
            return "malformed"
        properties = entry.get("properties", {})
        if "show" not in properties:
            continue
        value = literal_bool(properties["show"])
        if value is True:
            return "on"
        if value is None:
            state = "other"
        elif "selector" not in entry and state != "other":
            state = "off"
    return state


def annotation(container_json, name):
    items = container_json.get("annotations") if isinstance(container_json, dict) else None
    if not isinstance(items, list):
        return None
    for item in items:
        if isinstance(item, dict) and item.get("name") == name:
            return item.get("value")
    return None


def excused_cards(container_json):
    """Cards a HeaderTooltipException annotation excuses: () when there is none or it is not well formed."""
    value = annotation(container_json, EXCEPTION_ANNOTATION)
    if not isinstance(value, str) or ":" not in value:
        return ()
    scope, _, reason = value.partition(":")
    if not reason.strip():
        return ()
    return EXCEPTION_SCOPES.get(scope.strip().lower(), ())


def slug(text):
    return re.sub(r"[^A-Za-z0-9]", "", text if isinstance(text, str) else "")


def is_label(label, page_name, page_display):
    """Page_Type_Subject: the page part, then at least a type part and a subject part."""
    if not isinstance(label, str) or not NAME_OK.match(label) or len(label) > NAME_MAX:
        return False
    prefixes = {p for p in (page_name, slug(page_display)) if isinstance(p, str) and p}
    for prefix in prefixes:
        if label.startswith(prefix + "_"):
            rest = label[len(prefix) + 1:].split("_")
            if len(rest) >= 2 and all(rest):
                return True
    return False


def _walk(root):
    """os.walk that skips Git folders and the template's own test data."""
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith(".git") and d != "node_modules"
                   and not (d == "fixtures" and os.path.basename(folder) == "tests")]
        yield folder, dirs, files


def _project_folders(root, suffix, with_definition):
    found = []
    for folder, dirs, files in _walk(root):
        if folder.endswith(suffix) and os.path.isdir(os.path.join(folder, "definition")) == with_definition:
            found.append(folder)
    return sorted(found)


def find_reports(root):
    return _project_folders(root, ".Report", True)


def find_models(root):
    return _project_folders(root, ".SemanticModel", True)


def find_old_format(root):
    """Report and model folders saved in the older single-file layout, which these checks cannot read."""
    return _project_folders(root, ".Report", False) + _project_folders(root, ".SemanticModel", False)


def iter_pages(report_dir):
    """Yield (page_folder_name, page_folder_path, page_json_path)."""
    pages_dir = os.path.join(report_dir, "definition", "pages")
    if not os.path.isdir(pages_dir):
        return
    for name in sorted(os.listdir(pages_dir)):
        folder = os.path.join(pages_dir, name)
        page_json = os.path.join(folder, "page.json")
        if os.path.isdir(folder) and os.path.isfile(page_json):
            yield name, folder, page_json


def iter_visuals(page_folder):
    """Yield (visual_folder_name, visual_json_path)."""
    visuals_dir = os.path.join(page_folder, "visuals")
    if not os.path.isdir(visuals_dir):
        return
    for name in sorted(os.listdir(visuals_dir)):
        visual_json = os.path.join(visuals_dir, name, "visual.json")
        if os.path.isfile(visual_json):
            yield name, visual_json


def check_all_json(folder, findings):
    """J001 for every JSON file of a report or model folder. Returns the paths that failed."""
    bad = set()
    for sub, dirs, files in os.walk(folder):
        dirs[:] = [d for d in dirs if d != ".pbi"]
        for name in sorted(files):
            if name.lower().endswith((".json", ".pbir", ".pbism")):
                path = os.path.join(sub, name)
                before = len(findings.items)
                load_json(path, findings)
                if len(findings.items) != before:
                    bad.add(path)
    return bad


def check_schema(data, path, findings):
    schema = data.get("$schema") if isinstance(data, dict) else None
    if not isinstance(schema, str) or not schema.startswith(SCHEMA_PREFIX):
        findings.add("S001", path, 0, "'$schema' is missing or is not a Microsoft Fabric schema address")


def check_theme(report_dir, report_json, findings):
    path = os.path.join(report_dir, "definition", "report.json")
    collection = report_json.get("themeCollection")
    custom = collection.get("customTheme") if isinstance(collection, dict) else None
    name = custom.get("name") if isinstance(custom, dict) else None
    if not isinstance(name, str) or not name:
        findings.add("T001", path, 0, "no custom theme is registered (themeCollection.customTheme)")
        return
    theme_path = os.path.join(report_dir, "StaticResources", "RegisteredResources", name)
    if not os.path.isfile(theme_path):
        findings.add("T001", path, 0, "registered theme file not found: StaticResources/RegisteredResources/%s" % name)
        return
    if load_object(theme_path) is None:
        findings.add("T001", theme_path, 0, "registered theme file is not a valid JSON object")


HEADER_CARDS = (("visualHeader", "H001", "Header icons"), ("visualTooltip", "H002", "Tooltips"))


def check_header_and_tooltip(data, visual_path, findings):
    excused = excused_cards(data)
    if not excused and annotation(data, EXCEPTION_ANNOTATION) is not None:
        findings.add("H001", visual_path, 0,
                     "the %s annotation must start with 'header:', 'tooltip:' or 'both:' and then give the reason; "
                     "correct it or remove it" % EXCEPTION_ANNOTATION)
    how = ("set %s show to false, or add a %s annotation that says what stays on and why "
           "(\"header: ...\", \"tooltip: ...\" or \"both: ...\")")
    for card, code, label in HEADER_CARDS:
        if card in excused:
            continue
        state = show_state(data, card)
        if state == "on":
            problem = "%s are on for this visual" % label
        elif state == "missing":
            problem = "%s are not set on this visual" % label
        elif state == "other":
            problem = "%s: 'show' is not written as the literal true/false form" % label
        elif state == "malformed":
            problem = "%s: '%s' is not a list of { \"properties\": { ... } } entries" % (label, card)
        else:
            problem = None
        if problem:
            findings.add(code, visual_path, 0, problem + "; " + how % (card, EXCEPTION_ANNOTATION))
    mobile_path = os.path.join(os.path.dirname(visual_path), "mobile.json")
    if os.path.isfile(mobile_path):
        mobile = load_object(mobile_path)
        if mobile is not None:
            for card, code, label in HEADER_CARDS:
                if card not in excused and show_state({"visual": mobile}, card) in ("on", "other", "malformed"):
                    findings.add(code, mobile_path, 0,
                                 "%s are on, or not written in the literal form, in this visual's mobile layout; " % label
                                 + how % (card, EXCEPTION_ANNOTATION))


def check_page(page_folder, page_path, bad, findings):
    if page_path in bad:
        return
    page = load_json(page_path)
    if not isinstance(page, dict):
        findings.add("J002", page_path, 0, "page.json must be a JSON object")
        return
    check_schema(page, page_path, findings)
    page_name = page.get("name")
    page_display = page.get("displayName")
    if not isinstance(page_name, str) or not NAME_OK.match(page_name) or len(page_name) > NAME_MAX:
        findings.add("N001", page_path, 0,
                     "page name must use only letters, digits, _ and -, and be at most %d characters" % NAME_MAX)
        page_name = page_name if isinstance(page_name, str) else ""

    visuals_dir = os.path.join(page_folder, "visuals")
    if os.path.isdir(visuals_dir):
        for name in sorted(os.listdir(visuals_dir)):
            folder = os.path.join(visuals_dir, name)
            if not os.path.isdir(folder):
                continue
            if not NAME_OK.match(name):
                findings.add("N002", folder, 0,
                             "visual folder name has characters Power BI Desktop ignores (allowed: letters, digits, _ and -)")
            if not os.path.isfile(os.path.join(folder, "visual.json")):
                findings.add("F002", folder, 0, "visual folder has no visual.json")

    names = {}
    labels = {}
    for folder_name, visual_path in iter_visuals(page_folder):
        if visual_path in bad:
            continue
        data = load_json(visual_path)
        if not isinstance(data, dict):
            findings.add("J002", visual_path, 0, "visual.json must be a JSON object")
            continue
        check_schema(data, visual_path, findings)
        is_visual = isinstance(data.get("visual"), dict)
        is_group = isinstance(data.get("visualGroup"), dict)
        if is_visual == is_group:
            findings.add("J002", visual_path, 0, "visual.json needs exactly one of 'visual' or 'visualGroup', as an object")
        position = data.get("position")
        if not isinstance(position, dict) or not all(
                isinstance(position.get(k), (int, float)) and not isinstance(position.get(k), bool)
                for k in ("x", "y", "width", "height")):
            findings.add("J002", visual_path, 0, "'position' must be an object with numeric x, y, width and height")
        if "annotations" in data and not isinstance(data["annotations"], list):
            findings.add("J002", visual_path, 0, "'annotations' must be a list of { \"name\", \"value\" } entries")
        name = data.get("name")
        if not isinstance(name, str) or not NAME_OK.match(name) or len(name) > NAME_MAX:
            findings.add("N002", visual_path, 0,
                         "visual name must use only letters, digits, _ and -, and be at most %d characters" % NAME_MAX)
            name = name if isinstance(name, str) else ""
        if name in names:
            findings.add("N005", visual_path, 0,
                         "visual name '%s' is also used by %s on the same page" % (name, names[name]))
        names[name] = folder_name

        label = annotation(data, LABEL_ANNOTATION)
        named = is_label(name, page_name, page_display)
        labelled = is_label(label, page_name, page_display)
        if not named and not labelled:
            findings.add("N003", visual_path, 0,
                         "visual needs a Page_Type_Subject name, or a %s annotation holding one" % LABEL_ANNOTATION)
        if named and folder_name != name:
            findings.add("N004", visual_path, 0,
                         "visual is named '%s' but its folder is '%s'; give both the same name" % (name, folder_name))
        shown = label if labelled else (name if named else None)
        if shown is not None:
            if shown in labels:
                findings.add("N005", visual_path, 0,
                             "label '%s' is also used by %s on the same page" % (shown, labels[shown]))
            labels[shown] = folder_name

        if is_visual and not is_group:
            check_header_and_tooltip(data, visual_path, findings)


def check_report(report_dir, findings):
    bad = check_all_json(report_dir, findings)
    definition = os.path.join(report_dir, "definition")
    report_path = os.path.join(definition, "report.json")
    if not os.path.isfile(report_path):
        findings.add("T001", report_path, 0, "report.json not found, so no theme is registered")
    elif report_path not in bad:
        report_json = load_json(report_path)
        if isinstance(report_json, dict):
            check_schema(report_json, report_path, findings)
            check_theme(report_dir, report_json, findings)
        else:
            findings.add("J002", report_path, 0, "report.json must be a JSON object")
    for extra in ("version.json", os.path.join("pages", "pages.json")):
        path = os.path.join(definition, extra)
        if os.path.isfile(path) and path not in bad:
            check_schema(load_json(path), path, findings)

    pages_dir = os.path.join(definition, "pages")
    if os.path.isdir(pages_dir):
        for name in sorted(os.listdir(pages_dir)):
            folder = os.path.join(pages_dir, name)
            if not os.path.isdir(folder):
                continue
            if not NAME_OK.match(name):
                findings.add("N001", folder, 0,
                             "page folder name has characters Power BI Desktop ignores (allowed: letters, digits, _ and -)")
            if not os.path.isfile(os.path.join(folder, "page.json")):
                findings.add("F002", folder, 0, "page folder has no page.json, so its visuals cannot be checked")

    for page_folder_name, page_folder, page_path in iter_pages(report_dir):
        try:
            check_page(page_folder, page_path, bad, findings)
        except (AttributeError, TypeError, KeyError, ValueError) as exc:
            findings.add("J002", page_path, 0, "a file of this page has an unexpected structure (%s)" % exc)


def check_model(model_dir, findings):
    check_all_json(model_dir, findings)
    definition = os.path.join(model_dir, "definition")
    count = 0
    for folder, dirs, files in os.walk(definition):
        for name in sorted(files):
            if name.lower().endswith(".tmdl"):
                count += 1
                check_tmdl_file(os.path.join(folder, name), findings)
    if count == 0:
        findings.add("F003", definition, 0, "the model's 'definition' folder holds no .tmdl file")


# ---------------------------------------------------------------- review table

def _plain(text):
    return re.sub("[​‌‍﻿ ]", "", text).strip()


def _no_evidence(text):
    words = re.sub(r"&\w+;|<[^>]*>|[`*_~]", " ", text).strip().lower()
    if not re.search(r"[^\W_]", words):
        return True
    return words.strip(" .:!?") in EMPTY_EVIDENCE or re.match(r"(todo|tbd)\b", words) is not None


def check_review(path, findings):
    try:
        with open(path, encoding="utf-8-sig") as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        findings.add("R001", path, 0, "cannot read review file as UTF-8 text: %s" % exc)
        return
    rows = {}
    in_table = False
    found_table = False
    for number, line in enumerate(lines, 1):
        text = line.strip()
        if not text.startswith("|"):
            if in_table:
                break                          # the review table ends at the first line that is not a table row
            continue
        cells = [_plain(c) for c in text.strip("|").split("|")]
        if not in_table:
            if [c.lower() for c in cells[:3]] == ["item", "status", "evidence"]:
                in_table = True
                found_table = True
            continue
        if len(cells) < 3 or not (cells[0].isascii() and cells[0].isdigit() and len(cells[0]) <= 4):
            continue
        item = int(cells[0])
        if item in rows:
            findings.add("R002", path, number, "item %d appears more than once" % item)
        rows[item] = (number, cells[1], cells[2])
    if not found_table:
        findings.add("R001", path, 0, "no table with the header | Item | Status | Evidence | was found")
        return
    for item in range(1, ITEM_COUNT + 1):
        if item not in rows:
            findings.add("R003", path, 0, "item %d has no row" % item)
            continue
        number, status, evidence = rows[item]
        if status not in REVIEW_STATUSES:
            findings.add("R004", path, number,
                         "item %d: status must be exactly one of: %s" % (item, ", ".join(REVIEW_STATUSES)))
        if _no_evidence(evidence):
            findings.add("R005", path, number, "item %d: the evidence cell is empty or a placeholder" % item)
    for item in sorted(rows):
        if item < 1 or item > ITEM_COUNT:
            findings.add("R006", path, rows[item][0], "item %d is not a checklist item (1 to %d)" % (item, ITEM_COUNT))


# ---------------------------------------------------------------- main

def run(root):
    findings = Findings()
    models = find_models(root)
    reports = find_reports(root)
    for folder in find_old_format(root):
        findings.add("F001", folder, 0,
                     "no 'definition' folder: this item is saved in an older format these checks cannot read; "
                     "save it from Power BI Desktop as a project with TMDL and PBIR")
    for model in models:
        check_model(model, findings)
    for report in reports:
        check_report(report, findings)
    return findings, models, reports


def main(argv):
    safe_output()
    if len(argv) == 3 and argv[1] == "--review":
        findings = Findings()
        check_review(argv[2], findings)
        findings.print_all(os.path.dirname(os.path.abspath(argv[2])))
        errors = findings.errors()
        print("Review table: %d error(s)." % len(errors))
        return 1 if errors else 0
    if len(argv) != 2 or argv[1].startswith("-"):
        print(__doc__)
        return 2
    root = os.path.abspath(argv[1])
    if not os.path.isdir(root):
        print("Not a folder: %s" % argv[1])
        return 2
    findings, models, reports = run(root)
    if not models and not reports and not findings.items:
        print("No Power BI project found under %s (looked for *.SemanticModel and *.Report folders)." % argv[1])
        return 2
    findings.print_all(root)
    errors = findings.errors()
    infos = len(findings.items) - len(errors)
    print("Checked %d model(s) and %d report(s): %d error(s), %d note(s)." % (len(models), len(reports), len(errors), infos))
    if errors:
        codes = sorted({f[0] for f in errors})
        print("If you created or changed these files in this task, fix them and record one lesson for each code (%s): "
              "python scripts/lessons.py add --trigger check --key <code> --mistake \"...\" --correction \"...\""
              % ", ".join(codes))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
