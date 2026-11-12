#!/usr/bin/env python3
"""Machine checks for a Power BI project (PBIP: TMDL model + PBIR report).

Usage:
    python scripts/check_project.py <folder>            check every project found under <folder>
    python scripts/check_project.py --review <file>     check a finished 79-item review table

Needs Python 3.8 or later. Uses the standard library only. Reads files; never changes them.
Exit code: 0 = no errors, 1 = at least one error, 2 = wrong usage or nothing to check.

Finding codes (errors unless marked warn or note; only errors change the exit code):
    D001  visible table, column or measure has no '///' description
    D002  shared Power Query query or parameter ('expression') has no '///' description
    D003  '///' description is not directly above an object
    I001  (note) description still holds the placeholder TODO(owner)
    C001  '//' comment outside a Power Query (M) or DAX expression block
    P001  Power Query step has no '//' (or '/* */') description line directly above it (template convention)
    F001  a .Report or .SemanticModel folder is not in PBIR / TMDL format (no 'definition' folder)
    F002  a page folder has no page.json, or a visual folder has no visual.json
    F003  a model's 'definition' folder holds no .tmdl file
    J001  a project JSON file is not valid JSON or starts with a byte-order mark; or a .tmdl file is not UTF-8
    J002  a project JSON file does not have the structure Power BI expects
    J003  a project JSON file does not fit the Microsoft schema its '$schema' line names (scripts/json_schema.py)
    J004  (note) a project JSON file names a schema version that scripts/schemas holds no copy of: not checked
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

  Model standard (.github/skills/pbi-semantic-model/references/model-standard.md):
    M001  measure outside the table _Measures
    M002  the table _Measures is hidden, or does not have exactly one column, hidden
    M003  measure has no display folder, or not one folder with exactly two levels, Subject\\Type
    M004  a display folder level of a measure is not on its list
    M005  two measures share a name
    M006  measure has the name of a column in the model
    M007  measure name is code-style (underscores, CamelCase, ALL CAPS) or has a space at either end
    M008  (warn) measure name: Title Case, period spelling, unit, '#', 'vs', order; or folder type against name
    M009  visible measure has no format string
    M010  (warn) DAX names a column without its table, or a measure with its table
    M101  (warn) table with 20 or more visible fields has columns outside the four column folders
    M102  (warn) visible foreign key or sort-by key
    M103  (warn) visible numeric column that a measure already totals
    M104  (warn) hidden column used by a hierarchy or a report visual
    M105  calculated column or calculated table has no CalculatedReason annotation
    M106  (warn) more than five calculated columns, or a calculated column that uses RELATED
    M107  visible numeric column whose summarizeBy is not none
    M108  (warn) column has the floating-point type (double)
    M109  the two columns of a relationship have different data types
    M110  (warn) relationship column is not a whole number
    M111  (warn) column may hold a date and a time together
    M112  (warn) visible date or numeric column has no format string
    M201  (note) hidden column or measure that nothing refers to
    M301  (note) hidden columns whose isAvailableInMdx could be turned off (only when the brief turns this on)
    M302  (note) description longer than 200 characters (only when the brief turns this on)
    M303  (note) dimension table with no column marked isDefaultLabel (only when the brief turns this on)

  Layout standard (.github/skills/pbi-report/references/layout-standard.md):
    G001  visual reaches outside the page
    G002  two data visuals overlap
    G003  (warn) x, y, width or height is not on the grid
    G004  (warn) outer margins differ from the margin
    G005  (warn) visuals of the same kind in one row have different heights
    G006  (warn) gap between neighbours differs from the gap
    G007  (warn) page size differs from the brief or the standard
    G008  (note) position not checked: a rotated visual, or visuals inside a group

  Relationships, dates and names (.github/skills/pbi-semantic-model/references/relationships-and-dates.md):
    M113  (warn) text column that looks like a month name has no sort column
    M114  (warn) column that looks like a place has no data category
    M115  (warn) column repeated in the related table
    M116  (warn) flag column shown as a number
    M117  (warn) the one partition of a table is not named after the table
    M118  (warn) visible table, column or hierarchy name: capital, underscores, words run together, technical prefix
    M119  (warn) column and hierarchy of one table share a name
    M120  (warn) table that shows more than 30 columns
    M401  (warn) Auto date/time is on
    M402  time intelligence is used and no table is marked as a date table
    M403  (warn) date columns, and no table marked as a date table
    M404  (warn) table that looks like a date table is not marked as one
    M405  (warn) relationship filters in both directions
    M406  (warn) many-to-many relationship
    M407  (warn) many-to-many relationship that filters in both directions
    M408  (warn) more than 30% of the relationships are both-direction or many-to-many
    M409  (warn) one-to-one relationship
    M410  (warn) inactive relationship that no formula turns on
    M411  (warn) table with no relationship
    M412  (warn) snowflake: a table is the many side of one relationship and the one side of another
    M413  (warn) one-side column of a relationship is not marked as the key
    M414  (warn) security roles in a model with inactive relationships
    M415  USERELATIONSHIP towards a table that has a row-level security rule
    M416  (note) relationship key column that allows blanks (no isNullable: false)
    M417  (warn) a number column for each month: unpivot
    M901  relationship names a table or column the model does not have
    M902  hierarchy level on a column the table does not have
    M903  sort column the table does not have
    M904  data column without sourceColumn
    M905  measure, calculated column or calculation item with an empty expression
    M906  control character, other than white space, in a name or a description
    M907  isAvailableInMdx off on a column used for sorting or in a hierarchy

  DAX (.github/skills/pbi-semantic-model/references/dax-standard.md):
    M501  (warn) IFERROR or ISERROR
    M502  division with '/' by something that is not a fixed number: use DIVIDE
    M503  (warn) COUNT or COUNTA of a column where COUNTROWS says what is meant
    M504  (warn) HASONEVALUE with VALUES: use SELECTEDVALUE
    M505  (warn) FILTER over a whole table as a filter argument of CALCULATE
    M506  (warn) a blank turned into a value
    M507  (warn) the same expression written twice: use a variable
    M508  (warn) two measures with the same formula
    M509  (warn) a measure that only repeats another measure
    M510  (warn) INTERSECT where TREATAS is meant
    M511  (warn) a number plus or minus a ratio (1 - x / y)
    M512  (warn) EVALUATEANDLOG left in a formula
    M513  (warn) time intelligence in a model with DirectQuery tables
    M514  (warn) EARLIER or EARLIEST: use a variable
    M516  (warn) window function without ORDERBY
    M517  (warn) VALUES compared with one value
    M518  (warn) DIVIDE by a fixed number: use '/'
    M519  (warn) ALL as a filter argument of CALCULATE where REMOVEFILTERS is meant
    M520  (warn) formulas that do not follow the DAX style (one finding for each table file)
    M521  (warn) CALCULATE written directly inside CALCULATE
    M522  (warn) SUMMARIZE that adds a new column
    M523  (note) SUMMARIZECOLUMNS with a filter argument inside a measure
    M524  (warn) USERCULTURE in an imported calculated column or calculated table
    M525  (warn) SWITCH over USERCULTURE with no default value, or naming a culture that has no culture file
    M908  DAX names a Table[Column] the model does not have
    M909  (warn) DAX calls a function that is not in the DAX function index

  Power Query, storage modes and security (.github/skills/pbi-semantic-model/references/storage-and-security.md):
    P002  (warn) native query built by joining text
    P003  (warn) one shared query feeds two or more tables
    P004  (warn) Dataverse query without its options
    P005  (warn) query reads a file from a local drive
    P006  (warn) heavy reshaping in Power Query
    P007  (warn) loaded table that only feeds other queries
    M601  (warn) row-level security rule uses text or lookup functions
    M602  (warn) row-level security rule on a fact table
    M603  (warn) row-level security rule uses USERNAME
    M604  (warn) row-level security rule next to a many-to-many relationship
    M605  (warn) user-based rule that ends in TRUE for everyone else
    M606  (warn) object-level security hides a field that a report visual uses
    M607  (warn) row rules and object rules in different roles
    M608  object-level security on a table in the middle of a chain of relationships
    M609  (warn) relationship that applies the security filter in both directions
    M701  DirectQuery native query with a common table expression or a stored procedure
    M702  (warn) DirectQuery table with transformation steps in Power Query
    M703  (warn) DirectQuery table filtered on the current date in Power Query
    M704  (warn) calculated column of a DirectQuery table used in a relationship
    M705  calculated column of a DirectQuery table that uses CALCULATE or an iterator
    M706  (warn) imported dimension of a DirectQuery fact: consider Dual
    M707  incremental refresh without the parameters RangeStart and RangeEnd, or not of type Date/Time
    M708  (warn) incremental refresh on a native query
    M709  incremental refresh filter that includes both ends of the window
    M711  (warn) Direct Lake table with a Power Query partition
    M832  (warn) data source that no partition uses
    M833  legacy query partition on a structured data source
    M910  (warn) column of a calculated table whose sourceColumn the formula does not produce

  Model objects (.github/skills/pbi-semantic-model/references/model-objects.md):
    M801  user-defined function in a model below compatibility level 1702
    M802  user-defined function name breaks Microsoft's naming rules
    M803  (warn) user-defined function has no '///' description
    M804  (warn) user-defined function parameter has no type
    M805  user-defined function calls itself
    M806  (warn) user-defined function names an object that a role hides with object-level security
    M807  (warn) user-defined function or parameter name outside the naming style
    M811  (warn) calculation group with no items
    M812  (warn) calculation item has no '///' description
    M813  (warn) two or more calculation groups without their own precedence
    M814  (warn) calculation group in a model without discourageImplicitMeasures
    M815  (warn) detail rows expressions in a model with a calculation group
    M821  field parameter names a field the model does not have
    M822  (warn) field parameter not wired the way Power BI Desktop writes it
    M831  (warn) perspective with no objects
    M841  (warn) the model uses a preview feature that section 11 of the brief does not list (calendars, value
          filter behavior, user-context calculated columns, calculated tables over Direct Lake data)

  Report standard (.github/skills/pbi-report/references/report-standard.md):
    V001  drillthrough page without a back button
    V002  (warn) tooltip page that is not hidden
    V003  (warn) tooltip page much larger than the built-in tooltip size
    V004  (warn) slicer or button on a tooltip page
    V005  (warn) tooltip page with fewer than three fields
    V006  more than 16 visuals that show data on one page
    V007  (warn) 13 to 16 visuals that show data on one page
    V008  (warn) button whose action goes to a page or bookmark the report does not have
    V009  (warn) colour, font, size, border, shadow or background set on a single visual
    V010  (warn) bookmark that holds a page or visual the report no longer has
    V011  (warn) pages.json and the page folders disagree
    V012  (warn) report-level measure without the prefix
    V013  (warn) filter values left on a tooltip page or in a drillthrough filter
    V014  (warn) visible drillthrough page without a reset button
    V015  (warn) filter whose Where part uses a source its From part does not declare
    V016  (warn) visual type that Microsoft is retiring or has deprecated
    V017  (warn) image or other resource that is not registered or not in the report folder
    V018  (note) page with no text box for its title
    V019  (warn) report-level measure that calls USERCULTURE
    V020  (warn) typed text in a report on a model with translations (one finding for each report)
    V021  (warn) more than one page tab in a report on a model with translations
    V022  (warn) the report uses a preview feature that section 11 of the brief does not list (Gantt visual,
          format string on a visual)
    V023  (warn) cross-report drillthrough page in a report that does not switch the feature on
    V024  data bars without a bar colour: Power BI Desktop fails to load the report
    A001  (warn) visuals without alt text (one finding for each page)
    A002  (warn) visuals that share a tab order number
    A003  (warn) visuals that show a title made up from field names (one finding for each page)
    A004  (warn) alt text longer than 250 characters

  Suggestions: a native feature may do this better (.github/skills/pbi-checklist-review/references/native-features.md):
    U001  (note) three or more measures of one formula pattern: a user-defined function
    U002  (note) many time variants of measures: a calculation group
    U003  (note) a measure that switches between measures: a field parameter
    U004  (note) DirectQuery tables and no aggregation table
    U005  (note) a measure that returns formatted text: a dynamic format string
    U006  (note) two or more inactive relationships to one table: a role-playing dimension
    U007  (note) a natural drill path and no hierarchy
    U008  (note) relationship between two DirectQuery tables without Assume referential integrity
    U101  (note) the same slicer on two or more pages, not synced
    U102  (note) three or more page buttons on a page: a page navigator
    U103  (note) stacked visuals switched by bookmarks: a field parameter
    U104  (note) two or more slicers on a page of a DirectQuery model and no Apply button
    U105  (note) legacy card or multi-row card: the new card visual
    U106  (note) Top N filter or filter on a measure, on a model with DirectQuery tables

    B001  a report file uses a table, column or measure the model in this project does not have; for a report on
          a published model: one that the saved field list, docs/model-fields.md, does not have
    B002  (note) a report on a published model has no saved field list, so its fields are not checked

The M, G and B checks read their numbers, lists and exceptions from docs/report-brief.md under <folder>.
An exception counts only when its row there names the same code and object and gives a reason.
Formulas are read once, in six states, by scripts/formula_scanner.py (separate rules for DAX and Power Query).
It is a scanner, not a parser: it knows names, text, comments and brackets, not what a formula means.
Levels of the checks added in round 3: fail when Microsoft says it breaks something or gives wrong numbers, or
the checklist gives a hard number, and the files show it for certain; warn for every other rule; note (U) for a
suggestion. The checks are in scripts/model_rules.py and scripts/report_rules.py.

A visual may keep Header icons or Tooltips on only with a HeaderTooltipException annotation whose value
names what stays on and why: "header: <reason>", "tooltip: <reason>" or "both: <reason>".
The Power Query step check reads the outer 'let' of each query with the same scanner.
"""
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import formula_scanner as fs  # noqa: E402
import json_schema  # noqa: E402
import model_rules  # noqa: E402
import report_rules  # noqa: E402

