#!/usr/bin/env python3
"""The model checks added in round 3: relationships, DAX, security, storage modes, model objects, Power Query.

scripts/check_project.py calls check() once for each model. This file is not run by itself.
Each rule, its level and its source address are listed in the standards under
.github/skills/pbi-semantic-model/references/ (the code after a rule is the finding it gives here).

Levels of these checks:
    fail  Microsoft says it breaks something or gives wrong numbers, or the checklist gives a hard number,
          and the files show the breach for certain
    warn  every other rule, and every rule the files can only suggest (a text pattern, a name)
    note  a suggestion (codes that start with U)

Formulas are read with scripts/formula_scanner.py, never with a pattern on raw text.
Needs Python 3.8 or later. Uses the standard library only.
"""
import os
import re

import formula_scanner as fs

HERE = os.path.dirname(os.path.abspath(__file__))
DAX_INDEX = os.path.join(os.path.dirname(HERE), ".github", "skills", "pbi-semantic-model", "references",
                         "dax-functions.md")
AUTO_DATE_ANNOTATION = "__PBI_TimeIntelligenceEnabled"     # seen in projects Power BI Desktop saved; not documented
UDF_LEVEL = 1702                    # Microsoft Learn, "DAX user-defined functions": compatibility level 1702 or higher
MANY_TO_MANY_SHARE = 0.3            # Microsoft's best practice rule on excessive both-direction or many-to-many relationships
REPEAT_TOKENS = 6                   # a call this long, written twice in one formula, belongs in a variable
TOOL_FUNCTIONS = ("EVALUATEANDLOG",)
ERROR_FUNCTIONS = ("IFERROR", "ISERROR")
ROW_FUNCTIONS = ("EARLIER", "EARLIEST")
WINDOW_FUNCTIONS = ("OFFSET", "WINDOW", "INDEX", "RANK", "ROWNUMBER")
RLS_TEXT_FUNCTIONS = ("LEFT", "RIGHT", "UPPER", "LOWER", "FIND", "LOOKUPVALUE")
ITERATORS = ("SUMX", "AVERAGEX", "MINX", "MAXX", "COUNTX", "COUNTAX", "PRODUCTX", "RANKX", "CONCATENATEX",
             "MEDIANX", "STDEVX.S", "STDEVX.P", "VARX.S", "VARX.P", "PERCENTILEX.INC", "PERCENTILEX.EXC",
             "GEOMEANX", "XIRR", "XNPV")
M_TRANSFORMS = ("Table.Combine", "Table.Join", "Table.NestedJoin", "Table.AddColumn", "Table.Group", "Table.Sort",
                "Table.Pivot", "Table.Unpivot", "Table.UnpivotOtherColumns", "Table.Distinct")
M_NATIVE = ("Value.NativeQuery", "OleDb.Query", "Odbc.Query")
M_RELATIVE_DATES = ("DateTime.LocalNow", "DateTime.FixedLocalNow", "DateTimeZone.LocalNow", "DateTimeZone.UtcNow",
                    "DateTimeZone.FixedLocalNow", "DateTimeZone.FixedUtcNow")
MONTHS = ("jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec")
PLACE_WORDS = ("country", "continent", "city")
DAX_NOT_FUNCTIONS = fs.DAX_KEYWORDS | frozenset(("IN", "NOT"))
MANY_COLUMNS = 30                   # Microsoft's skill (skills-for-fabric): more visible columns hints at a design problem
CALCULATED_TABLE_MAKERS = ("ROW", "SELECTCOLUMNS", "DATATABLE")
SUMMARIZECOLUMNS_FILTERS = ("FILTER", "TREATAS", "KEEPFILTERS")
UDF_NAME = re.compile(r"[A-Za-z_][A-Za-z0-9_]*(?:\.[A-Za-z0-9_]+)*\Z")

_index = None


def dax_index():
    """{'functions': names in capitals, 'time': the time intelligence ones} from the DAX function index file."""
    global _index
    if _index is None:
        _index = {"functions": set(), "time": set()}
        try:
            with open(DAX_INDEX, encoding="utf-8") as handle:
                group = ""
                for line in handle:
                    if line.startswith("## "):
                        group = line[3:].strip().lower()
                    elif line.startswith("- ") and ": https://" in line and group not in ("statements", "language"):
                        name = line[2:].split(":", 1)[0].strip().upper()
                        name = name.split(" (")[0]              # 'DISTINCT (column)' and 'DISTINCT (table)' are DISTINCT
                        if " " in name:
                            continue                            # a page about functions, not a function
                        _index["functions"].add(name)
                        if group.startswith("time intelligence"):
                            _index["time"].add(name)
        except OSError:
            pass
    return _index


def _reference(text):
    """'Table'.'Column' or Table.Column -> (table, column); a bare table name -> (table, None)."""
    text = (text or "").strip()
    match = re.match(r"('(?:[^']|'')*'|[^.']+)(?:\.('(?:[^']|'')*'|.+?))?\s*\Z", text)
    if not match:
        return None

    def plain(name):
        name = name.strip()
        return name[1:-1].replace("''", "'") if len(name) >= 2 and name[0] == "'" and name[-1] == "'" else name
    return plain(match.group(1)), plain(match.group(2)) if match.group(2) else None


def _span_text(parsed, span):
    return fs.text_of(parsed["tokens"], span[0], span[1])


def _calls(parsed, *names):
    return [call for call in parsed["calls"] if call.name in names]


def _label(owner):
    kind = owner["kind"]
    if kind == "measure":
        return "[%s]" % owner["name"]
    if kind == "column":
        return "%s[%s]" % (owner["table"]["name"] if owner["table"] else "?", owner["name"])
    if kind == "tablepermission":
        return "role '%s', table '%s'" % (owner["parent"]["name"] if owner["parent"] else "?", owner["name"])
    if kind == "calculationitem":
        return "calculation item '%s'" % owner["name"]
    if kind == "function":
        return "function %s" % owner["name"]
    if kind == "partition":
        return "calculated table '%s'" % (owner["table"]["name"] if owner["table"] else owner["name"])
    return "%s '%s'" % (kind, owner["name"])


def relationships(context):
    """Each relationship as a dict: both ends, cardinalities, direction, active, label."""
    out = []
    for relationship in context["model"]["relationships"]:
        props = relationship["props"]
        ends = [_reference(props.get(key, "")) for key in ("fromcolumn", "tocolumn")]
        if None in ends or None in (ends[0][1], ends[1][1]):
            continue
        out.append({"object": relationship, "from": ends[0], "to": ends[1],
                    "from_many": props.get("fromcardinality", "many").lower() == "many",
                    "to_many": props.get("tocardinality", "one").lower() == "many",
                    "both": props.get("crossfilteringbehavior", "").lower() == "bothdirections",
                    "active": props.get("isactive", "true").lower() != "false",
                    "label": "%s[%s] to %s[%s]" % (ends[0][0], ends[0][1], ends[1][0], ends[1][1])})
    return out


def table_modes(table):
    return {p["props"].get("mode", "").lower() for p in table["partitions"] if p["props"].get("mode")}


def check(context):
    """context: model, tables, own_tables, automatic, measure_tables, all_measures, all_columns, expressions
    (owner, parsed DAX), objects, brief, usage, add(code, object, message, level, keys)."""
    tables = context["tables"]
    add = context["add"]
    objects = context["objects"]
    automatic = context["automatic"]
    rels = [r for r in relationships(context) if r["from"][0] not in automatic and r["to"][0] not in automatic]
    column_at = {(t["name"], c["name"]): (t, c) for t, c in context["all_columns"]}
    measure_names = {m["name"].lower() for _, m in context["all_measures"]}
    roles = [o for o in objects if o["kind"] == "role" and o["top"] and not o["translation"]]
    permissions = [o for o in objects if o["kind"] == "tablepermission" and not o["translation"]]
    functions = [o for o in objects if o["kind"] == "function" and o["top"] and not o["translation"]]
    function_names = {f["name"].upper() for f in functions}
    direct_query = {t["name"] for t in tables.values() if "directquery" in table_modes(t)}
    index = dax_index()
    secured = {p["name"] for p in permissions if (p["expr"] or "").strip()}

    _integrity(context, rels, column_at, measure_names, function_names, index)
    _dates(context, index)
    _relationships(context, rels, column_at, roles, secured)
    _columns(context, rels, column_at)
    _dax(context, measure_names, direct_query, index)
    _style(context)
    _security(context, rels, permissions, secured)
    _storage(context, rels, column_at, direct_query)
    _objects(context, functions, function_names)
    _power_query(context, direct_query)
    _suggestions(context, rels, direct_query, index)
    _more(context, rels, column_at, permissions, functions, direct_query)


# ---------------------------------------------------------------- things that stop a model from loading

