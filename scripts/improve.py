#!/usr/bin/env python3
"""The evaluate-and-improve flow: safety first, a fix plan, and before-and-after counts.

Usage (run from the repository root; <folder> is '.' when left out):
    python scripts/improve.py next [<folder>]        say which step the flow is at, and what to run
    python scripts/improve.py start [<folder>]       stop unless everything is committed, a branch is checked
                                                     out and no earlier flow left its files; make a new branch;
                                                     copy the project, unchanged, to _before/
    python scripts/improve.py snapshot [<folder>]    keep the first review as docs/checklist-review-before.md
    python scripts/improve.py plan [<folder>]        write docs/fix-plan.md from the review and the project check
    python scripts/improve.py check-plan [<folder>]  check the plan: every row has a kind, a change, files, a risk
    python scripts/improve.py release [<folder>]     give every row without a status its status
    python scripts/improve.py compare [<folder>]     Pass, Fail and Not applicable before and after; the items
                                                     that changed; the pages to look at; what was skipped; the
                                                     questions left for a person

The steps, and who does what, are in the skill 'pbi-improve'. This script changes no report or model file.
'start' makes a Git branch and the copy; 'snapshot' and 'plan' write the two files named above.

The copy: the .pbip file points to the report folder, and the report points to the model, both by relative
path (Microsoft Learn, "Power BI Desktop projects"). So the three are copied together, names unchanged, and
nothing inside them is edited. Each .platform file holds a logicalId that must stay unique in a Git branch
(Microsoft Learn, "Git integration source code format"), so the copy must never be committed: 'start' makes
it only when Git ignores _before/, and skips it, saying so, when a path would pass 260 characters.

Kinds of fix, in the order they are applied, one commit each: Theme (the owner's theme is registered),
Mechanical (descriptions, format strings, folders, hiding, header icons and tooltips, alt text, titles, the
DAX style), Layout (positions and sizes, a back button, tab order), Measures (every measure moves to
_Measures), Renames (names the naming standard rejects), Data (changes that make Power BI Desktop load a table
again: a query's text, a partition's name, a data type). Needs a person is everything else: a fact or a
decision that no file holds. Those rows are questions, listed once at the end; they are never asked mid-run.

Nothing waits for an approval and no row is held back. Measures move and names are corrected even though a
report on a published copy of the model may break: no file here can show such a report, so the final answer
says so. Data rows are applied last, and 'compare' says that Power BI Desktop must refresh the model once: a
changed query, a renamed partition, a new data type or a new table is empty until then.
The branch, the copy in _before/ and one commit for each kind are the safeguard: each kind can be undone alone.

Needs Python 3.8 or later and Git. Uses the standard library only.
Exit code: 0 = done, 1 = stopped or a problem found, 2 = wrong usage.
"""
import datetime
import os
import re
import shutil
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp  # noqa: E402

REVIEW = os.path.join("docs", "checklist-review.md")
REVIEW_BEFORE = os.path.join("docs", "checklist-review-before.md")
PLAN = os.path.join("docs", "fix-plan.md")
BRANCH_PREFIX = "improve/"
PATH_LIMIT = 260                                     # Microsoft Learn, "Power BI Desktop projects", limitations
COMMITS = {"Theme": "Improve: theme", "Mechanical": "Improve: mechanical fixes", "Layout": "Improve: layout fixes",
           "Measures": "Improve: measures moved", "Renames": "Improve: renames",
           "Data": "Improve: changes that need a refresh"}
AUTO_KINDS = ("Theme", "Mechanical", "Layout", "Measures", "Renames", "Data")       # applied in this order
PERSON_KIND = "Needs a person"
KINDS = AUTO_KINDS + (PERSON_KIND,)
STATUS = re.compile(r"(?i)(to do|done|question|answered|skipped: \S.*)\Z")
PLAN_HEADER = ["Id", "Kind", "Item or code", "Object", "What will change", "Files", "What could break", "Status"]