NAME_OK = re.compile(r"[A-Za-z0-9_-]+\Z")           # Microsoft Learn: PBIR naming convention
NAME_MAX = 50                                        # Microsoft schemas: page 2.1.0, visualContainer 2.13.0
LABEL_ANNOTATION = "VisualLabel"                     # template convention
EXCEPTION_ANNOTATION = "HeaderTooltipException"      # template convention
EXCEPTION_SCOPES = {"header": ("visualHeader",), "tooltip": ("visualTooltip",),
                    "both": ("visualHeader", "visualTooltip")}
PLACEHOLDER = "TODO(owner)"                          # template convention
SCHEMA_PREFIX = "https://developer.microsoft.com/json-schemas/fabric/"
REVIEW_STATUSES = ("Pass", "Fail", "Not applicable")

# The model standard: .github/skills/pbi-semantic-model/references/model-standard.md
MEASURE_TABLE = "_Measures"                          # the table: Microsoft Learn, "Organize your measures"; the name: the owner's
FOLDER_SUBJECTS = ("Reliability", "Energy and Gas", "Customer", "Safety", "Finance", "Workforce",
                   "IT and Security", "Work Management")             # the eight business definition areas
FOLDER_TYPES = ("Base", "Time Intelligence", "Comparisons", "Ratios", "Counts")
COLUMN_FOLDERS = ("Attributes", "Keys", "Facts", "Hierarchy")
FOLDER_THRESHOLD = 20                                # checklist item 22
REASON_ANNOTATION = "CalculatedReason"               # template convention
CALCULATED_COLUMN_LIMIT = 5                          # Microsoft's best practice rule "Reduce number of calculated columns"
COPILOT_DESCRIPTION_LIMIT = 200                      # Microsoft Learn, "Use Copilot with semantic models"
NUMERIC_TYPES = ("int64", "decimal", "double")
AUTO_DATE_PREFIXES = ("LocalDateTable_", "DateTableTemplate_")       # tables Power BI makes for Auto date/time
SMALL_WORDS = frozenset(("a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "per", "the", "to",
                         "vs", "with"))
TOTAL_FUNCTIONS = ("SUM", "AVERAGE", "AVERAGEA", "COUNT", "COUNTA", "COUNTBLANK", "DISTINCTCOUNT", "MIN", "MINA",
                   "MAX", "MAXA", "VALUES", "DISTINCT")              # the list in "Hide fact table columns"
CODE_RE = re.compile(r"[A-Z][0-9]{3}\Z")

# The layout standard: .github/skills/pbi-report/references/layout-standard.md
PAGE_SIZE = (1280, 720)
LAYOUT_SETS = {1280: (24, 16), 1920: (32, 24)}       # page width -> (outer margin, gap between visuals)
GRID_STEP = 8
EPSILON = 0.01

# What the checks read from the brief. scripts/check_template.py fails if the brief loses one of these.
BRIEF = os.path.join("docs", "report-brief.md")
BRIEF_LABELS = {"page_size": "Page size in pixels, width x height",
                "margin": "Outer margin in pixels",
                "gap": "Gap between visuals in pixels",
                "grid": "Grid step in pixels",
                "subjects": "Measure folder subjects",
                "own_spelling": "Acronyms and words with their own spelling",
                "excel": "Excel check on",
                "copilot": "Power BI Copilot check on",
                "report_prefix": "Prefix for report-level measures"}
MODEL_EXCEPTIONS = "Exceptions to the model standard"
LAYOUT_EXCEPTIONS = "Exceptions to the layout standard"
PREVIEW_AGREED = "Preview features and optional tools"       # section 11 of the brief: one row for each yes
FIELD_LIST = os.path.join("docs", "model-fields.md")  # the saved field list of a published model (skill pbi-report)
BEFORE_COPY = "_before"                              # the untouched copy made by scripts/improve.py
ITEM_COUNT = 79
FAILED = object()                                    # returned by load_json when a file cannot be parsed

DESCRIBED_KINDS = ("table", "column", "measure")
DESCRIBED_PROPERTIES = ("multipleoremptyselectionexpression", "noselectionexpression", "datacoveragedefinition")
DECL_RE = re.compile(r"^([A-Za-z]+)\s+('(?:[^']|'')*'|[^\s=:]+)\s*(.*)$")
PROP_EQ_RE = re.compile(r"^([A-Za-z_]\w*)\s*=\s*(.*)$")
PROP_COLON_RE = re.compile(r"^([A-Za-z_]\w*)\s*:")
OBJECT_KEYWORDS = frozenset((
    "table", "column", "measure", "expression", "partition", "hierarchy", "level",
    "calculationgroup", "calculationitem", "function", "role", "tablepermission", "columnpermission",
    "relationship", "perspective", "perspectivetable", "perspectivecolumn", "perspectivemeasure",
    "perspectivehierarchy", "culture", "cultureinfo", "datasource", "model", "database",
    "annotation", "extendedproperty", "querygroup", "variation", "kpi", "calendar"))
# Objects written as one bare word, with their properties below (the spelling Microsoft's TMDL serializer writes).
NAMELESS_OBJECTS = frozenset(("calculationgroup", "kpi", "refreshpolicy", "alternateof", "relatedcolumndetails",
                              "translations"))
M_PROPERTIES = frozenset(("sourceexpression", "pollingexpression"))    # Power Query held by a refresh policy
VALUE_ONLY = frozenset(("annotation", "extendedproperty"))       # 'name = value' lines, not real objects
PLAIN_VALUE_KEYS = frozenset(("changedproperty",))               # 'key = value' where the value is not an expression
FREE_TEXT_KEYS = frozenset(("sourcecolumn", "formatstring", "displayfolder", "sortbycolumn",
                            "sourcelineagetag", "description", "displayname", "caption"))
HIDING_FLAGS = frozenset(("ishidden", "ishidden:true", "isprivate", "isprivate:true"))
BARE_FLAG_RE = re.compile(r"[A-Za-z_]\w*\Z")
QUOTED = re.compile(r"'(?:[^']|'')*'|\"(?:[^\"]|\"\")*\"")
EMPTY_EVIDENCE = frozenset(("todo", "tbd", "na", "n/a", "none", "nbsp", "br", "x", "evidence"))


