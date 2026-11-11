#!/usr/bin/env python3
"""Integrity checks for the template itself (not for a report).

Usage:
    python scripts/check_template.py                    all checks that need no spreadsheet
    python scripts/check_template.py --xlsx <file>      also compare the checklist, cell by cell,
                                                        with the owner's spreadsheet

Needs Python 3.8 or later. Uses the standard library only. Reads files; never changes them.
Exit code: 0 = no errors, 1 = at least one error, 2 = wrong usage.

What it checks:
    K  checklist/checklist.md holds 79 items in order and is unchanged (hash); with --xlsx, every
       Area, Category, Topic, link text and link address equals the spreadsheet cell
    T  theme/theme.json is byte-for-byte the owner's theme (hash); a theme registered in any report
       folder of the template has the same content
    S  every skill has a valid name and description; always-loaded files stay small;
       no file pins an AI model; no file calls an excluded command-line tool;
       docs/report-brief.md still holds every label and table the project check reads
    L  every relative link and every repository path written in a Markdown file exists
    C  every skill and instruction file cites checklist items, all between 1 and 79 (or says 'none'),
       and together they cover all 79
    X  docs/lessons.md is well formed, no lesson points at the checklist or the theme, and a mistake
       that has come back has been built into the template or declined (see scripts/lessons.py)
"""
import hashlib
import json
import os
import re
import sys
import urllib.parse
import xml.etree.ElementTree as ET
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp  # noqa: E402
import lessons  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# If the owner deliberately replaces the theme or the checklist, update these three values.
THEME_SHA256 = "1f7626241de5d9389bc8013b4778d886ba8ab8c4e37528a1959d03d9e374d934"
CHECKLIST_MD_SHA256 = "86e47c4ce40c7e635796f7c69beb147b6db83817c9b17e06e9d4148a507d74a5"
XLSX_SHA256 = "7524763f9f91591ece47eda7cda15b90b351c322133134d9d8f03bf12c8d4ae8"

ITEM_COUNT = 79
HEADER = ["Area", "Category", "Topic", "Microsoft documentation"]
SHEET_NAME = "Checklist Review"
LINE_BUDGET = {"copilot-instructions.md": 40, ".instructions.md": 40, "SKILL.md": 120}
SKILL_NAME = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")           # agentskills.io specification
MODEL_WORDS = re.compile(r"\b(gpt-?[0-9o]|claude|sonnet|opus|haiku|gemini|llama|mistral|deepseek|grok)\b", re.I)
TOOL_CALLS = re.compile(r"(?<![.\w/-])pbir\s+[a-z]|powerbi-report-author|AskUserQuestion|CLAUDE_PLUGIN_ROOT")
CREATED_LATER = {"docs/checklist-review.md",        # written by a review, not part of the template
                 "docs/checklist-review-before.md", "docs/fix-plan.md"}      # written by the evaluate-and-improve flow
NS = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main",
      "r": "http://schemas.openxmlformats.org/officeDocument/2006/relationships",
      "p": "http://schemas.openxmlformats.org/package/2006/relationships"}

errors = []
notes = []


def error(code, where, message):
    errors.append("%s  %s  %s" % (code, where, message))


def sha256(path):
    with open(path, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def read_text(path):
    """File content as text. A file that is not UTF-8 is reported once and read as empty."""
    try:
        with open(path, encoding="utf-8-sig") as fh:
            return fh.read()
    except (UnicodeDecodeError, OSError):
        message = "L003  %s  file cannot be read as UTF-8 text, so it cannot be checked" % rel(path)
        if message not in errors:
            errors.append(message)
        return ""


def rel(path):
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def repo_files():
    for folder, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "node_modules")]
        for name in sorted(files):
            yield os.path.join(folder, name)


# ---------------------------------------------------------------- checklist

ITEM_BLOCK = re.compile(
    r"^## Item (\d+)\n\n"
    r"- ([^:\n]+): ([^\n]*)\n"
    r"- ([^:\n]+): ([^\n]*)\n"
    r"- ([^:\n]+): \[([^\n]*)\]\(([^\n]*)\)\n"
    r"- ([^:\n]+):\n\n"
    r"~~~text\n((?:.|\n)*?)\n~~~\n", re.M)


