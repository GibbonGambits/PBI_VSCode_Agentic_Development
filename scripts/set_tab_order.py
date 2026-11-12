#!/usr/bin/env python3
"""Set the keyboard tab order of the visuals on each page to the reading order. Only 'position.tabOrder' changes.

Usage:
    python scripts/set_tab_order.py <folder> [--dry-run] [--page <page>]

<page>    the page's folder name, its 'name' or its tab name, as list_visuals.py prints them.

Reading order: rows from top to bottom, and left to right inside a row. Visuals whose tops lie within two grid
steps of the row's first visual share that row (the grid step of the layout standard: 8 pixels unless
docs/report-brief.md under <folder> gives another step).

Numbers: the page keeps the set of numbers it has when every visual already has its own number; otherwise the
visuals get 0, 1, 2 and so on. Which end of the reading order gets the low numbers follows the page's own
numbers when most pairs of visuals agree on it, then the report's, and otherwise the high numbers go to the top
of the page, as in most of Microsoft's own sample reports. Microsoft's schema says only that tabOrder is the
keyboard selection order: it does not say which end comes first, so look at View > Selection > Tab order in
Power BI Desktop after a run (not confirmed from Microsoft).

Left alone, always: tooltip pages, the visuals inside a group (the group itself takes its place in the order),
every position value but tabOrder, and every mobile.json. Nothing is written if one file cannot be read.

Run it with --dry-run first to see the old and new numbers. Save in Power BI Desktop before running this;
afterwards reload the project in Desktop. Needs Python 3.8 or later. Uses the standard library only.
Exit code: 0 = done, 1 = a file could not be read (nothing written), 2 = wrong usage.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp          # noqa: E402
import set_visual_defaults as svd   # noqa: E402


def reading_order(visuals, tolerance):
    """The visuals in reading order: rows top to bottom, left to right inside a row."""
    rows = []
    for visual in sorted(visuals, key=lambda v: (v["y"], v["x"])):
        if rows and visual["y"] - rows[-1][0]["y"] <= tolerance:
            rows[-1].append(visual)
        else:
            rows.append([visual])
    return [visual for row in rows for visual in sorted(row, key=lambda v: (v["x"], v["y"]))]


def agreement(ordered):
    """(pairs whose numbers rise with the reading order, pairs whose numbers fall) among numbered visuals."""
    numbered = [v["tab"] for v in ordered if cp._is_number(v["tab"])]
    rising = falling = 0
    for first in range(len(numbered)):
        for second in range(first + 1, len(numbered)):
            if numbered[first] < numbered[second]:
                rising += 1
            elif numbered[first] > numbered[second]:
                falling += 1
    return rising, falling


def direction(rising, falling):
    """'up' (low numbers first), 'down' (high numbers first) or None when the numbers do not say."""
    if rising and rising >= 2 * falling:
        return "up"
    if falling and falling >= 2 * rising:
        return "down"
    return None


def main(argv):
    cp.safe_output()
    args = argv[1:]
    dry_run = "--dry-run" in args
    args = [a for a in args if a != "--dry-run"]
    wanted_page = None
    try:
        if "--page" in args:
            at = args.index("--page")
            wanted_page = args[at + 1]
            del args[at:at + 2]
    except IndexError:
        print(__doc__)
        return 2
    if len(args) != 1 or args[0].startswith("-"):
        print(__doc__)
        return 2
    root = os.path.abspath(args[0])
    reports = cp.find_reports(root)
    if not reports:
        print("No *.Report folder found under %s." % args[0])
        return 2
    tolerance = 2 * cp.read_brief(root)["grid"]

    pages, refused, found_page = [], [], False      # pages: (report, tab name, visuals in reading order)
    for report in reports:
        for folder_name, folder, page_path in cp.iter_pages(report):
            page = cp.load_object(page_path) or {}
            keys = {k for k in (folder_name, page.get("name"), page.get("displayName")) if isinstance(k, str)}
            if wanted_page is not None and wanted_page not in keys:
                continue
            found_page = True
            tab = page.get("displayName") if isinstance(page.get("displayName"), str) else folder_name
            if page.get("type") == "Tooltip":
                print("left alone  %s: a tooltip page" % tab)
                continue
            visuals = [v for v in cp.page_layout(folder) if not v["parent"]]
            for visual in visuals:
                try:
                    data, style = svd.read_with_style(visual["path"])
                    if not isinstance(data.get("position"), dict):
                        raise ValueError("no 'position' object")
                except (OSError, ValueError, RecursionError) as exc:
                    refused.append("%s/%s: the file cannot be read safely (%s)" % (tab, cp._shown(visual), str(exc)[:200]))
                    continue
                visual["file"], visual["tab"] = (data, style), data["position"].get("tabOrder")
            if len(visuals) > 1:
                pages.append((report, tab, reading_order(visuals, tolerance)))
    if wanted_page is not None and not found_page:
        print("Page not found: %s" % wanted_page)
        return 2
    if refused:
        for line in refused:
            print("refused  %s" % line)
        print("Nothing was written.")
        return 1

    by_report = {}
    for report, tab, ordered in pages:
        rising, falling = agreement(ordered)
        total = by_report.setdefault(report, [0, 0])
        total[0] += rising
        total[1] += falling
    changed, changed_pages = 0, []
    for report, tab, ordered in pages:
        way, said = direction(*agreement(ordered)), "the page's own numbers"
        if way is None:
            way, said = direction(*by_report[report]), "the report's numbers"
        if way is None:
            way, said = "down", "no clear pattern in the numbers, so the default"
        numbers = [v["tab"] for v in ordered]
        if all(cp._is_number(n) for n in numbers) and len(set(numbers)) == len(numbers):
            numbers = sorted(numbers)
        else:
            numbers = list(range(len(ordered)))
        if way == "down":
            numbers.reverse()
        page_changes = [(v, n) for v, n in zip(ordered, numbers) if v["tab"] != n]
        print("page %s: reading order, %s numbers first (%s)" % (tab, "low" if way == "up" else "high", said))
        for visual, number in page_changes:
            print("  %s  %s: tabOrder %s -> %s" % ("would change" if dry_run else "changed", cp._shown(visual),
                                                  "none" if visual["tab"] is None else visual["tab"], number))
            if not dry_run:
                data, style = visual["file"]
                data["position"]["tabOrder"] = number
                svd.write_with_style(visual["path"], data, style)
        if page_changes:
            changed += len(page_changes)
            changed_pages.append(tab)
    print("%d visual(s) %s." % (changed, "would change" if dry_run else "changed"))
    if changed_pages:
        print("Reload the project in Power BI Desktop and look at View > Selection > Tab order on: %s."
              % ", ".join(changed_pages))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
