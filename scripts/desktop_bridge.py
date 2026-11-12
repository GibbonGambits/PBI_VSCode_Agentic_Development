#!/usr/bin/env python3
"""Optional: reload the project in Power BI Desktop and take a picture of every page, through Microsoft's
Desktop Bridge. With it, Copilot reloads and looks at the pages itself instead of asking the developer.

Usage (run from the repository root; <folder> is '.' when left out):
    python scripts/desktop_bridge.py status [<folder>]                is Desktop open on this project? unsaved changes?
    python scripts/desktop_bridge.py open [<folder>]                  open the project's .pbip file in Power BI Desktop
    python scripts/desktop_bridge.py reload [<folder>] [--with-model] reload the report files (and the model definition)
    python scripts/desktop_bridge.py screenshots [<folder>] [--out <dir>]   one PNG for each page
    python scripts/desktop_bridge.py clean <dir>                      delete a folder of pictures this script made

Everything in the template works without this script. It is a thin layer over two command-line tools that
Microsoft publishes on npm and the developer installs: @microsoft/powerbi-desktop-bridge-cli (command
'powerbi-desktop') and @microsoft/powerbi-report-authoring-cli (command 'powerbi-report-author'). This script
never installs anything, never publishes or deploys, and never refreshes data. It calls only:
'powerbi-desktop status', 'open', 'reload' and 'screenshot-all', and, for --with-model,
'powerbi-report-author preview --host desktop --reload-with-model'. 'open' starts Power BI Desktop on this
project's own .pbip file, and only when no Desktop window has the project open already.

Status of the feature (Microsoft Learn, "Power BI Desktop Bridge overview" and "Edit PBIP files outside Power
BI Desktop"): the Desktop Bridge needs Power BI Desktop of June 2026 (2.155.756.0) or later on Windows, with
the Desktop Bridge option on (Options > Security; on by default). Microsoft's pages disagree on whether it is
still a preview. The developer installs the two tools, and that is the yes: Copilot uses the Bridge whenever
this script finds them, without asking and without a row in the brief.

What the script guards:
    - Windows only; elsewhere, and when a tool is missing, it says "not available" and exits with code 3.
      When a tool is missing it also prints the setup lines for the developer.
    - It acts only on the Desktop window that has THIS project open (matched by the report folder's path).
    - 'reload' first runs the project check and stops on errors, so Desktop is never handed broken files.
    - 'reload' stops when Desktop has unsaved changes: a reload would throw them away. The developer saves first.
    - A reload reloads definitions. It does not refresh data, so numbers on a page may be old.
    - Pictures can show data. They go to a temporary folder outside the project; delete them with 'clean'.

'status' and 'screenshots' ran on a developer's computer in November 2026. 'open' and 'reload --with-model'
follow the tools' own code and documentation and have not been run yet. The tests replace the tools with stand-ins.
Needs Python 3.8 or later. Uses the standard library only.
Exit code: 0 = done, 1 = stopped or a problem, 2 = wrong usage, 3 = not available here (carry on without it).
"""
import json
import os
import shutil
import subprocess
import time
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_project as cp  # noqa: E402

BRIDGE = "powerbi-desktop"                 # from @microsoft/powerbi-desktop-bridge-cli
AUTHOR = "powerbi-report-author"           # from @microsoft/powerbi-report-authoring-cli
PICTURE_PREFIX = "pbi-pages-"
WAIT_SECONDS = "90"
CALL_TIMEOUT = 180
PICTURES_TIMEOUT = 300
NOT_AVAILABLE = 3
IS_WINDOWS = os.name == "nt"
WITHOUT = ("Carry on without it: ask the developer to reload the project in Power BI Desktop and to look at the "
           "pages that changed.")
SETUP = ("To set it up once, the developer runs two lines in a terminal: winget install OpenJS.NodeJS.LTS (then "
         "closes and reopens VS Code), and npm.cmd install -g @microsoft/powerbi-desktop-bridge-cli "
         "@microsoft/powerbi-report-authoring-cli. In PowerShell write npm.cmd, not npm: Windows often blocks npm's "
         "PowerShell script. In Power BI Desktop the option File > Options and settings > Options > Security > "
         "'Enable external tool access to Power BI Desktop through secure local APIs' must be on; it is on by default.")


class Unavailable(Exception):
    pass


def find_tool(name):
    path = shutil.which(name)
    if path is None:
        raise Unavailable("Microsoft's tool '%s' is not installed on this computer." % name)
    return path


