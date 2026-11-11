#!/usr/bin/env python3
"""Set Header icons off and Tooltips off on every visual, and add labels to existing visuals.

Usage:
    python scripts/set_visual_defaults.py <folder> [--dry-run]
    python scripts/set_visual_defaults.py <folder> --label <page>/<visual>=<Page_Type_Subject> [--label ...]

What it changes in each visual.json under <folder>:
  * visual.visualContainerObjects.visualHeader  -> show = false
  * visual.visualContainerObjects.visualTooltip -> show = false
  A setting named in the visual's HeaderTooltipException annotation ("header: ...", "tooltip: ..." or
  "both: ...") is left alone. Groups (visualGroup) are left alone.
  A 'show' that is on in a visual's mobile layout (mobile.json) is turned off as well.
With --label it also adds or updates a VisualLabel annotation on the named visual. It never renames a visual.
<page> and <visual> are the folder names (or the 'name' values) of the page and the visual, as printed by
list_visuals.py in its 'Page' line and its 'folder' column.

Only those settings change. A file that is changed is written again as a whole with two-space
indentation, so its layout and character escapes may look different in a diff; every value stays the same.
A file that is not valid JSON, or whose structure is not what Power BI expects, is reported and left untouched.

Save your work in Power BI Desktop before running this. Afterwards reload the project in Desktop.
Needs Python 3.8 or later. Uses the standard library only.
Exit code: 0 = done, 1 = a file was skipped or a --label could not be applied, 2 = wrong usage.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp  # noqa: E402

CARDS = (("visualHeader", "header icons off"), ("visualTooltip", "tooltips off"))


def _false():
    return {"expr": {"Literal": {"Value": "false"}}}


def set_show_false(data, card, only_if_on=False):
    """Return True when the JSON was changed. Raises ValueError when the structure is not as expected."""
    state = cp.show_state(data, card)
    if state == "malformed":
        raise ValueError("'%s' is not a list of { \"properties\": { ... } } entries" % card)
    if state == "off" or (only_if_on and state not in ("on", "other")):
        return False
    objects = data["visual"].setdefault("visualContainerObjects", {})
    entries = objects.setdefault(card, [])
    target = None
    for entry in entries:
        properties = entry.setdefault("properties", {})
        if "show" in properties and cp.literal_bool(properties["show"]) is not False:
            properties["show"] = _false()          # was on, or not in the literal form
        if target is None and "selector" not in entry:
            target = entry
    if cp.show_state(data, card) != "off":
        if target is None:
            target = {"properties": {}}
            entries.append(target)
        target["properties"]["show"] = _false()
    return True


def _no_constants(name):
    raise ValueError("%s is not valid JSON" % name)


def _no_repeats(pairs):
    seen = {}
    for key, value in pairs:
        if key in seen:
            raise ValueError("the key '%s' appears twice in one object" % key)
        seen[key] = value
    return seen


def read_with_style(path):
    """Parse a JSON object, keeping every decimal number exactly as it is written in the file."""
    with open(path, "rb") as fh:
        raw = fh.read()
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    text = raw.decode("utf-8")
    numbers = []

    def keep(literal):
        numbers.append(literal)
        return "\x00number%d\x00" % (len(numbers) - 1)

    data = json.loads(text, parse_float=keep, parse_constant=_no_constants, object_pairs_hook=_no_repeats)
    if not isinstance(data, dict):
        raise ValueError("the file is not a JSON object")
    return data, {"newline": "\r\n" if "\r\n" in text else "\n", "final_newline": text.endswith("\n"),
                  "numbers": numbers}


def write_with_style(path, data, style):
    """Build the whole file in memory first, then swap it in, so a failure never leaves a half-written file."""
    text = json.dumps(data, indent=2, ensure_ascii=False)
    for index, literal in enumerate(style["numbers"]):
        text = text.replace(json.dumps("\x00number%d\x00" % index), literal)
    if style["final_newline"]:
        text += "\n"
    payload = text.replace("\n", style["newline"]).encode("utf-8")     # UTF-8 without BOM
    temporary = path + ".tmp"
    with open(temporary, "wb") as fh:
        fh.write(payload)
    os.replace(temporary, path)


def set_label(data, label):
    annotations = data.setdefault("annotations", [])
    if not isinstance(annotations, list):
        raise ValueError("'annotations' is not a list")
    for item in annotations:
        if isinstance(item, dict) and item.get("name") == cp.LABEL_ANNOTATION:
            if item.get("value") == label:
                return False
            item["value"] = label
            return True
    annotations.append({"name": cp.LABEL_ANNOTATION, "value": label})
    return True


def check_shape(data):
    is_visual = isinstance(data.get("visual"), dict)
    is_group = isinstance(data.get("visualGroup"), dict)
    if is_visual == is_group:
        raise ValueError("needs exactly one of 'visual' or 'visualGroup', as an object")
    if "annotations" in data and not isinstance(data["annotations"], list):
        raise ValueError("'annotations' is not a list")
    return is_visual


def fix_mobile(visual_path, excused, dry_run):
    """Turn off a header or tooltip that is on in the visual's mobile layout. Returns ['mobile layout'] if changed."""
    mobile_path = os.path.join(os.path.dirname(visual_path), "mobile.json")
    if not os.path.isfile(mobile_path):
        return []
    mobile, style = read_with_style(mobile_path)
    wrapper = {"visual": mobile}
    changed = [card for card, _ in CARDS if card not in excused and set_show_false(wrapper, card, only_if_on=True)]
    if changed and not dry_run:
        write_with_style(mobile_path, mobile, style)
    return ["mobile layout"] if changed else []


