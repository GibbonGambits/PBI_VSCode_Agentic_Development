#!/usr/bin/env python3
"""The routine for keeping the template's sources up to date. For the template's maintainer.

Usage (run from the repository root):
    python scripts/refresh_sources.py check                  compare each Git source in maintenance/sources.md
                                                             with its repository today; list the ones that moved
    python scripts/refresh_sources.py dax-index              rebuild the DAX function index from Microsoft Learn
                                                             (its table of contents and its sitemap)
    python scripts/refresh_sources.py schemas <folder>       copy every version of Microsoft's report schemas from a
                                                             local clone of https://github.com/microsoft/json-schemas

The routine, in order:
    1. python scripts/refresh_sources.py check
    2. For each source that moved: read what changed, update the guidance, the checks and maintenance/coverage.md
       where a rule changed, and write the new commit and today's date in maintenance/sources.md.
    3. python scripts/refresh_sources.py schemas <clone of microsoft/json-schemas>
       python scripts/refresh_sources.py dax-index
    4. python -m unittest discover -s tests   and   python scripts/check_template.py
    5. One pull request. A person approves it.

'check' and 'dax-index' need a network connection ('check' also needs Git). Nothing here publishes, deploys or
connects to a Power BI or Fabric workspace. Needs Python 3.8 or later. Uses the standard library only.
Exit code: 0 = done (for 'check': nothing moved), 1 = something moved or a problem, 2 = wrong usage.
"""
import datetime
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SOURCES = os.path.join(ROOT, "maintenance", "sources.md")
SCHEMAS = os.path.join(ROOT, "scripts", "schemas")
DAX_INDEX = os.path.join(ROOT, ".github", "skills", "pbi-semantic-model", "references", "dax-functions.md")
DAX_TOC = "https://learn.microsoft.com/en-us/dax/toc.json"
DAX_PAGE = "https://learn.microsoft.com/dax/"
DAX_PAGE_EN = "https://learn.microsoft.com/en-us/dax/"
DAX_SITEMAP = "https://learn.microsoft.com/_sitemaps/sitemapindex.xml"
SCHEMA_ADDRESS = "https://developer.microsoft.com/json-schemas/"
NOT_COPIED = ("schedules", "localSettings", "unappliedChanges", "editorSettings")    # not project files Copilot writes
TIMEOUT = 30


# ---------------------------------------------------------------- check

def read_sources(path=SOURCES):
    """Rows of the sources table: dicts with source, address, version, licence."""
    rows = []
    try:
        with open(path, encoding="utf-8-sig") as handle:
            lines = handle.read().splitlines()
    except OSError:
        return rows
    for line in lines:
        cells = [c.strip().strip("`") for c in line.strip().strip("|").split("|")]
        if len(cells) >= 4 and cells[1].startswith("https://") and not set(cells[0]) <= set("-: "):
            rows.append({"source": cells[0], "address": cells[1], "version": cells[2], "licence": cells[3]})
    return rows


def remote_head(address):
    """The commit a Git repository's default branch points to now, or None."""
    try:
        done = subprocess.run(("git", "ls-remote", address, "HEAD"), stdout=subprocess.PIPE,
                              stderr=subprocess.DEVNULL, timeout=TIMEOUT * 2)
    except (OSError, subprocess.TimeoutExpired):
        return None
    text = done.stdout.decode("utf-8", "replace").split()
    return text[0] if done.returncode == 0 and text else None


def check():
    rows = read_sources()
    if not rows:
        print("No sources found in maintenance/sources.md.")
        return 1
    moved = unknown = 0
    for row in rows:
        commit = re.search(r"\b[0-9a-f]{7,40}\b", row["version"])
        if "github.com" not in row["address"] or not commit:
            print("read on a date  %s  %s" % (row["source"], row["version"]))
            continue
        now = remote_head(row["address"])
        if now is None:
            unknown += 1
            print("not reached     %s  %s" % (row["source"], row["address"]))
        elif now.startswith(commit.group(0)):
            print("unchanged       %s  %s" % (row["source"], commit.group(0)))
        else:
            moved += 1
            print("MOVED           %s  recorded %s, now %s" % (row["source"], commit.group(0), now[:12]))
    print("%d source(s) moved, %d could not be reached, %d listed." % (moved, unknown, len(rows)))
    return 1 if moved or unknown else 0


# ---------------------------------------------------------------- DAX function index

def fetch_text(address):
    request = urllib.request.Request(address, headers={"User-Agent": "pbi-template-refresh"})
    with urllib.request.urlopen(request, timeout=TIMEOUT) as response:
        return response.read().decode("utf-8-sig")


