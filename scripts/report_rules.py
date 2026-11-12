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
import json
import os
import re

TOOLTIP_SIZE = (320, 240)           # the built-in Tooltip page size (Microsoft Learn, "Extend visuals with report page tooltips")
TOOLTIP_FIELDS = 3                  # checklist item 65
ALT_TEXT_LIMIT = 250                # Microsoft Learn, "Design Power BI reports for accessibility"
DENSITY_REVIEW = 13                 # checklist item 20: 13 to 16 visuals = review
DENSITY_LIMIT = 16                  # checklist item 20: more than 16 = justification required
TABLE_TYPES = frozenset(("tableEx", "pivotTable"))
BIG_TABLE_SHARE = 1.0 / 3           # checklist item 20 counts a "dominant large" table or matrix twice; this template
                                    # reads that as one that covers a third of the page or more
NO_DATA_TYPES = frozenset(("textbox", "shape", "basicShape", "image", "actionButton", "pageNavigator",
                           "bookmarkNavigator"))
INTERACTIVE_TYPES = frozenset(("slicer", "advancedSlicerVisual", "listSlicer", "textSlicer", "actionButton",
                               "pageNavigator", "bookmarkNavigator"))
SLICER_TYPES = frozenset(("slicer", "advancedSlicerVisual", "listSlicer", "textSlicer"))
STYLE_PROPERTIES = frozenset(("fontFamily", "fontSize", "fontColor", "color", "bold", "italic", "underline"))
STYLE_CARDS = frozenset(("border", "dropShadow", "background"))
HEX_COLOUR = re.compile(r"#[0-9A-Fa-f]{6}(?:[0-9A-Fa-f]{2})?\b")
SCALE_KEYS = ("minimum", "center", "maximum", "null", "background")   # theme colours a colour scale may use
SCALE_PARTS = frozenset(("linearGradient2", "linearGradient3"))
_SCALE_COLOURS = None


def scale_colours():
    """The colour codes of the owner's theme file a colour scale may use, in upper case: its data colours, its
    background, and its minimum, center, maximum and null colours."""
    global _SCALE_COLOURS
    if _SCALE_COLOURS is None:
        path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "theme", "theme.json")
        try:
            with open(path, encoding="utf-8-sig") as fh:
                theme = json.load(fh)
        except (OSError, ValueError):
            theme = {}
        colours = [theme[k] for k in SCALE_KEYS if isinstance(theme.get(k), str)]
        colours += [c for c in theme.get("dataColors", []) if isinstance(c, str)]
        _SCALE_COLOURS = frozenset(c.upper() for c in colours)
    return _SCALE_COLOURS


def theme_colour(key):
    """One colour code of the owner's theme file, in upper case, or None."""
    path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "theme", "theme.json")
    try:
        with open(path, encoding="utf-8-sig") as fh:
            value = json.load(fh).get(key)
    except (OSError, ValueError, AttributeError):
        return None
    return value.upper() if isinstance(value, str) else None


def _scale_end(part):
    """'minimum', 'maximum' or None: which of the theme's scale colours one end of a colour scale uses."""
    colour = part.get("color") if isinstance(part, dict) else None
    text = literal({"expr": colour}) if isinstance(colour, dict) and "Literal" in colour else literal(colour)
    if not isinstance(text, str):
        return None
    for keyword, key in (("minColor", "minimum"), ("maxColor", "maximum")):
        if text == keyword or text.upper() == theme_colour(key):
            return key
    return None


def red_green_scales(node, found=None):
    """How many colour scales in a visual run from the theme's minimum colour to its maximum colour, either way."""
    found = [] if found is None else found
    if isinstance(node, dict):
        for key, value in node.items():
            if key in SCALE_PARTS and isinstance(value, dict):
                ends = {_scale_end(value.get("min")), _scale_end(value.get("max"))}
                if ends == {"minimum", "maximum"}:
                    found.append(key)
            else:
                red_green_scales(value, found)
    elif isinstance(node, list):
        for value in node:
            red_green_scales(value, found)
    return len(found)


RETIRING_TYPES = {"map": "the Bing map (deprecated: use the Azure map, azureMap)",
                  "filledMap": "the filled Bing map (deprecated: use the Azure map, azureMap)",
                  "qnaVisual": "the Q&A visual (deprecated with Q&A)",
                  "scriptVisual": "the R visual (Microsoft is retiring it)",
                  "pythonVisual": "the Python visual (Microsoft is retiring it)"}