# code -> (what will change, what could break), one table for each kind. A code that is in none needs a person.
THEME = {
    "T001": ("Register theme/theme.json in the report files (python scripts/scaffold.py theme .)",
             "Every visual takes the theme's colours and fonts. Microsoft Learn describes importing the theme in "
             "Power BI Desktop as the supported route: look at the colours when the report is first opened"),
}
MECHANICAL = {
    "D001": ("Add a '///' description from the brief, or a TODO(owner) question when the brief does not say",
             "Nothing in the report. A placeholder still leaves checklist item 23 open"),
    "D002": ("Add a '///' description above the shared query or parameter", "Nothing in the report"),
    "D003": ("Move the '///' description directly above its object", "Nothing in the report"),
    "C001": ("Turn the '//' comment into a '///' description, or move it inside the expression", "Nothing in the report"),
    "H001": ("Set Header icons off on the visual (scripts/set_visual_defaults.py)",
             "Drill, focus and export icons no longer show in reading view"),
    "H002": ("Set Tooltips off on the visual (scripts/set_visual_defaults.py)", "Hover tooltips no longer show"),
    "N003": ("Add a VisualLabel annotation; the visual keeps its name", "Nothing: Power BI Desktop ignores annotations"),
    "M003": ("Set the measure's display folder to Subject\\Type (scripts/set_model_properties.py)",
             "The measure moves in the Data pane; visuals keep working"),
    "M004": ("Set the measure's display folder to a subject and a type from the lists",
             "The measure moves in the Data pane; visuals keep working"),
    "M009": ("Set the measure's format string to the brief's format for that kind of number",
             "Numbers show differently wherever the measure is used"),
    "M101": ("Put each visible column in one of the four column folders", "Columns move in the Data pane"),
    "M102": ("Hide the key column (scripts/set_model_properties.py --from-findings M102)",
             "Report authors no longer see it; a visual that uses it is reported as M104"),
    "M103": ("Hide the numeric column the measure totals (--from-findings M103)",
             "Report authors no longer see it; a visual that uses it is reported as M104"),
    "M112": ("Set the column's format string to the brief's format", "Values show differently wherever the column is used"),
    "M114": ("Set the data category the column's name states (City, Country, Latitude and so on)",
             "A map may place the values differently"),
    "M518": ("Replace DIVIDE by the '/' operator where the divisor is a fixed number",
             "Nothing: a fixed number is never zero or blank"),
    "M519": ("Replace ALL by REMOVEFILTERS in the filter argument", "Nothing: as a filter argument the two do the same"),
    "M520": ("Lay the formula out in the DAX style; the formula itself does not change", "Nothing: only spaces and line breaks change"),
    "M803": ("Add a '///' description above the function, from the brief, or a TODO(owner) question", "Nothing in the report"),
    "M812": ("Add a '///' description above each calculation item, from the brief, or a TODO(owner) question", "Nothing in the report"),
    "M907": ("Set isAvailableInMdx back to true on the column", "Nothing: the column is used for sorting or in a hierarchy"),
    "V002": ("Hide the tooltip page (visibility HiddenInViewMode)", "The page no longer shows as a tab; the tooltip still works"),
    "V009": ("Remove the colour, font, size, border, shadow or background set on the visual, so that it follows the theme. "
             "Remove a whole setting, never one part of a setting made of parts (data bars, a colour scale, icons)",
             "The visual looks different: it takes the theme's style"),
    "V024": ("Put the missing bar colour of the data bars back with a theme colour, or remove the data bars as a whole",
             "Nothing: without the part Power BI Desktop does not load the report at all"),
    "V011": ("List every page folder once in pages.json, in the present order, new ones last", "The tab order of pages may change"),
    "A001": ("Write alt text that says what the visual shows, from its fields and the page's question in the brief",
             "Nothing on screen; screen readers read the new text"),
    "A003": ("Write a title that says what the visual shows, from its fields and the page's question in the brief",
             "The title text on the page changes"),
    "A004": ("Shorten the alt text to 250 characters or fewer", "Nothing on screen"),
}
LAYOUT = {
    "G001": ("Move or resize the visual so that it sits inside the page (scripts/set_positions.py)", "The page looks different"),
    "G002": ("Move or resize one of the two visuals so that they no longer overlap", "The page looks different"),
    "G003": ("Put x, y, width and height on the grid (scripts/set_positions.py --snap)", "Sizes change by a few pixels; text may wrap"),
    "G004": ("Move the outer visuals to the margin", "The page looks different"),
    "G005": ("Give the visuals of one row the same height", "The page looks different"),
    "G006": ("Make the gaps between neighbours equal to the gap", "The page looks different"),
    "G007": ("Write the page size in the brief; or resize the page in Power BI Desktop", "A resized page changes every position"),
    "V001": ("Add a back button to the drillthrough page (copy the shipped example) at the top-left of the page",
             "The page gains a visual; other visuals may have to move"),
    "A002": ("Give each visual its own tab order number, in reading order: left to right, top to bottom",
             "Keyboard users reach the visuals in a new order"),
}
MEASURES = {
    "M001": ("Move the measure to _Measures and repair every reference to it (python scripts/find_references.py, "
             "then the checks). All measures move in one commit",
             "A report on a published copy of this model names the measure with its old table and breaks"),
    "M002": ("Make or repair the _Measures table: visible, exactly one column, that column hidden "
             "(python scripts/scaffold.py measures-table makes the table when it is missing)",
             "A new table is empty until Power BI Desktop refreshes the model"),
}
RENAMES = {
    "M005": ("Rename one of the two measures as the naming standard asks, and repair every reference",
             "A report on a published copy of this model names the old name and breaks"),
    "M006": ("Rename the measure or the column as the naming standard asks, and repair every reference",
             "A report on a published copy of this model names the old name and breaks"),
    "M007": ("Rename the measure to a business name, and repair every reference",
             "A report on a published copy of this model names the old name and breaks"),
    "M008": ("Rename the measure as the naming standard asks, and repair every reference",
             "A report on a published copy of this model names the old name and breaks"),
    "M118": ("Rename the table, column or hierarchy as the naming standard asks, and repair every reference",
             "A report on a published copy of this model names the old name and breaks"),
    "M119": ("Rename the column or the hierarchy as the naming standard asks, and repair every reference",
             "A report on a published copy of this model names the old name and breaks"),
    "M802": ("Rename the function, and change every formula that calls it",
             "A report on a published copy of this model that calls the function breaks"),
    "M807": ("Rename the function or its parameters, and change every formula that calls it",
             "A report on a published copy of this model that calls the function breaks"),
    "V012": ("Rename the report-level measure with the prefix, and update the visuals that use it",
             "Nothing outside this report: a report-level measure lives in the report"),
}
DATA = {
    "P001": ("Add a '//' line above the Power Query step that says what it does",
             "The query's text changes, so Power BI Desktop may load the table again: it is empty until a refresh"),
    "M108": ("Change the column from the floating-point type to fixed decimal, or to whole number when the brief "
             "says its values are whole", "The column is stored again: the table is empty until a refresh, and "
             "values keep four decimals at most"),
    "M117": ("Give the table's one partition the table's name",
             "A renamed partition is a new partition: the table is empty until a refresh. A refresh script that "
             "names the partition must be updated"),
}
PERSON = {
    "M010": "Edit the DAX reference; the developer checks the result",
    "M104": "Decide whether the hidden column should be shown again",
    "M105": "The developer states why it is calculated in the model; then the reason is written as an annotation",
    "M106": "Decide whether the calculated columns can come from the source",
    "M107": "Decide on 'do not summarise': Microsoft does not document its effect on visuals that already total the column",
    "M109": "Give both relationship columns the same type, at the source or in Power Query",
    "M110": "Decide whether the relationship can use whole-number keys",
    "M111": "Look at the data: split date and time, or keep the date only",
    "B001": "Repair the field reference: find what the field is called now (scripts/find_references.py), or ask which field is meant",
    "M113": "Say which column holds the order of the month names; then sortByColumn is set",
    "M115": "Decide which table keeps the column; removing it from the other needs a yes",
    "M116": "Decide whether the flag is shown as Yes and No text",
    "M401": "The developer turns Auto date/time off in Power BI Desktop (Options, Current File, Time intelligence)",
    "M402": "Name the date table; then it is marked (dataCategory Time, isKey on its date column) or built from the shipped example",
    "M403": "Decide whether the model gets a date table",
    "M404": "Confirm the table is the date table and that its date column has one row per day; then it is marked",
    "M405": "Decide: a single direction, CROSSFILTER in one measure, or a reason in the brief",
    "M406": "Decide: a shared dimension or a bridge table, or a reason in the brief",
    "M407": "Decide which single direction the many-to-many relationship filters",
    "M408": "Review the design of the relationships",
    "M409": "Decide whether the two tables become one",
    "M410": "Decide: use the inactive relationship in a measure, or remove it",
    "M411": "Say what the table is for: relate it, or list it in the brief",
    "M412": "Decide whether the dimension tables are flattened into one",
    "M413": "Confirm the column's values are unique; then it is marked as the key",
    "M414": "Check each security role against the inactive relationships",
    "M415": "Rework the measure or the role: USERELATIONSHIP towards a secured table raises an error",
    "M417": "Unpivot the month columns in Power Query; visuals that use them must be rebuilt",
    "M501": "Rewrite without IFERROR or ISERROR; the developer checks the numbers",
    "M502": "Rewrite the division with DIVIDE; where the divisor was zero or blank the result becomes blank, so the developer checks the numbers",
    "M503": "Confirm the measure counts rows; then it becomes COUNTROWS",
    "M504": "Rewrite with SELECTEDVALUE; the developer checks the result",
    "M505": "Rewrite the filter on the column itself; the developer checks the numbers",
    "M506": "Decide whether a zero is really wanted where there is no data",
    "M507": "Store the repeated expression in a variable; the developer checks the numbers",
    "M508": "Decide which of the measures stays; the others are replaced wherever they are used",
    "M509": "Decide whether the repeating measure is removed; visuals that use it must change",
    "M510": "Rewrite with TREATAS; the developer checks the numbers",
    "M511": "Rewrite as one DIVIDE of the difference; the developer checks the numbers",
    "M512": "Remove EVALUATEANDLOG from the formula",
    "M513": "Decide: date table columns and plain filters, or accept the slower measure",
    "M514": "Rewrite with a variable; the developer checks the numbers",
    "M516": "Say the order the function should use; then ORDERBY is added",
    "M517": "Rewrite with SELECTEDVALUE; the developer checks the result",
    "M120": "Decide which columns are hidden, or whether the table is split",
    "M521": "Give one CALCULATE all the filters, or move the inner part to a variable; the developer checks the numbers",
    "M522": "Group with SUMMARIZE and add the column with ADDCOLUMNS; the developer checks the numbers",
    "M609": "Decide whether the security filter must travel both ways; the roles must be tested again",
    "M711": "Replace the Power Query partition by an entity partition, from the shipped Direct Lake example; the developer confirms the source",
    "M806": "Decide: keep the hidden object out of the function, or change the role; the function is tested for that role",
    "M832": "Confirm nothing else uses the data source; then it is removed",
    "M833": "Convert the partition to a Power Query (m) partition; the model must be refreshed and checked",
    "M910": "Say which name the calculated table's formula should return for the column",
    "P007": "Decide whether the table's load is turned off (Enable load in Power BI Desktop)",
    "V013": "The developer clears the filter in Power BI Desktop and saves",
    "V014": "Decide: hide the drillthrough page, or add a reset button with a bookmark",
    "V015": "Say which table the filter is on; then the filter is repaired",
    "V016": "Plan the replacement of the visual, or give the reason in section 10 of the brief",
    "V017": "Add the file to the report's registered resources, or say which picture is meant",
    "M524": "Move the USERCULTURE logic to a measure; a calculated column or table cannot follow the reader",
    "M525": "Say the default text of the label, and which languages the model supports",
    "V019": "Move the measure to the model",
    "V020": "Decide: label measures for the report's text, or one language (a row in section 10 of the brief)",
    "V021": "Decide: hide the pages and add navigation buttons, or one language (a row in section 10 of the brief)",
    "V022": "The developer says yes or no to the preview feature; a yes gets its row in section 11 of the brief",
    "M815": "Decide: the calculation group or the detail rows expressions",
    "V023": "Decide whether other reports may drill through to this report; then the setting is switched on",
    "M601": "Simplify the security rule; the role must be tested again",
    "M602": "Move the security rule to a dimension table; the role must be tested again",
    "M603": "Replace USERNAME with USERPRINCIPALNAME; the role must be tested again",
    "M604": "Review the role and the many-to-many relationship together",
    "M605": "End the rule in FALSE for people it does not name; the role must be tested again",
    "M606": "Decide: take the hidden field out of the visuals, or change the role",
    "M607": "Put the row rules and the object rules in the same role; the roles must be tested again",
    "M608": "Secure columns instead of the table, or change the chain of relationships",
    "M701": "Rewrite the native query as a plain SELECT, or use a view at the source",
    "M702": "Move the transformation to the source",
    "M703": "Replace the date filter in Power Query with a relative date filter in the report",
    "M704": "Use a source column for the relationship",
    "M705": "Build the column at the source, or keep its formula to values of the same row",
    "M706": "Confirm both tables come from one source; then the dimension's storage mode becomes Dual",
    "M707": "Add the parameters RangeStart and RangeEnd, of type Date/Time, and filter the table on them",
    "M708": "Check that the date filter reaches the source; or filter on a table or view instead",
    "M709": "Include one end of the refresh window only; the next refresh then loads boundary rows once",
    "M801": "Raise the model's compatibility level to 1702; an older Power BI Desktop can then no longer open it",
    "M804": "Say the type of each parameter",
    "M805": "Rewrite the function without calling itself",
    "M811": "Add calculation items, or remove the empty calculation group",
    "M813": "Say in which order the calculation groups apply; then each gets its precedence",
    "M814": "Decide on discourageImplicitMeasures: with it on, report authors can no longer drag a number column for an automatic total",
    "M821": "Say which field the field parameter should name",
    "M822": "Rebuild the field parameter from the shipped example; slicers and visuals bound to it must be checked",
    "M831": "Add objects to the perspective, or remove it",
    "M841": "The developer says yes or no to the preview feature; a yes gets its row in section 11 of the brief",
    "M901": "Say which column the relationship should use; the model does not load until it is repaired",
    "M902": "Say which column the hierarchy level should use",
    "M903": "Say which column sorts this one",
    "M904": "Say which source column the column reads",
    "M905": "Give the object its formula, or remove it",
    "M906": "Remove the control character from the name or description",
    "M908": "Say which column the formula should name; it returns an error until it is repaired",
    "M909": "Check the function's name on Microsoft Learn (skill pbi-lookup)",
    "P002": "Pass the values as parameters of the native query",
    "P003": "Decide: keep the shared query, or move the work to a dataflow or the source",
    "P004": "Set the Dataverse options; the query's columns may change",
    "P005": "Move the file to a shared location, or record the gateway in the brief",
    "P006": "Decide whether the reshaping moves to the source or a dataflow",
    "V003": "The developer gives the tooltip page the built-in tooltip size in Power BI Desktop and fits its visuals",
    "V004": "Take the slicer or button off the tooltip page, or make it a drillthrough page",
    "V005": "Decide which facts the tooltip page adds",
    "V006": "Split the page, or give the reason in section 10 of the brief",
    "V007": "Review the number of visuals on the page",
    "V008": "Say where the button should go",
    "V010": "Say what the bookmark should show; a simple one is written again from the shipped example, another the developer captures again in Power BI Desktop",
}
PERSON_ITEMS = frozenset((3, 11, 14, 17, 18, 21, 31, 39, 40, 41, 42, 43, 44, 45, 67, 68, 76, 77, 78, 79))