def fetch_json(address):
    return json.loads(fetch_text(address))


def _find(items, title):
    for item in items:
        if item.get("toc_title") == title:
            return item
        found = _find(item.get("children", []), title)
        if found is not None:
            return found
    return None


FUNCTION_NAME = re.compile(r"[A-Z][A-Z0-9.]*( \([a-z]+\))?\Z")     # SUM, PERCENTILE.INC, DISTINCT (column)


def _hrefs(items):
    """Every page address in the table of contents, without query or anchor."""
    found = set()
    for item in items:
        if item.get("href"):
            found.add(item["href"].split("?")[0].split("#")[0])
        found |= _hrefs(item.get("children", []))
    return found


def sitemap_pages(index_text, fetch=fetch_text):
    """The page names (such as 'sum-function-dax') of the English DAX pages in Microsoft Learn's sitemap.

    The table of contents leaves some function pages out; the sitemap lists every page."""
    pages = []
    for address in re.findall(r"<loc>\s*([^<\s]*/dax_en-us_\d+\.xml)\s*</loc>", index_text):
        for page in re.findall(r"<loc>\s*https://learn\.microsoft\.com/en-us/dax/([^<\s/?#]+)\s*</loc>", fetch(address)):
            if page not in pages:
                pages.append(page)
    return pages


def page_title(html):
    """The heading of a Microsoft Learn page, such as 'TOPNSKIP'."""
    match = re.search(r"<h1[^>]*>\s*([^<]+?)\s*</h1>", html)
    return match.group(1).strip() if match else ""


def missing_pages(toc, pages):
    """(functions, statements): sitemap pages that the table of contents leaves out, as page names."""
    listed = _hrefs(toc.get("items", []))
    extra = [p for p in pages if p not in listed]
    return ([p for p in extra if p.endswith("-function-dax")], [p for p in extra if p.endswith("-statement-dax")])


def dax_index_text(toc, today, extra_functions=(), extra_statements=()):
    """The index file, built from the table of contents of Microsoft Learn's DAX reference and, for the pages the
    table of contents leaves out, from its sitemap. extra_functions and extra_statements are (title, page) pairs."""
    functions = _find(toc.get("items", []), "DAX functions")
    if functions is None:
        raise ValueError("the table of contents has no 'DAX functions' section")
    body = []
    count = 0
    seen = {}
    other_pages = []                                   # entries in a function group that are not functions
    for group in functions.get("children", []):
        members = [(c.get("toc_title", ""), c.get("href", "")) for c in group.get("children", [])
                   if c.get("href") and not c.get("toc_title", "").lower().endswith("overview")]
        names = [(t, h) for t, h in members if FUNCTION_NAME.match(t)]
        other_pages += [(t, h) for t, h in members if not FUNCTION_NAME.match(t)]
        if not names:
            continue
        body += ["## %s" % group.get("toc_title", ""), ""]
        for title, href in names:
            body.append("- %s: %s%s" % (title, DAX_PAGE, href))
            seen.setdefault(title, set()).add(group.get("toc_title", ""))
            count += 1
        body.append("")
    extra = [(t, h) for t, h in extra_functions if FUNCTION_NAME.match(t) and t not in seen]
    if extra:
        body += ["## Functions not in the table of contents", "",
                 "Microsoft Learn documents these functions, but its table of contents does not list them: they were "
                 "found in its sitemap. Read the page before you use one.", ""]
        for title, href in sorted(extra):
            body.append("- %s: %s%s" % (title, DAX_PAGE, href))
            seen.setdefault(title, set()).add("sitemap")
            count += 1
        body.append("")
    section = _find(toc.get("items", []), "DAX statements")
    statements = [(c.get("toc_title", ""), c["href"]) for c in (section or {}).get("children", []) if c.get("href")]
    statements += [(t, h) for t, h in extra_statements if h not in [s for _, s in statements]]
    if statements:
        body += ["## Statements", ""]
        body += ["- %s: %s%s" % (t, DAX_PAGE, h) for t, h in statements]
        body.append("")
    body += ["## Language", "",
             "- Operators: %sdax-operator-reference" % DAX_PAGE,
             "- Syntax: %sdax-syntax-reference" % DAX_PAGE,
             "- Queries: %sdax-queries" % DAX_PAGE,
             "- New functions: %snew-dax-functions" % DAX_PAGE]
    body += ["- %s: %s%s" % (t, DAX_PAGE, h) for t, h in other_pages]
    body += ["", "Functions listed: %d." % count, "", "Checklist items: 32, 33, 34"]
    twice = sorted(t for t, groups in seen.items() if len(groups) > 1)
    lines = ["# DAX function index", "",
             "Each DAX function and its Microsoft Learn address, and nothing else: no descriptions are kept here. "
             "Built by `python scripts/refresh_sources.py dax-index` from the table of contents of Microsoft "
             "Learn's DAX reference (%s) and, for the function pages it leaves out, from Microsoft Learn's sitemap "
             "(%s), on %s." % (DAX_TOC, DAX_SITEMAP, today), "",
             "- Before you use a function that is new to this model, read its page: skill `pbi-lookup`.",
             "- A function that is not in this list is not a DAX function Microsoft documents. Do not use it.",
             ("- These functions are listed in two groups: %s. " % ", ".join(twice) if twice
              else "- Each function is listed once. ") +
             "Functions marked as not recommended or deprecated on their page are still listed: the page says so.",
             "- Pages under Language that are not functions (an overview, the table constructor) are not counted.", ""]
    return "\n".join(lines + body) + "\n", count