OLD_CARD_TYPES = frozenset(("card", "multiRowCard"))
REPORT_MEASURE_PREFIX = "_"         # Microsoft Learn, "Separate reports from models": its example of a prefix
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


DATA_BAR_PARTS = ("positiveColor", "negativeColor")      # the two bar colours; the axis colour is optional


def _half_data_bars(node, missing=None):
    """Names of the bar colours that a 'dataBars' setting anywhere in a visual lacks."""
    missing = [] if missing is None else missing
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "dataBars" and isinstance(value, dict):
                missing.extend(part for part in DATA_BAR_PARTS if part not in value and part not in missing)
            else:
                _half_data_bars(value, missing)
    elif isinstance(node, list):
        for value in node:
            _half_data_bars(value, missing)
    return missing


def styling(node, path, found, scale=False):
    """Add the names of colour, font and size settings written on a visual itself.
    Inside a colour scale (scale=True) the theme file's own scale colours pass: a scale cannot use ThemeDataColor."""
    if isinstance(node, dict):
        for key, value in node.items():
            if key in STYLE_PROPERTIES and isinstance(value, dict):
                text = literal(value)
                solid = value.get("solid") if isinstance(value.get("solid"), dict) else None
                if solid is not None:
                    text = literal(solid.get("color"))
                    if text is None and isinstance(solid.get("color"), dict) and "ThemeDataColor" in solid["color"].get("expr", {}):
                        continue                         # a colour taken from the theme
                if text is not None and key.lower().endswith("color") and not HEX_COLOUR.search(text):
                    continue                             # a theme colour named by keyword, such as 'maxColor'
                if text is not None and scale and text.strip("'").upper() in scale_colours():
                    continue                             # the theme file's colour for a colour scale
                if text is not None or solid is not None:
                    found.add("%s.%s" % (path, key) if path else key)
            elif isinstance(value, str) and HEX_COLOUR.search(value) and key == "Value":
                if not (scale and value.strip("'").upper() in scale_colours()):
                    found.add("%s (a colour written as a code)" % path if path else "a colour written as a code")
            else:
                styling(value, path if key in ("properties", "expr", "solid", "Literal") or isinstance(node, list) else key,
                        found, scale or key in SCALE_PARTS)
    elif isinstance(node, list):
        for value in node:
            styling(value, path, found, scale)


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
    _report_level(cp, report_dir, pages, brief, findings)
    direct_query = _reads_direct_query(cp, report_dir)
    report = cp.load_object(os.path.join(report_dir, "definition", "report.json")) or {}
    reduction = report.get("slowDataSourceSettings") if isinstance(report.get("slowDataSourceSettings"), dict) else {}
    apply_buttons = reduction.get("isSlicerSelectionsButtonEnabled") is True or reduction.get("isApplyAllButtonEnabled") is True
    registered = _registered(report)
    auto_subtitles = _subtitles_on(cp, report_dir, report, registered)
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
            active = [(v, kind) for v, kind in types
                      if isinstance(v["visual"].get("query"), dict) and v["data"].get("isHidden") is not True]
            count = len(active)
            area = page["page"].get("width", 0) * page["page"].get("height", 0) if all(
                cp._is_number(page["page"].get(k)) for k in ("width", "height")) else 0
            big = []
            for visual, kind in active:
                position = visual["data"].get("position") if isinstance(visual["data"].get("position"), dict) else {}
                if (kind in TABLE_TYPES and area and cp._is_number(position.get("width")) and cp._is_number(position.get("height"))
                        and position["width"] * position["height"] >= area * BIG_TABLE_SHARE):
                    big.append(shown(visual))
            count += len(big)
            twice = " (%s counted twice: a large table or matrix)" % ", ".join(big) if big else ""
            if count > DENSITY_LIMIT:
                add("V006", page, None, "page '%s' has %d visuals that show data%s; the checklist asks for a written "
                    "reason above %d. Split the page, or list the reason in section 10 of the brief"
                    % (title, count, twice, DENSITY_LIMIT), level="error")
            elif count >= DENSITY_REVIEW:
                add("V007", page, None, "page '%s' has %d visuals that show data%s; the checklist asks for a review "
                    "from %d" % (title, count, twice, DENSITY_REVIEW))

        page_filters = _filters(page["page"])
        left_over = [f.get("name") or "?" for f in page_filters if isinstance(f.get("filter"), dict)
                     and (page["kind"] == "Tooltip" or f.get("howCreated") == "Drillthrough")]
        if left_over:
            add("V013", page, None, "page '%s' has values saved in its %s filter(s) (%s). They are left over from "
                "design time and readers would start from them: clear the filter in Power BI Desktop and save"
                % (title, "tooltip" if page["kind"] == "Tooltip" else "drillthrough", ", ".join(left_over[:5])))
        if (page["kind"] == "Drillthrough" and not hidden_page
                and not any(kind == "Bookmark" for _, (kind, _) in actions)):
            add("V014", page, None, "drillthrough page '%s' is visible and has no reset button (a button whose action "
                "is a bookmark). Microsoft advises hiding a drillthrough page; a visible one needs a way back to its "
                "starting state" % title)
        for owner, visual in [(page["page"], None)] + [(v["data"], v) for v in page["visuals"]]:
            lost = _lost_sources(owner)
            if lost:
                add("V015", page, visual, "a filter of %s uses the source name(s) %s in its Where part, and its From "
                    "part does not declare them; the filter cannot be read"
                    % ("'%s'" % shown(visual) if visual else "page '%s'" % title, ", ".join(lost)))
        old_cards = []
        for visual, kind in types:
            if kind in RETIRING_TYPES:
                add("V016", page, visual, "'%s' is %s. Do not build new ones; plan a replacement for this one, or "
                    "list the reason in section 10 of the brief" % (shown(visual), RETIRING_TYPES[kind]))
            elif kind in OLD_CARD_TYPES and not excused("U105", page, visual):
                old_cards.append(shown(visual))
            red_green = red_green_scales(visual["visual"])
            if red_green:
                add("V026", page, visual, "'%s' colours %d colour scale(s) from the theme's red (minimum) to its green "
                    "(maximum). That says low is bad and high is good, and red with green is hard to tell apart. For an "
                    "amount use one colour from light to dark; keep red to green only where the brief says which way is "
                    "good, with an icon, a sign or a word beside it, and list the reason in section 10 of the brief"
                    % (shown(visual), red_green))
            half = _half_data_bars(visual["visual"])
            if half:
                add("V024", page, visual, "the data bars of '%s' lack %s. Data bars are one setting made of parts; "
                    "without their bar colours Power BI Desktop fails to load the whole report. Put the part back with a "
                    "theme colour, or remove the data bars as a whole" % (shown(visual), ", ".join(half)), level="error")
            used_items = set()
            _resources(visual["data"], used_items)
            lost = sorted(item for item in used_items if item not in registered
                          or not os.path.isfile(os.path.join(report_dir, "StaticResources", "RegisteredResources",
                                                             *registered[item].split("/"))))
            if lost:
                add("V017", page, visual, "'%s' uses the resource file(s) %s, which report.json does not register or "
                    "which are not in StaticResources/RegisteredResources; the picture stays empty"
                    % (shown(visual), ", ".join(lost)))
        if old_cards:
            add("U105", page, None, "page '%s' uses the older card visuals (%s). The new card visual (cardVisual) "
                "replaces the card and the multi-row card and can show several values" % (title, ", ".join(old_cards[:6])),
                level="note")
        if (page["kind"] != "Tooltip" and any(isinstance(v["visual"].get("query"), dict) for v in page["visuals"])
                and not any(kind == "textbox" for _, kind in types)):
            add("V018", page, None, "page '%s' has no text box, so it has no visible page title. The layout standard "
                "keeps the top-left of every page for a title text box" % title, level="note")
        binding = page["page"].get("pageBinding") if isinstance(page["page"].get("pageBinding"), dict) else {}
        settings = report.get("settings") if isinstance(report.get("settings"), dict) else {}
        if binding.get("referenceScope") == "CrossReport" and settings.get("useCrossReportDrillthrough") is not True:
            add("V023", page, None, "page '%s' is a target for cross-report drillthrough, but report.json does not "
                "switch the feature on (settings.useCrossReportDrillthrough). Other reports cannot reach the page "
                "until it is on" % title)
        if direct_query:
            costly = sorted({shown(v) for v in page["visuals"] for f in _filters(v["data"])
                             if f.get("type") in ("TopN", "VisualTopN")
                             or (isinstance(f.get("field"), dict) and "Measure" in f["field"] and isinstance(f.get("filter"), dict))})
            if costly:
                add("U106", page, None, "page '%s', on a model with DirectQuery tables: %s use a Top N filter or a filter "
                    "on a measure. Each sends extra queries to the source; keep them only where readers need them"
                    % (title, ", ".join(costly[:6])), level="note")
        slicers = [v for v, kind in types if kind in SLICER_TYPES]
        if direct_query and len(slicers) >= 2 and not apply_buttons and page["kind"] is None:
            add("U104", page, None, "page '%s' has %d slicers on a model with DirectQuery tables, and the report has no "
                "Apply button for slicers. With an Apply button the source is asked once, after all choices are made "
                "(Options, Query reduction)" % (title, len(slicers)), level="note")

        for visual, (kind, link) in actions:
            for wanted, key, target in LINK_TARGETS:
                name = literal(link.get(key))
                if kind == wanted and name is not None:
                    known = bookmark_names if target == "bookmark" else page_names
                    if name not in known:
                        add("V008", page, visual, "the action of '%s' goes to %s '%s', which this report does not have; "
                            "the button does nothing" % (shown(visual), target, name))

        no_alt, made_up, second = [], [], []
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
            if ((has_data or kind == "image") and visual["data"].get("isHidden") is not True and "altText" not in general
                    and not excused("A001", page, visual)):
                no_alt.append(shown(visual))
            alt = literal(general.get("altText"))
            if alt is not None and len(alt) > ALT_TEXT_LIMIT and not excused("A004", page, visual):
                add("A004", page, visual, "the alt text of '%s' has %d characters; Power BI's alt text box takes %d"
                    % (shown(visual), len(alt), ALT_TEXT_LIMIT))
            title_card = card(body, "title")
            if (has_data and kind not in SLICER_TYPES and literal(title_card.get("show")) != "false"
                    and "text" not in title_card and page["kind"] != "Tooltip" and not excused("A003", page, visual)):
                made_up.append(shown(visual))
            subtitle = card(body, "subTitle")
            if (auto_subtitles and has_data and kind not in SLICER_TYPES and literal(title_card.get("show")) != "false"
                    and literal(subtitle.get("show")) != "false" and "text" not in subtitle
                    and not excused("V025", page, visual)):
                second.append(shown(visual))
            if kind in SLICER_TYPES and page["kind"] is None:
                used = set()
                fields(body.get("query"), used)
                for field in used:
                    slicer_fields.setdefault(field, []).append((page, visual, isinstance(body.get("syncGroup"), dict)))

        if no_alt:
            add("A001", page, None, "page '%s': %d visual(s) have no alt text: %s. Microsoft's accessibility checklist "
                "asks for alt text on every visual that is not decoration: say what the visual shows (general.altText). "
                "An image that is only decoration is listed in section 10 of the brief instead"
                % (title, len(no_alt), ", ".join(no_alt[:10]) + (" ..." if len(no_alt) > 10 else "")))
        if second:
            add("V025", page, None, "page '%s': %d visual(s) may show an automatic subtitle under the title: %s. Their files "
                "neither switch the subtitle off nor write one, and the report's base theme switches it on (it then "
                "repeats the field names). Set subTitle show to false, or write a subtitle that adds something"
                % (title, len(second), ", ".join(second[:10]) + (" ..." if len(second) > 10 else "")))
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