def git(root, *args):
    try:
        done = subprocess.run(("git", "-C", root) + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except OSError:
        return 127, "git was not found"
    return done.returncode, done.stdout.decode("utf-8", "replace").strip()


def project_parts(root):
    """The .pbip files and the .Report and .SemanticModel folders directly under root."""
    return sorted(name for name in os.listdir(root)
                  if name.lower().endswith(".pbip") or name.endswith((".Report", ".SemanticModel")))


def read_review(path):
    """{item: status} of a review table, or None when the file cannot be read."""
    try:
        with open(path, encoding="utf-8-sig") as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    rows = {}
    inside = False
    for line in lines:
        text = line.strip()
        if not text.startswith("|"):
            if inside:
                break
            continue
        cells = [cp._plain(c) for c in text.strip("|").split("|")]
        if not inside:
            inside = [c.lower() for c in cells[:3]] == ["item", "status", "evidence"]
        elif len(cells) >= 3 and cells[0].isdigit():
            rows[int(cells[0])] = (cells[1], cells[2])
    return rows


def counts(rows):
    return tuple(sum(1 for status, _ in rows.values() if status == wanted) for wanted in cp.REVIEW_STATUSES)


def _cell(text):
    return " ".join(str(text).split()).replace("|", "\\|")


def read_plan(path):
    """(rows, problems) of a fix plan. rows: dicts keyed by PLAN_HEADER."""
    try:
        with open(path, encoding="utf-8-sig") as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeDecodeError) as exc:
        return [], ["cannot read %s: %s" % (PLAN.replace(os.sep, "/"), exc)]
    rows, problems = [], []
    inside = False
    for number, line in enumerate(lines, 1):
        text = line.strip()
        if not text.startswith("|"):
            continue
        cells = [c.replace("\\|", "|").strip() for c in re.split(r"(?<!\\)\|", text.strip("|"))]
        if cells == PLAN_HEADER:
            inside = True
        elif inside and not all(set(c) <= set("-: ") for c in cells):
            if len(cells) != len(PLAN_HEADER):
                problems.append("line %d: the row has %d cells, expected %d" % (number, len(cells), len(PLAN_HEADER)))
                continue
            row = dict(zip(PLAN_HEADER, cells))
            where = "row %s" % (row["Id"] or "on line %d" % number)
            if row["Kind"] not in KINDS:
                problems.append("%s: Kind must be one of: %s" % (where, ", ".join(KINDS)))
            for column in ("Item or code", "What will change", "Files", "What could break"):
                if not re.search(r"[^\W_]", row[column]) or row[column].startswith("<"):
                    problems.append("%s: '%s' is empty" % (where, column))
            if not row["Status"]:
                problems.append("%s: Status is empty. Run: python scripts/improve.py release" % where)
            elif not STATUS.match(row["Status"]):
                problems.append("%s: Status must be one of: to do, done, question, answered, "
                                "'skipped: <why>'" % where)
            elif row["Kind"] in KINDS and (row["Kind"] == PERSON_KIND) != (status_of(row) in ("question", "answered")):
                problems.append("%s: a '%s' row is a question or answered; every other row is to do, done or "
                                "skipped" % (where, PERSON_KIND))
            rows.append(row)
    if not inside:
        problems.append("no table with the header | %s |" % " | ".join(PLAN_HEADER))
    return rows, problems