def parse_checklist_md(path):
    text = read_text(path).replace("\r\n", "\n")
    items = []
    for m in ITEM_BLOCK.finditer(text):
        items.append({"n": int(m.group(1)),
                      "labels": [m.group(2), m.group(4), m.group(9), m.group(6)],
                      "area": m.group(3), "category": m.group(5),
                      "doc_text": m.group(7), "doc_url": m.group(8), "topic": m.group(10)})
    return items


def read_xlsx(path):
    """Return (header, rows) of the checklist sheet. rows: (area, category, topic, doc_text, doc_url)."""
    with zipfile.ZipFile(path) as z:
        shared = []
        if "xl/sharedStrings.xml" in z.namelist():
            for si in ET.fromstring(z.read("xl/sharedStrings.xml")).findall("m:si", NS):
                shared.append("".join(t.text or "" for t in si.iter("{%s}t" % NS["m"])))
        workbook = ET.fromstring(z.read("xl/workbook.xml"))
        rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read("xl/_rels/workbook.xml.rels"))}
        target = None
        names = []
        for sheet in workbook.find("m:sheets", NS):
            names.append(sheet.get("name"))
            if sheet.get("name") == SHEET_NAME:
                target = rels[sheet.get("{%s}id" % NS["r"])]
        if target is None:
            raise ValueError("sheet '%s' not found (sheets: %s)" % (SHEET_NAME, ", ".join(names)))
        sheet_path = target.lstrip("/") if target.startswith("/") else "xl/" + target
        sheet = ET.fromstring(z.read(sheet_path))
        cells = {}
        for c in sheet.iter("{%s}c" % NS["m"]):
            kind = c.get("t")
            if kind == "inlineStr":
                value = "".join(t.text or "" for t in c.iter("{%s}t" % NS["m"]))
            else:
                v = c.find("m:v", NS)
                value = "" if v is None or v.text is None else v.text
                if kind == "s":
                    value = shared[int(value)]
            cells[c.get("r")] = value.replace("\r\n", "\n").replace("_x000D_", "")
        links = {}
        rel_path = os.path.dirname(sheet_path) + "/_rels/" + os.path.basename(sheet_path) + ".rels"
        if rel_path in z.namelist():
            sheet_rels = {r.get("Id"): r.get("Target") for r in ET.fromstring(z.read(rel_path))}
            for h in sheet.iter("{%s}hyperlink" % NS["m"]):
                rid = h.get("{%s}id" % NS["r"])
                if rid in sheet_rels:
                    links[h.get("ref")] = sheet_rels[rid]
    header = [cells.get(col + "1", "") for col in "ABCD"]
    rows = []
    row = 2
    while any(cells.get(col + str(row), "") for col in "ABCD"):
        rows.append((cells.get("A%d" % row, ""), cells.get("B%d" % row, ""), cells.get("C%d" % row, ""),
                     cells.get("D%d" % row, ""), links.get("D%d" % row, "")))
        row += 1
    return header, rows