def _filters(owner):
    config = owner.get("filterConfig") if isinstance(owner, dict) else None
    filters = config.get("filters") if isinstance(config, dict) else None
    return [f for f in filters if isinstance(f, dict)] if isinstance(filters, list) else []


def _lost_sources(owner):
    """Source names that the Where part of a filter uses and its From part does not declare."""
    lost = set()
    for entry in _filters(owner):
        body = entry.get("filter")
        if not isinstance(body, dict) or not isinstance(body.get("From"), list):
            continue
        declared = {source.get("Name") for source in body["From"] if isinstance(source, dict)}
        used = set()

        def walk(node):
            if isinstance(node, dict):
                reference = node.get("SourceRef")
                if isinstance(reference, dict) and isinstance(reference.get("Source"), str):
                    used.add(reference["Source"])
                for value in node.values():
                    walk(value)
            elif isinstance(node, list):
                for value in node:
                    walk(value)
        walk(body.get("Where"))
        lost |= used - declared
    return sorted(lost)


def _resources(node, found):
    """Add the ItemName of every file a JSON value takes from the report's registered resources."""
    if isinstance(node, dict):
        item = node.get("ResourcePackageItem")
        if isinstance(item, dict) and isinstance(item.get("ItemName"), str) \
                and item.get("PackageName", "RegisteredResources") == "RegisteredResources":
            found.add(item["ItemName"])
        for value in node.values():
            _resources(value, found)
    elif isinstance(node, list):
        for value in node:
            _resources(value, found)


