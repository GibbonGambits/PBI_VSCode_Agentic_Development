#!/usr/bin/env python3
"""List every open question the model still holds: each '/// TODO(owner): <question>' description.

Usage:
    python scripts/list_todos.py <folder>

A description never blocks the work. When the brief and the developer have not said what an object means,
Copilot writes '/// TODO(owner): <question>' above it and carries on. That line is the only record of the
question. This script prints all of them, so that Copilot can ask the developer about them together at the
end of the task, not in the middle of it.

Needs Python 3.8 or later. Uses the standard library only. Reads files; never changes them.
Exit code: 0 = listed (also when there are none), 2 = wrong usage or no model found.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp  # noqa: E402


def questions(root):
    """(file, line, kind, name, question) for every placeholder description under root."""
    out = []
    for model in cp.find_models(root):
        for folder, dirs, files in os.walk(os.path.join(model, "definition")):
            dirs.sort()
            for name in sorted(files):
                if not name.lower().endswith(".tmdl"):
                    continue
                path = os.path.join(folder, name)
                for obj in cp.check_tmdl_file(path, cp.Findings()) or []:
                    if obj["placeholder"] and not obj["translation"]:
                        text = obj["description"]
                        start = text.lower().find(cp.PLACEHOLDER.lower())
                        question = text[start + len(cp.PLACEHOLDER):].lstrip(": ").strip() or "(no question written)"
                        out.append((path, obj["line"], obj["kind"], obj["name"], question))
    return out


def main(argv):
    cp.safe_output()
    if len(argv) != 2 or argv[1].startswith("-"):
        print(__doc__)
        return 2
    root = os.path.abspath(argv[1])
    if not os.path.isdir(root) or not cp.find_models(root):
        print("No semantic model found under %s." % argv[1])
        return 2
    found = questions(root)
    for number, (path, line, kind, name, question) in enumerate(found, 1):
        print("%d. %s '%s' (%s:%d): %s" % (number, kind, name, os.path.relpath(path, root).replace(os.sep, "/"), line, question))
    if found:
        print("%d open question(s). Ask the developer about them together, at the end of the task. Each answer "
              "replaces its TODO(owner) line with the description; record a confirmed definition in section 5 of "
              "docs/report-brief.md." % len(found))
    else:
        print("No open questions: no description holds a %s placeholder." % cp.PLACEHOLDER)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