def _integrity(context, rels, column_at, measure_names, function_names, index):
    tables, add = context["tables"], context["add"]
    for relationship in context["model"]["relationships"]:
        for key in ("fromcolumn", "tocolumn"):
            end = _reference(relationship["props"].get(key, ""))
            if end is None or end[1] is None:
                continue
            if end[0].startswith(tuple(context["auto_prefixes"])):
                continue
            if end not in column_at and not (end[0] in tables and any(c["name"] == end[1] for c in tables[end[0]]["columns"])):
                add("M901", relationship, "relationship '%s' names %s[%s], which the model does not have; the model "
                    "will not load" % (relationship["name"], end[0], end[1]), keys=(relationship["name"],))
    for table in context["own_tables"]:
        names = {c["name"] for c in table["columns"]}
        for hierarchy in table["hierarchies"]:
            for level in hierarchy.get("levels", []):
                if level and level not in names:
                    add("M902", hierarchy, "hierarchy '%s' of table '%s' has a level on column '%s', which the table "
                        "does not have" % (hierarchy["name"], table["name"], level),
                        keys=("%s[%s]" % (table["name"], hierarchy["name"]),))
        for column in table["columns"]:
            key = "%s[%s]" % (table["name"], column["name"])
            target = _reference(column["props"].get("sortbycolumn", ""))
            if target and target[0] not in names:
                add("M903", column, "column %s is sorted by '%s', which table '%s' does not have"
                    % (key, target[0], table["name"]), keys=(key,))
            if (not column.get("calculated") and not column["props"].get("sourcecolumn")
                    and not table["calculated"] and not table.get("calculation_group")):
                add("M904", column, "column %s has no sourceColumn; a data column needs the name of the source "
                    "column it reads; Microsoft's rule says processing the model then gives an error" % key, keys=(key,))
            if column["props"].get("isavailableinmdx", "").lower() == "false":
                used = [what for what, hit in (
                    ("sorts another column", any(_reference(c["props"].get("sortbycolumn", "")) == (column["name"], None)
                                                 for c in table["columns"])),
                    ("is sorted by another column", bool(column["props"].get("sortbycolumn"))),
                    ("is a hierarchy level", any(column["name"] in h.get("levels", []) for h in table["hierarchies"])))
                    if hit]
                if used:
                    add("M907", column, "column %s has isAvailableInMdx off but %s; Microsoft's rule says this "
                        "causes an error, so turn it back on" % (key, " and ".join(used)), keys=(key,))
    for obj in context["objects"]:
        if obj["translation"] or obj["kind"] not in ("table", "column", "measure", "hierarchy", "level", "role",
                                                      "calculationitem", "perspective", "partition", "function"):
            continue
        if any(ord(ch) < 32 and ch not in "\t\n\r" for ch in obj["name"] + obj["description"]):
            add("M906", obj, "%s '%s' has a control character in its name or description; remove it"
                % (obj["kind"], obj["name"].encode("unicode_escape").decode("ascii")), keys=(obj["name"],))
    for owner, parsed in context["expressions"]:
        if owner["kind"] in ("measure", "calculationitem") or (owner["kind"] == "column" and owner.get("calculated")):
            if owner["has_expr"] and not parsed["tokens"]:
                add("M905", owner, "%s has an empty expression; give it a formula or remove it" % _label(owner),
                    keys=(_label(owner),))
        unknown = set()
        strange = set()
        for table_name, name, _ in parsed["references"]:
            if table_name is None or table_name not in tables:
                continue
            table = tables[table_name]
            if (name.lower() not in {c["name"].lower() for c in table["columns"]}
                    and name.lower() not in measure_names):
                unknown.add("%s[%s]" % (table_name, name))
        if unknown:
            add("M908", owner, "DAX of %s names %s, which the model does not have; the formula returns an error"
                % (_label(owner), ", ".join(sorted(unknown))), keys=(_label(owner),))
        if index["functions"]:
            variables = fs.dax_variables(parsed["tokens"])
            for call in parsed["calls"]:
                name = call.name
                if (name not in index["functions"] and name not in function_names and name not in DAX_NOT_FUNCTIONS
                        and name.lower() not in variables and name not in context["table_names_upper"]):
                    strange.add(name)
        if strange:
            add("M909", owner, "DAX of %s calls %s, which is neither in the DAX function index nor a function of this "
                "model. Check the name on Microsoft Learn (skill pbi-lookup)" % (_label(owner), ", ".join(sorted(strange))),
                level="warn", keys=(_label(owner),))


# ---------------------------------------------------------------- dates

def _dates(context, index):
    tables, add = context["tables"], context["add"]
    automatic = sorted(context["automatic"])
    model_object = context["model_object"]
    switched_on = model_object is not None and model_object["annotations"].get(AUTO_DATE_ANNOTATION, "").strip() == "1"
    if (automatic or switched_on) and model_object is not None:
        what = ("the model holds %d hidden date table(s) Power BI made (%s%s)"
                % (len(automatic), ", ".join(automatic[:3]), " ..." if len(automatic) > 3 else "")) if automatic \
            else "model.tmdl carries the annotation %s = 1" % AUTO_DATE_ANNOTATION
        add("M401", model_object, "Auto date/time is on: %s. Turn it off in Power BI Desktop (Options, Current File, "
            "Time intelligence) and use one date table" % what, level="warn", keys=("model",))
    marked = [t for t in context["own_tables"] if t["props"].get("datacategory", "").lower() == "time"]
    has_calendar = any(o["kind"] == "calendar" for o in context["objects"])
    time_users = sorted({_label(owner) for owner, parsed in context["expressions"]
                         if any(call.name in index["time"] for call in parsed["calls"])})
    anchor = model_object or (context["own_tables"][0]["objects"][0] if context["own_tables"] else None)
    if anchor is None:
        return
    if not marked and not has_calendar:
        if time_users:
            add("M402", anchor, "time intelligence is used (%s%s) but no table is marked as a date table; the "
                "checklist expects one dedicated date table. Mark it: dataCategory Time on the table and isKey on its "
                "date column" % (", ".join(time_users[:4]), " ..." if len(time_users) > 4 else ""), keys=("model",))
        elif any(c["props"].get("datatype", "").lower() == "datetime" for _, c in context["all_columns"]):
            add("M403", anchor, "the model has date columns but no table marked as a date table", level="warn",
                keys=("model",))
    for table in context["own_tables"]:
        name = table["name"].upper()
        if ("DATE" in name or "CALENDAR" in name) and table["name"] not in context["measure_tables"]:
            is_marked = table["props"].get("datacategory", "").lower() == "time" and any(
                c["props"].get("iskey", "").lower() == "true" and c["props"].get("datatype", "").lower() == "datetime"
                for c in table["columns"])
            if not is_marked:
                add("M404", table["objects"][0], "table '%s' looks like a date table but is not marked as one "
                    "(dataCategory Time on the table, isKey on its date column)" % table["name"], level="warn",
                    keys=(table["name"],))


# ---------------------------------------------------------------- relationships and the star schema

def _relationships(context, rels, column_at, roles, secured):
    tables, add = context["tables"], context["add"]
    used_pairs = set()
    for owner, parsed in context["expressions"]:
        for call in _calls(parsed, "USERELATIONSHIP"):
            ends = []
            for span in call.args[:2]:
                stream = parsed["tokens"][span[0]:span[1]]
                if len(stream) == 2 and stream[1].kind == fs.BRACKET_NAME:
                    ends.append((stream[0].value.lower(), stream[1].value.lower()))
            if len(ends) == 2:
                used_pairs.add(frozenset(ends))
                for end in ends:
                    table_name = next((t for t in tables if t.lower() == end[0]), None)
                    if table_name in secured and call.args:
                        other = ends[1] if end == ends[0] else ends[0]
                        target = ends[1][0]
                        if end[0] == target:
                            add("M415", owner, "DAX of %s uses USERELATIONSHIP towards table '%s', which has a "
                                "row-level security rule. Microsoft's rule says this combination raises an error"
                                % (_label(owner), table_name), keys=(_label(owner),))
                        del other
    special = sum(1 for r in rels if r["both"] or (r["from_many"] and r["to_many"]))
    for r in rels:
        many_many = r["from_many"] and r["to_many"]
        one_one = not r["from_many"] and not r["to_many"]
        if r["both"] and not many_many and not one_one:
            add("M405", r["object"], "relationship %s filters in both directions; the checklist targets none. Use a "
                "single direction, or CROSSFILTER in the one measure that needs it, or list the reason in the brief"
                % r["label"], level="warn", keys=(r["label"],))
        if many_many:
            add("M406", r["object"], "relationship %s is many-to-many. Check that a shared dimension or a bridge "
                "table would not model it better, and list the reason in the brief" % r["label"], level="warn",
                keys=(r["label"],))
            if r["both"]:
                add("M407", r["object"], "many-to-many relationship %s filters in both directions; Microsoft's rule "
                    "asks for a single direction" % r["label"], level="warn", keys=(r["label"],))
        if one_one:
            add("M409", r["object"], "relationship %s is one-to-one. Microsoft advises merging the two tables into "
                "one where the rows describe the same thing" % r["label"], level="warn", keys=(r["label"],))
        if not r["active"]:
            pair = frozenset(((r["from"][0].lower(), r["from"][1].lower()), (r["to"][0].lower(), r["to"][1].lower())))
            if pair not in used_pairs:
                add("M410", r["object"], "relationship %s is inactive and no formula turns it on with USERELATIONSHIP. "
                    "Use it in a measure, or remove it" % r["label"], level="warn", keys=(r["label"],))
        if not r["to_many"] and r["to"] in column_at:
            table, column = column_at[r["to"]]
            if (column["props"].get("iskey", "").lower() != "true"
                    and table["props"].get("datacategory", "").lower() != "time"):
                add("M413", column, "column %s[%s] is the one side of a relationship but is not marked as the key "
                    "(isKey)" % r["to"], level="warn", keys=("%s[%s]" % r["to"],))
    if rels and special / float(len(rels)) > MANY_TO_MANY_SHARE and context["model_anchor"] is not None:
        add("M408", context["model_anchor"], "%d of the %d relationships filter in both directions or are "
            "many-to-many (more than %d%%); review the model's design" % (special, len(rels), MANY_TO_MANY_SHARE * 100),
            level="warn", keys=("model",))
    if roles and any(not r["active"] for r in rels) and context["model_anchor"] is not None:
        add("M414", context["model_anchor"], "the model has security roles and inactive relationships (%s). A "
            "row-level security filter never travels over an inactive relationship: check each role"
            % ", ".join(r["label"] for r in rels if not r["active"]), level="warn", keys=("model",))
    related = {r["from"][0] for r in rels} | {r["to"][0] for r in rels}
    from_tables = {r["from"][0] for r in rels if r["from_many"] and not r["to_many"]}
    to_tables = {r["to"][0] for r in rels if r["from_many"] and not r["to_many"]}
    plain = [t for t in context["own_tables"] if t["name"] not in context["measure_tables"]
             and not t.get("calculation_group") and not t.get("field_parameter") and not t.get("parameter_table")]
    for table in plain:
        name = table["name"]
        if name not in related and len(plain) > 1:
            add("M411", table["objects"][0], "table '%s' has no relationship. Relate it, or list it in the brief "
                "with its purpose (a table that only feeds a slicer or a formula is a valid reason)" % name,
                level="warn", keys=(name,))
        if name in from_tables and name in to_tables:
            add("M412", table["objects"][0], "table '%s' is the many side of one relationship and the one side of "
                "another (a snowflake). Microsoft advises one flat dimension table where practical" % name,
                level="warn", keys=(name,))