def _registered(report):
    """{item name: path} of the files report.json registers in its RegisteredResources package."""
    out = {}
    packages = report.get("resourcePackages") if isinstance(report, dict) else None
    for package in packages if isinstance(packages, list) else []:
        if not isinstance(package, dict) or package.get("type") != "RegisteredResources":
            continue
        for item in package.get("items") if isinstance(package.get("items"), list) else []:
            if isinstance(item, dict) and isinstance(item.get("name"), str) and isinstance(item.get("path"), str):
                out[item["name"]] = item["path"]
    return out


SUBTITLE_BASE_THEMES = ("Fluent2",)   # Microsoft's Fluent2-CY26SU08 base theme switches subTitle on for every visual


def _subtitle_switch(theme):
    """True or False when a theme sets subTitle show for every visual ('*'), None when it does not say."""
    styles = theme.get("visualStyles") if isinstance(theme, dict) else None
    every = styles.get("*", {}).get("*", {}) if isinstance(styles, dict) and isinstance(styles.get("*"), dict) else {}
    entries = every.get("subTitle") if isinstance(every, dict) else None
    for entry in entries if isinstance(entries, list) else []:
        if isinstance(entry, dict) and isinstance(entry.get("show"), bool):
            return entry["show"]
    return None


def _subtitles_on(cp, report_dir, report, registered):
    """True when the report's themes show a subtitle on every visual unless the visual says otherwise: the custom
    theme decides when it says; else the base theme file, when the project holds it; else the base theme's name."""
    collection = report.get("themeCollection") if isinstance(report.get("themeCollection"), dict) else {}
    custom = collection.get("customTheme") if isinstance(collection.get("customTheme"), dict) else {}
    if isinstance(custom.get("name"), str) and custom["name"] in registered:
        path = os.path.join(report_dir, "StaticResources", "RegisteredResources", *registered[custom["name"]].split("/"))
        said = _subtitle_switch(cp.load_object(path) or {})
        if said is not None:
            return said
    base = collection.get("baseTheme") if isinstance(collection.get("baseTheme"), dict) else {}
    name = base.get("name") if isinstance(base.get("name"), str) else ""
    if not name:
        return False
    path = os.path.join(report_dir, "StaticResources", "SharedResources", "BaseThemes", name + ".json")
    if os.path.isfile(path):
        said = _subtitle_switch(cp.load_object(path) or {})
        if said is not None:
            return said
    return name.startswith(SUBTITLE_BASE_THEMES)