def code_levels():
    """{code: 'fail', 'warn' or 'note'} for every finding code, read from the list at the top of this file."""
    levels = {}
    for code, mark in re.findall(r"^ {4}([A-Z][0-9]{3})  (\(warn\)|\(note\))?", __doc__, re.M):
        levels[code] = mark.strip("()") or "fail"
    return levels


class Findings:
    """Each item is (code, path, line, message, level): level is False for an error, else "warn" or "note"."""

    def __init__(self):
        self.items = []
        self.fixes = []       # (code, object key, property, value): changes a script may apply after approval

    def add(self, code, path, line, message, info=False, level=None):
        if level is None:
            level = "note" if info else "error"
        self.items.append((code, path, line, message, False if level == "error" else level))

    def errors(self):
        return [f for f in self.items if not f[4]]

    def warnings(self):
        return [f for f in self.items if f[4] == "warn"]

    def print_all(self, base):
        for code, path, line, message, level in self.items:
            rel = os.path.relpath(path, base) if path else "-"
            where = "%s:%d" % (rel, line) if line else rel
            print("%s  %s  %s%s" % (code, where.replace(os.sep, "/"), "(%s) " % level if level else "", message))


def safe_output():
    """Never stop on a character the console cannot show."""
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(errors="backslashreplace")


# ---------------------------------------------------------------- TMDL

def split_lines(text):
    """Lines of a file, split only at real line breaks. (str.splitlines also splits at characters such as
    U+2028, which can sit inside a text value and are not line breaks to Power BI.)"""
    lines = re.split(r"\r\n|\n|\r", text)
    return lines[:-1] if lines and lines[-1] == "" else lines


def _width(line):
    return len(line) - len(line.lstrip(" \t"))


def _unquote(name):
    if len(name) >= 2 and name[0] == "'" and name[-1] == "'":
        return name[1:-1].replace("''", "'")
    return name


def _property_text(value):
    """The text of a 'name: value' property: outer double quotes removed, as TMDL reads it."""
    value = value.strip()
    if len(value) >= 2 and value[0] == '"' and value[-1] == '"':
        return value[1:-1].replace('""', '"')
    return value


def _has_comment(text):
    """True when text holds '//' that is not '///', not inside quotes and not part of an address such as http://."""
    return re.search(r"(?<![:/])//(?!/)", QUOTED.sub("''", text)) is not None


def check_m_steps(block, path, owner, findings):
    """block: list of (line_number, text) of one Power Query expression.

    The formula scanner finds the steps of the query's outer 'let'. A step with no comment line directly
    above it is reported.
    """
    steps, found = fs.m_steps("\n".join(text for _, text in block))
    if not found:
        return
    for step in steps:
        number = block[min(step["line"], len(block)) - 1][0]
        if step["on_let_line"]:
            findings.add("P001", path, number,
                         "Power Query step %s in %s starts on the 'let' line; put it on its own line with a '//' description above"
                         % (step["name"], owner))
        elif not step["described"]:
            findings.add("P001", path, number,
                         "Power Query step %s in %s has no '//' description line directly above it" % (step["name"], owner))


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
        lines = split_lines(raw.decode("utf-8-sig"))
    except UnicodeDecodeError:
        findings.add("J001", path, 0, "file is not UTF-8 text, so it cannot be checked; save it as UTF-8 without BOM")
        return
    return check_tmdl_lines(path, lines, findings)


def check_tmdl_lines(path, lines, findings):
    """The file checks on the lines of one .tmdl file. Returns the objects declared in it."""
    uses_tabs = any(line.startswith("\t") for line in lines)

    objects = []          # dicts: kind, name, line, described, hidden, table, top, placeholder
    stack = []            # (indent width, object) for the objects the current line sits inside
    pending = []          # (line_number, text) of '///' lines waiting for their object
    block = None          # the expression block being read
    partition_is_m = False
    translations = False  # inside a cultureInfo file: names there are translations, not model objects

    def close_block(end=None):
        """end: line number of a closing fence; None when the block ends at its last line of text."""
        nonlocal block
        if block and block["is_m"]:
            check_m_steps(block["lines"], path, block["owner"], findings)
        if block:
            written = [n for n, t in block["lines"] if t.strip()]
            last = end or (written[-1] if written else block["start"])
            text = "\n".join(t for _, t in block["lines"])
            kind, target, key = block["target"]
            if kind == "object":
                target["expr"] = text
                target["expr_end"] = last
            elif kind == "property" and target is not None:
                target["props"][key] = text
            elif kind == "annotation" and target is not None:
                target["annotations"][key] = text
            for owner_object in block["owners"]:
                owner_object["last_line"] = max(owner_object["last_line"], last)
        block = None

    def comment(number):
        findings.add("C001", path, number, "'//' comment outside a Power Query or DAX expression block")

    for number, line in enumerate(lines, 1):
        stripped = line.strip()

        if block is not None:
            if block["fenced"]:
                if stripped == "```":
                    close_block(number)
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
        for _, enclosing in stack:
            enclosing["last_line"] = number
        parent = stack[-1][1] if stack else None
        target = ("none", None, "")

        decl = DECL_RE.match(stripped)
        keyword = decl.group(1).lower() if decl else ""
        is_object = bool(decl) and keyword in OBJECT_KEYWORDS
        nameless = stripped.lower() in NAMELESS_OBJECTS
        if nameless:
            keyword = stripped.lower()
            is_object = True
        opens_block = False
        fenced = False
        is_m = False
        owner = ""
        steps_deeper = 1      # tab levels between this line and the first line of its expression

        if is_object:
            raw_name = "" if nameless else decl.group(2)
            rest = "" if nameless else decl.group(3).strip()
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
                if keyword == "annotation" and parent is None:
                    # model.tmdl writes the model's own annotations at the left margin, below the model's properties
                    parent = next((o for o in objects if o["kind"] == "model" and o["top"] and not o["translation"]), None)
                if keyword == "annotation" and parent is not None:
                    parent["annotations"][name] = tail or ""
                    parent["annotation_lines"][name] = number
                    target = ("annotation", parent, name)
                elif keyword == "extendedproperty" and parent is not None:
                    parent.setdefault("extended", {})[name] = tail or ""
            else:
                if keyword == "cultureinfo":
                    translations = True
                table = None
                for _, enclosing in stack:
                    if enclosing["kind"] == "table":
                        table = enclosing
                obj = {"kind": keyword, "name": name, "line": number, "described": bool(description),
                       "hidden": False, "table": table, "top": not stack, "translation": translations,
                       "placeholder": PLACEHOLDER.lower() in description.lower(),
                       "file": path, "parent": parent, "description": description, "props": {}, "prop_lines": {},
                       "annotations": {}, "annotation_lines": {}, "expr": tail if tail not in (None, "", "```") else None,
                       "has_expr": tail is not None, "expr_end": number, "last_line": number,
                       "indent": line[:len(line) - len(line.lstrip(" \t"))]}
                objects.append(obj)
                stack.append((width, obj))
                target = ("object", obj, "")
                if keyword == "partition":
                    partition_is_m = (tail or "").split("//")[0].strip().lower() == "m"
                is_m = keyword == "expression"
                owner = "query '%s'" % name
                steps_deeper = 2
        else:
            prop = PROP_EQ_RE.match(stripped)
            colon = PROP_COLON_RE.match(stripped)
            if had_pending and prop and prop.group(1).lower() in DESCRIBED_PROPERTIES:
                pass                                  # child objects that Microsoft's serializer writes with a description
            elif had_pending and (prop or colon or stripped.replace(" ", "").lower() in HIDING_FLAGS):
                findings.add("D003", path, pending_line, "'///' description is not directly above an object")
            if prop:
                key = prop.group(1).lower()
                tail = prop.group(2).strip()
                if parent is not None:
                    parent["props"][key] = tail
                    parent["prop_lines"][key] = number
                    target = ("property", parent, key)
                if tail == "":
                    opens_block = True
                elif tail == "```":
                    opens_block = True
                    fenced = True
                elif key in PLAIN_VALUE_KEYS and _has_comment(" " + tail):
                    comment(number)
                is_m = (key == "source" and partition_is_m) or key in M_PROPERTIES
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
                if parent is not None and colon:
                    parent["props"][key] = _property_text(stripped.split(":", 1)[1])
                    parent["prop_lines"][key] = number
                elif parent is not None and BARE_FLAG_RE.match(stripped):
                    parent["props"][stripped.lower()] = "true"
                    parent["prop_lines"][stripped.lower()] = number

        if opens_block:
            limit = width + steps_deeper if uses_tabs and line.startswith("\t") or (uses_tabs and width == 0) else None
            block = {"limit": limit, "owner_width": width, "fenced": fenced, "is_m": is_m,
                     "owner": owner, "lines": [], "start": number, "target": target,
                     "owners": [enclosing for _, enclosing in stack]}

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
    return objects


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
    """os.walk that skips Git folders, the template's own test data and the untouched copy made by improve.py."""
    if BEFORE_COPY in os.path.abspath(root).split(os.sep):
        return
    for folder, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if not d.startswith(".git") and d not in ("node_modules", BEFORE_COPY)
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
            if name.lower().endswith((".json", ".pbir", ".pbism")) or name == ".platform":
                path = os.path.join(sub, name)
                before = len(findings.items)
                data = load_json(path, findings)
                if len(findings.items) != before:
                    bad.add(path)
                elif data is not FAILED:
                    check_against_schema(data, path, findings)
    return bad


def check_against_schema(data, path, findings):
    """J003: the file does not fit the Microsoft schema its '$schema' line names. J004: no copy of that schema."""
    try:
        state, problems = json_schema.check_value(data)
    except RecursionError:
        return
    if state == "failed":
        findings.add("J003", path, 0, "does not fit Microsoft's schema (%s): %s. Power BI Desktop refuses a file "
                     "that breaks its schema" % (data.get("$schema", "").split("/json-schemas/")[-1],
                                                 "; ".join(problems[:3])))
    elif state == "not shipped":
        findings.add("J004", path, 0, "not checked against Microsoft's schema: scripts/schemas holds no copy of %s"
                     % data.get("$schema"), level="note")


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
        if not isinstance(position, dict) or not all(_is_number(position.get(k)) for k in ("x", "y", "width", "height")) \
                or position["width"] < 0 or position["height"] < 0:
            findings.add("J002", visual_path, 0, "'position' must be an object with numeric x, y, width and height "
                         "(finite numbers; width and height not below 0)")
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