# ---------------------------------------------------------------- columns

def _columns(context, rels, column_at):
    add = context["add"]
    one_side_of = {}
    for r in rels:
        if r["from_many"] and not r["to_many"]:
            one_side_of.setdefault(r["from"][0], set()).add(r["to"][0])
    in_relationship = {r["from"] for r in rels} | {r["to"] for r in rels}
    for table in context["own_tables"]:
        if table["name"] in context["measure_tables"]:
            continue
        month_columns = [c for c in table["columns"] if c["props"].get("datatype", "").lower() in ("int64", "decimal", "double")
                         and any(month in c["name"].lower() for month in MONTHS)]
        if len({m for m in MONTHS if any(m in c["name"].lower() for c in month_columns)}) == 12:
            add("M417", table["objects"][0], "table '%s' has a number column for each month. Unpivot them in Power "
                "Query into one month column and one value column" % table["name"], level="warn", keys=(table["name"],))
        hierarchy_names = {h["name"].lower() for h in table["hierarchies"]}
        if len(table["partitions"]) == 1 and table["partitions"][0]["name"] != table["name"]:
            add("M117", table["partitions"][0], "table '%s' has one partition, named '%s'; give the partition the "
                "table's name" % (table["name"], table["partitions"][0]["name"]), level="warn", keys=(table["name"],))
        for column in table["columns"]:
            key = "%s[%s]" % (table["name"], column["name"])
            name = column["name"]
            lower = name.lower()
            kind = column["props"].get("datatype", "").lower()
            visible = not (table["hidden"] or column["hidden"])
            if (kind == "string" and "month" in lower and "months" not in lower
                    and not column["props"].get("sortbycolumn")):
                add("M113", column, "text column %s looks like a month name and has no sortByColumn, so it sorts "
                    "by the alphabet" % key, level="warn", keys=(key,))
            if not column["props"].get("datacategory") and visible:
                place = kind == "string" and any(word in lower for word in PLACE_WORDS)
                point = lower in ("latitude", "longitude") and kind in ("decimal", "double")
                if place or point:
                    add("M114", column, "column %s looks like a place and has no data category; set dataCategory so "
                        "that maps read it correctly" % key, level="warn", keys=(key,))
            if (table["name"], name) not in in_relationship:
                twins = [other for other in one_side_of.get(table["name"], ())
                         if (other, name) in column_at]
                if twins:
                    add("M115", column, "column %s is also in the related table '%s'; keep it in one place"
                        % (key, twins[0]), level="warn", keys=(key,))
            if visible and ((name.startswith("Is") and kind == "int64") or (name.endswith(" Flag") and kind != "string")):
                add("M116", column, "flag column %s shows numbers; Microsoft's rule asks for Yes and No as text"
                    % key, level="warn", keys=(key,))
            if lower in hierarchy_names:
                add("M119", column, "column %s has the same name as a hierarchy of its table; Microsoft Learn asks "
                    "for different names" % key, level="warn", keys=(key,))
        for obj in [table["objects"][0]] + table["columns"] + table["hierarchies"]:
            if table["hidden"] or obj["hidden"]:
                continue                    # the default is for names report authors see; hidden keys keep source names
            problems = _table_column_name(obj["name"], context["brief"])
            if problems:
                shown = obj["name"] if obj["kind"] == "table" else "%s[%s]" % (table["name"], obj["name"])
                add("M118", obj, "%s name '%s': %s. Renaming follows the brief (model standard, 'Existing models')"
                    % (obj["kind"], obj["name"], "; ".join(problems)), level="warn", keys=(shown,))


def _table_column_name(name, brief):
    """Problems of a table, column or hierarchy name against the default naming of the model standard."""
    problems = []
    own = brief["own_spelling"]
    if name != name.strip():
        problems.append("it starts or ends with a space")
    if "\t" in name:
        problems.append("it holds a tab")
    stripped = name.strip()
    if stripped[:1].isalpha() and stripped[:1].islower() and stripped.split()[0] not in own:
        problems.append("it does not start with a capital")
    if "_" in stripped and stripped not in own and not stripped.startswith("_"):
        problems.append("it uses underscores instead of spaces")
    if any(re.search(r"[a-z][A-Z]", word) and word not in own for word in stripped.split()):
        problems.append("it runs words together")
    if re.match(r"(?i)(dim|fact|stg)[ _A-Z]", stripped) and stripped.split()[0] not in own:
        problems.append("it carries a technical prefix")
    return problems


# ---------------------------------------------------------------- DAX