def check_checklist(xlsx):
    path = os.path.join(ROOT, "checklist", "checklist.md")
    if not os.path.isfile(path):
        error("K001", "checklist/checklist.md", "file is missing")
        return
    items = parse_checklist_md(path)
    numbers = [i["n"] for i in items]
    if numbers != list(range(1, ITEM_COUNT + 1)):
        error("K002", "checklist/checklist.md", "expected items 1 to %d in order, found %d item block(s)" % (ITEM_COUNT, len(items)))
    for item in items:
        if item["labels"] != HEADER:
            error("K003", "checklist/checklist.md", "item %d: column labels differ from %s" % (item["n"], HEADER))
    digest = sha256(path)
    if digest != CHECKLIST_MD_SHA256:
        error("K004", "checklist/checklist.md", "file content has changed since it was taken from the spreadsheet (sha256 %s)" % digest)
    if xlsx is None:
        notes.append("Checklist: structure and hash checked. Run with --xlsx <file> to compare word for word with the spreadsheet.")
        return
    try:
        header, rows = read_xlsx(xlsx)
    except (OSError, KeyError, ValueError, zipfile.BadZipFile, ET.ParseError) as exc:
        error("K005", xlsx, "cannot read spreadsheet: %s" % exc)
        return
    if sha256(xlsx) != XLSX_SHA256:
        notes.append("Checklist: the spreadsheet given is not the exact file the checklist was taken from (different hash); comparing its cells anyway.")
    differences = 0
    if header != HEADER:
        error("K006", xlsx, "header row is %s, expected %s" % (header, HEADER))
        differences += 1
    if len(rows) != len(items):
        error("K007", xlsx, "spreadsheet has %d item rows, checklist.md has %d" % (len(rows), len(items)))
        differences += 1
    for item, row in zip(items, rows):
        for label, ours, theirs in (("Area", item["area"], row[0]), ("Category", item["category"], row[1]),
                                    ("Topic", item["topic"], row[2]),
                                    ("Microsoft documentation (text)", item["doc_text"], row[3]),
                                    ("Microsoft documentation (link)", item["doc_url"], row[4])):
            if ours != theirs:
                differences += 1
                error("K008", "checklist/checklist.md", "item %d: %s differs from the spreadsheet" % (item["n"], label))
    if differences == 0:
        notes.append("Checklist: all %d items match the spreadsheet word for word (%d cells and %d link addresses compared)."
                     % (len(items), len(items) * 4 + 4, len(items)))


# ---------------------------------------------------------------- theme

def check_theme():
    path = os.path.join(ROOT, "theme", "theme.json")
    if not os.path.isfile(path):
        error("T101", "theme/theme.json", "file is missing")
        return
    digest = sha256(path)
    unchanged = digest == THEME_SHA256
    if not unchanged:
        error("T102", "theme/theme.json", "file differs from the owner's theme (sha256 %s)" % digest)
    with open(path, "rb") as fh:
        original_bytes = fh.read()
    try:
        original = json.loads(original_bytes.decode("utf-8"))
    except (ValueError, RecursionError):
        if unchanged:
            error("T102", "theme/theme.json", "file is not valid JSON")
        return
    reports = cp.find_reports(ROOT)
    if not reports:
        if unchanged:
            notes.append("Theme: theme/theme.json matches the owner's file. No report folder in the template yet, so no registered copy to compare.")
        return
    for report in reports:
        report_json = cp.load_object(os.path.join(report, "definition", "report.json"))
        collection = report_json.get("themeCollection") if report_json else None
        custom = collection.get("customTheme") if isinstance(collection, dict) else None
        name = custom.get("name") if isinstance(custom, dict) else None
        if not isinstance(name, str) or not name:
            error("T103", rel(report), "no custom theme is registered in report.json")
            continue
        copy = os.path.join(report, "StaticResources", "RegisteredResources", name)
        if not os.path.isfile(copy):
            error("T104", rel(report), "registered theme file is missing: %s" % name)
            continue
        with open(copy, "rb") as fh:
            copy_bytes = fh.read()
        try:
            same = json.loads(copy_bytes.decode("utf-8-sig")) == original
        except (ValueError, RecursionError):
            same = False
        if not same:
            error("T105", rel(copy), "registered theme content differs from theme/theme.json")
        else:
            notes.append("Theme: %s has the same content as theme/theme.json (%s)."
                         % (rel(copy), "byte-identical" if copy_bytes == original_bytes else "same JSON values, different bytes"))


# ---------------------------------------------------------------- guidance files

def front_matter(text):
    if not text.startswith("---\n"):
        return {}
    end = text.find("\n---", 4)
    if end < 0:
        return {}
    fields = {}
    for line in text[4:end].split("\n"):
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip().strip('"').strip("'")
    return fields


def guidance_files():
    base = os.path.join(ROOT, ".github")
    for folder, dirs, files in os.walk(base):
        for name in sorted(files):
            if name.endswith(".md"):
                yield os.path.join(folder, name)


