"""Tests of the shipped examples (tests/fixtures/examples) and their index.

Run from the repository root:
    python -m unittest discover -s tests -v

"Verified" in the index means: the files parse, report files pass Microsoft's schema, and the folder passes
the project check with no error and no warning. These tests hold the last two; that the model files load in
Microsoft's own library was established when they were built, and is recorded in the index.
"""
import json
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "scripts"))

import check_project as cp            # noqa: E402
import json_schema                    # noqa: E402
import report_rules                   # noqa: E402

EXAMPLES = os.path.join(HERE, "fixtures", "examples")
INDEX = os.path.join(EXAMPLES, "INDEX.md")


def index_text():
    with open(INDEX, encoding="utf-8") as fh:
        return fh.read()


def json_files():
    for folder, dirs, files in os.walk(EXAMPLES):
        dirs.sort()
        for name in sorted(files):
            if name.lower().endswith((".json", ".pbir", ".pbism", ".pbip")):
                yield os.path.join(folder, name)


class ShippedExamples(unittest.TestCase):
    def test_examples_pass_the_project_check_with_no_error_and_no_warning(self):
        findings, models, reports = cp.run(EXAMPLES)
        self.assertGreaterEqual(len(models), 5)
        self.assertGreaterEqual(len(reports), 2)
        problems = [(f[0], os.path.relpath(f[1], EXAMPLES), f[3][:120]) for f in findings.items if f[4] != "note"]
        self.assertEqual(problems, [])

    def test_every_report_file_passes_microsofts_schema(self):
        checked = 0
        for path in json_files():
            with open(path, encoding="utf-8") as fh:
                data = json.load(fh)
            state, problems = json_schema.check_value(data)
            self.assertNotEqual(state, "failed", "%s: %s" % (os.path.relpath(path, EXAMPLES), problems))
            self.assertNotEqual(state, "not shipped", "%s names a schema version that scripts/schemas does not hold"
                                % os.path.relpath(path, EXAMPLES))
            checked += state == "ok"
        self.assertGreater(checked, 80)

    def test_the_project_check_skips_the_examples_when_it_checks_a_project(self):
        findings, models, reports = cp.run(REPO)
        self.assertEqual((models, reports), ([], []))
        self.assertEqual(findings.items, [])

    def test_every_file_the_index_names_exists(self):
        named = re.findall(r"`((?:Examples\.|storage/|preview/|starter/|measures-table/)[^`]*)`", index_text())
        self.assertGreater(len(named), 100)
        for entry in named:
            for part in entry.split(";"):
                path = os.path.join(EXAMPLES, *part.strip().split("/"))
                self.assertTrue(os.path.exists(path), "the index names %s, which does not exist" % part.strip())

    def test_every_visual_and_every_table_of_the_examples_is_in_the_index(self):
        text = index_text()
        missing = []
        for folder, dirs, files in os.walk(EXAMPLES):
            rel = os.path.relpath(folder, EXAMPLES).replace(os.sep, "/")
            if "visual.json" in files and "Examples.Report" in rel and (rel + "/visual.json") not in text:
                missing.append(rel)
            for name in files:
                if name.endswith(".tmdl") and rel.startswith("Examples.SemanticModel") and (rel + "/" + name) not in text:
                    missing.append(rel + "/" + name)
        self.assertEqual(missing, [])

    def test_examples_carry_no_styling_and_keep_header_icons_and_tooltips_off(self):
        on = []
        for folder, dirs, files in os.walk(EXAMPLES):
            if "visual.json" not in files:
                continue
            path = os.path.join(folder, "visual.json")
            data = cp.load_object(path)
            body = data.get("visual") if isinstance(data.get("visual"), dict) else None
            if body is None:
                continue                                     # a group
            found = set()
            report_rules.styling(body.get("objects"), "", found)
            self.assertEqual(found, set(), os.path.relpath(path, EXAMPLES))
            for card in ("visualHeader", "visualTooltip"):
                if cp.show_state(data, card) != "off":
                    on.append((os.path.basename(folder), card))
        self.assertEqual(len(on), 1, on)                      # the one tooltip example
        self.assertEqual(on[0][1], "visualTooltip")
        with open(os.path.join(EXAMPLES, "docs", "report-brief.md"), encoding="utf-8") as fh:
            self.assertIn(on[0][0], fh.read())                # and it carries its exception in the brief

    def test_index_says_what_verified_means_and_that_nothing_was_opened_in_desktop(self):
        text = index_text()
        self.assertIn("Not yet opened in Desktop", text)
        self.assertIn("passes the project check", text.replace("pass the project check", "passes the project check"))

    def test_preview_examples_sit_apart(self):
        calendars = []
        for folder, dirs, files in os.walk(EXAMPLES):
            for name in files:
                if name.endswith(".tmdl"):
                    with open(os.path.join(folder, name), encoding="utf-8") as fh:
                        if re.search(r"^\tcalendar ", fh.read(), re.M):
                            calendars.append(os.path.relpath(folder, EXAMPLES).replace(os.sep, "/"))
        self.assertTrue(calendars)
        self.assertTrue(all(path.startswith("preview/") for path in calendars), calendars)


if __name__ == "__main__":
    unittest.main()