def status_of(row):
    """'to do', 'done', 'question', 'answered' or 'skipped'; '' when the cell holds anything else."""
    m = STATUS.match(row["Status"])
    return m.group(1).split(":")[0].lower() if m else ""


def with_status(rows, kind, *wanted):
    return [r for r in rows if r["Kind"] == kind and status_of(r) in wanted]


# ---------------------------------------------------------------- the first status

def _model_text(root):
    """(file, text) of every TMDL file of the models under root."""
    for model in cp.find_models(root):
        for folder, _, files in os.walk(os.path.join(model, "definition")):
            for name in sorted(files):
                if name.lower().endswith(".tmdl"):
                    try:
                        with open(os.path.join(folder, name), encoding="utf-8-sig") as fh:
                            yield os.path.join(folder, name), fh.read()
                    except (OSError, UnicodeDecodeError):
                        continue


def has_measures_table(root):
    name = re.compile(r"(?m)^table\s+'?%s'?\s*$" % re.escape(cp.MEASURE_TABLE))
    return any(name.search(text) for _, text in _model_text(root))


def made_measures_table(root):
    """True when a file that defines the table _Measures was added since 'start'; None when that cannot be told."""
    code, base = git(root, "config", "--get", "improve.base")
    if code != 0 or not base:
        return None
    code, out = git(root, "diff", "--name-only", "--diff-filter=A", "--relative", base, "HEAD")
    if code != 0:
        return None
    name = re.compile(r"(?m)^table\s+'?%s'?\s*$" % re.escape(cp.MEASURE_TABLE))
    for line in out.splitlines():
        path = os.path.join(root, line.strip().strip('"'))
        if path.lower().endswith(".tmdl"):
            try:
                with open(path, encoding="utf-8-sig") as fh:
                    if name.search(fh.read()):
                        return True
            except (OSError, UnicodeDecodeError):
                continue
    return False