def check_guidance():
    skills_dir = os.path.join(ROOT, ".github", "skills")
    for path in guidance_files():
        text = read_text(path).replace("\r\n", "\n")
        name = os.path.basename(path)
        lines = text.count("\n") + 1
        for suffix, budget in LINE_BUDGET.items():
            if name.endswith(suffix) and lines > budget:
                error("S001", rel(path), "%d lines; the limit for this kind of file is %d" % (lines, budget))
        fields = front_matter(text)
        if "model" in fields:
            error("S002", rel(path), "front matter has a 'model' field; the template must not pin an AI model")
        if name == "SKILL.md":
            folder = os.path.basename(os.path.dirname(path))
            skill = fields.get("name", "")
            if skill != folder or not SKILL_NAME.match(skill) or len(skill) > 64:
                error("S003", rel(path), "skill name must equal its folder name, use lowercase letters, digits and single hyphens, and be at most 64 characters")
            description = fields.get("description", "")
            if not description or len(description) > 1024:
                error("S004", rel(path), "skill description is missing or longer than 1024 characters")
    if os.path.isdir(skills_dir):
        for folder in sorted(os.listdir(skills_dir)):
            if os.path.isdir(os.path.join(skills_dir, folder)) and not os.path.isfile(os.path.join(skills_dir, folder, "SKILL.md")):
                error("S005", ".github/skills/" + folder, "skill folder has no SKILL.md")
    for path in list(guidance_files()) + [os.path.join(ROOT, "docs", "report-brief.md"), os.path.join(ROOT, "README.md")]:
        if not os.path.isfile(path):
            continue
        text = read_text(path)
        for number, line in enumerate(text.splitlines(), 1):
            if MODEL_WORDS.search(line):
                error("S006", "%s:%d" % (rel(path), number), "names an AI model or model vendor")
            if not path.endswith("README.md") and TOOL_CALLS.search(line):
                error("S007", "%s:%d" % (rel(path), number), "calls a command-line tool or feature the template must not depend on")


def check_brief():
    """The project check reads numbers, lists and exceptions from the brief by these labels."""
    path = os.path.join(ROOT, cp.BRIEF)
    if not os.path.isfile(path):
        error("S008", "docs/report-brief.md", "the report brief is missing")
        return
    text = read_text(path).lower()
    for label in list(cp.BRIEF_LABELS.values()) + [cp.MODEL_EXCEPTIONS, cp.LAYOUT_EXCEPTIONS]:
        if label.lower() not in text:
            error("S008", "docs/report-brief.md", "the label '%s' is gone; scripts/check_project.py reads it" % label)


REPO_PATH = re.compile(r"(?<![\w/.-])((?:\.github|scripts|docs|checklist|theme|tests|evals)/[\w./-]*[\w/-])")


def check_links():
    for path in repo_files():
        if not path.endswith(".md") or rel(path) == "checklist/checklist.md":
            continue
        text = read_text(path)
        folder = os.path.dirname(path)
        for number, line in enumerate(text.splitlines(), 1):
            for target in re.findall(r"\]\(([^)\s]+)\)", line):
                if re.match(r"^[a-z]+:", target) or target.startswith("#"):
                    continue
                target = urllib.parse.unquote(target.split("#")[0])
                if target and not os.path.exists(os.path.join(folder, target)):
                    error("L001", "%s:%d" % (rel(path), number), "link target does not exist: %s" % target)
            # repository paths anywhere on the line, including inside commands and code blocks
            plain = re.sub(r"https?://\S+", " ", line).replace("\\", "/").replace(" ./", " ").replace("`./", "`")
            for token in REPO_PATH.findall(plain):
                token = token.rstrip(".,;:")
                if token in CREATED_LATER or any(ch in token for ch in "<>*{}"):
                    continue
                if not os.path.exists(os.path.join(ROOT, token)):
                    error("L002", "%s:%d" % (rel(path), number), "path does not exist: %s" % token)
            for script in re.findall(r"\bpy(?:thon3?)?\s+(?!-)([\w./-]+\.py)\b", plain):
                if not os.path.exists(os.path.join(ROOT, script)):
                    error("L002", "%s:%d" % (rel(path), number), "script does not exist: %s" % script)
            for target in re.findall(r"\bdiscover\s+-s\s+([\w./-]+)", plain):
                if not os.path.isdir(os.path.join(ROOT, target)):
                    error("L002", "%s:%d" % (rel(path), number), "folder does not exist: %s" % target)
            for token in re.findall(r"`(references/[\w.-]+)`", line):
                if not os.path.exists(os.path.join(folder, token)):
                    error("L002", "%s:%d" % (rel(path), number), "path does not exist: %s" % token)


