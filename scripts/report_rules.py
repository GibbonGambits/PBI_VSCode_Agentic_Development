#!/usr/bin/env python3
"""The report checks added in round 3: pages for drillthrough and tooltips, buttons, bookmarks, page density,
styling on single visuals, accessibility, and notes that suggest a native feature.

scripts/check_project.py calls check() once for each report. This file is not run by itself.
Each rule, its level and its source address are listed in
.github/skills/pbi-report/references/report-standard.md (the code after a rule is the finding it gives here).

Where things are stored comes from Microsoft's report schemas (scripts/schemas): page 2.1.0, visualContainer
2.13.0, visualConfiguration 2.8.0, bookmark 2.1.0 and pagesMetadata 1.1.0. The values of a button's action
type ('Back', 'Bookmark', 'PageNavigation', 'Drillthrough', 'WebUrl', 'Qna') are not in the schemas; they
follow Microsoft's report skill (microsoft/skills-for-fabric, MIT).

An exception counts only when section 10 of docs/report-brief.md lists the code, the page and the visual
(or '-' for a whole page) with a reason.
Needs Python 3.8 or later. Uses the standard library only.
"""
import os
import re

TOOLTIP_SIZE = (320, 240)           # the built-in Tooltip page size (Microsoft Learn, "Extend visuals with report page tooltips")
TOOLTIP_FIELDS = 3                  # checklist item 65
DENSITY_REVIEW = 13                 # checklist item 20: 13 to 16 visuals = review
DENSITY_LIMIT = 16                  # checklist item 20: more than 16 = justification required
NO_DATA_TYPES = frozenset(("textbox", "shape", "basicShape", "image", "actionButton", "pageNavigator",
                           "bookmarkNavigator"))
INTERACTIVE_TYPES = frozenset(("slicer", "advancedSlicerVisual", "listSlicer", "textSlicer", "actionButton",
                               "pageNavigator", "bookmarkNavigator"))
SLICER_TYPES = frozenset(("slicer", "advancedSlicerVisual", "listSlicer", "textSlicer"))
STYLE_PROPERTIES = frozenset(("fontFamily", "fontSize", "fontColor", "color", "bold", "italic", "underline"))
STYLE_CARDS = frozenset(("border", "dropShadow", "background"))
HEX_COLOUR = re.compile(r"#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?\b")
LINK_TARGETS = (("Bookmark", "bookmark", "bookmark"), ("PageNavigation", "navigationSection", "page"),
                ("Drillthrough", "drillthroughSection", "page"))


def literal(value):
    """The text of {"expr": {"Literal": {"Value": "'Back'"}}} without its quotes; None for anything else."""
    try:
        text = value["expr"]["Literal"]["Value"]
    except (TypeError, KeyError):
        return None
    if not isinstance(text, str):
        return None
    if len(text) >= 2 and text[0] == "'" and text[-1] == "'":
        return text[1:-1].replace("''", "'")
    return text


def card(visual, name):
    """The properties of every entry of visual.visualContainerObjects.<name>, merged."""
    out = {}
    objects = visual.get("visualContainerObjects") if isinstance(visual, dict) else None
    entries = objects.get(name) if isinstance(objects, dict) else None
    for entry in entries if isinstance(entries, list) else []:
        properties = entry.get("properties") if isinstance(entry, dict) else None
        if isinstance(properties, dict):
            out.update(properties)
    return out


def action(visual):
    """(type, properties) of a visual's action when it is switched on; (None, {}) otherwise."""
    link = card(visual, "visualLink")
    if literal(link.get("show")) != "true":
        return None, {}
    return literal(link.get("type")), link


def fields(node, found):
    """Add 'Table.Field' for every column or measure a JSON value names."""
    if isinstance(node, dict):
        for kind in ("Column", "Measure"):
            value = node.get(kind)
            if isinstance(value, dict) and isinstance(value.get("Property"), str):
                source = value.get("Expression", {}).get("SourceRef", {}) if isinstance(value.get("Expression"), dict) else {}
                found.add("%s.%s" % (source.get("Entity", "?") if isinstance(source, dict) else "?", value["Property"]))
        for value in node.values():
            fields(value, found)
    elif isinstance(node, list):
        for value in node:
            fields(value, found)