def run_tool(name, args, timeout=CALL_TIMEOUT):
    """(exit code, parsed JSON or None, raw text) of one call of a Microsoft tool."""
    try:
        done = subprocess.run([find_tool(name)] + list(args), stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, timeout=timeout)
    except subprocess.TimeoutExpired:
        return 1, None, "the tool did not answer within %d seconds" % timeout
    except OSError as exc:
        raise Unavailable("'%s' could not be started: %s" % (name, exc))
    text = done.stdout.decode("utf-8", "replace").strip()
    try:
        data = json.loads(text) if text else None
    except ValueError:
        data = None
    return done.returncode, data, text or done.stderr.decode("utf-8", "replace").strip()


def same_folder(first, second):
    def plain(path):
        return os.path.normcase(os.path.abspath(path)).rstrip("\\/")
    return bool(first) and bool(second) and plain(first) == plain(second)


def our_instance(report_dir):
    """The Desktop window that has this report open: its entry from 'powerbi-desktop status', or None."""
    code, data, text = run_tool(BRIDGE, ["status"])
    instances = data.get("instances") if isinstance(data, dict) else None
    if not isinstance(instances, list):
        raise Unavailable("the Desktop Bridge gave no list of Desktop windows (%s)" % text[:160])
    for instance in instances:
        if isinstance(instance, dict) and instance.get("bridgeStatus") == "connected" \
                and same_folder(instance.get("reportDir"), report_dir):
            return instance
    return None


def error_text(data, text):
    error = data.get("error") if isinstance(data, dict) else None
    if isinstance(error, dict):
        return "%s (%s)" % (error.get("message", "error"), error.get("code", "?"))
    return text[:300]


def find_report(folder):
    reports = cp.find_reports(folder)
    if len(reports) != 1:
        print("Expected one report under %s, found %d." % (folder, len(reports)))
        return None
    return reports[0]


def need_instance(report):
    instance = our_instance(report)
    if instance is None:
        print("Power BI Desktop does not have this project open (no Desktop window reports the folder %s). Open it: "
              "python scripts/desktop_bridge.py open ." % os.path.basename(report))
    return instance


def open_project(folder):
    """Open this project's .pbip file in Power BI Desktop, unless a Desktop window has it open already."""
    report = find_report(folder)
    if report is None:
        return 1
    instance = our_instance(report)
    if instance is not None:
        print("Power BI Desktop has this project open already (process %s). Nothing was started." % instance.get("pid"))
        return 0
    projects = sorted(name for name in os.listdir(folder) if name.lower().endswith(".pbip"))
    if len(projects) != 1:
        print("Expected one .pbip file directly under %s, found %d." % (folder, len(projects)))
        return 1
    code, data, text = run_tool(BRIDGE, ["open", os.path.join(folder, projects[0]), "--timeout", WAIT_SECONDS])
    if code != 0 or not isinstance(data, dict) or data.get("status") != "launched":
        print("Power BI Desktop did not open the project: %s. %s" % (error_text(data, text), WITHOUT))
        return 1
    # 'open' waits for any Desktop window; wait until the one that has this project answers.
    deadline = time.time() + int(WAIT_SECONDS)
    instance = our_instance(report)
    while instance is None and time.time() < deadline:
        time.sleep(5)
        instance = our_instance(report)
    if instance is None:
        print("Power BI Desktop started, but no window reported this project within %s seconds. Run "
              "python scripts/desktop_bridge.py status . again in a minute. %s" % (WAIT_SECONDS, WITHOUT))
        return 1
    print("Opened %s in Power BI Desktop (process %s). It shows the data it last saved: refresh in Desktop when "
          "queries changed." % (projects[0], instance.get("pid")))
    return 0


def status(folder):
    report = find_report(folder)
    if report is None:
        return 1
    instance = need_instance(report)
    if instance is None:
        return 1
    pages = instance.get("pages") if isinstance(instance.get("pages"), list) else []
    print("Power BI Desktop has this project open (process %s)." % instance.get("pid"))
    print("Unsaved changes in Desktop: %s" % {True: "yes - the developer must save before any reload",
                                              False: "no"}.get(instance.get("hasUnsavedChanges"), "not reported"))
    print("Pages Desktop reports: %s" % (", ".join(str(p.get("displayName")) for p in pages if isinstance(p, dict)) or "none"))
    return 0