def check_report(report_dir, findings, brief=None):
    brief = brief or read_brief(os.path.dirname(report_dir))
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

    hidden_by_bookmark = bookmark_hidden(report_dir)
    for page_folder_name, page_folder, page_path in iter_pages(report_dir):
        try:
            check_page(page_folder, page_path, bad, findings)
            if page_path not in bad:
                check_layout(report_dir, page_folder_name, page_folder, page_path, hidden_by_bookmark, brief, findings)
        except (AttributeError, TypeError, KeyError, ValueError, OverflowError) as exc:
            findings.add("J002", page_path, 0, "a file of this page has an unexpected structure (%s)" % exc)
    try:
        report_rules.check(sys.modules[__name__], report_dir, brief, findings)
    except (AttributeError, TypeError, KeyError, ValueError, OverflowError, RecursionError) as exc:
        findings.add("J002", report_path, 0, "the report has a structure the report checks cannot read (%s)" % exc)


def check_model(model_dir, findings):
    """File checks of one model. Returns the objects read from its .tmdl files."""
    check_all_json(model_dir, findings)
    definition = os.path.join(model_dir, "definition")
    count = 0
    objects = []
    for folder, dirs, files in os.walk(definition):
        dirs.sort()
        for name in sorted(files):
            if name.lower().endswith(".tmdl"):
                count += 1
                objects.extend(check_tmdl_file(os.path.join(folder, name), findings) or [])
    if count == 0:
        findings.add("F003", definition, 0, "the model's 'definition' folder holds no .tmdl file")
    return objects


# ---------------------------------------------------------------- the brief

def _brief_value(lines, label):
    """Text after 'label ...:' on the first list line that holds the label; '' when there is none."""
    for line in lines:
        text = line.strip()
        if text.startswith(("-", "*")) and label.lower() in text.lower():
            rest = text[text.lower().index(label.lower()) + len(label):]
            if ":" in rest:
                return rest.split(":", 1)[1].strip().strip("`").strip()
    return ""


def _brief_list(text):
    return [part.strip().strip("`").strip() for part in text.split(",") if part.strip().strip("`").strip()]


def _brief_rows(lines, heading, cells):
    """Rows of the first table under the heading that holds 'heading': lists of exactly 'cells' cells."""
    rows = []
    inside = False
    for line in lines:
        text = line.strip()
        if text.startswith("#"):
            inside = heading.lower() in text.lower()
            continue
        if not inside or not text.startswith("|"):
            continue
        parts = [c.replace("\\|", "|").strip().strip("`").strip()
                 for c in re.split(r"(?<!\\)\|", text.strip("|"))]
        if len(parts) == cells and CODE_RE.match(parts[0]) and not _no_evidence(parts[-1]):
            rows.append(parts)
    return rows


def read_brief(root):
    """The numbers, lists, switches and exceptions the checks take from docs/report-brief.md under root.

    A missing brief, or an empty field, gives the default of the model standard or the layout standard.
    """
    path = os.path.join(root, BRIEF)
    lines = []
    if os.path.isfile(path):
        try:
            with open(path, encoding="utf-8-sig") as fh:
                lines = fh.read().splitlines()
        except (OSError, UnicodeDecodeError):
            lines = []
    numbers = {key: [int(n) for n in re.findall(r"\d+", re.sub(r"\b(\d{1,2}),(\d{3})\b", r"\1\2",
                                                                _brief_value(lines, BRIEF_LABELS[key])))]
               for key in ("page_size", "margin", "gap", "grid")}
    size = tuple(numbers["page_size"][:2]) if len(numbers["page_size"]) >= 2 else None
    subjects = _brief_list(_brief_value(lines, BRIEF_LABELS["subjects"]))
    return {
        "page_size": size,
        "margin": numbers["margin"][0] if numbers["margin"] else None,
        "gap": numbers["gap"][0] if numbers["gap"] else None,
        "grid": numbers["grid"][0] if numbers["grid"] and numbers["grid"][0] > 0 else GRID_STEP,
        "subjects": subjects or list(FOLDER_SUBJECTS),
        "own_spelling": set(_brief_list(_brief_value(lines, BRIEF_LABELS["own_spelling"]))),
        "excel": _brief_value(lines, BRIEF_LABELS["excel"]).lower().startswith("yes"),
        "copilot": _brief_value(lines, BRIEF_LABELS["copilot"]).lower().startswith("yes"),
        "report_prefix": _brief_value(lines, BRIEF_LABELS["report_prefix"]).strip().strip("`").strip(),
        "model_exceptions": {(row[0], row[1]) for row in _brief_rows(lines, MODEL_EXCEPTIONS, 3)},
        "layout_exceptions": {(row[0], row[1], row[2]) for row in _brief_rows(lines, LAYOUT_EXCEPTIONS, 4)},
        "agreed": _agreed(lines),
    }


def _agreed(lines):
    """Lower-case names of the preview features and optional tools that section 11 of the brief lists with a name."""
    names = []
    inside = False
    for line in lines:
        text = line.strip()
        if text.startswith("#"):
            inside = PREVIEW_AGREED.lower() in text.lower()
            continue
        if inside and text.startswith("|"):
            cells = [c.strip().strip("`").strip() for c in text.strip("|").split("|")]
            if len(cells) >= 3 and cells[0] and not set(cells[0]) <= set("-: ") and cells[0].lower() != "feature or tool" \
                    and not _no_evidence(cells[1]):
                names.append(cells[0].lower())
    return names


def model_excused(brief, code, *keys):
    return any((code, key) in brief["model_exceptions"] for key in keys)


def layout_excused(brief, code, page_keys, visual_keys):
    return any((code, page, visual) in brief["layout_exceptions"] for page in page_keys for visual in visual_keys)


def page_numbers(brief, width):
    """(margin, gap) for a page of this width: the brief first, then the layout standard's set for that width."""
    margin, gap = LAYOUT_SETS.get(int(width), (None, None)) if width == int(width) else (None, None)
    return (brief["margin"] if brief["margin"] is not None else margin,
            brief["gap"] if brief["gap"] is not None else gap)


# ---------------------------------------------------------------- model standard

def _dax(text):
    """One DAX expression, read once by the formula scanner: its tokens, its [Name] references and its calls."""
    stream = fs.tokens(text or "", fs.DAX)
    return {"tokens": stream, "references": fs.dax_references(stream), "calls": fs.calls(stream)}


def _only_text(stream):
    """True when a DAX expression is one text value and nothing else."""
    return len(stream) == 1 and stream[0].kind == fs.TEXT


def _split_reference(text):
    """'Table'.'Column' or Table.Column -> (table, column), or None."""
    m = re.match(r"\s*('(?:[^']|'')*'|[^.']+)\.('(?:[^']|'')*'|.+?)\s*\Z", text or "")
    return (_unquote(m.group(1).strip()), _unquote(m.group(2).strip())) if m else None


def build_model(objects):
    """Tables, columns, measures, hierarchies and relationships of one model, from the objects of its files."""
    tables = {}
    relationships = []
    expressions = []                    # (owner text, DAX) of every DAX expression in the model
    for obj in objects:
        if obj["translation"]:
            continue
        kind = obj["kind"]
        if kind == "table" and obj["top"]:
            table = tables.setdefault(obj["name"], {"name": obj["name"], "objects": [], "columns": [], "measures": [],
                                                    "hierarchies": [], "partitions": [], "hidden": False,
                                                    "annotations": {}, "props": {}, "calculation_group": None,
                                                    "refresh_policy": None})
            table["objects"].append(obj)
            table["hidden"] = table["hidden"] or obj["hidden"]
            table["annotations"].update(obj["annotations"])
            table["props"].update(obj["props"])
    for obj in objects:
        if obj["translation"]:
            continue
        kind = obj["kind"]
        owner = obj["table"]
        table = tables.get(owner["name"]) if owner is not None and owner["top"] else None
        if kind == "relationship" and obj["top"]:
            relationships.append(obj)
        elif table is not None and obj["parent"] is owner:
            if kind == "column":
                table["columns"].append(obj)
                obj["calculated"] = obj["has_expr"]
            elif kind == "measure":
                table["measures"].append(obj)
            elif kind == "hierarchy":
                table["hierarchies"].append(obj)
                obj["levels"] = []
            elif kind == "partition":
                table["partitions"].append(obj)
            elif kind == "calculationgroup":
                table["calculation_group"] = obj
            elif kind == "refreshpolicy":
                table["refresh_policy"] = obj
        elif kind == "level" and obj["parent"] is not None and obj["parent"]["kind"] == "hierarchy":
            obj["parent"].setdefault("levels", []).append(_unquote(obj["props"].get("column", "")))
        elif kind == "alternateof" and obj["parent"] is not None and obj["parent"]["kind"] == "column":
            obj["parent"]["alternate_of"] = obj
        if obj["has_expr"] and kind in ("measure", "column", "tablepermission", "calculationitem", "function"):
            expressions.append((obj, obj["expr"] or ""))
        if kind == "partition" and (obj["expr"] or "").split("//")[0].strip().lower() == "calculated":
            expressions.append((obj, obj["props"].get("source", "")))
        for key in ("formatstringdefinition", "detailrowsdefinition"):
            if key in obj["props"]:
                expressions.append((obj, obj["props"][key]))
    for table in tables.values():
        table["calculated"] = any((p["expr"] or "").split("//")[0].strip().lower() == "calculated"
                                  for p in table["partitions"])
        # A field parameter: Power BI marks its fields column with the extended property ParameterMetadata.
        table["field_parameter"] = any("parametermetadata" in {k.lower() for k in c.get("extended", {})}
                                       for c in table["columns"])
        # A numeric range ("what-if") parameter: a calculated table made with GENERATESERIES.
        table["parameter_table"] = table["calculated"] and any(
            call.name == "GENERATESERIES" for p in table["partitions"]
            for call in fs.calls(fs.tokens(p["props"].get("source", ""), fs.DAX)))
    return {"tables": tables, "relationships": relationships, "expressions": expressions}