def styling(node, path, found):
    """Add the names of colour, font and size settings written on a visual itself."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in STYLE_PROPERTIES and isinstance(value, dict):
                text = literal(value)
                solid = value.get("solid") if isinstance(value.get("solid"), dict) else None
                if solid is not None:
                    text = literal(solid.get("color"))
                    if text is None and isinstance(solid.get("color"), dict) and "ThemeDataColor" in solid["color"].get("expr", {}):
                        continue                         # a colour taken from the theme
                if text is not None or solid is not None:
                    found.add("%s.%s" % (path, key) if path else key)
            elif isinstance(value, str) and HEX_COLOUR.search(value) and key == "Value":
                found.add("%s (a colour written as a code)" % path if path else "a colour written as a code")
            else:
                styling(value, path if key in ("properties", "expr", "solid", "Literal") or isinstance(node, list) else key, found)
    elif isinstance(node, list):
        for value in node:
            styling(value, path, found)


def read_pages(cp, report_dir):
    """Every page of a report whose page.json can be read."""
    pages = []
    for folder_name, folder, page_path in cp.iter_pages(report_dir):
        page = cp.load_object(page_path)
        if page is None:
            continue
        visuals = []
        for visual_folder, visual_path in cp.iter_visuals(folder):
            data = cp.load_object(visual_path)
            if data is not None:
                visuals.append({"folder": visual_folder, "path": visual_path, "data": data,
                                "visual": data.get("visual") if isinstance(data.get("visual"), dict) else {},
                                "name": data.get("name") if isinstance(data.get("name"), str) else visual_folder,
                                "label": cp.annotation(data, cp.LABEL_ANNOTATION)})
        binding = page.get("pageBinding") if isinstance(page.get("pageBinding"), dict) else {}
        kind = page.get("type") if page.get("type") in ("Tooltip", "Drillthrough") else None
        if kind is None and binding.get("type") in ("Tooltip", "Drillthrough"):
            kind = binding["type"]
        pages.append({"folder": folder_name, "path": page_path, "page": page, "visuals": visuals, "kind": kind,
                      "name": page.get("name") if isinstance(page.get("name"), str) else folder_name,
                      "keys": {k for k in (folder_name, page.get("name"), page.get("displayName")) if isinstance(k, str) and k}})
    return pages


def check(cp, report_dir, brief, findings):
    """cp: the check_project module (its file readers and its brief are reused)."""
    pages = read_pages(cp, report_dir)
    page_names = {p["name"] for p in pages}
    bookmark_names = _bookmarks(cp, report_dir, pages, brief, findings)

    def excused(code, page, *visuals):
        keys = set()
        for visual in visuals:
            keys |= {k for k in (visual["label"], visual["name"], visual["folder"]) if isinstance(k, str) and k}
        return cp.layout_excused(brief, code, page["keys"], keys or {"-"})

    def shown(visual):
        return visual["label"] if isinstance(visual["label"], str) and visual["label"] else visual["name"]

    def add(code, page, visual, message, level="warn"):
        if not excused(code, page, *([visual] if visual else [])):
            findings.add(code, visual["path"] if visual else page["path"], 0, message, level=level)

    _page_list(cp, report_dir, pages, findings)
    slicer_fields = {}
    for page in pages:
        title = page["page"].get("displayName") or page["name"]
        hidden_page = page["page"].get("visibility") == "HiddenInViewMode"
        types = [(v, v["visual"].get("visualType")) for v in page["visuals"]]
        actions = [(v, action(v["visual"])) for v in page["visuals"]]

        if page["kind"] == "Drillthrough" and not any(kind == "Back" for _, (kind, _) in actions):
            add("V001", page, None, "drillthrough page '%s' has no back button (a button whose action is Back). The "
                "checklist asks for back navigation on every drillthrough page" % title, level="error")
        if page["kind"] == "Tooltip":
            if not hidden_page:
                add("V002", page, None, "tooltip page '%s' is not hidden; Microsoft advises hiding every tooltip page "
                    "(visibility HiddenInViewMode)" % title)
            width, height = page["page"].get("width"), page["page"].get("height")
            if cp._is_number(width) and cp._is_number(height) and (width > TOOLTIP_SIZE[0] * 2 or height > TOOLTIP_SIZE[1] * 2):
                add("V003", page, None, "tooltip page '%s' is %g x %g; a tooltip covers the page behind it, so keep it "
                    "near the built-in Tooltip size, %d x %d" % (title, width, height, TOOLTIP_SIZE[0], TOOLTIP_SIZE[1]))
            busy = [shown(v) for v, kind in types if kind in INTERACTIVE_TYPES]
            if busy:
                add("V004", page, None, "tooltip page '%s' holds slicers or buttons (%s); a tooltip cannot be clicked. "
                    "Use a drillthrough page when readers must interact" % (title, ", ".join(busy)))
            used = set()
            for visual in page["visuals"]:
                fields(visual["visual"].get("query"), used)
            if len(used) < TOOLTIP_FIELDS:
                add("V005", page, None, "tooltip page '%s' shows %d field(s); the checklist expects a report page "
                    "tooltip to add three or more facts beyond the value hovered over" % (title, len(used)))
        else:
            active = [v for v, kind in types if isinstance(v["visual"].get("query"), dict) and v["data"].get("isHidden") is not True]
            if len(active) > DENSITY_LIMIT:
                add("V006", page, None, "page '%s' has %d visuals that show data; the checklist asks for a written "
                    "reason above %d. Split the page, or list the reason in section 10 of the brief"
                    % (title, len(active), DENSITY_LIMIT), level="error")
            elif len(active) >= DENSITY_REVIEW:
                add("V007", page, None, "page '%s' has %d visuals that show data; the checklist asks for a review "
                    "from %d" % (title, len(active), DENSITY_REVIEW))

        for visual, (kind, link) in actions:
            for wanted, key, target in LINK_TARGETS:
                name = literal(link.get(key))
                if kind == wanted and name is not None:
                    known = bookmark_names if target == "bookmark" else page_names
                    if name not in known:
                        add("V008", page, visual, "the action of '%s' goes to %s '%s', which this report does not have; "
                            "the button does nothing" % (shown(visual), target, name))

        no_alt, made_up = [], []
        for visual in page["visuals"]:
            body = visual["visual"]
            if not body:
                continue
            kind = body.get("visualType")
            found = set()
            for name, entries in (body.get("visualContainerObjects") or {}).items() if isinstance(body.get("visualContainerObjects"), dict) else []:
                if name in STYLE_CARDS and any(literal((e.get("properties") or {}).get("show")) == "true"
                                               for e in entries if isinstance(e, dict) and isinstance(e.get("properties"), dict)):
                    found.add("%s on" % name)
                styling(entries, name, found)
            styling(body.get("objects"), "", found)
            if found:
                add("V009", page, visual, "'%s' sets its own styling (%s). The theme does this work: remove the "
                    "setting so the visual follows the theme, or list the reason in the brief"
                    % (shown(visual), ", ".join(sorted(found)[:6]) + (" ..." if len(found) > 6 else "")))
            has_data = isinstance(body.get("query"), dict)
            general = card(body, "general")
            if (has_data and visual["data"].get("isHidden") is not True and "altText" not in general
                    and not excused("A001", page, visual)):
                no_alt.append(shown(visual))
            title_card = card(body, "title")
            if (has_data and kind not in SLICER_TYPES and literal(title_card.get("show")) != "false"
                    and "text" not in title_card and page["kind"] != "Tooltip" and not excused("A003", page, visual)):
                made_up.append(shown(visual))
            if kind in SLICER_TYPES and page["kind"] is None:
                used = set()
                fields(body.get("query"), used)
                for field in used:
                    slicer_fields.setdefault(field, []).append((page, visual, isinstance(body.get("syncGroup"), dict)))

        if no_alt:
            add("A001", page, None, "page '%s': %d visual(s) have no alt text: %s. Microsoft's accessibility checklist "
                "asks for alt text on every visual that is not decoration: say what the visual shows (general.altText)"
                % (title, len(no_alt), ", ".join(no_alt[:10]) + (" ..." if len(no_alt) > 10 else "")))
        if made_up:
            add("A003", page, None, "page '%s': %d visual(s) show a title Power BI makes up from field names: %s. "
                "Write a title that says what the visual shows (title.text), or switch the title off when a text box "
                "does that job" % (title, len(made_up), ", ".join(made_up[:10]) + (" ..." if len(made_up) > 10 else "")))
        orders = {}
        for visual in page["visuals"]:
            position = visual["data"].get("position") if isinstance(visual["data"].get("position"), dict) else {}
            if cp._is_number(position.get("tabOrder")) and not visual["data"].get("parentGroupName"):
                orders.setdefault(position["tabOrder"], []).append(shown(visual))
        same = ["%s (%g)" % (", ".join(names), order) for order, names in sorted(orders.items()) if len(names) > 1]
        if same:
            add("A002", page, None, "page '%s': visuals share a tab order number: %s. Give each visual its own number, "
                "in reading order (left to right, top to bottom)" % (title, "; ".join(same[:4])))

        buttons = [v for v, (kind, _) in actions if kind == "PageNavigation"]
        if len(buttons) >= 3:
            add("U102", page, None, "page '%s' has %d buttons that each go to a page. A page navigator makes those "
                "buttons from the list of pages and keeps them up to date" % (title, len(buttons)), level="note")
    for field, uses in sorted(slicer_fields.items()):
        on_pages = {id(page): page for page, _, _ in uses}
        if len(on_pages) >= 2 and not all(synced for _, _, synced in uses):
            page, visual, _ = uses[0]
            add("U101", page, visual, "a slicer on %s is on %d pages and is not synced on all of them. Sync slicers "
                "keeps one selection across pages (the checklist asks to review this)"
                % (field.replace(".", "[", 1) + "]", len(on_pages)), level="note")
    _stacked(cp, report_dir, pages, add)


def _bookmarks(cp, report_dir, pages, brief, findings):
    """Names of the report's bookmarks. V010: a bookmark that holds a page or a visual the report no longer has."""
    names = set()
    folder = os.path.join(report_dir, "definition", "bookmarks")
    if not os.path.isdir(folder):
        return names
    by_page = {p["name"]: {v["name"] for v in p["visuals"]} for p in pages}
    for file_name in sorted(os.listdir(folder)):
        if not file_name.endswith(".bookmark.json"):
            continue
        path = os.path.join(folder, file_name)
        data = cp.load_object(path) or {}
        name = data.get("name") if isinstance(data.get("name"), str) else file_name[:-len(".bookmark.json")]
        names.add(name)
        state = data.get("explorationState") if isinstance(data.get("explorationState"), dict) else {}
        sections = state.get("sections") if isinstance(state.get("sections"), dict) else {}
        gone = []
        for page, section in sections.items():
            if page not in by_page:
                gone.append("page '%s'" % page)
                continue
            containers = section.get("visualContainers") if isinstance(section, dict) else None
            for visual in containers if isinstance(containers, dict) else []:
                if visual not in by_page[page]:
                    gone.append("visual '%s' on page '%s'" % (visual, page))
        if gone and not cp.layout_excused(brief, "V010", {name}, {"-"}):
            findings.add("V010", path, 0, "bookmark '%s' holds %s, which the report no longer has. Power BI Desktop "
                         "drops such entries when it saves; capture the bookmark again"
                         % (data.get("displayName") or name, ", ".join(gone[:5]) + (" ..." if len(gone) > 5 else "")),
                         level="warn")
    return names


