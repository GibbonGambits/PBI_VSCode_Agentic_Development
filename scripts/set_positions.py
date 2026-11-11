#!/usr/bin/env python3
"""Write approved positions and sizes of visuals. Only 'position' x, y, width and height change.

Usage:
    python scripts/set_positions.py <folder> [--dry-run] --move "<page>/<visual>=<x>,<y>,<width>,<height>" [--move ...]
    python scripts/set_positions.py <folder> [--dry-run] --snap [--page <page>]

<page>    the page's folder name, its 'name' or its tab name, as list_visuals.py prints them.
<visual>  the visual's folder name, its 'name' or its label.
--snap    rounds x, y, width and height of each visual to the grid step of the layout standard
          (8 pixels unless docs/report-brief.md under <folder> gives another step).

Left alone, always: groups and the visuals inside a group (Microsoft's schema does not say whether a member's
position counts from the page or from its group), rotated visuals, tooltip pages (for --snap), every mobile.json,
the stacking order (z) and the tab order. A --move that would put a visual outside its page is refused, and then
no file at all is written.

Run it with --dry-run first and show the developer the old and new numbers. A file that changes is written again
as a whole; its values stay the same. Save in Power BI Desktop before running this; afterwards reload the project
in Desktop and look at the pages the script names: files that pass the checks can still look wrong on screen.
Needs Python 3.8 or later. Uses the standard library only.
Exit code: 0 = done, 1 = a change was refused (nothing written), 2 = wrong usage.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp          # noqa: E402
import set_visual_defaults as svd   # noqa: E402

KEYS = ("x", "y", "width", "height")


def _plain(number):
    return int(number) if float(number) == int(number) else number


def _show(values):
    return ", ".join("%s %g" % (k, v) for k, v in zip(KEYS, values))


def pages(root):
    """(report, page folder name, page folder, page.json content) for every page under root."""
    for report in cp.find_reports(root):
        for folder_name, folder, page_path in cp.iter_pages(report):
            yield report, folder_name, folder, cp.load_object(page_path) or {}


def main(argv):
    cp.safe_output()
    args = argv[1:]
    dry_run = "--dry-run" in args
    snap = "--snap" in args
    args = [a for a in args if a not in ("--dry-run", "--snap")]
    moves, wanted_page = {}, None
    try:
        while "--move" in args:
            at = args.index("--move")
            target, numbers = args[at + 1].rsplit("=", 1)
            page, visual = target.split("/", 1)
            values = [float(n) for n in numbers.split(",")]
            if len(values) != 4 or not all(cp._is_number(v) for v in values):
                raise ValueError
            moves[(page.strip(), visual.strip())] = values
            del args[at:at + 2]
        if "--page" in args:
            at = args.index("--page")
            wanted_page = args[at + 1]
            del args[at:at + 2]
    except (ValueError, IndexError):
        print(__doc__)
        return 2
    if len(args) != 1 or args[0].startswith("-") or not (moves or snap) or (moves and snap):
        print(__doc__)
        return 2
    root = os.path.abspath(args[0])
    if not cp.find_reports(root):
        print("No *.Report folder found under %s." % args[0])
        return 2
    grid = cp.read_brief(root)["grid"]

    planned = []            # (path, shown name, page tab name, old values, new values)
    refused = []
    matches = {key: [] for key in moves}
    for report, folder_name, folder, page in pages(root):
        page_keys = {k for k in (folder_name, page.get("name"), page.get("displayName")) if isinstance(k, str)}
        tab = page.get("displayName") if isinstance(page.get("displayName"), str) else folder_name
        width, height = page.get("width"), page.get("height")
        sized = cp._is_number(width) and cp._is_number(height)
        if snap and ((wanted_page is not None and wanted_page not in page_keys) or page.get("type") == "Tooltip"):
            continue
        for visual in cp.page_layout(folder):
            keys = cp._keys(visual)
            old = [visual["x"], visual["y"], visual["w"], visual["h"]]
            where = "%s/%s" % (tab, cp._shown(visual))
            fixed = ("it is a group" if visual["group"] else "it is inside the group '%s'" % visual["parent"]
                     if visual["parent"] else "it is rotated" if visual["rotated"] else None)
            if snap:
                if fixed:
                    print("left alone  %s: %s" % (where, fixed))
                    continue
                left, top = round(old[0] / grid) * grid, round(old[1] / grid) * grid
                right, bottom = round((old[0] + old[2]) / grid) * grid, round((old[1] + old[3]) / grid) * grid
                new = [left, top, max(right - left, grid), max(bottom - top, grid)]      # edges move, so neighbours that touch still touch
                if not sized or new[0] + new[2] > width or new[1] + new[3] > height or new[0] < 0 or new[1] < 0:
                    print("left alone  %s: on the grid it would reach outside the page" % where)
                    continue
                planned.append((visual["path"], where, tab, old, new))
            else:
                for key in moves:
                    if key[0] in page_keys and key[1] in keys:
                        matches[key].append((visual, where, tab, old, fixed, sized, width, height))
    for key, found in matches.items():
        if not found:
            refused.append("--move target not found: %s/%s" % key)
            continue
        if len(found) > 1:
            refused.append("--move target %s/%s fits %d visuals (%s); name the page by its folder and the visual by its folder"
                           % (key[0], key[1], len(found), ", ".join(item[1] for item in found)))
            continue
        visual, where, tab, old, fixed, sized, width, height = found[0]
        new = moves[key]
        if fixed:
            refused.append("%s: %s, so this script does not move it" % (where, fixed))
        elif new[2] <= 0 or new[3] <= 0:
            refused.append("%s: width and height must be more than 0" % where)
        elif not sized:
            refused.append("%s: the page has no width and height, so the move cannot be checked" % where)
        elif new[0] < 0 or new[1] < 0 or new[0] + new[2] > width or new[1] + new[3] > height:
            refused.append("%s: %s would reach outside the page (%g x %g)" % (where, _show(new), width, height))
        else:
            planned.append((visual["path"], where, tab, old, new))
    planned = [item for item in planned if [float(v) for v in item[4]] != [float(v) for v in item[3]]]
    if len({item[0] for item in planned}) != len(planned):
        refused.append("two --move entries name the same visual")
    loaded = {}
    for path, where, tab, old, new in planned:               # read every file first: nothing is written if one cannot be
        try:
            loaded[path] = svd.read_with_style(path)
            if not isinstance(loaded[path][0].get("position"), dict):
                raise ValueError("no 'position' object")
        except (OSError, ValueError, RecursionError) as exc:
            refused.append("%s: the file cannot be read safely (%s)" % (where, str(exc)[:200]))
    if refused:
        for line in refused:
            print("refused  %s" % line)
        print("Nothing was written.")
        return 1

    changed_pages = []
    for path, where, tab, old, new in planned:
        print("%s  %s: %s -> %s" % ("would change" if dry_run else "changed", where, _show(old), _show(new)))
        if tab not in changed_pages:
            changed_pages.append(tab)
        if not dry_run:
            data, style = loaded[path]
            for key, value in zip(KEYS, new):
                data["position"][key] = _plain(value)
            svd.write_with_style(path, data, style)
    print("%d visual(s) %s." % (len(planned), "would change" if dry_run else "changed"))
    if changed_pages:
        print("Reload the project in Power BI Desktop and look at these pages: %s." % ", ".join(changed_pages))
        print("Also check there: the phone layout if the report has one, and the tab order (View > Selection > Tab order).")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