def _dax(context, measure_names, direct_query, index):
    add = context["add"]
    formulas = {}
    for owner, parsed in context["expressions"]:
        if owner["kind"] not in ("measure", "column", "calculationitem", "tablepermission", "function", "partition"):
            continue
        stream = parsed["tokens"]
        label = _label(owner)
        keys = (label,)
        found = [call.name for call in parsed["calls"]]

        used = sorted(set(found) & set(ERROR_FUNCTIONS))
        if used:
            add("M501", owner, "DAX of %s uses %s. Microsoft advises against it: it scans every row and hides real "
                "errors. Use DIVIDE for a division, or test the cause with IF" % (label, ", ".join(used)),
                level="warn", keys=keys)

        divisions = []
        for position, token in enumerate(stream):
            if fs.is_symbol(token, "/"):
                after = stream[position + 1] if position + 1 < len(stream) else None
                if after is None or after.kind != "number":
                    divisions.append(token.line)
        if divisions:
            add("M502", owner, "DAX of %s divides with '/' by something that is not a fixed number (%d place(s)). "
                "Use DIVIDE, which handles a zero or blank divisor; the checklist asks for it in every such division"
                % (label, len(divisions)), keys=keys)

        if owner["kind"] == "measure" and len(parsed["calls"]) == 1:
            call = parsed["calls"][0]
            if (call.name in ("COUNT", "COUNTA") and call.at == 0 and call.close == len(stream) - 1
                    and len(call.args) == 1):
                add("M503", owner, "measure %s counts with %s over a column. If it counts rows, use COUNTROWS on the "
                    "table: it says what is meant and does not depend on blanks in one column" % (label, call.name),
                    level="warn", keys=keys)

        one_value = {_span_text(parsed, c.args[0]) for c in _calls(parsed, "HASONEVALUE") if c.args}
        values = {_span_text(parsed, c.args[0]) for c in _calls(parsed, "VALUES") if c.args}
        if one_value & values:
            add("M504", owner, "DAX of %s tests HASONEVALUE and then reads VALUES of the same column; "
                "SELECTEDVALUE does both" % label, level="warn", keys=keys)

        for call in _calls(parsed, "CALCULATE", "CALCULATETABLE"):
            for span in call.args[1:]:
                first = stream[span[0]] if span[0] < span[1] else None
                if first is None or first.kind != "word" or first.value.upper() != "FILTER":
                    continue
                inner = next((c for c in parsed["calls"] if c.at == span[0]), None)
                if inner is None or not inner.args:
                    continue
                table_span = inner.args[0]
                if table_span[1] - table_span[0] == 1 and stream[table_span[0]].kind in ("word", fs.QUOTED_NAME):
                    add("M505", owner, "DAX of %s passes FILTER over the whole table '%s' to %s. Filter the column "
                        "itself (a true/false test on the column, or KEEPFILTERS), or FILTER over VALUES of the column "
                        "when the test is on a measure" % (label, stream[table_span[0]].value, call.name),
                        level="warn", keys=keys)
                    break

        blanks = []
        for call in parsed["calls"]:
            last = _span_text(parsed, call.args[-1]) if call.args else ""
            if call.name == "IF" and len(call.args) >= 2 and _span_text(parsed, call.args[1]) == "0":
                test = stream[call.args[0][0]]
                if test.kind == "word" and test.value.upper() == "ISBLANK":
                    blanks.append("IF ( ISBLANK ( ... ), 0, ... )")
            elif call.name == "COALESCE" and len(call.args) >= 2 and last == "0":
                blanks.append("COALESCE ( ..., 0 )")
            elif call.name == "DIVIDE" and len(call.args) == 3 and last == "0":
                blanks.append("DIVIDE ( ..., ..., 0 )")
        if len(stream) >= 3 and fs.is_symbol(stream[-2], "+") and stream[-1].kind == "number" and float_or_none(stream[-1].value) == 0:
            blanks.append("+ 0")
        if owner["kind"] == "measure" and blanks:
            add("M506", owner, "measure %s turns a blank into a value (%s). Microsoft advises returning blank: "
                "visuals then leave empty groups out and queries stay fast. Keep it only when the brief asks for a zero"
                % (label, ", ".join(sorted(set(blanks)))), level="warn", keys=keys)

        seen = {}
        for call in parsed["calls"]:
            if call.close - call.at + 1 >= REPEAT_TOKENS:
                seen.setdefault(fs.text_of(stream, call.at, call.close + 1), []).append(call)
        repeated = {text: group for text, group in seen.items() if len(group) > 1}
        outer = [text for text in repeated
                 if not any(other != text and text in other for other in repeated)]
        if outer:
            add("M507", owner, "DAX of %s writes the same expression %d times: %s. Store it in a variable (VAR): "
                "it is worked out once and the formula reads better"
                % (label, len(repeated[outer[0]]), outer[0][:80] + (" ..." if len(outer[0]) > 80 else "")),
                level="warn", keys=keys)

        if owner["kind"] == "measure":
            if len(stream) == 1 and stream[0].kind == fs.BRACKET_NAME and stream[0].value.lower() in measure_names:
                add("M509", owner, "measure %s only repeats measure [%s]; use that measure and remove this one"
                    % (label, stream[0].value), level="warn", keys=keys)
            elif stream:
                formulas.setdefault(fs.text_of(stream), []).append(owner)

        if "INTERSECT" in found:
            add("M510", owner, "DAX of %s uses INTERSECT; for a relationship made in a formula, Microsoft's rule "
                "asks for TREATAS" % label, level="warn", keys=keys)
        for position, token in enumerate(stream[:-2]):
            if not (token.kind == "number" and stream[position + 1].kind == "symbol" and stream[position + 1].value in "+-"
                    and (position == 0 or stream[position - 1].kind == "symbol")):
                continue
            then = position + 2
            while then < len(stream) and fs.is_symbol(stream[then], "("):
                then += 1
            ratio = then < len(stream) and stream[then].kind == "word" and stream[then].value.upper() == "DIVIDE"
            if not ratio and then + 1 < len(stream) and stream[then].kind == "word" and fs.is_symbol(stream[then + 1], "("):
                closer = fs.match_close(stream, then + 1)          # 1 - SUM ( x ) / ...
                ratio = closer + 1 < len(stream) and fs.is_symbol(stream[closer + 1], "/")
            if ratio:
                add("M511", owner, "DAX of %s is written as a number plus or minus a ratio (such as 1 - x / y). "
                    "Microsoft's rule asks for one DIVIDE of the difference: it returns blank where the ratio does"
                    % label, level="warn", keys=keys)
                break
        if set(found) & set(TOOL_FUNCTIONS):
            add("M512", owner, "DAX of %s still calls EVALUATEANDLOG, a function for testing; remove it" % label,
                level="warn", keys=keys)
        if direct_query and owner["kind"] in ("measure", "calculationitem"):
            used = sorted(set(found) & index["time"])
            if used:
                add("M513", owner, "DAX of %s uses time intelligence (%s) in a model with DirectQuery tables; "
                    "Microsoft's rule says these functions perform poorly there. Consider columns in the date table "
                    "and plain filters" % (label, ", ".join(used)), level="warn", keys=keys)
        used = sorted(set(found) & set(ROW_FUNCTIONS))
        if used:
            add("M514", owner, "DAX of %s uses %s; a variable holds the outer value more clearly" % (label, ", ".join(used)),
                level="warn", keys=keys)
        for call in _calls(parsed, *WINDOW_FUNCTIONS):
            inside = {c.name for c in parsed["calls"] if call.open < c.at < call.close}
            if "ORDERBY" not in inside:
                add("M516", owner, "DAX of %s calls %s without ORDERBY; state the order so the result does not "
                    "depend on a default" % (label, call.name), level="warn", keys=keys)
                break
        if "HASONEVALUE" not in found and "SELECTEDVALUE" not in found:
            for call in _calls(parsed, "VALUES"):
                after = stream[call.close + 1] if call.close + 1 < len(stream) else None
                before = stream[call.at - 1] if call.at else None
                if any(t is not None and t.kind == "symbol" and t.value in ("=", "<>") for t in (after,)) \
                        and not (before is not None and before.kind == "word" and before.value.upper() == "IN"):
                    add("M517", owner, "DAX of %s compares VALUES of a column with one value. With more than one "
                        "value in the filter this returns an error; use SELECTEDVALUE" % label, level="warn", keys=keys)
                    break
    for text, owners in sorted(formulas.items()):
        if len(owners) > 1:
            names = ", ".join("[%s]" % o["name"] for o in owners)
            add("M508", owners[1], "measures %s have the same formula; keep one and use it everywhere" % names,
                level="warn", keys=tuple("[%s]" % o["name"] for o in owners))


OPERATORS = frozenset(("+", "-", "*", "/", "&", "=", "<", ">", "<=", ">=", "<>", "&&", "||"))
TEMPORARY_COLUMN_FUNCTIONS = ("ADDCOLUMNS", "SELECTCOLUMNS")


def style_problems(parsed, temporary_columns):
    """Which rules of the DAX style one formula breaks (short texts). The style follows SQLBI's formatting rules."""
    stream = parsed["tokens"]
    problems = set()
    tables = {position - 1 for table, _, position in parsed["references"] if table is not None}
    for position, token in enumerate(stream):
        before = stream[position - 1] if position else None
        after = stream[position + 1] if position + 1 < len(stream) else None
        if token.kind == "symbol":
            if token.value == "(":
                if before is not None and before.kind == fs.BRACKET_NAME:
                    problems.add("write CALCULATE in full, not [Measure] ( filter )")
                elif before is not None and before.kind == "word" and before.end == token.start:
                    problems.add("put a space between a function name and '('")
                if before is not None and before.line != token.line:
                    problems.add("keep '(' on the line of its function name")
            elif token.value == ")":
                if before is not None and before.end == token.start and not fs.is_symbol(before, "("):
                    problems.add("put a space before ')'")
            elif token.value == ",":
                if before is not None and (before.line != token.line or before.end != token.start):
                    problems.add("put each comma directly after its argument")
                if after is not None and after.line == token.line and after.start == token.end:
                    problems.add("put a space after a comma")
            elif token.value in OPERATORS:
                unary = token.value in "+-" and (before is None or (before.kind == "symbol" and before.value not in ")"))
                if not unary:
                    if (before is not None and before.end == token.start) or (after is not None and after.start == token.end):
                        problems.add("put a space on both sides of an operator")
                    declares = (token.value == "=" and position >= 2 and stream[position - 2].kind == "word"
                                and stream[position - 2].value.upper() == "VAR")
                    if after is not None and after.line != token.line and not declares:
                        problems.add("start a continued line with the operator, do not end the line before with it")
        elif position in tables and after is not None and after.start != token.end:
            problems.add("write a column directly after its table, with no space: Table[Column]")
    for call in parsed["calls"]:
        if call.close >= len(stream):
            continue
        one_line = stream[call.at].line == stream[call.close].line
        nested = any(other.at > call.open and other.close < call.close for other in parsed["calls"])
        if one_line and (len(call.args) >= 2 or nested):
            problems.add("put each argument on its own line when a function has two or more arguments, or holds "
                         "another function")
        if temporary_columns and call.name in TEMPORARY_COLUMN_FUNCTIONS:
            for span in call.args[1:]:
                if span[1] - span[0] == 1 and stream[span[0]].kind == fs.TEXT and not stream[span[0]].value.startswith("@"):
                    problems.add("start the name of a column the formula makes with @")
    return sorted(problems)


def _style(context):
    """M520: one finding for each table file, listing the formulas that break the DAX style."""
    by_file = {}
    for owner, parsed in context["expressions"]:
        if owner["kind"] not in ("measure", "column", "calculationitem", "function", "tablepermission"):
            continue
        problems = style_problems(parsed, owner["kind"] in ("measure", "calculationitem", "function"))
        if problems:
            by_file.setdefault(owner["file"], []).append((owner, problems))
    for path in sorted(by_file):
        kept = [(owner, problems) for owner, problems in by_file[path]
                if not context["excused"]("M520", _label(owner))]
        if not kept:
            continue
        rules = sorted({p for _, problems in kept for p in problems})
        names = ", ".join(_label(owner) for owner, _ in kept[:8]) + (" ..." if len(kept) > 8 else "")
        context["findings"].add("M520", path, kept[0][0]["line"], "%d formula(s) in this file do not follow the DAX "
                                "style (%s): %s" % (len(kept), names, "; ".join(rules)), level="warn")


def float_or_none(text):
    try:
        return float(text)
    except ValueError:
        return None


# ---------------------------------------------------------------- security