def parse_items(text):
    numbers = set()
    for part in re.split(r"[,;]", text):
        part = part.strip().rstrip(".")
        m = re.match(r"^(\d+)\s*[-–]\s*(\d+)$", part)
        if m:
            numbers.update(range(int(m.group(1)), int(m.group(2)) + 1))
        elif part.isdigit():
            numbers.add(int(part))
        elif part:
            return None
    return numbers


def check_citations():
    cited = set()
    review_only = set()
    for path in guidance_files():
        name = os.path.basename(path)
        must_cite = name == "SKILL.md" or name.endswith(".instructions.md") or name == "copilot-instructions.md"
        found = False
        for number, line in enumerate(read_text(path).splitlines(), 1):
            m = re.match(r"^(Checklist items|Review-only items):\s*(.+)$", line.strip())
            if not m:
                continue
            if m.group(1) == "Checklist items" and m.group(2).strip().lower() == "none":
                found = True            # a file that applies no checklist item says so
                continue
            numbers = parse_items(m.group(2))
            if numbers is None or not numbers or min(numbers) < 1 or max(numbers) > ITEM_COUNT:
                error("C001", "%s:%d" % (rel(path), number), "item list must be numbers and ranges between 1 and %d" % ITEM_COUNT)
                continue
            if m.group(1) == "Review-only items":
                review_only |= numbers
            else:
                found = True
                if "pbi-checklist-review" not in rel(path):
                    cited |= numbers
        if must_cite and not found:
            error("C002", rel(path), "has no 'Checklist items:' line")
    everything = set(range(1, ITEM_COUNT + 1))
    missing = everything - cited - review_only
    if missing:
        error("C003", ".github", "no skill or instruction file applies item(s): %s" % ", ".join(str(n) for n in sorted(missing)))
    both = cited & review_only
    if both:
        error("C004", ".github", "item(s) listed as review-only but also applied elsewhere: %s" % ", ".join(str(n) for n in sorted(both)))
    template = os.path.join(ROOT, ".github", "skills", "pbi-checklist-review", "references", "review-template.md")
    if os.path.isfile(template):
        rows = re.findall(r"^\|\s*(\d+)\s*\|", read_text(template), re.M)
        if [int(n) for n in rows] != list(range(1, ITEM_COUNT + 1)):
            error("C005", rel(template), "review template must have one row for each item 1 to %d, in order" % ITEM_COUNT)
    else:
        error("C005", ".github/skills/pbi-checklist-review/references/review-template.md", "file is missing")


def check_lessons():
    path = os.path.join(ROOT, lessons.LESSONS)
    if not os.path.isfile(path):
        error("X001", lessons.LESSONS, "the lessons file is missing")
        return
    lessons.ROOT = ROOT
    errors.extend(lessons.check_file(path))


def main(argv):
    cp.safe_output()
    args = argv[1:]
    xlsx = None
    if args[:1] == ["--xlsx"] and len(args) == 2:
        xlsx = args[1]
    elif args:
        print(__doc__)
        return 2
    check_checklist(xlsx)
    check_theme()
    check_guidance()
    check_brief()
    check_links()
    check_citations()
    check_lessons()
    for line in errors:
        print(line)
    for line in notes:
        print("note  " + line)
    print("Template check: %d error(s)." % len(errors))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
