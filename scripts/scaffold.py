#!/usr/bin/env python3
"""Create a new Power BI project, or the measures table of a model, from the shipped examples.

Usage (run from the repository root; <folder> is '.' when left out):
    python scripts/scaffold.py project <Name> [<folder>] [--register-theme]
    python scripts/scaffold.py measures-table [<folder>] [--form import|calculated]

'project' copies tests/fixtures/examples/starter to <folder> under the new name: <Name>.pbip, <Name>.Report
(PBIR, one empty page named Overview) and <Name>.SemanticModel (TMDL, with the table _Measures). It refuses
when the folder already holds a project.

The theme. Microsoft Learn ("Power BI Desktop project report folder") supports changing a file under
RegisteredResources only for a resource that Power BI Desktop itself has registered. So by default the new
report has NO custom theme, and the developer imports theme/theme.json once in Power BI Desktop
(Design ribbon > Import theme). Until then the project check reports T001.
With --register-theme the script registers the theme in the files instead, the way Microsoft's own report
skill does (a customTheme entry and a resource package entry in report.json, and the theme file under
StaticResources/RegisteredResources). That route is outside what Microsoft Learn describes as supported:
use it only when the developer has said yes.

'measures-table' adds the table _Measures to a model that has none, in the form the model standard gives
(rule 1): an imported one-column table for an import model, a calculated table for a model with Direct Lake
or DirectQuery tables. --form overrides the choice.

Not yet opened in Power BI Desktop by the template's builder: what this script writes parses with
Microsoft's TMDL library, passes Microsoft's schemas and passes the project check.
Needs Python 3.8 or later. Uses the standard library only.
Exit code: 0 = done, 1 = refused or a problem, 2 = wrong usage.
"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EXAMPLES = os.path.join(ROOT, "tests", "fixtures", "examples")
STARTER = os.path.join(EXAMPLES, "starter")
STARTER_NAME = "Starter"
TABLE_FORMS = {"import": os.path.join(EXAMPLES, "measures-table", "import.tmdl"),
               "calculated": os.path.join(EXAMPLES, "measures-table", "calculated.tmdl")}
THEME = os.path.join(ROOT, "theme", "theme.json")
PROJECT_NAME = re.compile(r"[A-Za-z0-9][A-Za-z0-9 _-]{0,62}\Z")
THEME_FILE = "theme.json"


def existing_project(folder):
    return sorted(name for name in os.listdir(folder)
                  if name.lower().endswith(".pbip") or name.endswith((".Report", ".SemanticModel")))


def project(name, folder, register_theme):
    if not PROJECT_NAME.match(name) or name != name.strip():
        print("Name '%s' is not usable: use letters, digits, spaces, hyphens and underscores, at most 63 characters." % name)
        return 1
    if not os.path.isdir(folder):
        print("Not a folder: %s" % folder)
        return 1
    found = existing_project(folder)
    if found:
        print("This folder already holds a Power BI project (%s). A repository holds one project; nothing was written."
              % ", ".join(found))
        return 1
    for item in sorted(os.listdir(STARTER)):
        source = os.path.join(STARTER, item)
        target = os.path.join(folder, item.replace(STARTER_NAME, name, 1))
        if os.path.isdir(source):
            shutil.copytree(source, target)
        else:
            shutil.copyfile(source, target)
    report = os.path.join(folder, "%s.Report" % name)
    model = os.path.join(folder, "%s.SemanticModel" % name)
    _replace_json(os.path.join(folder, "%s.pbip" % name),
                  lambda data: data["artifacts"][0]["report"].update({"path": "%s.Report" % name}))
    _replace_json(os.path.join(report, "definition.pbir"),
                  lambda data: data["datasetReference"]["byPath"].update({"path": "../%s.SemanticModel" % name}))
    database = os.path.join(model, "definition", "database.tmdl")
    with open(database, encoding="utf-8") as handle:
        text = handle.read()
    quoted = name if re.match(r"[A-Za-z_][A-Za-z0-9_]*\Z", name) else "'%s'" % name
    with open(database, "w", encoding="utf-8", newline="\n") as handle:
        handle.write(text.replace("database %s" % STARTER_NAME, "database %s" % quoted, 1))
    resources = os.path.join(report, "StaticResources")
    if register_theme:
        shutil.copyfile(THEME, os.path.join(resources, "RegisteredResources", THEME_FILE))
        print("Registered theme/theme.json in the report files, the way Microsoft's report skill does. Microsoft Learn "
              "describes this as supported only after Power BI Desktop has registered the theme itself: tell the "
              "developer, and ask them to check the colours when they first open the report.")
    else:
        shutil.rmtree(resources, ignore_errors=True)

        def no_theme(data):
            data["themeCollection"] = {}
            data.pop("resourcePackages", None)
        _replace_json(os.path.join(report, "definition", "report.json"), no_theme)
        print("The report has no custom theme yet. The developer imports theme/theme.json once in Power BI Desktop "
              "(Design ribbon > Import theme) and saves; until then the project check reports T001.")
    print("Created %s.pbip, %s.Report and %s.SemanticModel in %s." % (name, name, name, folder))
    print("Next: python scripts/check_project.py %s" % folder)
    return 0


def _replace_json(path, change):
    with open(path, encoding="utf-8") as handle:
        data = json.load(handle)
    change(data)
    with open(path, "w", encoding="utf-8", newline="\n") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def choose_form(objects):
    """'calculated' when any table of the model is read in Direct Lake or DirectQuery mode, else 'import'."""
    modes = {o["props"].get("mode", "").lower() for o in objects if o["kind"] == "partition"}
    return "calculated" if modes & {"directlake", "directquery"} else "import"


def measures_table(folder, form):
    models = cp.find_models(folder)
    if len(models) != 1:
        print("Expected one semantic model under %s, found %d. A report on a published model has no model here: "
              "its measures live in the published model." % (folder, len(models)))
        return 1
    definition = os.path.join(models[0], "definition")
    objects = []
    for sub, dirs, files in os.walk(definition):
        for name in sorted(files):
            if name.lower().endswith(".tmdl"):
                objects.extend(cp.check_tmdl_file(os.path.join(sub, name), cp.Findings()) or [])
    if any(o["kind"] == "table" and o["top"] and o["name"] == cp.MEASURE_TABLE and not o["translation"] for o in objects):
        print("The model already has the table %s; nothing was written." % cp.MEASURE_TABLE)
        return 0
    form = form or choose_form(objects)
    target = os.path.join(definition, "tables", "%s.tmdl" % cp.MEASURE_TABLE)
    os.makedirs(os.path.dirname(target), exist_ok=True)
    shutil.copyfile(TABLE_FORMS[form], target)
    model_file = os.path.join(definition, "model.tmdl")
    listed = False
    if os.path.isfile(model_file):
        with open(model_file, encoding="utf-8-sig", newline="") as handle:
            text = handle.read()
        lines = text.splitlines(True)
        refs = [i for i, line in enumerate(lines) if line.startswith("ref table ")]
        if refs:
            ending = "\r\n" if lines[refs[-1]].endswith("\r\n") else "\n"
            if not lines[refs[-1]].endswith(("\n", "\r")):
                lines[refs[-1]] += ending
            lines.insert(refs[-1] + 1, "ref table %s%s" % (cp.MEASURE_TABLE, ending))
            with open(model_file, "w", encoding="utf-8", newline="") as handle:
                handle.write("".join(lines))
            listed = True
    print("Wrote %s as %s table%s." % (os.path.relpath(target, folder).replace(os.sep, "/"),
                                       "an imported" if form == "import" else "a calculated",
                                       ", and listed it in model.tmdl" if listed else ""))
    if form == "calculated":
        print("It carries a CalculatedReason line that gives the standard's own reason. Record the form in section 4 "
              "of docs/report-brief.md.")
    print("Next: python scripts/check_project.py %s" % folder)
    return 0


def main(argv):
    cp.safe_output()
    args = argv[1:]
    register = "--register-theme" in args
    args = [a for a in args if a != "--register-theme"]
    form = None
    if "--form" in args:
        position = args.index("--form")
        if position + 1 >= len(args) or args[position + 1] not in TABLE_FORMS:
            print(__doc__)
            return 2
        form = args[position + 1]
        del args[position:position + 2]
    if any(a.startswith("-") for a in args):
        print(__doc__)
        return 2
    if len(args) in (2, 3) and args[0] == "project":
        return project(args[1], os.path.abspath(args[2] if len(args) == 3 else "."), register)
    if len(args) in (1, 2) and args[0] == "measures-table" and not register:
        return measures_table(os.path.abspath(args[1] if len(args) == 2 else "."), form)
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