def _security(context, rels, permissions, secured):
    tables, add = context["tables"], context["add"]
    parsed_by_id = {id(owner): parsed for owner, parsed in context["expressions"]}
    many_side = {r["from"][0] for r in rels if r["from_many"] and not r["to_many"]}
    one_side = {r["to"][0] for r in rels if r["from_many"] and not r["to_many"]}
    used_fields = {(entity, prop) for _, entity, prop in context["usage"] if isinstance(prop, str)}
    for permission in permissions:
        role = permission["parent"]["name"] if permission["parent"] else "?"
        label = _label(permission)
        keys = ("%s/%s" % (role, permission["name"]),)
        parsed = parsed_by_id.get(id(permission))
        if parsed is not None and parsed["tokens"]:
            found = {call.name for call in parsed["calls"]}
            used = sorted(found & set(RLS_TEXT_FUNCTIONS))
            if used:
                add("M601", permission, "the rule of %s uses %s. Such functions run for every row and slow every "
                    "query; store the value to compare in a column and keep the rule a plain comparison"
                    % (label, ", ".join(used)), level="warn", keys=keys)
            if permission["name"] in many_side and permission["name"] not in one_side:
                add("M602", permission, "the rule of %s filters a fact table. Microsoft advises filtering a "
                    "dimension table and letting the relationship pass the filter on" % label, level="warn", keys=keys)
            if "USERNAME" in found:
                add("M603", permission, "the rule of %s uses USERNAME, which gives a different form of name in "
                    "Power BI Desktop and in the service; use USERPRINCIPALNAME" % label, level="warn", keys=keys)
            stream = parsed["tokens"]
            if found & {"USERNAME", "USERPRINCIPALNAME"} and stream and len(stream) >= 3:
                tail = fs.text_of(stream, len(stream) - 4) if len(stream) >= 4 else ""
                if tail.replace(" ", "").endswith("TRUE())") or tail.replace(" ", "").endswith(",TRUE)"):
                    add("M605", permission, "the rule of %s ends in TRUE for everyone it does not name, so an unknown "
                        "user sees every row. End in FALSE instead" % label, level="warn", keys=keys)
        if any(r["from_many"] and r["to_many"] and permission["name"] in (r["from"][0], r["to"][0]) for r in rels) \
                and permission["name"] in secured:
            add("M604", permission, "table '%s' has a row-level security rule and a many-to-many relationship; "
                "Microsoft's rule says this performs poorly" % permission["name"], level="warn", keys=keys)
        hidden_columns = [o["name"] for o in context["objects"]
                          if o["kind"] == "columnpermission" and o["parent"] is permission
                          and "none" in ((o["expr"] or "").strip().lower(), o["props"].get("metadatapermission", "").lower())]
        whole_table = permission["props"].get("metadatapermission", "").lower() == "none"
        broken = sorted({"%s[%s]" % (e, p) for e, p in used_fields
                         if e == permission["name"] and (whole_table or p in hidden_columns)})
        if broken:
            add("M606", permission, "role '%s' hides %s with object-level security, and report visuals use %s. For "
                "people in that role those visuals fail" % (role, "table '%s'" % permission["name"] if whole_table
                                                            else "column(s) %s" % ", ".join(hidden_columns),
                                                            ", ".join(broken[:6])), level="warn", keys=keys)
    by_role = {}
    for permission in permissions:
        role = permission["parent"]["name"] if permission["parent"] else "?"
        kinds = by_role.setdefault(role, {"rows": False, "objects": False, "first": permission})
        kinds["rows"] = kinds["rows"] or bool((permission["expr"] or "").strip())
        kinds["objects"] = kinds["objects"] or permission["props"].get("metadatapermission", "").lower() == "none" or any(
            o["kind"] == "columnpermission" and o["parent"] is permission for o in context["objects"])
        if permission["props"].get("metadatapermission", "").lower() == "none" \
                and permission["name"] in many_side and permission["name"] in one_side:
            add("M608", permission, "role '%s' hides table '%s' with object-level security, and that table sits "
                "between two other tables in a chain of relationships. Microsoft says this gives an error at design "
                "time: secure the columns instead, or change the design" % (role, permission["name"]),
                keys=("%s/%s" % (role, permission["name"]),))
    rows_only = sorted(r for r, k in by_role.items() if k["rows"] and not k["objects"])
    objects_only = sorted(r for r, k in by_role.items() if k["objects"] and not k["rows"])
    if rows_only and objects_only:
        add("M607", by_role[objects_only[0]]["first"], "role(s) %s filter rows and role(s) %s hide objects. A person "
            "in one of each gets an error at query time: Microsoft asks for row-level and object-level security in the "
            "same role" % (", ".join(rows_only), ", ".join(objects_only)), level="warn", keys=("model",))
    del tables


# ---------------------------------------------------------------- storage modes

def _storage(context, rels, column_at, direct_query):
    tables, add = context["tables"], context["add"]
    parsed_by_id = {id(owner): parsed for owner, parsed in context["expressions"]}
    for table in context["own_tables"]:
        modes = table_modes(table)
        if "directquery" in modes:
            for column in table["columns"]:
                if not column.get("calculated"):
                    continue
                key = "%s[%s]" % (table["name"], column["name"])
                parsed = parsed_by_id.get(id(column))
                found = {call.name for call in parsed["calls"]} if parsed else set()
                heavy = sorted(found & (set(ITERATORS) | {"CALCULATE", "CALCULATETABLE"}))
                if heavy:
                    add("M705", column, "calculated column %s sits in a DirectQuery table and uses %s. Microsoft says "
                        "such a column returns an error when a visual uses it: keep the formula to values of the same "
                        "row, or build the column at the source" % (key, ", ".join(heavy)), keys=(key,))
                if any((table["name"], column["name"]) in (r["from"], r["to"]) for r in rels) \
                        and "COMBINEVALUES" not in found:
                    add("M704", column, "calculated column %s of a DirectQuery table is used in a relationship; "
                        "Microsoft advises a real source column (COMBINEVALUES is the one exception)" % key,
                        level="warn", keys=(key,))
        policy = table.get("refresh_policy")
        if policy is not None:
            names = {o["name"] for o in context["objects"] if o["kind"] == "expression" and o["top"]}
            missing = [n for n in ("RangeStart", "RangeEnd") if n not in names]
            if missing:
                add("M707", policy, "table '%s' has an incremental refresh policy but the model has no parameter "
                    "named %s. Microsoft requires both RangeStart and RangeEnd, spelled this way, of type Date/Time"
                    % (table["name"], " and ".join(missing)), keys=(table["name"],))
            wrong = []
            for obj in context["objects"]:
                if obj["kind"] == "expression" and obj["top"] and obj["name"] in ("RangeStart", "RangeEnd"):
                    stream = fs.tokens(obj["expr"] or "", fs.M)
                    if not any((t.kind == fs.TEXT and t.value == "DateTime") or (t.kind == "word" and t.value == "#datetime")
                               for t in stream):
                        wrong.append(obj["name"])
            if wrong:
                add("M707", policy, "table '%s' has an incremental refresh policy, and parameter %s is not of type "
                    "Date/Time. Microsoft requires that type, also when the source column is a number"
                    % (table["name"], " and ".join(wrong)), keys=(table["name"],))
            stream = fs.tokens(policy["props"].get("sourceexpression", "") or next(
                (p["props"].get("source", "") for p in table["partitions"]), ""), fs.M)
            closed = {"RangeStart": False, "RangeEnd": False}
            for position, token in enumerate(stream):
                if token.kind == "word" and token.value in closed:
                    before = stream[position - 1] if position else None
                    after = stream[position + 1] if position + 1 < len(stream) else None
                    if any(t is not None and t.kind == "symbol" and t.value in ("<=", ">=") for t in (before, after)):
                        closed[token.value] = True
            if all(closed.values()):
                add("M709", policy, "the query of table '%s' compares with RangeStart and with RangeEnd and includes "
                    "both ends (>= and <=). Microsoft says a row on a boundary can then be loaded twice: include one "
                    "end only (>= RangeStart and < RangeEnd)" % table["name"], keys=(table["name"],))
    for r in rels:
        if r["from"][0] in direct_query and r["from_many"] and not r["to_many"]:
            other = tables.get(r["to"][0])
            if other is not None and table_modes(other) == {"import"} and not other["calculated"] \
                    and not other.get("calculation_group"):
                add("M706", other["objects"][0], "table '%s' is imported and filters the DirectQuery table '%s'. If "
                    "both come from the same source, Microsoft advises Dual storage mode for the dimension"
                    % (other["name"], r["from"][0]), level="warn", keys=(other["name"],))
    del column_at


# ---------------------------------------------------------------- functions, calculation groups, field parameters