def strings(*values):
    return {v for v in values if isinstance(v, str)}


def main(argv):
    cp.safe_output()
    args = argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    labels = {}
    while "--label" in args:
        at = args.index("--label")
        if at + 1 >= len(args) or "=" not in args[at + 1] or "/" not in args[at + 1].split("=")[0]:
            print(__doc__)
            return 2
        target, label = args[at + 1].split("=", 1)
        labels[tuple(target.split("/", 1))] = label
        del args[at:at + 2]
    if len(args) != 1 or args[0].startswith("-"):
        print(__doc__)
        return 2
    root = os.path.abspath(args[0])
    reports = cp.find_reports(root)
    if not reports:
        print("No *.Report folder found under %s." % args[0])
        return 2

    failed = False
    changed = 0
    used = set()
    for report in reports:
        for page_folder_name, page_folder, page_path in cp.iter_pages(report):
            page = cp.load_object(page_path) or {}
            page_keys = strings(page_folder_name, page.get("name"))
            visuals = list(cp.iter_visuals(page_folder))
            taken = {}                                   # name or label -> folder, for every visual on the page
            for folder_name, visual_path in visuals:
                other = cp.load_object(visual_path) or {}
                for value in strings(other.get("name"), cp.annotation(other, cp.LABEL_ANNOTATION)):
                    taken.setdefault(value, folder_name)
            for folder_name, visual_path in visuals:
                rel = os.path.relpath(visual_path, root).replace(os.sep, "/")
                try:
                    data, style = read_with_style(visual_path)
                    is_visual = check_shape(data)
                except (OSError, ValueError, RecursionError) as exc:
                    print("skipped  %s: %s" % (rel, str(exc)[:200]))
                    failed = True
                    continue
                touched = []
                try:
                    for (page_key, visual_key), label in labels.items():
                        if page_key in page_keys and visual_key in strings(folder_name, data.get("name")):
                            used.add((page_key, visual_key))
                            if not cp.is_label(label, page.get("name"), page.get("displayName")):
                                print("Label '%s' is not a Page_Type_Subject label for page '%s'." % (label, page.get("displayName")))
                                failed = True
                            elif taken.get(label, folder_name) != folder_name:
                                print("Label '%s' is already the name or label of another visual on this page (%s)." % (label, taken[label]))
                                failed = True
                            elif set_label(data, label):
                                taken[label] = folder_name
                                touched.append("label")
                    if is_visual:
                        excused = cp.excused_cards(data)
                        for card, words in CARDS:
                            if card in excused:
                                continue
                            replaced = cp.show_state(data, card) == "other"
                            if set_show_false(data, card):
                                touched.append(words + (" (replaced a value that was not a plain true/false)" if replaced else ""))
                        if not excused and cp.annotation(data, cp.EXCEPTION_ANNOTATION) is not None:
                            print("note     %s: its %s annotation does not start with 'header:', 'tooltip:' or 'both:', so it was not applied"
                                  % (rel, cp.EXCEPTION_ANNOTATION))
                    if touched and not dry_run:
                        write_with_style(visual_path, data, style)
                    if is_visual:
                        try:
                            touched += fix_mobile(visual_path, excused, dry_run)
                        except (OSError, ValueError, AttributeError, TypeError, KeyError, RecursionError) as exc:
                            print("skipped  %s: unexpected content (%s)" % (rel[:-len("visual.json")] + "mobile.json", str(exc)[:200]))
                            failed = True
                except (OSError, ValueError, AttributeError, TypeError, KeyError, RecursionError) as exc:
                    print("skipped  %s: unexpected content (%s)" % (rel, str(exc)[:200]))
                    failed = True
                    continue
                if touched:
                    changed += 1
                    print("%s  %s: %s" % ("would change" if dry_run else "changed", rel, ", ".join(touched)))
    for key in labels:
        if key not in used:
            print("--label target not found: %s/%s" % key)
            failed = True
    print("%d visual file(s) %s." % (changed, "would change" if dry_run else "changed"))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