def _is_hidden(table, obj):
    return table["hidden"] or obj["hidden"]


def _name_problems(name, brief):
    """(errors, warnings) of one measure name against rule 3 of the model standard."""
    errors, warnings = [], []
    own = brief["own_spelling"]
    if name != name.strip():
        errors.append("it starts or ends with a space")
    words = [w for w in name.split() if w]
    letters = [re.sub(r"[^A-Za-z]", "", w) for w in words]
    if "_" in name:
        errors.append("it uses underscores")
    if any(re.search(r"[a-z][A-Z]", w) and w not in own and w.strip("()") not in own for w in words):
        errors.append("it runs words together (CamelCase)")
    spelled = [w for w in letters if w]
    if (len(spelled) >= 2 and all(w.isupper() for w in spelled)
            and any(len(w) > 4 and w not in own for w in spelled)):
        errors.append("it is all in capitals")
    elif any(w.isupper() and len(w) >= 6 and w not in own for w in spelled):
        errors.append("it has a word of six or more letters in capitals (list a real acronym in the brief)")
    for index, word in enumerate(words):
        bare = word.strip("()")
        if bare in own or word in own or not bare[:1].isalpha():
            continue
        if bare[:1].islower() and (index == 0 or bare.lower() not in SMALL_WORDS):
            warnings.append("'%s' should start with a capital (Title Case)" % bare)
            break
    for match in re.finditer(r"(?i)\b(ytd|qtd|mtd|py)\b", name):
        if match.group(1) != match.group(1).upper():
            warnings.append("write the period as %s" % match.group(1).upper())
    if re.search(r"\bLY\b|(?i:\b(last|prior|previous) year\b)", name):
        warnings.append("write the prior year as PY")
    if re.search(r"(?i)\b(year|quarter|month)[ -]to[ -]date\b", name):
        warnings.append("write the period as YTD, QTD or MTD")
    if re.search(r"(?i)\bvs\.|\bversus\b", name) or re.search(r"\b(VS|Vs)\b", name):
        warnings.append("write comparisons with 'vs'")
    if "%" in name and not name.rstrip().endswith("(%)"):
        warnings.append("write the unit as '(%)' at the end of the name")
    elif re.search(r"\([^()]*\)\s*\S", name):
        warnings.append("a unit in brackets goes at the end of the name")
    if re.match(r"(?i)(count of|number of|no\.? of|nr\.? of)\b", name) or re.search(r"(?i)\scount\Z", name):
        warnings.append("start a count measure with '# '")
    if re.match(r"(?i)(ytd|qtd|mtd|py)\b", name):
        warnings.append("put the period after the base name")
    return errors, warnings


def _expected_type(name):
    """The level 2 folder a name points to, when exactly one of the three signals is in the name."""
    signals = []
    if name.startswith("#"):
        signals.append("Counts")
    if re.search(r"\bvs\b", name):
        signals.append("Comparisons")
    if re.search(r"\b(YTD|QTD|MTD|PY)\b", name):
        signals.append("Time Intelligence")
    return signals[0] if len(signals) == 1 else None