def _reads_direct_query(cp, report_dir):
    """True when the report's model is in this project and has a table in DirectQuery mode."""
    model_dir = cp.report_model(report_dir)
    tables = os.path.join(model_dir, "definition", "tables") if model_dir else None
    if not tables or not os.path.isdir(tables):
        return False
    for name in sorted(os.listdir(tables)):
        if name.lower().endswith(".tmdl"):
            try:
                with open(os.path.join(tables, name), encoding="utf-8-sig") as handle:
                    if re.search(r"(?mi)^\s*mode:\s*directQuery\s*$", handle.read()):
                        return True
            except (OSError, UnicodeDecodeError):
                continue
    return False


def _projection_format(node):
    """True when a field of a visual's query carries its own format string."""
    if isinstance(node, dict):
        projections = node.get("projections")
        if isinstance(projections, list) and any(isinstance(p, dict) and isinstance(p.get("format"), str) for p in projections):
            return True
        return any(_projection_format(value) for value in node.values())
    if isinstance(node, list):
        return any(_projection_format(value) for value in node)
    return False


def _translated(cp, report_dir):
    """True when the report's model is in this project and a culture file of it holds translations."""
    model_dir = cp.report_model(report_dir)
    folder = os.path.join(model_dir, "definition", "cultures") if model_dir else None
    if not folder or not os.path.isdir(folder):
        return False
    for name in sorted(os.listdir(folder)):
        if name.lower().endswith(".tmdl"):
            try:
                with open(os.path.join(folder, name), encoding="utf-8-sig") as handle:
                    if re.search(r"(?m)^\s*translations\s*$", handle.read()):
                        return True
            except (OSError, UnicodeDecodeError):
                continue
    return False