def first_status(kind):
    """The status a row starts with: 'question' for a row that needs a person, 'to do' for every other row."""
    return "question" if kind == PERSON_KIND else "to do"


def _write_statuses(path, statuses):
    """Write {row id: status} into the Status cell of those rows; every other character of the file stays."""
    with open(path, encoding="utf-8-sig") as fh:
        lines = fh.read().split("\n")
    for index, line in enumerate(lines):
        cells = re.split(r"(?<!\\)\|", line.strip().strip("|"))
        if line.strip().startswith("|") and len(cells) == len(PLAN_HEADER) and cells[0].strip() in statuses:
            lines[index] = re.sub(r"\|[^|]*\|\s*$", "| %s |" % statuses[cells[0].strip()], line.rstrip())
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines))


def review_problems(path):
    """Error lines of an unfinished review table; [] when it has all 79 rows with a status and evidence."""
    findings = cp.Findings()
    cp.check_review(path, findings)
    return ["%s  %s" % (f[0], f[3]) for f in findings.errors()]


# ---------------------------------------------------------------- commands

def start(root):
    code, out = git(root, "rev-parse", "--is-inside-work-tree")
    if code != 0:
        print("Stopped: %s is not a Git repository, so the original cannot be kept on a branch." % root)
        return 1
    code, out = git(root, "status", "--porcelain", "--untracked-files=all")
    if code != 0 or out:
        print("Stopped: not everything is committed. Commit these yourself (git add -A, then git commit -m \"Before improve: the report as found\"), then run this again:")
        print(out)
        return 1
    parts = project_parts(root)
    if not parts:
        print("Stopped: no .pbip file, .Report or .SemanticModel folder directly under %s." % root)
        return 1
    _, old_branch = git(root, "rev-parse", "--abbrev-ref", "HEAD")
    code, commit = git(root, "rev-parse", "HEAD")
    if code != 0 or old_branch == "HEAD":
        print("Stopped: no branch is checked out (or there is no commit yet), so no branch would keep the original. "
              "Check out a branch first.")
        return 1
    if old_branch.startswith(BRANCH_PREFIX):
        print("Stopped: this is already a flow branch (%s). Finish that flow (python scripts/improve.py next), "
              "or go back to your own branch before starting a new one." % old_branch)
        return 1
    left = [name.replace(os.sep, "/") for name in (PLAN, REVIEW_BEFORE, cp.BEFORE_COPY) if os.path.exists(os.path.join(root, name))]
    if left:
        print("Stopped: an earlier flow left %s. They would be taken for this flow's plan and 'before'. "
              "Remove them (Git keeps the committed ones in its history), commit, then run this again."
              % ", ".join(left))
        return 1
    name = BRANCH_PREFIX + datetime.date.today().isoformat()
    number = 1
    while git(root, "rev-parse", "--verify", "--quiet", "refs/heads/" + name)[0] == 0:
        number += 1
        name = "%s%s-%d" % (BRANCH_PREFIX, datetime.date.today().isoformat(), number)
    code, out = git(root, "checkout", "-b", name)
    if code != 0:
        print("Stopped: could not make the branch %s: %s" % (name, out))
        return 1
    git(root, "config", "improve.base", commit)
    print("New branch: %s. The original stays untouched on %s (commit %s)." % (name, old_branch, commit[:7]))

    target = os.path.join(root, cp.BEFORE_COPY)
    longest = max((len(os.path.join(target, os.path.relpath(os.path.join(folder, f), root)))
                   for part in parts for folder, _, files in os.walk(os.path.join(root, part)) for f in files),
                  default=0)
    if git(root, "check-ignore", "-q", cp.BEFORE_COPY + "/x")[0] != 0:
        print("No second copy: Git does not ignore %s/, and a committed copy would repeat each logicalId. "
              "Add '%s/' to .gitignore if you want the copy. The branch is the safeguard." % (cp.BEFORE_COPY, cp.BEFORE_COPY))
    elif longest >= PATH_LIMIT:
        print("No second copy: a path in it would be %d characters long (the limit is %d). The branch is the safeguard."
              % (longest, PATH_LIMIT))
    else:
        try:
            os.mkdir(target)
            for part in parts:
                source = os.path.join(root, part)
                if os.path.isdir(source):
                    shutil.copytree(source, os.path.join(target, part), symlinks=True)
                else:
                    shutil.copy2(source, os.path.join(target, part))
        except (OSError, shutil.Error) as exc:
            shutil.rmtree(target, ignore_errors=True)            # never leave half a copy that looks like 'before'
            print("No second copy: copying failed (%s). The branch is the safeguard." % str(exc)[:300])
            return 0
        print("Second copy: %s/ holds the project as it was (%s). Open its .pbip file to see 'before'. "
              "Git ignores the folder and the checks skip it. Do not edit it." % (cp.BEFORE_COPY, ", ".join(parts)))
    return 0