def check_standards(model_dir, objects, usage, brief, findings):
    """The model standard (codes M...). usage: (file, entity, property) of every field a report of this model uses."""
    model = build_model(objects)
    tables = model["tables"]
    if not tables:
        return model
    automatic = {name for name in tables if name.startswith(AUTO_DATE_PREFIXES)}     # made by Auto date/time: item 18
    own_tables = [t for t in tables.values() if t["name"] not in automatic]
    measure_tables = {MEASURE_TABLE} | {name for name in tables if model_excused(brief, "M001", name)}
    all_measures = [(t, m) for t in own_tables for m in t["measures"]]
    all_columns = [(t, c) for t in own_tables for c in t["columns"]]
    column_names = {}
    for table, column in all_columns:
        column_names.setdefault(column["name"].lower(), "%s[%s]" % (table["name"], column["name"]))
    measure_names = {m["name"].lower() for _, m in all_measures}
    code_by_owner = [(owner, _dax(text)) for owner, text in model["expressions"]
                     if owner["table"] is None or owner["table"]["name"] not in automatic]
    parsed_by_id = {id(owner): parsed for owner, parsed in code_by_owner}
    used_fields = {(entity, prop) for _, entity, prop in usage if isinstance(prop, str)}

    def add(code, obj, message, level="error", keys=()):
        if not model_excused(brief, code, *keys):
            findings.add(code, obj["file"], obj["line"], message, level=level)
            return True
        return False

    # ---- A. measures
    seen = {}
    for table, measure in all_measures:
        name = measure["name"]
        key = "[%s]" % name
        if table["name"] not in measure_tables:
            add("M001", measure, "measure %s lives in table '%s'; every measure lives in '%s' (or in a measure table "
                "the brief lists). A new measure is written there. An existing one is moved by Copilot, with every reference "
                "repaired, when the developer asks or the improve flow runs (model standard, 'Existing models')"
                % (key, table["name"], MEASURE_TABLE), keys=(key, table["name"]))
        folder = measure["props"].get("displayfolder", "")
        levels = folder.split("\\")
        if not folder:
            add("M003", measure, "measure %s has no display folder; give it one as Subject\\Type" % key, keys=(key,))
        elif ";" in folder or len(levels) != 2 or not all(levels) or any(part != part.strip() for part in levels):
            hint = " Levels are separated by a backslash, not a forward slash." if "/" in folder else ""
            hint += " A level has no space before or after it." if any(part != part.strip() for part in levels) else ""
            add("M003", measure, "measure %s has display folder '%s'; it needs one folder with exactly two levels, "
                "Subject\\Type.%s" % (key, folder, hint), keys=(key,))
        else:
            wrong = []
            if levels[0] not in brief["subjects"]:
                wrong.append("'%s' is not one of the subjects (%s)" % (levels[0], ", ".join(brief["subjects"])))
            if levels[1] not in FOLDER_TYPES:
                wrong.append("'%s' is not one of the types (%s)" % (levels[1], ", ".join(FOLDER_TYPES)))
            if wrong:
                add("M004", measure, "measure %s, display folder '%s': %s" % (key, folder, "; ".join(wrong)), keys=(key,))
        if name.lower() in seen:
            add("M005", measure, "measure name %s is used twice (also in table '%s')" % (key, seen[name.lower()]),
                keys=(key,))
        seen.setdefault(name.lower(), table["name"])
        if name.lower() in column_names:
            add("M006", measure, "measure %s has the same name as column %s; a measure never takes the name of a column"
                % (key, column_names[name.lower()]), keys=(key,))
        errors, warnings = _name_problems(name, brief)
        if errors:
            add("M007", measure, "measure name %s is not a business name: %s. Renaming follows the brief (model standard, 'Existing models')"
                % (key, "; ".join(errors)), keys=(key,))
        expected = _expected_type(name)
        if expected and len(levels) == 2 and levels[1] in FOLDER_TYPES and levels[1] != expected:
            warnings.append("its name points to the folder type '%s', not '%s'" % (expected, levels[1]))
        if warnings:
            add("M008", measure, "measure name %s: %s" % (key, "; ".join(warnings)), level="warn", keys=(key,))
        only_text = _only_text(parsed_by_id[id(measure)]["tokens"] if id(measure) in parsed_by_id
                               else fs.tokens(measure["expr"] or "", fs.DAX))
        if (not _is_hidden(table, measure) and not measure["props"].get("formatstring")
                and "formatstringdefinition" not in measure["props"] and not only_text):
            add("M009", measure, "visible measure %s has no format string" % key, keys=(key,))

    for name in sorted(measure_tables):
        table = tables.get(name)
        if table is None or not table["measures"]:
            continue
        first = table["objects"][0]
        problems = []
        if table["hidden"]:
            problems.append("the table is hidden, which hides its measures; keep it visible")
        if len(table["columns"]) != 1:
            problems.append("it has %d columns; it needs exactly one placeholder column" % len(table["columns"]))
        if any(not c["hidden"] for c in table["columns"]) and not table["hidden"]:
            problems.append("its placeholder column is visible; hide the column")
        if problems:
            add("M002", first, "measure table '%s': %s" % (name, "; ".join(problems)), keys=(name,))

    # ---- rule 5: references in DAX (a text check, not a parser)
    for owner, parsed in code_by_owner:
        if owner["kind"] not in ("measure", "column", "calculationitem", "tablepermission", "function"):
            continue
        loose = set()
        tied = set()
        for table_name, name, _ in parsed["references"]:
            if table_name is None:
                if name.lower() in column_names and name.lower() not in measure_names:
                    loose.add("[%s]" % name)
                continue
            table = tables.get(table_name)
            if (name.lower() in measure_names and table is not None
                    and name.lower() not in {c["name"].lower() for c in table["columns"]}):
                tied.add("%s[%s]" % (table_name, name))
        if loose or tied:
            parts = []
            if loose:
                parts.append("write the column with its table: %s" % ", ".join(sorted(loose)))
            if tied:
                parts.append("write the measure without its table: %s" % ", ".join(sorted(tied)))
            label = model_rules._label(owner)
            add("M010", owner, "DAX of %s: %s" % (label, "; ".join(parts)), level="warn", keys=(label,))

    # ---- B. columns and tables
    relationship_ends = []
    foreign = {}                        # (table, column) -> relationship line
    sort_keys = {}
    for relationship in model["relationships"]:
        ends = [_split_reference(relationship["props"].get(k, "")) for k in ("fromcolumn", "tocolumn")]
        if None in ends or ends[0][0] in automatic or ends[1][0] in automatic:
            continue
        relationship_ends.append((relationship, ends[0], ends[1]))
        if relationship["props"].get("fromcardinality", "many").lower() == "many":
            foreign[ends[0]] = relationship
    column_at = {(t["name"], c["name"]): (t, c) for t, c in all_columns}
    for table, column in all_columns:
        target = _unquote(column["props"].get("sortbycolumn", ""))
        if target:
            sort_keys[(table["name"], target)] = column["name"]
    hierarchy_columns = {(t["name"], level) for t in own_tables for h in t["hierarchies"]
                         for level in h.get("levels", [])}
    with_variation = {id(o["parent"]) for o in objects if o["kind"] == "variation" and o["parent"] is not None}
    totalled = {}
    for owner, parsed in code_by_owner:
        if owner["kind"] != "measure":
            continue
        stream = parsed["tokens"]
        for call in parsed["calls"]:
            if call.name not in TOTAL_FUNCTIONS or len(call.args) != 1 or call.args[0][1] - call.args[0][0] != 2:
                continue
            first, second = stream[call.args[0][0]], stream[call.args[0][0] + 1]
            if first.kind in ("word", fs.QUOTED_NAME) and second.kind == fs.BRACKET_NAME:
                totalled.setdefault((first.value, second.value), owner["name"])

    calculated_columns = []
    for table, column in all_columns:
        key = "%s[%s]" % (table["name"], column["name"])
        place = (table["name"], column["name"])
        props = column["props"]
        kind = props.get("datatype", "").lower()
        visible = not _is_hidden(table, column)
        in_measure_table = table["name"] in measure_tables
        in_use = place in hierarchy_columns or place in used_fields
        advice = ("a hierarchy or a report visual uses it, so it stays visible: record its use in the brief" if in_use
                  else "hide it, or record its use in the brief")
        if visible and place in foreign:
            if add("M102", column, "column %s is the many side of a relationship (a foreign key) and is visible; %s"
                   % (key, advice), level="warn", keys=(key,)) and not in_use:
                findings.fixes.append(("M102", key, "isHidden", "true"))
        elif visible and place in sort_keys:
            if add("M102", column, "column %s only sorts column '%s' and is visible; %s"
                   % (key, sort_keys[place], advice), level="warn", keys=(key,)) and not in_use:
                findings.fixes.append(("M102", key, "isHidden", "true"))
        if visible and kind in NUMERIC_TYPES and place in totalled:
            if add("M103", column, "numeric column %s is visible, and measure [%s] already totals it; %s"
                   % (key, totalled[place], advice), level="warn", keys=(key,)) and not in_use:
                findings.fixes.append(("M103", key, "isHidden", "true"))
        if column["hidden"] and not table["hidden"] and not in_measure_table:
            needed = []
            if place in hierarchy_columns:
                needed.append("a hierarchy")
            if place in used_fields:
                needed.append("a report visual")
            if needed:
                add("M104", column, "hidden column %s is used by %s. It still works, but report authors can no longer "
                    "pick it; the standard keeps such a column visible unless the brief says why not"
                    % (key, " and ".join(needed)), level="warn", keys=(key,))
        if column.get("calculated"):
            calculated_columns.append((table, column))
            if not re.search(r"[^\W_]", column["annotations"].get(REASON_ANNOTATION, "")):
                add("M105", column, "calculated column %s has no '%s' annotation. Ask the developer what makes a DAX "
                    "calculation necessary here and what stops Power Query or the source from supplying the value"
                    % (key, REASON_ANNOTATION), keys=(key,))
            if any(call.name == "RELATED" for call in _dax(column["expr"] or "")["calls"]):
                add("M106", column, "calculated column %s uses RELATED; consider bringing the value in at the source"
                    % key, level="warn", keys=(key,))
        if visible and kind in NUMERIC_TYPES and props.get("summarizeby", "").lower() != "none":
            add("M107", column, "visible numeric column %s still totals by default (summarizeBy is '%s'); set it to "
                "none and use a measure, or list the column in the brief. Changing it needs the developer: Microsoft "
                "does not document the effect on visuals that already total the column"
                % (key, props.get("summarizeby", "not set")), keys=(key,))
        if kind == "double":
            add("M108", column, "column %s has the floating-point type (double, 'Decimal number' in Desktop); "
                "fixed decimal or whole number avoids rounding differences. A type change is the developer's decision"
                % key, level="warn", keys=(key,))
        if kind == "datetime":
            style = props.get("formatstring", "")
            if not style or style.lower() == "general date" or re.search(r"(?i)\bh{1,2}\b|:mm|\bss\b|time|am/pm|\btt\b", style):
                add("M111", column, "column %s may hold a date and a time together (format '%s'); if it does, "
                    "split it or keep the date only. The check cannot see the data" % (key, style or "not set"),
                    level="warn", keys=(key,))
        if visible and kind in NUMERIC_TYPES + ("datetime",) and not props.get("formatstring"):
            add("M112", column, "visible %s column %s has no format string"
                % ("date" if kind == "datetime" else "numeric", key), level="warn", keys=(key,))

    for table in own_tables:
        if table["name"] in measure_tables or table["hidden"]:
            continue
        shown = [c for c in table["columns"] if not c["hidden"]]
        fields = len(shown) + len([m for m in table["measures"] if not m["hidden"]]) \
            + len([h for h in table["hierarchies"] if not h["hidden"]])
        loose = [c["name"] for c in shown if c["props"].get("displayfolder", "") not in COLUMN_FOLDERS]
        if fields >= FOLDER_THRESHOLD and loose:
            add("M101", table["objects"][0], "table '%s' shows %d fields; group its columns in the folders %s. "
                "Not in one of them: %s" % (table["name"], fields, ", ".join(COLUMN_FOLDERS), ", ".join(loose[:12])
                                           + (" ..." if len(loose) > 12 else "")), level="warn", keys=(table["name"],))
    for table in own_tables:
        if table["calculated"]:
            if not re.search(r"[^\W_]", table["annotations"].get(REASON_ANNOTATION, "")):
                add("M105", table["objects"][0], "calculated table '%s' has no '%s' annotation. Ask the developer what "
                    "makes a DAX calculation necessary here and what stops Power Query or the source from supplying "
                    "the table" % (table["name"], REASON_ANNOTATION), keys=(table["name"],))
    if len(calculated_columns) > CALCULATED_COLUMN_LIMIT:
        table, column = calculated_columns[0]
        add("M106", column, "the model has %d calculated columns (more than %d): review whether they can come from "
            "the source: %s" % (len(calculated_columns), CALCULATED_COLUMN_LIMIT,
                                ", ".join("%s[%s]" % (t["name"], c["name"]) for t, c in calculated_columns)),
            level="warn", keys=("model",))

    for relationship, start, end in relationship_ends:
        if start not in column_at or end not in column_at:
            continue
        kinds = [column_at[side][1]["props"].get("datatype", "").lower() for side in (start, end)]
        label = "%s[%s] to %s[%s]" % (start[0], start[1], end[0], end[1])
        if kinds[0] and kinds[1] and kinds[0] != kinds[1]:
            add("M109", relationship, "relationship %s joins a %s column to a %s column; both need the same type"
                % (label, kinds[0], kinds[1]), keys=(label,))
        elif any(k and k != "int64" for k in kinds):
            add("M110", relationship, "relationship %s uses %s columns; whole number is preferred"
                % (label, " and ".join(sorted({k for k in kinds if k}))), level="warn", keys=(label,))

    # ---- C. assess only
    named = {}                          # lower-case [name] -> the owners whose DAX holds it
    for owner, parsed in code_by_owner:
        for _, name, _ in parsed["references"]:
            named.setdefault(name.lower(), []).append(owner)
    for table, column in all_columns:
        place = (table["name"], column["name"])
        if not _is_hidden(table, column) or table["name"] in measure_tables:
            continue
        if (place in foreign or place in sort_keys or place in hierarchy_columns or place in used_fields
                or any(place in (start, end) for _, start, end in relationship_ends)
                or column["props"].get("sortbycolumn") or column["name"].lower() in named):
            continue
        add("M201", column, "hidden column %s[%s]: nothing in the model or the report refers to it"
            % place, level="note", keys=("%s[%s]" % place,))
    for table, measure in all_measures:
        if not _is_hidden(table, measure):
            continue
        if (any(owner is not measure for owner in named.get(measure["name"].lower(), []))
                or any(prop == measure["name"] for _, _, prop in usage)):
            continue
        add("M201", measure, "hidden measure [%s]: nothing in the model or the report refers to it" % measure["name"],
            level="note", keys=("[%s]" % measure["name"],))

    # ---- D. only when the brief turns them on
    if brief["excel"]:
        for table in own_tables:
            if table["name"] in measure_tables:
                continue
            found = [c["name"] for c in table["columns"]
                     if _is_hidden(table, c) and id(c) not in with_variation and (table["name"], c["name"]) not in sort_keys
                     and not c["props"].get("sortbycolumn") and (table["name"], c["name"]) not in hierarchy_columns
                     and c["props"].get("isavailableinmdx", "true").lower() != "false"]
            if found:
                add("M301", table["objects"][0], "table '%s': isAvailableInMdx could be turned off on hidden column(s) %s. "
                    "That saves memory but removes them from Excel PivotTables. Change nothing without the developer's yes"
                    % (table["name"], ", ".join(found)), level="note", keys=(table["name"],))
    if brief["copilot"]:
        for obj in objects:
            home = obj if obj["kind"] == "table" else obj["table"]
            if (not obj["translation"] and obj["kind"] in DESCRIBED_KINDS and (home is None or home["name"] not in automatic)
                    and len(obj["description"]) > COPILOT_DESCRIPTION_LIMIT):
                findings.add("M302", obj["file"], obj["line"],
                             "%s '%s': its description has %d characters; Copilot in Power BI reads the first %d, so "
                             "put the key words first" % (obj["kind"], obj["name"], len(obj["description"]),
                                                          COPILOT_DESCRIPTION_LIMIT), level="note")

    # ---- the rules added in round 3 (scripts/model_rules.py)
    model_object = next((o for o in objects if o["kind"] == "model" and o["top"] and not o["translation"]), None)
    database = next((o for o in objects if o["kind"] == "database" and o["top"]), None)
    level = (database or {}).get("props", {}).get("compatibilitylevel", "") if database else ""
    model_rules.check({
        "model": model, "tables": tables, "own_tables": own_tables, "automatic": automatic,
        "auto_prefixes": AUTO_DATE_PREFIXES, "measure_tables": measure_tables, "all_measures": all_measures,
        "all_columns": all_columns, "expressions": code_by_owner, "objects": objects, "brief": brief,
        "usage": usage, "add": add, "parse": _dax, "model_object": model_object, "findings": findings,
        "excused": lambda code, *keys: model_excused(brief, code, *keys),
        "model_anchor": model_object or (own_tables[0]["objects"][0] if own_tables else None),
        "compatibility_level": int(level) if level.isdigit() else None,
        "table_names_upper": {name.upper() for name in tables}})
    return model