def _page_list(cp, report_dir, pages, findings):
    """V011: pages.json and the page folders disagree."""
    path = os.path.join(report_dir, "definition", "pages", "pages.json")
    data = cp.load_object(path)
    if data is None:
        return
    order = [name for name in data.get("pageOrder", []) if isinstance(name, str)] if isinstance(data.get("pageOrder"), list) else []
    names = [p["name"] for p in pages]
    problems = []
    twice = sorted({name for name in order if order.count(name) > 1})
    if twice:
        problems.append("listed twice: %s" % ", ".join(twice))
    missing = [name for name in order if name not in names]
    if missing:
        problems.append("listed but no page folder has that name: %s" % ", ".join(missing))
    extra = [name for name in names if name not in order]
    if extra and order:
        problems.append("page not listed in pageOrder: %s" % ", ".join(extra))
    for key in ("activePageName", "landingPageName"):
        if isinstance(data.get(key), str) and data[key] not in names:
            problems.append("%s is '%s', which is not a page" % (key, data[key]))
    if problems:
        findings.add("V011", path, 0, "pages.json and the page folders disagree: %s. Power BI Desktop repairs this "
                     "when it opens the report, and its order may not be the one you want" % "; ".join(problems),
                     level="warn")


def _stacked(cp, report_dir, pages, add):
    """U103: data visuals laid on top of each other that bookmarks show one at a time."""
    hidden = cp.bookmark_hidden(report_dir)
    for page in pages:
        states = hidden.get(page["name"], [])
        if not states:
            continue
        data_visuals = [v for v in page["visuals"] if isinstance(v["visual"].get("query"), dict)]
        for index, first in enumerate(data_visuals):
            for second in data_visuals[index + 1:]:
                a = first["data"].get("position") if isinstance(first["data"].get("position"), dict) else {}
                b = second["data"].get("position") if isinstance(second["data"].get("position"), dict) else {}
                if not all(cp._is_number(p.get(k)) for p in (a, b) for k in ("x", "y", "width", "height")):
                    continue
                same_place = all(abs(a[k] - b[k]) < 1 for k in ("x", "y", "width", "height"))
                same_type = first["visual"].get("visualType") == second["visual"].get("visualType")
                swapped = any((first["name"] in s[0]) != (second["name"] in s[0]) for s in states)
                if same_place and same_type and swapped:
                    add("U103", page, first, "'%s' and '%s' are the same kind of visual in the same place, and "
                        "bookmarks show one at a time. A field parameter lets one visual switch its measure or its "
                        "category, with a slicer" % (first["label"] or first["name"], second["label"] or second["name"]),
                        level="note")
                    return