def snapshot(root):
    source, target = os.path.join(root, REVIEW), os.path.join(root, REVIEW_BEFORE)
    if not os.path.isfile(source):
        print("Stopped: %s does not exist yet. Evaluate first (skill pbi-checklist-review)." % REVIEW.replace(os.sep, "/"))
        return 1
    if review_problems(source):
        print("Stopped: the review is not finished. Run: python scripts/check_project.py --review docs/checklist-review.md")
        return 1
    if os.path.isfile(target):
        print("Stopped: %s is already there. It is the 'before' of this flow and is not replaced."
              % REVIEW_BEFORE.replace(os.sep, "/"))
        return 1
    shutil.copyfile(source, target)
    print("Kept the first review as %s." % REVIEW_BEFORE.replace(os.sep, "/"))
    return 0


def plan(root):
    target = os.path.join(root, PLAN)
    if os.path.isfile(target):
        print("Stopped: %s is already there. Change it by hand, or remove it to start again." % PLAN.replace(os.sep, "/"))
        return 1
    review = read_review(os.path.join(root, REVIEW))
    if review is None:
        print("Stopped: %s does not exist yet. Evaluate first (skill pbi-checklist-review)." % REVIEW.replace(os.sep, "/"))
        return 1
    if review_problems(os.path.join(root, REVIEW)):
        print("Stopped: the review is not finished. Run: python scripts/check_project.py --review docs/checklist-review.md")
        return 1
    findings, _, _ = cp.run(root)
    tables = (("Theme", THEME), ("Mechanical", MECHANICAL), ("Layout", LAYOUT), ("Measures", MEASURES),
              ("Renames", RENAMES), ("Data", DATA))
    rows, notes = [], []
    for code, path, line, message, level in findings.items:
        rel = os.path.relpath(path, root).replace(os.sep, "/") if path else "-"
        if level == "note":
            notes.append("- %s  %s  %s" % (code, rel, message))
            continue
        for kind, table in tables:
            if code in table:
                rows.append((kind, code, message, table[code][0], rel, table[code][1],
                             first_status(kind)))
                break
        else:
            rows.append((PERSON_KIND, code, message, PERSON.get(code, "Say what should happen here"), rel,
                         "Depends on the answer", "question"))
    for item in sorted(review):
        status, evidence = review[item]
        if status == "Fail":
            if item in PERSON_ITEMS:
                rows.append((PERSON_KIND, "Item %d" % item, evidence, "<what will change>", "<files>",
                             "<what could break>", "question"))
            else:
                rows.append(("?", "Item %d" % item, evidence, "<what will change>", "<files>", "<what could break>", ""))
    order = {kind: index for index, kind in enumerate(KINDS + ("?",))}
    rows.sort(key=lambda row: order[row[0]])
    lines = ["# Fix plan", "",
             "Made on %s by `python scripts/improve.py plan` from the checklist review and the project check. "
             "Rules: skill `pbi-improve`." % datetime.date.today().isoformat(), "",
             "Kinds, in the order they are applied: %s. A `?` or a `<...>` cell is still to be filled in. "
             "Status: `to do`, `done`, `skipped: <why>`; for a row that needs a person `question` or `answered`. "
             "No row waits for an approval: every `to do` row is done, and the questions are listed once, at the end."
             % ", ".join(KINDS), "",
             "| %s |" % " | ".join(PLAN_HEADER), "|%s|" % "|".join("---" for _ in PLAN_HEADER)]
    for number, (kind, source, what, change, files, risk, status) in enumerate(rows, 1):
        lines.append("| F%d | %s | %s | %s | %s | %s | %s | %s |"
                     % (number, kind, source, _cell(what)[:300], _cell(change), _cell(files), _cell(risk), _cell(status)))
    lines += ["", "## For information", "",
              "Notes from the project check. They are not errors and are never fix rows.", ""] + (notes or ["- none"])
    os.makedirs(os.path.dirname(target), exist_ok=True)
    with open(target, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    print("Wrote %s with %d row(s). Give every '?' row a kind, fill in the '<...>' cells, then run: "
          "python scripts/improve.py release" % (PLAN.replace(os.sep, "/"), len(rows)))
    return 0


def release(root):
    """Give every row that has no status its first status."""
    path = os.path.join(root, PLAN)
    rows, problems = read_plan(path)
    if not rows:
        print("Stopped: %s has no rows. Write it first: python scripts/improve.py plan" % PLAN.replace(os.sep, "/"))
        return 1
    unsorted = [r["Id"] for r in rows if r["Kind"] not in KINDS]
    if unsorted:
        print("Stopped: give these rows one of the kinds first (%s): %s" % (", ".join(KINDS), ", ".join(unsorted)))
        return 1
    changes = {}
    for row in rows:
        if not row["Status"]:
            changes[row["Id"]] = first_status(row["Kind"])
    if changes:
        _write_statuses(path, changes)
    freed = sum(1 for new in changes.values() if new == "to do")
    print("Statuses written: %d. Rows to do now: %d of them." % (len(changes), freed))
    return 0


def check_plan(root):
    rows, problems = read_plan(os.path.join(root, PLAN))
    for line in problems:
        print("X  %s" % line)
    for kind in KINDS:
        of_kind = [r for r in rows if r["Kind"] == kind]
        if kind == PERSON_KIND:
            print("%s: %d row(s), %d still a question." % (kind, len(of_kind), len(with_status(rows, kind, "question"))))
        else:
            print("%s: %d row(s): %d to do, %d done, %d skipped."
                  % (kind, len(of_kind), len(with_status(rows, kind, "to do")), len(with_status(rows, kind, "done")),
                     len(with_status(rows, kind, "skipped"))))
    print("Fix plan: %d problem(s)." % len(problems))
    return 1 if problems else 0


def changed_pages(root):
    """Tab names of the pages whose files changed since 'start', or None when that cannot be told."""
    code, base = git(root, "config", "--get", "improve.base")
    if code != 0 or not base:
        return None
    code, out = git(root, "diff", "--name-only", "--relative", base, "HEAD")        # paths as seen from <folder>
    if code != 0:
        return None
    pages = []
    for name in out.splitlines():
        m = re.match(r"(.+\.Report/definition/pages/[^/]+)/", name.strip().strip('"'))
        if m:
            page = cp.load_object(os.path.join(root, m.group(1), "page.json")) or {}
            tab = page.get("displayName") if isinstance(page.get("displayName"), str) else os.path.basename(m.group(1))
            if tab not in pages:
                pages.append(tab)
    return pages


def compare(root):
    before = read_review(os.path.join(root, REVIEW_BEFORE))
    after = read_review(os.path.join(root, REVIEW))
    if before is None or after is None:
        print("Stopped: both %s and %s are needed." % (REVIEW_BEFORE.replace(os.sep, "/"), REVIEW.replace(os.sep, "/")))
        return 1
    for name in (REVIEW_BEFORE, REVIEW):
        if review_problems(os.path.join(root, name)):
            print("Stopped: %s is not a finished review, so its counts would be wrong. Run: "
                  "python scripts/check_project.py --review %s" % (name.replace(os.sep, "/"), name.replace(os.sep, "/")))
            return 1
    print("            Pass  Fail  Not applicable")
    print("Before      %4d  %4d  %4d" % counts(before))
    print("After       %4d  %4d  %4d" % counts(after))
    moved = [(item, before[item][0], after[item][0]) for item in sorted(after)
             if item in before and before[item][0] != after[item][0]]
    print("Items that changed: %s" % ("none" if not moved else ""))
    for item, old, new in moved:
        print("  Item %d: %s -> %s" % (item, old, new))
    pages = changed_pages(root)
    if pages is None:
        print("Pages to look at in Power BI Desktop: every page a fix touched (the start of this flow was not recorded).")
    else:
        print("Pages to look at in Power BI Desktop: %s" % (", ".join(pages) if pages else "none changed"))
    fails = [item for item in sorted(after) if after[item][0] == "Fail"]
    person = [item for item in fails if item in PERSON_ITEMS]
    other = [item for item in fails if item not in PERSON_ITEMS]
    print("Still Fail: %d item(s)." % len(fails))
    print("  %d can pass only on a fact from a person%s" % (len(person), _items(person)))
    print("  %d wait on a skipped fix or on an answer about the files%s" % (len(other), _items(other)))
    rows, _ = read_plan(os.path.join(root, PLAN))
    for kind in AUTO_KINDS:
        of_kind = [r for r in rows if r["Kind"] == kind]
        if of_kind:
            print("%s: %d done, %d skipped, %d to do."
                  % (kind, len(with_status(rows, kind, "done")), len(with_status(rows, kind, "skipped")),
                     len(with_status(rows, kind, "to do"))))
    if with_status(rows, "Data", "done") or made_measures_table(root):
        print("Refresh the model once in Power BI Desktop: this run changed a query, a partition, a data type or "
              "added a table, and such a table is empty until it is loaded again.")
    if with_status(rows, "Measures", "done") or with_status(rows, "Renames", "done"):
        print("Measures moved or names changed: a report that reads a published copy of this model names them the "
              "old way and may break. No file here can show such a report.")
    skipped = [r for r in rows if status_of(r) == "skipped"]
    print("Skipped: %d row(s)%s" % (len(skipped), ":" if skipped else "."))
    for row in skipped:
        print("  %s  %s  %s" % (row["Id"], row["Item or code"], row["Status"].split(":", 1)[1].strip()))
    people = with_status(rows, PERSON_KIND, "question")
    print("Questions for a person: %d row(s)%s" % (len(people), ":" if people else "."))
    for (source, change), group in _grouped(people, lambda r: (r["Item or code"], r["What will change"])):
        print("  %s  %s%s (%s)" % (source, change, "" if len(group) == 1 else "  [%d rows]" % len(group), _ids(group)))
    return 0


def _items(items):
    return " (items %s)." % ", ".join(str(item) for item in items) if items else "."


def _ids(rows):
    ids = [r["Id"] for r in rows]
    return ", ".join(ids) if len(ids) <= 6 else "%s ... %s" % (", ".join(ids[:3]), ids[-1])


def _grouped(rows, key):
    """[(key, rows)] in the order the keys first appear: twenty rows that ask the same thing print as one line."""
    groups = {}
    for row in rows:
        groups.setdefault(key(row), []).append(row)
    return list(groups.items())


def _has_commit(root, subject):
    code, base = git(root, "config", "--get", "improve.base")
    span = "%s..HEAD" % base if code == 0 and base else "HEAD"
    code, out = git(root, "log", "--format=%s", span)
    return code == 0 and subject in out.splitlines()


def next_step(root):
    def say(step, text):
        print("Step %s. %s" % (step, text))
        return 0

    code, branch = git(root, "rev-parse", "--abbrev-ref", "HEAD")
    if code != 0:
        return say(23, "This folder is not a Git repository. The flow needs one: the original stays on a branch.")
    if not branch.startswith(BRANCH_PREFIX):
        return say(23, "Safety first. The project must be saved and closed in Power BI Desktop. If anything is not committed, commit "
                       "it yourself, without asking: git add -A, then git commit -m \"Before improve: the report as found\". "
                       "Then run: python scripts/improve.py start")
    exists = {name: os.path.isfile(os.path.join(root, name)) for name in (REVIEW, REVIEW_BEFORE, PLAN)}
    if not exists[REVIEW_BEFORE]:
        if not exists[REVIEW]:
            return say(24, "Evaluate with the skill pbi-checklist-review. It writes docs/checklist-review.md.")
        return say(24, "Keep the review as the 'before': python scripts/improve.py snapshot")
    if not exists[PLAN]:
        return say(25, "Write the fix plan: python scripts/improve.py plan. Then give the '?' rows a kind and fill in the '<...>' cells.")
    rows, problems = read_plan(os.path.join(root, PLAN))
    if any(not r["Status"] for r in rows) and all(r["Kind"] in KINDS for r in rows):
        return say(25, "Give the new rows their status: python scripts/improve.py release")
    if problems:
        return say(25, "Finish the fix plan (%d problem(s)): python scripts/improve.py check-plan" % len(problems))
    for kind in AUTO_KINDS:
        todo = with_status(rows, kind, "to do")
        if todo:
            return say(27, "Apply the %d %s row(s) marked 'to do': no approval is needed. As each row is finished write "
                           "'done' in its Status, or 'skipped: <why>' when it cannot be done. Run python scripts/"
                           "check_project.py . and fix what it reports. Then commit with the message '%s'."
                           % (len(todo), kind, COMMITS[kind]))
        if with_status(rows, kind, "done") and not _has_commit(root, COMMITS[kind]):
            return say(27, "Commit the %s fixes with the message '%s'." % (kind, COMMITS[kind]))
    before = read_review(os.path.join(root, REVIEW_BEFORE))
    after = read_review(os.path.join(root, REVIEW)) if exists[REVIEW] else None
    with_fixes = any(_has_commit(root, subject) for subject in COMMITS.values())
    same = False
    if exists[REVIEW]:
        with open(os.path.join(root, REVIEW), "rb") as one, open(os.path.join(root, REVIEW_BEFORE), "rb") as two:
            same = one.read() == two.read()
    if after is None or (same and with_fixes) or review_problems(os.path.join(root, REVIEW)):
        return say(28, "Evaluate again with the skill pbi-checklist-review: go through all 79 items in order, not only "
                       "the rows you expect to change. docs/checklist-review.md is replaced without asking; the first "
                       "review is kept as docs/checklist-review-before.md.")
    return say("28 and 29", "Show the result: python scripts/improve.py compare. Then give the developer one final "
                            "answer: what changed, the pages to look at in Power BI Desktop, what was skipped, and the "
                            "questions. Do not merge, publish or deploy.")


def main(argv):
    cp.safe_output()
    commands = {"next": next_step, "start": start, "snapshot": snapshot, "plan": plan, "check-plan": check_plan,
                "release": release, "compare": compare}
    args = argv[1:]
    if not args or args[0] not in commands or len(args) > 2:
        print(__doc__)
        return 2
    root = os.path.abspath(args[1] if len(args) == 2 else ".")
    if not os.path.isdir(root):
        print("Not a folder: %s" % args[1])
        return 2
    return commands[args[0]](root)


if __name__ == "__main__":
    sys.exit(main(sys.argv))