# ---------------------------------------------------------------- fields a report uses

def report_model(report_dir):
    """The model folder a report points to with a relative path, or None (a published model, or unreadable)."""
    data = load_object(os.path.join(report_dir, "definition.pbir"))
    try:
        path = data["datasetReference"]["byPath"]["path"]
    except (TypeError, KeyError):
        return None
    return os.path.normpath(os.path.join(report_dir, path)) if isinstance(path, str) else None


def _source_table(expression, aliases):
    """The table a {"SourceRef": ...} names: directly ("Entity"), or by an alias of the nearest "From" list ("Source")."""
    source = expression.get("SourceRef") if isinstance(expression, dict) else None
    if not isinstance(source, dict):
        return None
    if isinstance(source.get("Entity"), str):
        return source["Entity"]
    return aliases.get(source.get("Source")) if isinstance(source.get("Source"), str) else None


def _field_references(node, found, aliases=None):
    """Adds (table, field) pairs to 'found'. field is None for a table named on its own, and ('hierarchy', name)
    for a hierarchy."""
    aliases = aliases or {}
    if isinstance(node, dict):
        listed = node.get("From")
        if isinstance(listed, list):
            aliases = dict(aliases)
            for entry in listed:
                if isinstance(entry, dict) and isinstance(entry.get("Name"), str) and isinstance(entry.get("Entity"), str):
                    aliases[entry["Name"]] = entry["Entity"]
                    found.append((entry["Entity"], None))
        for kind in ("Column", "Measure"):
            value = node.get(kind)
            if isinstance(value, dict) and isinstance(value.get("Property"), str):
                table = _source_table(value.get("Expression"), aliases)
                if table is not None:
                    found.append((table, value["Property"]))
        value = node.get("Hierarchy")
        if isinstance(value, dict) and isinstance(value.get("Hierarchy"), str):
            table = _source_table(value.get("Expression"), aliases)
            if table is not None:
                found.append((table, ("hierarchy", value["Hierarchy"])))
        source = node.get("SourceRef")
        if isinstance(source, dict) and isinstance(source.get("Entity"), str):
            found.append((source["Entity"], None))
        for value in node.values():
            _field_references(value, found, aliases)
    elif isinstance(node, list):
        for value in node:
            _field_references(value, found, aliases)


def report_fields(report_dir):
    """(file, table, field) for every column or measure the report's files name by table (SourceRef.Entity)."""
    out = []
    definition = os.path.join(report_dir, "definition")
    for folder, dirs, files in os.walk(definition):
        for name in sorted(files):
            if not name.lower().endswith(".json") or name == "reportExtensions.json":
                continue
            path = os.path.join(folder, name)
            data = load_json(path)
            if data is FAILED:
                continue
            found = []
            try:
                _field_references(data, found)
            except RecursionError:
                continue
            out.extend((path, entity, prop) for entity, prop in found)
    return out


def report_measures(report_dir):
    """(table, measure) of every measure defined in the report itself (reportExtensions.json)."""
    data = load_object(os.path.join(report_dir, "definition", "reportExtensions.json")) or {}
    out = set()
    for entity in data.get("entities") if isinstance(data.get("entities"), list) else []:
        if isinstance(entity, dict):
            for measure in entity.get("measures") if isinstance(entity.get("measures"), list) else []:
                if isinstance(measure, dict):
                    out.add((entity.get("name"), measure.get("name")))
    return out


def read_field_list(root):
    """The saved field list of a published model as a model the binding check can read, or None when there is none.

    docs/model-fields.md holds one table: | Table | Field | Kind |, with Kind column, measure or hierarchy.
    """
    path = os.path.join(root, FIELD_LIST)
    try:
        with open(path, encoding="utf-8-sig") as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return None
    tables = {}
    for line in lines:
        text = line.strip()
        if not text.startswith("|"):
            continue
        cells = [c.replace("\\|", "|").strip().strip("`").strip() for c in re.split(r"(?<!\\)\|", text.strip("|"))]
        if len(cells) < 3 or cells[2].lower() not in ("column", "measure", "hierarchy") or not cells[0] or not cells[1]:
            continue
        table = tables.setdefault(cells[0], {"name": cells[0], "columns": [], "measures": [], "hierarchies": []})
        table[{"column": "columns", "measure": "measures", "hierarchy": "hierarchies"}[cells[2].lower()]].append({"name": cells[1]})
    return {"tables": tables} if tables else None


def check_bindings(report_dir, model, usage, brief, findings):
    """B001: a report file names a table, column or measure the model in this project does not have."""
    own = report_measures(report_dir)
    tables = model["tables"]
    missing = {}
    for path, entity, prop in usage:
        if (entity, prop) in own or (isinstance(prop, str) and model_excused(brief, "B001", "%s[%s]" % (entity, prop))):
            continue
        table = tables.get(entity)
        if table is None:
            missing.setdefault(path, set()).add("table '%s'" % entity)
        elif isinstance(prop, tuple):
            if prop[1] not in {h["name"] for h in table["hierarchies"]}:
                missing.setdefault(path, set()).add("hierarchy '%s' of table '%s'" % (prop[1], entity))
        elif prop is not None and prop not in {o["name"] for o in table["columns"] + table["measures"]}:
            missing.setdefault(path, set()).add("%s[%s]" % (entity, prop))
    for path in sorted(missing):
        findings.add("B001", path, 0, "this file uses field(s) the model does not have: %s. A rename or a move of a "
                     "measure breaks such references" % ", ".join(sorted(missing[path])))


# ---------------------------------------------------------------- layout standard

def _is_number(value):
    """A real, finite number of a size a page can have."""
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return abs(float(value)) < 1e9
    except OverflowError:
        return False


def _text(value):
    return value if isinstance(value, str) else None


def bookmark_hidden(report_dir):
    """{page name: [(visual names, group names) that one bookmark hides, ...]}: one entry for each bookmark."""
    out = {}
    folder = os.path.join(report_dir, "definition", "bookmarks")
    if not os.path.isdir(folder):
        return out

    def groups(states, names):
        for name, state in states.items() if isinstance(states, dict) else []:
            if isinstance(state, dict):
                if state.get("isHidden") is True:
                    names.add(name)
                groups(state.get("children"), names)

    for name in sorted(os.listdir(folder)):
        if not name.endswith(".bookmark.json"):
            continue
        data = load_object(os.path.join(folder, name)) or {}
        state = data.get("explorationState")
        sections = state.get("sections") if isinstance(state, dict) else None
        for page, section in sections.items() if isinstance(sections, dict) else []:
            if not isinstance(section, dict):
                continue
            visuals, hidden_groups = set(), set()
            out.setdefault(page, []).append((visuals, hidden_groups))
            containers = section.get("visualContainers")
            for visual, saved in containers.items() if isinstance(containers, dict) else []:
                try:
                    if saved["singleVisual"]["display"]["mode"] == "hidden":
                        visuals.add(visual)
                except (TypeError, KeyError):
                    pass
            groups(section.get("visualContainerGroups"), hidden_groups)
    return out


def page_layout(page_folder):
    """Position and kind of every visual on a page whose visual.json can be read."""
    out = []
    for folder_name, path in iter_visuals(page_folder):
        data = load_object(path)
        position = data.get("position") if data else None
        if not isinstance(position, dict) or not all(_is_number(position.get(k)) for k in ("x", "y", "width", "height")):
            continue
        visual = data.get("visual") if isinstance(data.get("visual"), dict) else {}
        angle = position.get("angle")
        out.append({"folder": folder_name, "path": path, "name": _text(data.get("name")) or folder_name,
                    "label": _text(annotation(data, LABEL_ANNOTATION)),
                    "x": position["x"], "y": position["y"], "w": position["width"], "h": position["height"],
                    "group": isinstance(data.get("visualGroup"), dict), "parent": _text(data.get("parentGroupName")),
                    "hidden": data.get("isHidden") is True, "type": _text(visual.get("visualType")),
                    "data": isinstance(visual.get("query"), dict),
                    "rotated": _is_number(angle) and angle != 0})
    return out


def _shown(visual):
    return visual["label"] or visual["name"]


def _keys(visual):
    return {k for k in (visual["label"], visual["name"], visual["folder"]) if k}


