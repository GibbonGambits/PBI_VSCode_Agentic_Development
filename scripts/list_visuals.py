#!/usr/bin/env python3
"""List the visuals on a report page: label, type, x, y, width, height, and the visual's folder.

Usage:
    python scripts/list_visuals.py <folder>                 every page of every report under <folder>
    python scripts/list_visuals.py <folder> --page <page>   one page (its name, folder name or tab name)

The label is the visual's VisualLabel annotation when it has one, otherwise its name.
The folder column is what you pass to set_visual_defaults.py --label.
Needs Python 3.8 or later. Uses the standard library only. Reads files; never changes them.
Exit code: 0 = listed, 2 = wrong usage or page not found.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp  # noqa: E402

HEADER = ("label", "type", "x", "y", "width", "height", "folder")


def _number(value):
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return ""
    try:
        return ("%.2f" % value).rstrip("0").rstrip(".")
    except (OverflowError, ValueError):
        return str(value)


def visual_rows(page_folder):
    rows = []
    for folder_name, visual_path in cp.iter_visuals(page_folder):
        data = cp.load_object(visual_path)
        if data is None:
            rows.append((folder_name, "unreadable", "", "", "", "", folder_name))
            continue
        label = cp.annotation(data, cp.LABEL_ANNOTATION) or data.get("name")
        label = label if isinstance(label, str) and label else folder_name
        visual = data.get("visual")
        if "visualGroup" in data:
            kind = "group"
        elif isinstance(visual, dict) and isinstance(visual.get("visualType"), str):
            kind = visual["visualType"]
        else:
            kind = "?"
        position = data.get("position")
        if not isinstance(position, dict):
            position = {}
        rows.append((label, kind) + tuple(_number(position.get(k)) for k in ("x", "y", "width", "height"))
                    + (folder_name,))
    return rows


def print_table(rows):
    table = [HEADER] + [tuple(str(c) for c in row) for row in rows]
    widths = [max(len(row[i]) for row in table) for i in range(len(HEADER))]
    for index, row in enumerate(table):
        print("  ".join(cell.ljust(widths[i]) for i, cell in enumerate(row)).rstrip())
        if index == 0:
            print("  ".join("-" * w for w in widths))


def main(argv):
    cp.safe_output()
    args = argv[1:]
    wanted = None
    if "--page" in args:
        at = args.index("--page")
        if at + 1 >= len(args):
            print(__doc__)
            return 2
        wanted = args[at + 1]
        del args[at:at + 2]
    if len(args) != 1 or args[0].startswith("-"):
        print(__doc__)
        return 2
    root = os.path.abspath(args[0])
    reports = cp.find_reports(root)
    if not reports:
        print("No *.Report folder found under %s." % args[0])
        return 2
    shown = 0
    for report in reports:
        for folder_name, page_folder, page_path in cp.iter_pages(report):
            page = cp.load_object(page_path) or {}
            names = {n for n in (folder_name, page.get("name"), page.get("displayName")) if isinstance(n, str)}
            if wanted is not None and wanted not in names:
                continue
            shown += 1
            print("Report: %s   Page: %s (name %s, folder %s)   Size: %s x %s" % (
                os.path.basename(report), page.get("displayName"), page.get("name"), folder_name,
                _number(page.get("width")), _number(page.get("height"))))
            print_table(visual_rows(page_folder))
            print()
    if shown == 0:
        print("Page not found: %s" % wanted if wanted is not None else "The report has no pages.")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