def dax_index():
    try:
        toc = fetch_json(DAX_TOC)
        functions, statements = missing_pages(toc, sitemap_pages(fetch_text(DAX_SITEMAP)))
        extra_functions = [(page_title(fetch_text(DAX_PAGE_EN + p)) or p[:-len("-function-dax")].upper(), p)
                           for p in functions]
        extra_statements = [(page_title(fetch_text(DAX_PAGE_EN + p)) or p, p) for p in statements]
    except (urllib.error.URLError, OSError, ValueError) as exc:
        print("Microsoft Learn could not be reached (%s). The index was left as it is." % exc)
        return 1
    try:
        text, count = dax_index_text(toc, datetime.date.today().isoformat(), extra_functions, extra_statements)
    except ValueError as exc:
        print("The index was left as it is: %s." % exc)
        return 1
    with open(DAX_INDEX, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)
    print("Wrote %s with %d functions." % (os.path.relpath(DAX_INDEX, ROOT).replace(os.sep, "/"), count))
    return 0


# ---------------------------------------------------------------- schemas

def _references(path, relative):
    """Schema files that one schema file refers to, as paths relative to the clone's root."""
    out = set()

    def walk(node):
        if isinstance(node, dict):
            reference = node.get("$ref")
            if isinstance(reference, str) and not reference.startswith("#"):
                target = reference.split("#")[0]
                if target.startswith(SCHEMA_ADDRESS):
                    out.add(target[len(SCHEMA_ADDRESS):])
                elif "://" not in target:
                    out.add(posixpath.normpath(posixpath.join(posixpath.dirname(relative), target)))
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    with open(path, encoding="utf-8-sig") as handle:
        walk(json.load(handle))
    return out


def schemas(clone):
    """Copy every published version of each schema, and every file those refer to, into scripts/schemas.

    Every version, not only the newest: a project saved by an older Power BI Desktop names older versions,
    and its files should be checked too.
    """
    if not os.path.isdir(os.path.join(clone, "fabric")):
        print("Not a clone of microsoft/json-schemas (no 'fabric' folder): %s" % clone)
        return 1
    wanted = set()
    for folder, _, files in os.walk(os.path.join(clone, "fabric")):
        parts = os.path.relpath(folder, clone).split(os.sep)
        if "schema.json" in files and re.match(r"\d+\.\d+\.\d+\Z", parts[-1]) and not set(parts) & set(NOT_COPIED):
            wanted.add("/".join(parts) + "/schema.json")
    todo = list(wanted)
    while todo:
        relative = todo.pop()
        for target in _references(os.path.join(clone, *relative.split("/")), relative):
            if os.path.isfile(os.path.join(clone, *target.split("/"))) and target not in wanted:
                wanted.add(target)
                todo.append(target)
    if os.path.isdir(SCHEMAS):
        shutil.rmtree(SCHEMAS)
    for relative in sorted(wanted):
        target = os.path.join(SCHEMAS, *relative.split("/"))
        os.makedirs(os.path.dirname(target), exist_ok=True)
        shutil.copyfile(os.path.join(clone, *relative.split("/")), target)
    licence = os.path.join(clone, "LICENSE")
    if os.path.isfile(licence):
        shutil.copyfile(licence, os.path.join(SCHEMAS, "LICENSE"))
    print("Copied %d schema file(s) into scripts/schemas. Write the clone's commit in maintenance/sources.md, "
          "then run the tests: the shipped examples name schema versions, and a new version may need them updated."
          % len(wanted))
    return 0


def main(argv):
    if len(argv) == 2 and argv[1] == "check":
        return check()
    if len(argv) == 2 and argv[1] == "dax-index":
        return dax_index()
    if len(argv) == 3 and argv[1] == "schemas":
        return schemas(argv[2])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