def _objects(context, functions, function_names):
    tables, add = context["tables"], context["add"]
    parsed_by_id = {id(owner): parsed for owner, parsed in context["expressions"]}
    level = context["compatibility_level"]
    builtin = dax_index()["functions"]
    for function in functions:
        name = function["name"]
        keys = (name,)
        if level is not None and level < UDF_LEVEL:
            add("M801", function, "function %s needs compatibility level %d or higher; the model is at %d"
                % (name, UDF_LEVEL, level), keys=keys)
        problems = []
        if not UDF_NAME.match(name):
            problems.append("a name uses only letters, digits, underscores and single dots between parts")
        if name.upper() in builtin or name.upper() in fs.DAX_KEYWORDS:
            problems.append("it is the name of a built-in DAX function or keyword")
        if name.lower() in {t.lower() for t in tables}:
            problems.append("it is the name of a table")
        if problems:
            add("M802", function, "function name '%s' breaks Microsoft's naming rules: %s" % (name, "; ".join(problems)),
                keys=keys)
        if not function["described"]:
            add("M803", function, "function %s has no '///' description; say what it returns and what each "
                "parameter means" % name, level="warn", keys=keys)
        parsed = parsed_by_id.get(id(function))
        if parsed is None:
            continue
        stream = parsed["tokens"]
        if stream and fs.is_symbol(stream[0], "("):
            closer = fs.match_close(stream, 0)
            untyped = []
            for span in fs.split_arguments(stream, 0, closer):
                words = stream[span[0]:span[1]]
                if words and not any(fs.is_symbol(t, ":") for t in words):
                    untyped.append(words[0].value)
            if untyped:
                add("M804", function, "function %s: parameter(s) %s have no type; write one, such as "
                    "'amount : NUMERIC'" % (name, ", ".join(untyped)), level="warn", keys=keys)
        if any(call.name == name.upper() for call in parsed["calls"]):
            add("M805", function, "function %s calls itself; Microsoft does not support recursion in user-defined "
                "functions" % name, keys=keys)
    groups = [t for t in context["own_tables"] if t.get("calculation_group")]
    for table in groups:
        group = table["calculation_group"]
        items = [o for o in context["objects"] if o["kind"] == "calculationitem" and o["parent"] is group]
        if not items:
            add("M811", group, "calculation group '%s' has no calculation items" % table["name"], level="warn",
                keys=(table["name"],))
        bare = [i["name"] for i in items if not i["described"]]
        if bare:
            add("M812", group, "calculation group '%s': item(s) %s have no '///' description. The checklist asks "
                "that every calculation group is documented" % (table["name"], ", ".join(bare)), level="warn",
                keys=(table["name"],))
    if len(groups) > 1:
        orders = [t["calculation_group"]["props"].get("precedence", "") for t in groups]
        if len(set(orders)) < len(orders) or "" in orders:
            add("M813", groups[0]["calculation_group"], "the model has %d calculation groups; give each its own "
                "precedence number, so that the order they apply in is fixed" % len(groups), level="warn", keys=("model",))
    if groups:
        detailed = [o for o in context["objects"] if not o["translation"]
                    and ("detailrowsdefinition" in o["props"] or "defaultdetailrowsdefinition" in o["props"])]
        if detailed:
            add("M815", detailed[0], "the model has a calculation group and detail rows expressions (%s). Microsoft "
                "lists detail rows expressions as not supported in a model with a calculation group: keep one of the two"
                % ", ".join("'%s'" % o["name"] for o in detailed[:4]), level="warn", keys=("model",))
    model_object = context["model_object"]
    if groups and model_object is not None and model_object["props"].get("discourageimplicitmeasures", "").lower() != "true":
        add("M814", model_object, "the model has a calculation group but discourageImplicitMeasures is not set. "
            "Calculation items apply to measures only; Power BI Desktop sets this property when it makes a "
            "calculation group", level="warn", keys=("model",))
    for table in context["own_tables"]:
        if not table.get("field_parameter"):
            continue
        source = next((p["props"].get("source", "") for p in table["partitions"]), "")
        parsed = context["parse"](source)
        missing = []
        for call in _calls(parsed, "NAMEOF"):
            for table_name, name, position in parsed["references"]:
                if call.open < position < call.close and table_name is not None:
                    target = tables.get(table_name)
                    if target is None or name.lower() not in {o["name"].lower() for o in target["columns"] + target["measures"]}:
                        missing.append("%s[%s]" % (table_name, name))
        if missing:
            add("M821", table["objects"][0], "field parameter '%s' names %s, which the model does not have; the "
                "table fails to load" % (table["name"], ", ".join(missing)), keys=(table["name"],))
        fields = [c for c in table["columns"] if "parametermetadata" in {k.lower() for k in c.get("extended", {})}]
        shown = [c for c in table["columns"] if not c["hidden"]]
        problems = []
        if len(shown) != 1:
            problems.append("exactly one column is visible (the label people pick)")
        elif not any(o["kind"] == "relatedcolumndetails" and o["parent"] is shown[0] for o in context["objects"]):
            problems.append("the visible column carries relatedColumnDetails with a groupByColumn that names the fields column")
        if fields and not fields[0]["hidden"]:
            problems.append("the fields column is hidden")
        if problems:
            add("M822", table["objects"][0], "field parameter '%s' is not wired the way Power BI Desktop writes it: %s"
                % (table["name"], "; ".join(problems)), level="warn", keys=(table["name"],))
    preview = []                        # (words that find the row in section 11, the object, what the model uses)
    calendars = [o for o in context["objects"] if o["kind"] == "calendar" and not o["translation"]]
    if calendars:
        preview.append((("calendar",), calendars[0], "calendar-based time intelligence (calendar '%s')" % calendars[0]["name"]))
    if model_object is not None and model_object["props"].get("valuefilterbehavior"):
        preview.append((("value filter",), model_object, "value filter behavior (valueFilterBehavior in model.tmdl)"))
    lake = {t["name"].lower() for t in context["own_tables"] if "directlake" in table_modes(t)}
    for table in context["own_tables"]:
        for column in table["columns"]:
            if column["props"].get("expressioncontext", "").lower() == "usercontext":
                preview.append((("user-context", "user context"), column, "a user-context calculated column (%s[%s])"
                                % (table["name"], column["name"])))
                break
        if lake and table["calculated"] and not table.get("field_parameter") and not table.get("parameter_table"):
            source = next((p["props"].get("source", "") for p in table["partitions"]), "")
            parsed = context["parse"](source)
            if any(t.kind in ("word", fs.QUOTED_NAME) and t.value.lower() in lake for t in parsed["tokens"]):
                preview.append((("direct lake",), table["objects"][0], "a calculated table over Direct Lake data ('%s')"
                                % table["name"]))
    reported = set()
    for words, anchor, what in preview:
        if words in reported or any(word in name for word in words for name in context["brief"].get("agreed", [])):
            continue
        reported.add(words)
        add("M841", anchor, "the model uses %s, which Microsoft still lists as a preview feature. A preview feature is "
            "used only after the developer's yes: add its row to section 11 of the brief (name it '%s')"
            % (what, words[0]), level="warn", keys=("model",))
    for perspective in [o for o in context["objects"] if o["kind"] == "perspective" and o["top"] and not o["translation"]]:
        if not any(o["kind"] == "perspectivetable" and o["parent"] is perspective for o in context["objects"]):
            add("M831", perspective, "perspective '%s' holds no objects" % perspective["name"], level="warn",
                keys=(perspective["name"],))
    del function_names


# ---------------------------------------------------------------- Power Query

def _m_calls(text):
    stream = fs.tokens(text or "", fs.M)
    return stream, [stream[i].value for i in range(len(stream) - 1)
                    if stream[i].kind == "word" and fs.is_symbol(stream[i + 1], "(")]


def _power_query(context, direct_query):
    add = context["add"]
    shared = {o["name"]: o for o in context["objects"] if o["kind"] == "expression" and o["top"] and not o["translation"]}
    users = {}
    for table in context["own_tables"]:
        for partition in table["partitions"]:
            if (partition["expr"] or "").split("//")[0].strip().lower() != "m":
                continue
            source = partition["props"].get("source", "")
            policy = table.get("refresh_policy")
            if policy is not None and policy["props"].get("sourceexpression"):
                source = policy["props"]["sourceexpression"]
            stream, called = _m_calls(source)
            key = table["name"]
            texts = [t.value for t in stream if t.kind == fs.TEXT]
            for token in stream:
                if token.kind in ("word", fs.QUOTED_NAME) and token.value in shared:
                    users.setdefault(token.value, set()).add(table["name"])
            native = [t for t in texts if re.match(r"\s*(select|with|exec|execute)\b", t, re.I)]
            if table["name"] in direct_query:
                bad = [t for t in native if re.match(r"\s*(with|exec|execute)\b", t, re.I)]
                if bad:
                    add("M701", partition, "DirectQuery table '%s' reads a native query that starts with '%s'. "
                        "Microsoft says a DirectQuery native query cannot use a common table expression or a stored "
                        "procedure" % (key, bad[0].split()[0]), keys=(key,))
                moved = sorted(set(called) & (set(M_TRANSFORMS) | {"Table.TransformColumnTypes"}))
                if moved:
                    add("M702", partition, "DirectQuery table '%s' has transformation steps in Power Query (%s). "
                        "Every step becomes part of every query sent to the source: do the work at the source"
                        % (key, ", ".join(moved)), level="warn", keys=(key,))
                dated = sorted(set(called) & set(M_RELATIVE_DATES))
                if dated:
                    add("M703", partition, "DirectQuery table '%s' filters on the current date in Power Query (%s); "
                        "the date is fixed when the query is written, not when the report is read. Filter by a "
                        "relative date in the report instead" % (key, ", ".join(dated)), level="warn", keys=(key,))
            else:
                moved = sorted(set(called) & set(M_TRANSFORMS))
                if len(moved) >= 3:
                    add("P006", partition, "the query of table '%s' does much reshaping (%s). Microsoft's rule asks to "
                        "keep heavy transformation at the source or in a dataflow, where it can be reused"
                        % (key, ", ".join(moved)), level="warn", keys=(key,))
            if native or set(called) & set(M_NATIVE):
                joined = any(fs.is_symbol(stream[i], "&") and (stream[i - 1].kind == fs.TEXT or stream[i + 1].kind == fs.TEXT)
                             and any(re.search(r"(?i)\b(select|where|from)\b", t.value) for t in (stream[i - 1], stream[i + 1])
                                     if t.kind == fs.TEXT)
                             for i in range(1, len(stream) - 1))
                if joined:
                    add("P002", partition, "the query of table '%s' builds a native query by joining text. Pass the "
                        "values as parameters of Value.NativeQuery instead: it is safer and can still fold" % key,
                        level="warn", keys=(key,))
                if policy is not None:
                    add("M708", partition, "table '%s' has incremental refresh on a native query. Microsoft warns that "
                        "the date filter then may not fold to the source: check it, or filter on a table or a view"
                        % key, level="warn", keys=(key,))
            if "CommonDataService.Database" in called:
                problems = []
                if "CreateNavigationProperties" not in [t.value for t in stream if t.kind == "word"]:
                    problems.append("set CreateNavigationProperties=false unless relationship columns are expanded")
                if set(called) & set(M_NATIVE) and "EnableFolding" not in [t.value for t in stream if t.kind == "word"]:
                    problems.append("set EnableFolding=true on the native query")
                if problems:
                    add("P004", partition, "the Dataverse query of table '%s': %s" % (key, "; ".join(problems)),
                        level="warn", keys=(key,))
            local = [t for t in texts if re.match(r"[A-Za-z]:\\", t)]
            if local and set(called) & {"File.Contents", "Folder.Files", "Folder.Contents", "Excel.Workbook", "Csv.Document"}:
                add("P005", partition, "the query of table '%s' reads a file from a local drive (%s). A published "
                    "model cannot reach it without a gateway: use a shared location, or record the gateway in the brief"
                    % (key, local[0][:40]), level="warn", keys=(key,))
    for name, tables_using in sorted(users.items()):
        if len(tables_using) >= 2 and re.match(r"\s*let\b", shared[name]["expr"] or ""):
            add("P003", shared[name], "query '%s' feeds %d tables (%s). Power Query runs it again for each of them: "
                "that is fine for a light query; for a heavy one Microsoft advises a dataflow, or doing the work at "
                "the source" % (name, len(tables_using), ", ".join(sorted(tables_using))), level="warn", keys=(name,))