def check_layout(report_dir, page_folder_name, page_folder, page_path, hidden_by_bookmark, brief, findings):
    """The layout standard (codes G...) for one page."""
    page = load_object(page_path)
    if page is None:
        return
    if not _is_number(page.get("width")) or not _is_number(page.get("height")) or page["width"] <= 0 or page["height"] <= 0:
        if page.get("displayOption") != "DeprecatedDynamic":
            findings.add("G007", page_path, 0, "page has no usable width and height, so its layout cannot be checked",
                         level="warn")
        return
    width, height = page["width"], page["height"]
    page_keys = {k for k in (page_folder_name, _text(page.get("name")), _text(page.get("displayName"))) if k}
    visuals = page_layout(page_folder)
    by_name = {v["name"]: v for v in visuals}
    for visual in visuals:
        if visual["parent"] and not (visual["parent"] in by_name and by_name[visual["parent"]]["group"]):
            visual["parent"] = None            # names a group that is not on the page: treat it as a visual of the page
    states = hidden_by_bookmark.get(_text(page.get("name")) or page_folder_name, [])

    def hidden_in(visual, state, depth=0):
        """Hidden by default (state None), or hidden when one bookmark (a pair of name sets) is applied."""
        if state is None:
            own = visual["hidden"]
        else:
            own = visual["name"] in state[0] or (visual["group"] and visual["name"] in state[1])
        if own:
            return True
        parent = by_name.get(visual["parent"]) if visual["parent"] else None
        return parent is not None and depth < 20 and hidden_in(parent, state, depth + 1)

    def is_hidden(visual):
        return hidden_in(visual, None) or any(hidden_in(visual, state) for state in states)

    def shown_together(first, second):
        """False when the two are layered on purpose: a bookmark shows one of them without the other."""
        return not any(hidden_in(first, state) != hidden_in(second, state) for state in states)

    def excused(code, *some):
        keys = set()
        for visual in some:
            keys |= _keys(visual)
        return layout_excused(brief, code, page_keys, keys or {"-"})

    def right(v):
        return v["x"] + v["w"]

    def bottom(v):
        return v["y"] + v["h"]

    top_level = [v for v in visuals if not v["parent"]]
    for visual in top_level:
        if visual["rotated"]:
            findings.add("G008", visual["path"], 0, "visual '%s' is rotated; its position is not checked" % _shown(visual),
                         level="note")
        elif (visual["x"] < -EPSILON or visual["y"] < -EPSILON or right(visual) > width + EPSILON
              or bottom(visual) > height + EPSILON) and not excused("G001", visual):
            findings.add("G001", visual["path"], 0, "visual '%s' (x %g, y %g, width %g, height %g) reaches outside the "
                         "page (%g x %g)" % (_shown(visual), visual["x"], visual["y"], visual["w"], visual["h"], width, height))

    members = [_shown(v) for v in visuals if v["parent"]]
    if members:
        findings.add("G008", page_path, 0, "visuals inside a group are compared only with the other members of their "
                     "group, and not with the page: %s. Look at this page in Power BI Desktop"
                     % (", ".join(members[:8]) + (" ..." if len(members) > 8 else "")), level="note")

    plotted = [v for v in visuals if v["data"] and not v["rotated"] and not hidden_in(v, None)]
    for index, first in enumerate(plotted):
        for second in plotted[index + 1:]:
            if first["parent"] != second["parent"] or not shown_together(first, second):
                continue            # a member's position may count from its group: compare like with like only
            across = min(right(first), right(second)) - max(first["x"], second["x"])
            down = min(bottom(first), bottom(second)) - max(first["y"], second["y"])
            if across > EPSILON and down > EPSILON and not excused("G002", first) and not excused("G002", second):
                findings.add("G002", first["path"], 0, "data visuals '%s' and '%s' overlap by %g x %g pixels"
                             % (_shown(first), _shown(second), across, down))

    if page.get("type") == "Tooltip":
        return
    size = brief["page_size"] or PAGE_SIZE
    if (width, height) != tuple(size) and not layout_excused(brief, "G007", page_keys, {"-"}):
        findings.add("G007", page_path, 0, "page is %g x %g; the brief or the layout standard says %d x %d. "
                     "An existing report keeps its size: write it in the brief" % (width, height, size[0], size[1]),
                     level="warn")
    grid = brief["grid"]
    margin, gap = page_numbers(brief, width)
    placed = [v for v in top_level if not v["group"] and not v["rotated"] and not is_hidden(v)]
    for visual in placed:
        off = [k for k, value in (("x", visual["x"]), ("y", visual["y"]), ("width", visual["w"]), ("height", visual["h"]))
               if abs(value / grid - round(value / grid)) > EPSILON]
        if off and not excused("G003", visual):
            findings.add("G003", visual["path"], 0, "visual '%s': %s not on the %d-pixel grid (x %g, y %g, width %g, "
                         "height %g)" % (_shown(visual), ", ".join(off), grid, visual["x"], visual["y"], visual["w"], visual["h"]),
                         level="warn")
    edge = [v for v in placed if not excused("G004", v)]
    if margin is None or gap is None:
        findings.add("G004", page_path, 0, "the layout standard has no margin and gap for a page %g wide; write both "
                     "in the brief, so that margins and gaps can be checked" % width, level="warn")
    if edge and margin is not None:
        sides = (("left", min(v["x"] for v in edge)), ("top", min(v["y"] for v in edge)),
                 ("right", width - max(right(v) for v in edge)))
        below = height - max(bottom(v) for v in edge)
        wrong = ["%s %g" % (name, value) for name, value in sides if abs(value - margin) > EPSILON]
        if below < margin - EPSILON:
            wrong.append("bottom %g" % below)
        if wrong:
            findings.add("G004", page_path, 0, "outer margins differ from %d pixels: %s (left, top and right equal the "
                         "margin; bottom is at least the margin)" % (margin, ", ".join(wrong)), level="warn")
    rows = {}
    for visual in placed:
        if visual["type"]:
            rows.setdefault((visual["type"], visual["y"]), []).append(visual)
    for (kind, y), members in sorted(rows.items(), key=lambda item: (item[0][1], item[0][0])):
        if len({v["h"] for v in members}) > 1 and not any(excused("G005", v) for v in members):
            findings.add("G005", members[0]["path"], 0, "%s visuals in the row at y %g have different heights: %s"
                         % (kind, y, ", ".join("%s %g" % (_shown(v), v["h"]) for v in members)), level="warn")
    if gap is not None:
        spaced = [v for v in placed if not excused("G006", v)]
        wrong = []
        for first in spaced:
            beside = [v for v in spaced if v is not first and v["x"] >= right(first) - EPSILON
                      and min(bottom(first), bottom(v)) - max(first["y"], v["y"]) > EPSILON]
            under = [v for v in spaced if v is not first and v["y"] >= bottom(first) - EPSILON
                     and min(right(first), right(v)) - max(first["x"], v["x"]) > EPSILON]
            if beside:
                nearest = min(beside, key=lambda v: v["x"])
                if abs(nearest["x"] - right(first) - gap) > EPSILON:
                    wrong.append("%s to %s: %g across" % (_shown(first), _shown(nearest), nearest["x"] - right(first)))
            if under:
                nearest = min(under, key=lambda v: v["y"])
                if abs(nearest["y"] - bottom(first) - gap) > EPSILON:
                    wrong.append("%s to %s: %g down" % (_shown(first), _shown(nearest), nearest["y"] - bottom(first)))
        if wrong:
            findings.add("G006", page_path, 0, "gaps between neighbours differ from %d pixels: %s%s"
                         % (gap, "; ".join(wrong[:8]), " ..." if len(wrong) > 8 else ""), level="warn")


# ---------------------------------------------------------------- review table

def _plain(text):
    return re.sub("[​‌‍﻿ ]", "", text).strip()


def _no_evidence(text):
    words = re.sub(r"&\w+;|<[^>]*>|[`*_~]", " ", text).strip().lower()
    if not re.search(r"[^\W_]", words):
        return True
    return words.strip(" .:!?") in EMPTY_EVIDENCE or re.match(r"(todo|tbd)\b", words) is not None


CHECKLIST = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "checklist", "checklist.md")


def _applicability():
    """{item: [its 'Mark N/A when' line, its 'When applicable' line]} from the checklist; {} when it cannot be read."""
    try:
        with open(CHECKLIST, encoding="utf-8-sig") as fh:
            lines = fh.read().splitlines()
    except (OSError, UnicodeDecodeError):
        return {}
    found, item = {}, None
    for line in lines:
        heading = re.match(r"## Item (\d+)\s*$", line)
        if heading:
            item = int(heading.group(1))
        clause = re.match(r"\W*(Mark N/A when|When applicable)\s*:\s*(\S.*)$", line)
        if clause and item is not None:
            found.setdefault(item, []).append("%s: %s" % (clause.group(1), clause.group(2).strip()))
    return found


def _words(text):
    return " ".join(re.sub(r"[^a-z0-9]+", " ", text.lower()).split())


def _quotes(evidence, clauses):
    """True when the evidence holds the text of one of the item's own lines (the part after the colon)."""
    said = _words(evidence)
    return any(_words(clause.split(":", 1)[1]) in said for clause in clauses)


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
    applies = _applicability()
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
        elif status == "Not applicable" and item in applies and not _quotes(evidence, applies[item]):
            findings.add("R007", path, number,
                         "item %d: Not applicable needs the item's own line in the evidence cell, word for word (%s), and "
                         "why it holds for this report. A fact nobody gave is 'Fail' with 'Evidence missing:', never "
                         "Not applicable" % (item, " or ".join("'%s'" % clause for clause in applies[item])))
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
    brief = read_brief(root)
    parsed = {os.path.normpath(model): check_model(model, findings) for model in models}
    usage = {}
    for report in reports:
        check_report(report, findings, brief)
        target = report_model(report)
        if target is not None and not os.path.isdir(target):
            findings.add("B001", os.path.join(report, "definition.pbir"), 0,
                         "the report points to a model folder that does not exist: %s" % os.path.basename(target))
        if target in parsed:
            usage.setdefault(target, []).append((report, report_fields(report)))
        elif target is None:
            listed = read_field_list(root)
            if listed is None:
                findings.add("B002", os.path.join(report, "definition.pbir"), 0, "this report reads a published model and "
                             "%s does not exist, so its fields are not checked. Save the field list there (skill pbi-report)"
                             % FIELD_LIST.replace(os.sep, "/"), level="note")
            else:
                check_bindings(report, listed, report_fields(report), brief, findings)
    for model in models:
        used = usage.get(os.path.normpath(model), [])
        every = [field for _, fields in used for field in fields]
        try:
            built = check_standards(model, parsed[os.path.normpath(model)], every, brief, findings)
            for report, fields in used:
                check_bindings(report, built, fields, brief, findings)
        except (AttributeError, TypeError, KeyError, ValueError, RecursionError, OverflowError) as exc:
            findings.add("J002", os.path.join(model, "definition"), 0,
                         "the model has a structure the standard checks cannot read (%s)" % exc)
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
    warnings = findings.warnings()
    infos = len(findings.items) - len(errors) - len(warnings)
    print("Checked %d model(s) and %d report(s): %d error(s), %d warning(s), %d note(s)."
          % (len(models), len(reports), len(errors), len(warnings), infos))
    if errors:
        codes = sorted({f[0] for f in errors})
        print("If you created or changed these files in this task, fix them and record one lesson for each code (%s): "
              "python scripts/lessons.py add --trigger check --key <code> --mistake \"...\" --correction \"...\""
              % ", ".join(codes))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