def _report_level(cp, report_dir, pages, brief, findings):
    """V012: a report-level measure without the prefix. V015 and V017 for report.json itself."""
    definition = os.path.join(report_dir, "definition")
    path = os.path.join(definition, "reportExtensions.json")
    data = cp.load_object(path) if os.path.isfile(path) else None
    prefix = brief.get("report_prefix") or REPORT_MEASURE_PREFIX
    bare = []
    for entity in (data or {}).get("entities", []) if isinstance((data or {}).get("entities"), list) else []:
        for measure in entity.get("measures", []) if isinstance(entity, dict) and isinstance(entity.get("measures"), list) else []:
            name = measure.get("name") if isinstance(measure, dict) else None
            if isinstance(name, str) and not name.startswith(prefix) \
                    and not cp.layout_excused(brief, "V012", {"-"}, {name}):
                bare.append(name)
    if bare:
        findings.add("V012", path, 0, "report-level measure(s) %s do not start with '%s'. Microsoft advises a prefix on "
                     "measures a report defines, so that a measure added to the model later can never have the same "
                     "name. Renaming one changes the visuals that use it" % (", ".join("[%s]" % n for n in bare), prefix),
                     level="warn")
    if data is not None and "USERCULTURE" in str(data).upper() and not cp.layout_excused(brief, "V019", {"-"}, {"-"}):
        findings.add("V019", path, 0, "a report-level measure calls USERCULTURE. Microsoft says it can return the wrong "
                     "language there: write the measure in the model", level="warn")
    if _translated(cp, report_dir):
        typed, titled = [], 0
        for page in pages:
            for visual in page["visuals"]:
                if visual["visual"].get("visualType") == "textbox":
                    typed.append(visual["label"] or visual["name"])
                if literal(card(visual["visual"], "title").get("text")) is not None:
                    titled += 1
        if (typed or titled) and not cp.layout_excused(brief, "V020", {"-"}, {"-"}):
            findings.add("V020", os.path.join(definition, "report.json"), 0, "the model has translations, and this report "
                         "holds typed text that Power BI never translates: %d text box(es) and %d typed visual title(s). "
                         "Take such text from a label measure (multiple-languages.md), or list the reason in section 10 "
                         "of the brief with '-' for the page and the visual" % (len(typed), titled), level="warn")
        tabs = [p["page"].get("displayName") or p["name"] for p in pages
                if p["page"].get("visibility") != "HiddenInViewMode"]
        if len(tabs) > 1 and not cp.layout_excused(brief, "V021", {"-"}, {"-"}):
            findings.add("V021", os.path.join(definition, "pages", "pages.json"), 0, "the model has translations, and "
                         "this report shows %d page tabs. Tab names are never translated: Microsoft's design hides every "
                         "page but one and moves between pages with buttons" % len(tabs), level="warn")
    agreed = brief.get("agreed", [])
    seen = {}
    for page in pages:
        for visual in page["visuals"]:
            if visual["visual"].get("visualType") == "ganttChart":
                seen.setdefault(("gantt",), ("the Gantt visual", visual))
            if _projection_format(visual["visual"].get("query")):
                seen.setdefault(("format string on a visual", "visual-level format"),
                                ("a format string set on one visual (format on a field of the visual)", visual))
    for words, (what, visual) in sorted(seen.items()):
        if not any(word in name for word in words for name in agreed):
            findings.add("V022", visual["path"], 0, "the report uses %s, which Microsoft still lists as a preview "
                         "feature. A preview feature is used only after the developer's yes: add its row to section 11 "
                         "of the brief (name it '%s')" % (what, words[0]), level="warn")
    report_path = os.path.join(definition, "report.json")
    report = cp.load_object(report_path) or {}
    lost = _lost_sources(report)
    if lost:
        findings.add("V015", report_path, 0, "a report-level filter uses the source name(s) %s in its Where part, and "
                     "its From part does not declare them; the filter cannot be read" % ", ".join(lost), level="warn")
    missing = sorted(name for name, item_path in _registered(report).items()
                     if not os.path.isfile(os.path.join(report_dir, "StaticResources", "RegisteredResources",
                                                        *item_path.split("/"))))
    if missing:
        findings.add("V017", report_path, 0, "report.json registers the resource file(s) %s, which are not in "
                     "StaticResources/RegisteredResources" % ", ".join(missing), level="warn")