# ---------------------------------------------------------------- suggestions: a native feature may do this better

def _shape(parsed):
    """A formula with every name and every text replaced by a mark: two formulas of one pattern share a shape."""
    parts = []
    for token in parsed["tokens"]:
        if token.kind in (fs.BRACKET_NAME, fs.QUOTED_NAME):
            parts.append("@")
        elif token.kind == fs.TEXT:
            parts.append('"')
        elif token.kind == "word":
            parts.append(token.value.upper())
        else:
            parts.append(token.value)
    return " ".join(parts).replace("@ @", "@")


def _suggestions(context, rels, direct_query, index):
    add = context["add"]
    anchor = context["model_anchor"]
    if anchor is None:
        return
    shapes = {}
    time_measures = []
    switchers = []
    formatted = []
    for owner, parsed in context["expressions"]:
        if owner["kind"] != "measure":
            continue
        found = [call.name for call in parsed["calls"]]
        if len(parsed["tokens"]) >= 12:
            shapes.setdefault(_shape(parsed), []).append(owner["name"])
        if set(found) & index["time"]:
            time_measures.append(owner["name"])
        if "SWITCH" in found and "SELECTEDVALUE" in found and sum(
                1 for t in parsed["tokens"] if t.kind == fs.BRACKET_NAME) >= 3:
            switchers.append(owner["name"])
        if found[:1] == ["FORMAT"] and parsed["calls"][0].at == 0:
            formatted.append(owner["name"])
    for shape, names in sorted(shapes.items()):
        if len(names) >= 3:
            add("U001", anchor, "%d measures share one formula pattern (%s%s). A user-defined function would hold the "
                "pattern once; see native-features.md"
                % (len(names), ", ".join("[%s]" % n for n in names[:4]), " ..." if len(names) > 4 else ""),
                level="note", keys=("model",))
            break
    groups = any(t.get("calculation_group") for t in context["own_tables"])
    if len(time_measures) >= 6 and not groups:
        add("U002", anchor, "%d measures are time variants of other measures (%s ...). A calculation group would "
            "give every measure the same variants without a new measure for each"
            % (len(time_measures), ", ".join("[%s]" % n for n in time_measures[:3])), level="note", keys=("model",))
    if switchers and not any(t.get("field_parameter") for t in context["own_tables"]):
        add("U003", anchor, "measure(s) %s switch between measures with SWITCH and SELECTEDVALUE. A field "
            "parameter does this without a formula and keeps each measure's own format"
            % ", ".join("[%s]" % n for n in switchers[:4]), level="note", keys=("model",))
    if direct_query and not any(c.get("alternate_of") for _, c in context["all_columns"]):
        add("U004", anchor, "the model has DirectQuery tables (%s) and no aggregation table. If visuals are slow, "
            "an imported aggregation table answers summary queries from memory"
            % ", ".join(sorted(direct_query)[:4]), level="note", keys=("model",))
    if formatted:
        add("U005", anchor, "measure(s) %s return text made with FORMAT. A dynamic format string keeps the result a "
            "number, so it still sorts and charts" % ", ".join("[%s]" % n for n in formatted[:4]), level="note",
            keys=("model",))
    inactive = {}
    for r in rels:
        if not r["active"]:
            inactive.setdefault(r["to"][0], []).append(r["label"])
    for name, labels in sorted(inactive.items()):
        if len(labels) >= 2:
            add("U006", anchor, "table '%s' has %d inactive relationships. A second copy of the dimension for each "
                "role (a role-playing dimension) lets report authors filter by each role without special measures"
                % (name, len(labels)), level="note", keys=("model",))
    for table in context["own_tables"]:
        if table["hierarchies"] or table["name"] in context["measure_tables"]:
            continue
        names = {c["name"].lower() for c in table["columns"] if not c["hidden"]}
        if {"year", "month"} <= names or {"country", "city"} <= names or {"category", "subcategory"} <= names:
            add("U007", table["objects"][0], "table '%s' has columns that form a natural drill path and no "
                "hierarchy; a hierarchy lets readers drill down in one step" % table["name"], level="note",
                keys=(table["name"],))


# ---------------------------------------------------------------- rules added when the coverage file was closed

def _whole_call(parsed, span, *names):
    """The call that fills one argument completely, when its name is one of names; None otherwise."""
    stream = parsed["tokens"]
    if span[1] - span[0] < 3 or stream[span[0]].kind != "word" or stream[span[0]].value.upper() not in names:
        return None
    call = next((c for c in parsed["calls"] if c.at == span[0]), None)
    return call if call is not None and call.close == span[1] - 1 else None