def reload(folder, with_model):
    report = find_report(folder)
    if report is None:
        return 1
    findings, _, _ = cp.run(folder)
    errors = findings.errors()
    if errors:
        print("Not reloaded: the project check reports %d error(s) (%s). Fix them first: "
              "python scripts/check_project.py ." % (len(errors), ", ".join(sorted({f[0] for f in errors}))))
        return 1
    instance = need_instance(report)
    if instance is None:
        return 1
    if instance.get("hasUnsavedChanges") is not False:
        print("Not reloaded: Power BI Desktop %s unsaved changes, and a reload would throw them away. Ask the "
              "developer to save in Desktop (or to say that the changes can go), then run this again."
              % ("has" if instance.get("hasUnsavedChanges") else "did not say whether it has"))
        return 1
    if with_model:
        code, data, text = run_tool(AUTHOR, ["preview", report, "--host", "desktop", "--reload-with-model"])
    else:
        code, data, text = run_tool(BRIDGE, ["reload", "--pid", str(instance.get("pid")), "--wait-seconds", WAIT_SECONDS])
    if code != 0:
        print("Desktop did not reload: %s. %s" % (error_text(data, text), WITHOUT))
        return 1
    print("Reloaded %s in Power BI Desktop. A reload does not refresh data: numbers on a page may be old. Filters "
          "and selections were reset." % ("the report and the model definition" if with_model else "the report files"))
    if not with_model:
        print("Model files (.tmdl) changed too? Run this again with --with-model.")
    return 0


def screenshots(folder, out):
    report = find_report(folder)
    if report is None:
        return 1
    instance = need_instance(report)
    if instance is None:
        return 1
    if out is None:
        out = tempfile.mkdtemp(prefix=PICTURE_PREFIX)
    else:
        out = os.path.abspath(out)
        inside = os.path.commonpath([os.path.abspath(folder), out]) == os.path.abspath(folder)
        if inside or not os.path.basename(out).startswith(PICTURE_PREFIX):
            print("Not taken: pictures can show data, so they go outside the project, in a folder whose name starts "
                  "with '%s'." % PICTURE_PREFIX)
            return 1
        os.makedirs(out, exist_ok=True)
    code, data, text = run_tool(BRIDGE, ["screenshot-all", "--pid", str(instance.get("pid")), "--output-dir", out,
                                         "--scale", "2", "--settle", "400", "--wait-seconds", WAIT_SECONDS],
                                timeout=PICTURES_TIMEOUT)
    taken = data.get("screenshots") if isinstance(data, dict) and isinstance(data.get("screenshots"), list) else []
    failed = data.get("failures") if isinstance(data, dict) and isinstance(data.get("failures"), list) else []
    if not taken:
        print("No picture was taken: %s. %s" % (error_text(data, text), WITHOUT))
        return 1
    for shot in taken:
        if isinstance(shot, dict):
            print("%s: %s" % (shot.get("pageDisplayName"), shot.get("outputPath")))
    for miss in failed:
        if isinstance(miss, dict):
            print("NOT taken: %s (%s)" % (miss.get("pageDisplayName"), error_text(miss, "")))
    print("%d page(s) pictured in %s%s. Look at each picture: text that is cut off, visuals that overlap, an error "
          "icon in a visual, an empty visual. The pictures show the state Desktop is in, with the data it last loaded. "
          "They can show data: when you have looked, run: python scripts/desktop_bridge.py clean \"%s\""
          % (len(taken), out, "; %d page(s) failed" % len(failed) if failed else "", out))
    return 1 if failed else 0


def clean(path):
    path = os.path.abspath(path)
    if not os.path.basename(path).startswith(PICTURE_PREFIX) or not os.path.isdir(path):
        print("Not deleted: this command only deletes a folder of pictures this script made (its name starts with '%s')."
              % PICTURE_PREFIX)
        return 1
    others = [name for name in os.listdir(path) if not name.lower().endswith(".png")]
    if others:
        print("Not deleted: the folder holds files that are not pictures (%s)." % ", ".join(others[:5]))
        return 1
    shutil.rmtree(path)
    print("Deleted %s." % path)
    return 0


def main(argv):
    cp.safe_output()
    args = argv[1:]
    with_model = "--with-model" in args
    args = [a for a in args if a != "--with-model"]
    out = None
    if "--out" in args:
        position = args.index("--out")
        if position + 1 >= len(args):
            print(__doc__)
            return 2
        out = args[position + 1]
        del args[position:position + 2]
    if not args or args[0] not in ("status", "open", "reload", "screenshots", "clean") or len(args) > 2 \
            or any(a.startswith("-") for a in args):
        print(__doc__)
        return 2
    if args[0] == "clean":
        return clean(args[1]) if len(args) == 2 else 2
    if not IS_WINDOWS:
        print("Not available here: the Desktop Bridge works on Windows only. %s" % WITHOUT)
        return NOT_AVAILABLE
    folder = os.path.abspath(args[1] if len(args) == 2 else ".")
    try:
        if args[0] == "status":
            return status(folder)
        if args[0] == "open":
            return open_project(folder)
        if args[0] == "reload":
            return reload(folder, with_model)
        return screenshots(folder, out)
    except Unavailable as exc:
        print("Not available here: %s %s" % (exc, WITHOUT))
        print(SETUP)
        return NOT_AVAILABLE


if __name__ == "__main__":
    sys.exit(main(sys.argv))