def _more(context, rels, column_at, permissions, functions, direct_query):
    tables, add = context["tables"], context["add"]
    parsed_by_id = {id(owner): parsed for owner, parsed in context["expressions"]}

    # ---- keys, relationships, wide tables
    open_keys = {}
    for r in rels:
        if r["object"]["props"].get("securityfilteringbehavior", "").lower() == "bothdirections":
            add("M609", r["object"], "relationship %s applies the security filter in both directions. Microsoft says "
                "this costs query speed and is needed only when a row-level security rule must travel against the "
                "relationship: keep it only for that, with the reason in the brief" % r["label"], level="warn",
                keys=(r["label"],))
        if r["from_many"] and not r["to_many"] and r["to"] in column_at:
            table, column = column_at[r["to"]]
            if column["props"].get("isnullable", "").lower() != "false":
                open_keys.setdefault(table["name"], (table, []))[1].append(column["name"])
        if (r["from"][0] in direct_query and r["to"][0] in direct_query
                and r["object"]["props"].get("relyonreferentialintegrity", "").lower() != "true"):
            add("U008", r["object"], "relationship %s joins two DirectQuery tables without 'Assume referential "
                "integrity' (relyOnReferentialIntegrity). When the source guarantees that every key has a match, "
                "turning it on lets Power BI send faster joins" % r["label"], level="note", keys=(r["label"],))
    for name, (table, columns) in sorted(open_keys.items()):
        add("M416", table["objects"][0], "table '%s': key column(s) %s allow blanks. If a blank key must stop the "
            "refresh instead of loading, set isNullable: false on the column" % (name, ", ".join(sorted(set(columns)))),
            level="note", keys=(name,))
    dimensions = {r["to"][0] for r in rels if r["from_many"] and not r["to_many"]}
    for table in context["own_tables"]:
        if table["name"] in context["measure_tables"] or table["hidden"]:
            continue
        shown = [c for c in table["columns"] if not c["hidden"]]
        if len(shown) > MANY_COLUMNS:
            add("M120", table["objects"][0], "table '%s' shows %d columns (more than %d). Hide the columns report "
                "authors do not need, or split the table: so many columns in one table point to a design problem"
                % (table["name"], len(shown), MANY_COLUMNS), level="warn", keys=(table["name"],))
        if (context["brief"].get("copilot") and table["name"] in dimensions and shown
                and table["props"].get("datacategory", "").lower() != "time"
                and not any(c["props"].get("isdefaultlabel", "").lower() == "true" for c in table["columns"])):
            add("M303", table["objects"][0], "dimension table '%s' has no column marked isDefaultLabel. Mark its name "
                "column, so that Copilot in Power BI knows which column names a row" % table["name"], level="note",
                keys=(table["name"],))

    # ---- DAX
    for owner, parsed in context["expressions"]:
        if owner["kind"] not in ("measure", "column", "calculationitem", "tablepermission", "function", "partition"):
            continue
        stream = parsed["tokens"]
        label = _label(owner)
        keys = (label,)
        for call in _calls(parsed, "DIVIDE"):
            if len(call.args) >= 2 and call.args[1][1] - call.args[1][0] == 1:
                divisor = stream[call.args[1][0]]
                if divisor.kind == "number" and float_or_none(divisor.value) not in (None, 0.0):
                    add("M518", owner, "DAX of %s calls DIVIDE with the fixed number %s as the divisor. Microsoft "
                        "advises the '/' operator there: a fixed number is never zero or blank, and '/' is faster"
                        % (label, divisor.value), level="warn", keys=keys)
                    break
        cleared = nested = False
        for call in _calls(parsed, "CALCULATE", "CALCULATETABLE"):
            if not cleared and any(_whole_call(parsed, span, "ALL") for span in call.args[1:]):
                cleared = True
                add("M519", owner, "DAX of %s passes ALL ( ... ) to %s only to remove filters. REMOVEFILTERS does the "
                    "same and says what is meant; keep ALL for where a table is needed" % (label, call.name),
                    level="warn", keys=keys)
            if not nested and call.name == "CALCULATE" and call.args and _whole_call(parsed, call.args[0], "CALCULATE"):
                nested = True
                add("M521", owner, "DAX of %s writes CALCULATE directly inside CALCULATE. Give one CALCULATE all the "
                    "filters, or move the inner part to a variable or a measure of its own" % label, level="warn",
                    keys=keys)
        for call in _calls(parsed, "SUMMARIZE"):
            if any(span[1] - span[0] == 1 and stream[span[0]].kind == fs.TEXT for span in call.args[1:]):
                add("M522", owner, "DAX of %s adds a new column inside SUMMARIZE. Use SUMMARIZE only to group, and add "
                    "the column around it with ADDCOLUMNS (or use SUMMARIZECOLUMNS): the result is easier to predict"
                    % label, level="warn", keys=keys)
                break
        if owner["kind"] == "measure":
            for call in _calls(parsed, "SUMMARIZECOLUMNS"):
                if any(_whole_call(parsed, span, *SUMMARIZECOLUMNS_FILTERS) for span in call.args):
                    add("M523", owner, "measure %s gives SUMMARIZECOLUMNS a filter argument. Inside a measure, consider "
                        "putting the filter in a CALCULATETABLE around SUMMARIZECOLUMNS instead" % label, level="note", keys=keys)
                    break

    # ---- reports in more than one language
    model_object = context["model_object"]
    cultures = {o["name"].lower() for o in context["objects"] if o["kind"] == "cultureinfo"}
    if model_object is not None and model_object["props"].get("culture"):
        cultures.add(model_object["props"]["culture"].strip().lower())
    for owner, parsed in context["expressions"]:
        stream = parsed["tokens"]
        label = _label(owner)
        if any(call.name == "USERCULTURE" for call in parsed["calls"]):
            home = owner.get("table")
            fixed = (owner["kind"] == "partition"
                     or (owner["kind"] == "column" and owner.get("calculated")
                         and owner["props"].get("expressioncontext", "").lower() != "usercontext"))
            if fixed and (home is None or home["name"] not in direct_query):
                add("M524", owner, "DAX of %s calls USERCULTURE. In an imported calculated column or table the value is "
                    "fixed when the data is refreshed, so it is not the reader's language: use a measure"
                    % label, level="warn", keys=(label,))
        for call in _calls(parsed, "SWITCH"):
            if not call.args or not any(c.name == "USERCULTURE" and call.args[0][0] <= c.at < call.args[0][1]
                                        for c in parsed["calls"]):
                continue
            problems = []
            if len(call.args) % 2 == 1:
                problems.append("it has no last value for every other language, so those readers see a blank")
            named = [stream[span[0]].value for span in call.args[1::2]
                     if span[1] - span[0] == 1 and stream[span[0]].kind == fs.TEXT
                     and re.match(r"[A-Za-z]{2,3}-[A-Za-z]{2,4}\Z", stream[span[0]].value)]
            lost = sorted({name for name in named if name.lower() not in cultures})
            if lost:
                problems.append("the model has no culture file for %s, so table and column names stay untranslated "
                                "for those readers" % ", ".join(lost))
            if problems:
                add("M525", owner, "the SWITCH over USERCULTURE in %s: %s" % (label, "; ".join(problems)),
                    level="warn", keys=(label,))
                break

    # ---- user-defined functions
    hidden_tables, hidden_columns = set(), set()
    for permission in permissions:
        if permission["props"].get("metadatapermission", "").lower() == "none":
            hidden_tables.add(permission["name"].lower())
        for obj in context["objects"]:
            if (obj["kind"] == "columnpermission" and obj["parent"] is permission and "none" in (
                    (obj["expr"] or "").strip().lower(), obj["props"].get("metadatapermission", "").lower())):
                hidden_columns.add((permission["name"].lower(), obj["name"].lower()))
    for function in functions:
        name = function["name"]
        parsed = parsed_by_id.get(id(function))
        if parsed is None:
            continue
        stream = parsed["tokens"]
        secret = sorted({"%s[%s]" % (t, n) for t, n, _ in parsed["references"] if t is not None
                         and (t.lower() in hidden_tables or (t.lower(), n.lower()) in hidden_columns)}
                        | {"table '%s'" % t.value for t in stream if t.kind in ("word", fs.QUOTED_NAME)
                           and t.value.lower() in hidden_tables and t.value in tables})
        if secret:
            add("M806", function, "function %s names %s, which a role hides with object-level security. Microsoft "
                "says object-level security does not carry over to functions: for a member of that role the function "
                "behaves as if the object did not exist. Test the function for that role, and keep hidden names out of "
                "function names and descriptions" % (name, ", ".join(secret)), level="warn", keys=(name,))
        problems = []
        if "_" in name or any(part[:1].isalpha() and not part[:1].isupper() for part in name.split(".")):
            problems.append("write each part of the name with a capital first letter and no underscores (AddTax, "
                            "Finance.AddTax)")
        if stream and fs.is_symbol(stream[0], "("):
            closer = fs.match_close(stream, 0)
            wrong = [stream[span[0]].value for span in fs.split_arguments(stream, 0, closer)
                     if span[1] > span[0] and stream[span[0]].kind == "word"
                     and (not stream[span[0]].value[:1].islower() or "_" in stream[span[0]].value)]
            if wrong:
                problems.append("start each parameter with a small letter and use no underscores (%s)" % ", ".join(wrong))
        if problems:
            add("M807", function, "function %s does not follow the naming style for functions: %s"
                % (name, "; ".join(problems)), level="warn", keys=(name,))

    # ---- partitions and data sources
    sources = {o["name"]: o for o in context["objects"] if o["kind"] == "datasource" and o["top"] and not o["translation"]}
    used_sources = set()
    feeders = {}
    for table in context["own_tables"]:
        modes = table_modes(table)
        for partition in table["partitions"]:
            kind = (partition["expr"] or "").split("//")[0].strip().lower()
            named = (_reference(partition["props"].get("datasource", "")) or ("",))[0]
            text = " ".join(str(partition["props"].get(key, "")) for key in ("source", "query"))
            for source_name in sources:
                if named == source_name or source_name in text:
                    used_sources.add(source_name)
            if kind == "m" and "directlake" in modes:
                add("M711", partition, "table '%s' is in Direct Lake mode but its partition is a Power Query (m) "
                    "partition. A Direct Lake table reads a Delta table through an entity partition and has no "
                    "Power Query" % table["name"], level="warn", keys=(table["name"],))
            if kind == "query" and named in sources and sources[named]["props"].get("type", "").lower() == "structured":
                add("M833", partition, "partition '%s' of table '%s' is a legacy query partition on the structured "
                    "data source '%s'. Microsoft's rule says Power BI does not support that pair: use a Power Query "
                    "(m) partition" % (partition["name"], table["name"], named), keys=(table["name"],))
            if kind == "m":
                source = partition["props"].get("source", "")
                steps = {step["name"] for step in fs.m_steps(source)[0]}
                for token in fs.tokens(source, fs.M):
                    if (token.kind in ("word", fs.QUOTED_NAME) and token.value in tables
                            and token.value != table["name"] and token.value not in steps):
                        feeders.setdefault(token.value, set()).add(table["name"])
            if kind == "calculated" and not table.get("field_parameter"):
                parsed = context["parse"](partition["props"].get("source", ""))
                calls = parsed["calls"]
                if calls and calls[0].at == 0 and calls[0].close == len(parsed["tokens"]) - 1 \
                        and calls[0].name in CALCULATED_TABLE_MAKERS:
                    made = {t.value.lower() for t in parsed["tokens"] if t.kind in (fs.TEXT, fs.BRACKET_NAME)}
                    lost = sorted(c["name"] for c in table["columns"] if not c.get("calculated")
                                  and re.match(r"\[.*\]\Z", c["props"].get("sourcecolumn", "").strip())
                                  and c["props"]["sourcecolumn"].strip()[1:-1].lower() not in made)
                    if lost:
                        add("M910", partition, "calculated table '%s': column(s) %s read a sourceColumn that the "
                            "table's formula does not produce. Each sourceColumn must be '[Name]' with a name the "
                            "formula returns, or the column is empty or the table fails to load"
                            % (table["name"], ", ".join(lost)), level="warn", keys=(table["name"],))
    for name, source in sorted(sources.items()):
        if name not in used_sources and not any(name in (o["expr"] or "") for o in context["objects"] if o["kind"] == "expression"):
            add("M832", source, "data source '%s' is used by no partition; remove it" % name, level="warn", keys=(name,))
    in_use = {r["from"][0] for r in rels} | {r["to"][0] for r in rels}
    in_use |= {entity for _, entity, _ in context["usage"]}
    for owner, parsed in context["expressions"]:
        home = owner["table"]["name"] if owner.get("table") is not None else None
        for table_name, _, _ in parsed["references"]:
            if table_name is not None and table_name != home:
                in_use.add(table_name)
        for token in parsed["tokens"]:
            if token.kind in ("word", fs.QUOTED_NAME) and token.value in tables and token.value != home:
                in_use.add(token.value)
    for name, users in sorted(feeders.items()):
        table = tables[name]
        if name in in_use or table["measures"] or name in context["measure_tables"] or table["calculated"]:
            continue
        add("P007", table["objects"][0], "table '%s' is loaded, but only the queries of %s use it: no relationship, "
            "formula or visual does. Turn its load off (keep it as a shared query), so that it takes no memory and "
            "no refresh time" % (name, ", ".join(sorted(users))), level="warn", keys=(name,))

