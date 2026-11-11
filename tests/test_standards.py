"""Tests of the model standard, the layout standard and the evaluate-and-improve flow.

Run from the repository root:
    python -m unittest discover -s tests -v

Two made-up projects are used. tests/fixtures/good meets both standards. tests/fixtures/bad breaks many
rules at once. Neither is a report to open in Power BI Desktop. Each test works on a copy in a temporary folder.
"""
import contextlib
import io
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "scripts"))

import check_project as cp            # noqa: E402
import check_template as ct           # noqa: E402
import improve                        # noqa: E402
import set_model_properties as smp    # noqa: E402
import set_positions as sp            # noqa: E402
import set_visual_defaults as svd     # noqa: E402

TABLES = os.path.join("Sample.SemanticModel", "definition", "tables")
SALES = os.path.join(TABLES, "Sales.tmdl")
MEASURES = os.path.join(TABLES, "_Measures.tmdl")
RELATIONSHIPS = os.path.join("Sample.SemanticModel", "definition", "relationships.tmdl")
PAGE = os.path.join("Sample.Report", "definition", "pages", "Overview")
CARD = os.path.join(PAGE, "visuals", "Overview_Card_TotalSales", "visual.json")
BAR = os.path.join(PAGE, "visuals", "4f0c9d2a7b1e8a6c3d5f", "visual.json")
GROUP = os.path.join(PAGE, "visuals", "Overview_Group_Header", "visual.json")
BRIEF = os.path.join("docs", "report-brief.md")
BAD_TABLES = os.path.join("Bad.SemanticModel", "definition", "tables")
BAD_PAGES = os.path.join("Bad.Report", "definition", "pages")

BRIEF_TEXT = """# Brief

- Page size in pixels, width x height (52):%(size)s
- Outer margin in pixels (49):%(margin)s
- Gap between visuals in pixels (49):%(gap)s
- Grid step in pixels (49):%(grid)s
- Measure folder subjects (22):%(subjects)s
- Acronyms and words with their own spelling (7, 28):%(own)s
- Excel check on (yes or no):%(excel)s
- Power BI Copilot check on (yes or no):%(copilot)s

## 9. Exceptions to the model standard

| Code | Object | Reason |
|---|---|---|
%(model)s

## 10. Exceptions to the layout standard

| Code | Page | Visual | Reason |
|---|---|---|---|
%(layout)s
"""


def quiet(function, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = function(*args)
    return code, out.getvalue()


class Case(unittest.TestCase):
    FIXTURE = "good"

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, "project")
        shutil.copytree(os.path.join(HERE, "fixtures", self.FIXTURE), self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def path(self, relative):
        return os.path.join(self.root, relative)

    def read(self, relative):
        with open(self.path(relative), encoding="utf-8") as fh:
            return fh.read()

    def write(self, relative, text):
        os.makedirs(os.path.dirname(self.path(relative)), exist_ok=True)
        with open(self.path(relative), "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    def replace(self, relative, old, new):
        text = self.read(relative)
        self.assertIn(old, text, "test setup: text to replace not found")
        self.write(relative, text.replace(old, new, 1))

    def edit_json(self, relative, change):
        data = json.loads(self.read(relative))
        change(data)
        self.write(relative, json.dumps(data, indent=2))

    def brief(self, **values):
        fields = dict(size="", margin="", gap="", grid="", subjects="", own="", excel="", copilot="", model="", layout="")
        fields.update({key: (" " + value if key not in ("model", "layout") else value) for key, value in values.items()})
        self.write(BRIEF, BRIEF_TEXT % fields)

    def found(self):
        findings, _, _ = cp.run(self.root)
        return findings.items

    def codes(self, level=None):
        """Codes of the errors (level False), the warnings ("warn") or the notes ("note"); all when level is None."""
        return [f[0] for f in self.found() if level is None or f[4] == level]

    def messages(self, code):
        return [f[3] for f in self.found() if f[0] == code]

    def assertFails(self, code):
        self.assertIn(code, self.codes(False))

    def assertWarns(self, code):
        self.assertIn(code, self.codes("warn"))
        self.assertNotIn(code, self.codes(False))

    def assertNot(self, code):
        self.assertNotIn(code, self.codes())

    def add_measure(self, text, relative=MEASURES):
        self.replace(relative, "\tannotation SampleSource", text + "\n\tannotation SampleSource")


# ---------------------------------------------------------------- the two fixtures

class GoodProject(Case):
    def test_good_project_meets_both_standards(self):
        self.assertEqual(self.codes(), ["I001"])            # one placeholder note; no error, no warning

    def test_warnings_do_not_change_the_exit_code(self):
        self.replace(SALES, "\t\tdataType: decimal\n", "\t\tdataType: double\n")
        code, out = quiet(cp.main, ["check_project.py", self.root])
        self.assertEqual(code, 0)
        self.assertIn("M108", out)
        self.assertIn("(warn)", out)
        self.assertIn("0 error(s), 1 warning(s), 1 note(s)", out)
        self.assertNotIn("record one lesson", out)

    def test_a_failed_new_check_starts_the_improvement_loop(self):
        self.replace(MEASURES, "\t\tdisplayFolder: Finance\\Base\n", "")
        code, out = quiet(cp.main, ["check_project.py", self.root])
        self.assertEqual(code, 1)
        self.assertIn("record one lesson for each code (M003)", out)


class BadProject(Case):
    FIXTURE = "bad"
    ERRORS = ("B001", "D001", "G001", "G002", "H001", "H002", "M001", "M002", "M003", "M004", "M005", "M006",
              "M007", "M009", "M105", "M107", "M109", "M402", "N003")
    WARNINGS = ("A001", "A002", "A003", "G003", "G004", "G005", "G006", "G007", "M008", "M010", "M101", "M102",
                "M103", "M104", "M106", "M108", "M110", "M111", "M112", "M114", "M118", "M404", "M411", "M413",
                "M508", "M520", "V002", "V005")
    NOTES = ("G008", "M201", "M301", "M302", "U103")

    def test_every_breach_is_caught(self):
        items = self.found()
        for level, expected in ((False, self.ERRORS), ("warn", self.WARNINGS), ("note", self.NOTES)):
            got = {f[0] for f in items if f[4] == level}
            self.assertEqual(sorted(got), sorted(expected), "level %r" % level)

    def test_findings_name_the_object(self):
        text = "\n".join("%s %s" % (f[0], f[3]) for f in self.found())
        for wanted in ("M001 measure [total_sales] lives in table 'Orders'",
                       "M002 measure table '_Measures': the table is hidden",
                       "M003 measure [Total Sales] has display folder 'Finance/Base'",
                       "M003 measure [ytd Sales] has display folder 'Finance\\Time Intelligence\\Year'",
                       "M004 measure [Margin %], display folder 'Finance\\Extras'",
                       "M005 measure name [Order Count] is used twice",
                       "M006 measure [Quantity] has the same name as column Orders[Quantity]",
                       "M007 measure name [total_sales]",
                       "M009 visible measure [total_sales] has no format string",
                       "M010 DAX of [Total Sales]: write the column with its table: [Amount]",
                       "M010 DAX of [ytd Sales]: write the measure without its table: Orders[Total Sales]",
                       "M101 table 'Product' shows 21 fields",
                       "M102 column Orders[CustomerKey] is the many side of a relationship",
                       "M102 column Orders[Month Number] only sorts column 'Month Name'",
                       "M103 numeric column Orders[Amount] is visible, and measure [total_sales] already totals it",
                       "M104 hidden column Customer[Country] is used by a hierarchy",
                       "M104 hidden column Orders[Quantity] is used by a report visual",
                       "M105 calculated column Orders[Amount With Tax]",
                       "M105 calculated table 'Calendar'",
                       "M106 calculated column Orders[Customer Name] uses RELATED",
                       "M106 the model has 6 calculated columns",
                       "M107 visible numeric column Orders[OrderId]",
                       "M108 column Orders[Amount] has the floating-point type",
                       "M109 relationship Orders[Store Code] to Store[StoreId] joins a string column to a int64 column",
                       "M110 relationship Orders[Product Code] to Product[Product Code] uses string columns",
                       "M111 column Orders[Order Date] may hold a date and a time together (format 'General Date')",
                       "M112 visible date column Orders[Ship Date] has no format string",
                       "M201 hidden column Orders[Legacy Code]", "M201 hidden measure [Old Measure]",
                       "M301 table 'Orders': isAvailableInMdx could be turned off on hidden column(s) Quantity, Legacy Code",
                       "M302 table 'Orders': its description has",
                       "G001 visual 'Overview_Table_Orders'",
                       "G002 data visuals 'Overview_Bar_SalesByMonth' and 'Overview_Table_Orders' overlap",
                       "G005 card visuals in the row at y 20 have different heights",
                       "G007 page is 1920 x 1080",
                       "B001 this file uses field(s) the model does not have: Orders[Missing Measure]"):
            self.assertIn(wanted, text)

    def test_deliberate_layering_is_not_reported(self):
        overlaps = " ".join(self.messages("G002"))
        self.assertNotIn("Overview_Shape_Background", overlaps)      # a shape has no fields: it is not a data visual
        self.assertNotIn("Overview_Line_Toggle", overlaps)           # a bookmark hides it
        self.assertNotIn("Overview_Slicer_Store", overlaps)          # a group member is compared with members only
        self.assertEqual(len(self.messages("G002")), 1)

    def test_overlap_is_reported_once_no_bookmark_hides_it(self):
        os.remove(self.path(os.path.join("Bad.Report", "definition", "bookmarks", "ShowTrend.bookmark.json")))
        self.assertIn("Overview_Line_Toggle", " ".join(self.messages("G002")))

    def test_hidden_visual_is_not_an_overlap(self):
        os.remove(self.path(os.path.join("Bad.Report", "definition", "bookmarks", "ShowTrend.bookmark.json")))
        self.edit_json(os.path.join(BAD_PAGES, "Overview", "visuals", "Overview_Line_Toggle", "visual.json"),
                       lambda d: d.update({"isHidden": True}))
        self.assertNotIn("Overview_Line_Toggle", " ".join(self.messages("G002")))

    def test_tooltip_page_is_not_held_to_the_grid(self):
        for code in ("G003", "G004", "G006", "G007"):
            self.assertNotIn("Tip", " ".join(f[1] for f in self.found() if f[0] == code))

    def test_tooltip_page_still_may_not_overflow(self):
        self.edit_json(os.path.join(BAD_PAGES, "Tip", "visuals", "Tip_Card_Sales", "visual.json"),
                       lambda d: d["position"].update({"width": 400}))
        self.assertIn("Tip_Card_Sales", " ".join(self.messages("G001")))

    def test_listed_exception_passes_and_only_that_one(self):
        self.assertNotIn("Orders[OrderId]", " ".join(self.messages("M112")))
        self.replace(BRIEF, "| M112 | Orders[OrderId] | An identifier, shown as typed |\n", "")
        self.assertIn("Orders[OrderId]", " ".join(self.messages("M112")))

    def test_exception_without_a_reason_does_not_count(self):
        self.replace(BRIEF, "| M112 | Orders[OrderId] | An identifier, shown as typed |", "| M112 | Orders[OrderId] |  |")
        self.assertIn("Orders[OrderId]", " ".join(self.messages("M112")))

    def test_exception_for_another_code_does_not_count(self):
        self.replace(BRIEF, "| M112 | Orders[OrderId] |", "| M107 | Orders[OrderId] |")
        self.assertIn("Orders[OrderId]", " ".join(self.messages("M112")))
        self.assertNotIn("Orders[OrderId]", " ".join(self.messages("M107")))

    def test_background_shape_counts_for_margins_without_its_exception(self):
        before = " ".join(m for m in self.messages("G004") if "left 0" in m)
        self.assertEqual(before, "")
        self.replace(BRIEF, "| G004 | Overview | Overview_Shape_Background | Full-page background shape |\n", "")
        self.assertTrue(any("left 0" in m for m in self.messages("G004")))

    def test_optional_checks_are_off_unless_the_brief_turns_them_on(self):
        self.replace(BRIEF, "- Excel check on (yes or no): yes", "- Excel check on (yes or no):")
        self.replace(BRIEF, "- Power BI Copilot check on (yes or no): yes", "- Power BI Copilot check on (yes or no): no")
        self.assertNot("M301")
        self.assertNot("M302")

    def test_mechanical_fixes_repair_what_they_cover(self):
        page = "Overview"
        self.assertEqual(quiet(svd.main, ["set_visual_defaults.py", self.root, "--label",
                                          page + "/9a0c1d2e3f4a5b6c7d8e=Overview_Line_Trend"])[0], 0)
        self.assertEqual(quiet(smp.main, ["set_model_properties.py", self.root, "--from-findings", "M102,M103"])[0], 0)
        sets = ["[total_sales].displayFolder=Finance\\Base", "[total_sales].formatString=#,0",
                "[Total Sales].displayFolder=Finance\\Base", "[ytd Sales].displayFolder=Finance\\Time Intelligence",
                "[Margin %].displayFolder=Finance\\Ratios", "Orders[Ship Date].formatString=Short Date",
                "Product[Product Code].displayFolder=Keys"]
        sets += ["Product[Attribute %02d].displayFolder=Attributes" % n for n in range(1, 21)]
        args = ["set_model_properties.py", self.root]
        for one in sets:
            args += ["--set", one]
        code, out = quiet(smp.main, args)
        self.assertEqual(code, 0, out)
        left = self.codes()
        for code in ("H001", "H002", "N003", "M003", "M004", "M009", "M101", "M102", "M112"):
            self.assertNotIn(code, left)
        self.assertEqual(len(self.messages("M103")), 1)   # Orders[Cost] is hidden now; Orders[Amount] is not:
        self.assertIn("Orders[Amount]", self.messages("M103")[0])            # a visual uses it, so no script hides it
        self.assertIn("a report visual uses it, so it stays visible", self.messages("M103")[0])
        self.assertNotIn("column Amount\n\t\tisHidden", self.read(os.path.join(BAD_TABLES, "Orders.tmdl")))
        for code in ("M001", "M002", "M005", "M006", "M007", "M105", "M107", "M109", "B001", "D001"):
            self.assertIn(code, left)                    # these need a person: no script repairs them

    def test_layout_fixes_repair_the_page(self):
        moves = {"Overview_Card_Sales": "24,24,344,104", "Overview_Card_Orders": "384,24,336,104",
                 "Overview_Bar_SalesByMonth": "24,144,608,552", "Overview_Table_Orders": "648,144,608,552"}
        args = ["set_positions.py", self.root]
        for visual, numbers in moves.items():
            args += ["--move", "Overview/%s=%s" % (visual, numbers)]
        code, out = quiet(sp.main, args)
        self.assertEqual(code, 0, out)
        self.assertIn("look at these pages: Overview.", out)
        items = self.found()
        for code in ("G001", "G002", "G003", "G005", "G006"):
            self.assertNotIn(code, [f[0] for f in items])
        self.assertEqual([f[1] for f in items if f[0] == "G004" and "Overview" in f[1]], [])
        self.assertIn("G007", [f[0] for f in items])     # the page size is the developer's decision

    def test_fix_plan_sorts_every_finding_into_a_kind(self):
        rows = [(1, "Fail", "Evidence missing: no naming standard"), (39, "Fail", "Evidence missing: roles not tested")]
        rows += [(n, "Pass", "see the brief") for n in range(2, 80) if n != 39]
        self.write(os.path.join("docs", "checklist-review.md"),
                   "| Item | Status | Evidence |\n|---|---|---|\n" + "".join("| %d | %s | %s |\n" % r for r in sorted(rows)))
        code, out = quiet(improve.plan, self.root)
        self.assertEqual(code, 0, out)
        plan, problems = improve.read_plan(self.path(os.path.join("docs", "fix-plan.md")))
        kinds = {}
        for row in plan:
            kinds.setdefault(row["Item or code"], set()).add(row["Kind"])
        self.assertEqual(kinds["H001"], {"Mechanical"})
        self.assertEqual(kinds["M003"], {"Mechanical"})
        self.assertEqual(kinds["M102"], {"Mechanical"})
        self.assertEqual(kinds["G002"], {"Layout"})
        self.assertEqual(kinds["G003"], {"Layout"})
        for code in ("M001", "M007", "M105", "M107", "M108", "M109", "B001"):
            self.assertEqual(kinds[code], {"Needs a person"}, code)     # M107 and M108 are never Mechanical
        self.assertEqual(kinds["Item 39"], {"Needs a person"})
        self.assertEqual(kinds["Item 1"], {"?"})                          # for Copilot to sort; check-plan refuses a '?'
        self.assertTrue(any("Item 1" in p or "Kind" in p for p in problems))
        text = self.read(os.path.join("docs", "fix-plan.md"))
        self.assertIn("## For information", text)
        self.assertIn("M201", text)
        self.assertEqual(quiet(improve.check_plan, self.root)[0], 1)
        self.assertEqual(quiet(improve.plan, self.root)[0], 1)            # an existing plan is never overwritten


# ---------------------------------------------------------------- model standard, one rule at a time

class MeasureHome(Case):
    def test_measure_outside_the_measure_table_fails(self):
        self.add_measure("\t/// Units.\n\tmeasure 'Total Units' = COUNTROWS ( Sales )\n\t\tformatString: #,0\n"
                         "\t\tdisplayFolder: Finance\\Base\n", SALES)
        self.assertEqual(self.codes(False), ["M001"])

    def test_second_measure_table_passes_when_the_brief_lists_it(self):
        self.add_measure("\t/// Units.\n\tmeasure 'Total Units' = COUNTROWS ( Sales )\n\t\tformatString: #,0\n"
                         "\t\tdisplayFolder: Finance\\Base\n", SALES)
        self.brief(model="| M001 | Sales | Finance keeps its measures apart |")
        codes = self.codes(False)
        self.assertNotIn("M001", codes)
        self.assertIn("M002", codes)                 # a listed measure table is held to the same shape

    def test_hidden_measure_table_fails(self):
        self.replace(MEASURES, "table _Measures\n", "table _Measures\n\tisHidden\n")
        self.assertFails("M002")

    def test_visible_placeholder_column_fails(self):
        self.replace(MEASURES, "\t\tdataType: string\n\t\tisHidden\n", "\t\tdataType: string\n")
        self.assertFails("M002")

    def test_second_column_in_the_measure_table_fails(self):
        self.add_measure("\tcolumn Other\n\t\tdataType: string\n\t\tisHidden\n\t\tsummarizeBy: none\n\t\tsourceColumn: Other\n")
        self.assertFails("M002")

    def test_calculated_measure_table_needs_its_reason(self):
        text = self.read(MEASURES)
        start = text.index("\tpartition _Measures = m")
        end = text.index("\tannotation SampleSource")
        self.write(MEASURES, text[:start] + "\tpartition _Measures = calculated\n\t\tmode: import\n"
                   "\t\tsource = ROW(\"Placeholder\", BLANK())\n\n" + text[end:])
        self.assertEqual(self.codes(False), ["M105"])
        self.replace(MEASURES, "\tannotation SampleSource", "\tannotation CalculatedReason = Direct Lake model: an "
                     "entered table would make the model composite.\n\n\tannotation SampleSource")
        self.assertEqual(self.codes(False), [])


class MeasureFolders(Case):
    def folder(self, value):
        self.replace(MEASURES, "\t\tdisplayFolder: Finance\\Base\n", value)
        return self.codes(False)

    def test_no_folder_fails(self):
        self.assertEqual(self.folder(""), ["M003"])

    def test_one_level_fails(self):
        self.assertEqual(self.folder("\t\tdisplayFolder: Finance\n"), ["M003"])

    def test_three_levels_fail(self):
        self.assertEqual(self.folder("\t\tdisplayFolder: Finance\\Base\\Year\n"), ["M003"])

    def test_forward_slash_does_not_make_two_levels(self):
        self.assertEqual(self.folder("\t\tdisplayFolder: Finance/Base\n"), ["M003"])
        self.assertIn("backslash", self.messages("M003")[0])

    def test_several_folders_fail(self):
        self.assertEqual(self.folder("\t\tdisplayFolder: Finance\\Base;Customer\\Base\n"), ["M003"])

    def test_quoted_folder_is_read_as_its_text(self):
        self.assertEqual(self.folder('\t\tdisplayFolder: "Finance\\Base"\n'), [])

    def test_unknown_type_fails(self):
        self.assertEqual(self.folder("\t\tdisplayFolder: Finance\\Totals\n"), ["M004"])

    def test_unknown_subject_fails(self):
        self.assertEqual(self.folder("\t\tdisplayFolder: Sales\\Base\n"), ["M004"])

    def test_subjects_come_from_the_brief(self):
        self.brief(subjects="Sales, Customer")
        self.assertEqual(self.folder("\t\tdisplayFolder: Sales\\Base\n"), [])

    def test_default_subjects_are_the_eight_business_areas(self):
        names = set()
        with open(os.path.join(REPO, ".github", "skills", "business-definitions", "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read().lower()
        for subject in cp.FOLDER_SUBJECTS:
            names.add(subject)
            self.assertIn(subject.lower().replace(" and ", "-and-").replace(" ", "-") + ".md", text)
        self.assertEqual(len(names), 8)


class MeasureNames(Case):
    def named(self, name, folder="Finance\\Base"):
        self.add_measure("\t/// Made-up measure.\n\tmeasure %s = COUNTROWS ( Sales )\n\t\tformatString: #,0\n"
                         "\t\tdisplayFolder: %s\n" % ("'%s'" % name.replace("'", "''"), folder))
        items = self.found()
        return [f[0] for f in items if f[4] is False], " ".join(f[3] for f in items if f[0] == "M008")

    def test_good_names_pass(self):
        for name, folder in (("Total Sales YTD", "Finance\\Time Intelligence"), ("Total Sales vs Budget", "Finance\\Comparisons"),
                             ("Total Sales vs PY (%)", "Finance\\Comparisons"), ("Gross Margin (%)", "Finance\\Ratios"),
                             ("# Customers", "Customer\\Counts"), ("COGS YTD", "Finance\\Time Intelligence"),
                             ("Days of Supply", "Finance\\Base")):
            with self.subTest(name=name):
                self.setUp()
                self.assertEqual(self.named(name, folder), ([], ""))
                self.tearDown()

    def test_code_style_names_fail(self):
        for name in ("net_sales", "NetSales", "TOTAL COST", "TOTAL_COST", " Net Sales", "Net Sales "):
            with self.subTest(name=name):
                self.setUp()
                self.assertEqual(self.named(name)[0], ["M007"])
                self.tearDown()

    def test_word_with_its_own_spelling_passes_when_the_brief_lists_it(self):
        self.assertEqual(self.named("Energy Sold (kWh)")[0], ["M007"])
        self.brief(own="kWh, MWh")
        self.assertEqual(self.codes(False), [])

    def test_name_details_are_warnings(self):
        for name, part in (("Total Sales Ytd", "write the period as YTD"), ("Total Sales LY", "write the prior year as PY"),
                           ("Total Sales vs. Budget", "write comparisons with 'vs'"), ("Margin %", "'(%)' at the end"),
                           ("Order Count", "start a count measure with '# '"), ("YTD Total Sales", "put the period after the base name"),
                           ("Net sales", "should start with a capital"), ("Margin (%) Net", "at the end")):
            with self.subTest(name=name):
                self.setUp()
                errors, text = self.named(name)
                self.assertEqual(errors, [])
                self.assertIn(part, text)
                self.tearDown()

    def test_folder_type_is_compared_with_the_name(self):
        errors, text = self.named("Total Sales YTD", "Finance\\Base")
        self.assertEqual(errors, [])
        self.assertIn("points to the folder type 'Time Intelligence'", text)

    def test_duplicate_name_fails(self):
        self.assertIn("M005", self.named("Total Sales")[0])

    def test_name_of_a_column_fails_whatever_the_table(self):
        self.assertIn("M006", self.named("Channel")[0])
        self.assertIn("Sales[Channel]", self.messages("M006")[0])

    def test_measure_without_format_string_fails(self):
        self.replace(MEASURES, "\t\tformatString: 0.0%\n", "")
        self.assertEqual(self.codes(False), ["M009"])

    def test_hidden_measure_needs_no_format_string(self):
        self.replace(MEASURES, "\t\tformatString: 0.0%\n", "\t\tisHidden\n")
        self.assertNotIn("M009", self.codes())

    def test_text_measure_needs_no_format_string(self):
        self.assertIn("measure 'Help Link' = \"http://example.com/help\"\n\t\tdisplayFolder", self.read(MEASURES))
        self.assertNot("M009")

    def test_dynamic_format_counts_as_a_format(self):
        self.replace(MEASURES, "\t\tformatString: 0.0%\n", "\t\tformatStringDefinition = \"0.0%\"\n")
        self.assertNot("M009")

    def test_exception_in_the_brief_passes_one_measure(self):
        self.replace(MEASURES, "\t\tformatString: 0.0%\n", "")
        self.brief(model="| M009 | [Return Rate] | Shown as text in one card |")
        self.assertNot("M009")


class DaxReferences(Case):
    def test_unqualified_column_warns(self):
        self.replace(MEASURES, "SUM ( Sales[Amount] )", "SUM ( [Amount] )")
        self.assertWarns("M010")
        self.assertIn("[Amount]", self.messages("M010")[0])

    def test_qualified_measure_warns(self):
        self.add_measure("\t/// Twice the sales.\n\tmeasure 'Double Sales' = _Measures[Total Sales] * 2\n"
                         "\t\tformatString: #,0\n\t\tdisplayFolder: Finance\\Base\n")
        self.assertWarns("M010")
        self.assertIn("_Measures[Total Sales]", self.messages("M010")[0])

    def test_names_inside_text_and_comments_are_not_references(self):
        self.add_measure("\t/// Label.\n\tmeasure 'Sales Label' = \"[Amount] of \" & [Total Sales] // uses [Amount]\n"
                         "\t\tformatString: #,0\n\t\tdisplayFolder: Finance\\Base\n")
        self.assertNot("M010")

    def test_good_references_pass(self):
        self.assertNot("M010")


class ColumnsAndTables(Case):
    RELATION = "relationship r1\n\tfromColumn: Sales.%s\n\ttoColumn: Customer.%s\n"
    CUSTOMER = ("/// One row per customer.\ntable Customer\n\n\tcolumn CustomerKey\n\t\tdataType: %s\n\t\tisHidden\n"
                "\t\tformatString: 0\n\t\tsummarizeBy: none\n\t\tsourceColumn: CustomerKey\n\n"
                "\t/// Name of the customer.\n\tcolumn Name\n\t\tdataType: string\n\t\tsummarizeBy: none\n\t\tsourceColumn: Name\n")

    def relate(self, sales_column="OrderId", customer_type="int64"):
        self.write(os.path.join(TABLES, "Customer.tmdl"), self.CUSTOMER % customer_type)
        self.write(RELATIONSHIPS, self.RELATION % (sales_column, "CustomerKey"))

    def test_visible_foreign_key_warns(self):
        self.relate()
        self.replace(SALES, "\t\tdataType: int64\n\t\tisHidden\n", "\t\tdataType: int64\n\t\tformatString: 0\n")
        self.replace(SALES, "\tcolumn OrderId\n", "\t/// Order number.\n\tcolumn OrderId\n")
        self.assertWarns("M102")
        self.brief(model="| M102 | Sales[OrderId] | Authors need it to reconcile with the order system |")
        self.assertNot("M102")

    def test_one_to_one_relationship_has_no_foreign_key(self):
        self.relate()
        self.replace(SALES, "\t\tdataType: int64\n\t\tisHidden\n", "\t\tdataType: int64\n\t\tformatString: 0\n")
        self.replace(SALES, "\tcolumn OrderId\n", "\t/// Order number.\n\tcolumn OrderId\n")
        self.write(RELATIONSHIPS, self.read(RELATIONSHIPS) + "\tfromCardinality: one\n")
        self.assertNot("M102")

    def test_relationship_columns_of_different_types_fail(self):
        self.relate(customer_type="string")
        self.assertEqual(self.codes(False), ["M109"])

    def test_relationship_on_text_columns_warns(self):
        self.relate(sales_column="Channel", customer_type="string")
        self.assertWarns("M110")

    def test_relationship_on_whole_numbers_passes(self):
        self.relate()
        self.assertNot("M109")
        self.assertNot("M110")

    def test_visible_column_that_a_measure_totals_warns(self):
        self.replace(SALES, "\t\tdataType: decimal\n\t\tisHidden\n", "\t\tdataType: decimal\n")
        self.replace(SALES, "\t\tsummarizeBy: sum\n", "\t\tsummarizeBy: none\n")
        self.assertEqual(self.codes("warn"), ["M103"])
        self.assertEqual(self.codes(False), [])

    def test_visible_numeric_column_that_still_totals_fails(self):
        self.replace(SALES, "\t\tdataType: decimal\n\t\tisHidden\n", "\t\tdataType: decimal\n")
        self.assertEqual(self.codes(False), ["M107"])
        self.brief(model="| M107 | Sales[Amount] | Analysts total it in ad hoc tables |")
        self.assertEqual(self.codes(False), [])

    def test_hidden_numeric_column_may_total(self):
        self.assertIn("\t\tisHidden\n\t\tformatString: #,0.00\n\t\tsummarizeBy: sum\n", self.read(SALES))
        self.assertNot("M107")

    def test_floating_point_type_warns_and_is_never_a_script_fix(self):
        self.replace(SALES, "\t\tdataType: decimal\n", "\t\tdataType: double\n")
        self.assertWarns("M108")
        findings, _, _ = cp.run(self.root)
        self.assertEqual(findings.fixes, [])
        code, out = quiet(smp.main, ["set_model_properties.py", self.root, "--set", "Sales[Amount].dataType=decimal"])
        self.assertEqual(code, 1)
        self.assertIn("property not allowed", out)
        self.assertIn("dataType: double", self.read(SALES))

    def test_date_with_time_format_warns(self):
        column = ("\t/// When the order was placed.\n\tcolumn 'Ordered At'\n\t\tdataType: dateTime\n%s"
                  "\t\tsummarizeBy: none\n\t\tsourceColumn: OrderedAt\n")
        self.add_measure(column % "\t\tformatString: General Date\n", SALES)
        self.assertEqual(self.codes("warn"), ["M111", "M403"])     # M403: a date column, and no date table
        self.replace(SALES, "\t\tformatString: General Date\n", "\t\tformatString: Short Date\n")
        self.assertEqual(self.codes("warn"), ["M403"])
        self.replace(SALES, "\t\tformatString: Short Date\n", "\t\tformatString: dd/MM/yyyy hh:mm\n")
        self.assertEqual(self.codes("warn"), ["M111", "M403"])
        self.replace(SALES, "\t\tformatString: dd/MM/yyyy hh:mm\n", "")
        self.assertEqual(sorted(self.codes("warn")), ["M111", "M112", "M403"])

    def test_visible_number_without_format_warns(self):
        self.add_measure("\t/// Number of items on the line.\n\tcolumn Items\n\t\tdataType: int64\n"
                         "\t\tsummarizeBy: none\n\t\tsourceColumn: Items\n", SALES)
        self.assertEqual(self.codes("warn"), ["M112"])

    def test_calculated_column_needs_its_reason(self):
        self.add_measure("\t/// Amount with a flat tax.\n\tcolumn 'Amount With Tax' = Sales[Amount] * 1.1\n"
                         "\t\tdataType: decimal\n\t\tformatString: #,0.00\n\t\tsummarizeBy: none\n", SALES)
        self.assertEqual(self.codes(False), ["M105"])
        code, out = quiet(smp.main, ["set_model_properties.py", self.root, "--set",
                                     "Sales[Amount With Tax].CalculatedReason=The tax rate lives only in this model."])
        self.assertEqual(code, 0, out)
        self.assertIn("\t\tsummarizeBy: none\n\n\t\tannotation CalculatedReason = The tax rate lives only in this model.\n",
                      self.read(SALES))
        self.assertEqual(self.codes(False), [])

    def test_empty_reason_does_not_count(self):
        self.add_measure("\t/// Amount with a flat tax.\n\tcolumn 'Amount With Tax' = Sales[Amount] * 1.1\n"
                         "\t\tdataType: decimal\n\t\tformatString: #,0.00\n\t\tsummarizeBy: none\n\n"
                         "\t\tannotation CalculatedReason = -\n", SALES)
        self.assertEqual(self.codes(False), ["M105"])

    def test_auto_date_tables_are_not_asked_for_a_reason(self):
        self.write(os.path.join(TABLES, "LocalDateTable_1.tmdl"),
                   "table LocalDateTable_1\n\tisHidden\n\n\tcolumn Date\n\t\tdataType: dateTime\n\t\tisHidden\n"
                   "\t\tformatString: Short Date\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Date]\n\n"
                   "\tpartition LocalDateTable_1 = calculated\n\t\tmode: import\n\t\tsource = CALENDAR(DATE(2026,1,1), DATE(2026,12,31))\n")
        self.assertNot("M105")

    def test_many_visible_fields_need_column_folders(self):
        columns = "".join("\t/// Made-up attribute %d.\n\tcolumn 'Attribute %d'\n\t\tdataType: string\n"
                          "\t\tsummarizeBy: none\n\t\tsourceColumn: A%d\n\n" % (n, n, n) for n in range(1, 19))
        self.add_measure(columns, SALES)                      # 18 more: 20 visible fields with Channel and Returned
        self.assertWarns("M101")
        text = self.read(SALES).replace("\t\tdataType: string\n", "\t\tdataType: string\n\t\tdisplayFolder: Attributes\n")
        self.write(SALES, text.replace("\t\tdataType: boolean\n", "\t\tdataType: boolean\n\t\tdisplayFolder: Facts\n"))
        self.assertNot("M101")

    def test_nineteen_visible_fields_need_no_folders(self):
        columns = "".join("\t/// Made-up attribute %d.\n\tcolumn 'Attribute %d'\n\t\tdataType: string\n"
                          "\t\tsummarizeBy: none\n\t\tsourceColumn: A%d\n\n" % (n, n, n) for n in range(1, 18))
        self.add_measure(columns, SALES)
        self.assertNot("M101")

    def test_hidden_column_nothing_uses_is_a_note(self):
        self.replace(MEASURES, "DISTINCTCOUNT ( Sales[OrderId] )", "COUNTROWS ( Sales )")
        self.assertEqual(sorted(self.codes("note")), ["I001", "M201"])
        self.assertEqual(self.codes(False), [])


# ---------------------------------------------------------------- layout standard

class Layout(Case):
    def move(self, relative, **position):
        self.edit_json(relative, lambda d: d["position"].update(position))

    def test_visual_outside_the_page_fails(self):
        self.move(BAR, width=1300)
        self.assertFails("G001")

    def test_visual_touching_the_page_edge_is_inside(self):
        self.move(BAR, x=0, width=1280)
        self.assertNot("G001")

    def test_two_data_visuals_that_overlap_fail(self):
        fields = {"queryState": {"Values": {"projections": []}}}
        self.edit_json(CARD, lambda d: d["visual"].update({"query": fields}))
        self.edit_json(BAR, lambda d: d["visual"].update({"query": fields}))
        self.assertNot("G002")                               # side by side, 16 pixels apart
        self.move(BAR, y=100)
        self.assertFails("G002")
        self.brief(layout="| G002 | Overview | Overview_Card_TotalSales | The card sits on the chart on purpose |")
        self.assertNot("G002")

    def test_visuals_without_fields_may_overlap(self):
        self.move(BAR, y=100)
        self.assertNot("G002")

    def test_position_off_the_grid_warns(self):
        self.move(CARD, width=610)
        self.assertEqual(self.codes("warn"), ["G003"])

    def test_grid_step_comes_from_the_brief(self):
        self.move(CARD, width=610, x=20, y=20)
        self.move(BAR, x=20, y=150, width=1240, height=550)
        self.brief(grid="10", margin="20", gap="10")
        self.assertEqual(self.codes("warn"), [])

    def test_margin_that_differs_warns(self):
        self.move(BAR, x=32, width=1224)
        self.move(CARD, x=32)
        self.assertEqual(self.codes("warn"), ["G004"])
        self.assertIn("left 32", self.messages("G004")[0])

    def test_bottom_margin_may_be_larger_but_not_smaller(self):
        self.move(BAR, height=400)
        self.assertNot("G004")
        self.move(BAR, height=552)
        self.assertIn("bottom 8", self.messages("G004")[0])

    def test_gap_that_differs_warns(self):
        self.move(BAR, y=168, height=528)
        self.assertEqual(self.codes("warn"), ["G006"])

    def test_same_kind_in_one_row_with_other_height_warns(self):
        shutil.copytree(os.path.dirname(self.path(CARD)), self.path(os.path.join(PAGE, "visuals", "Overview_Card_Second")))
        second = os.path.join(PAGE, "visuals", "Overview_Card_Second", "visual.json")
        self.edit_json(second, lambda d: (d.update({"name": "Overview_Card_Second"}), d["position"].update({"tabOrder": 5})))
        self.move(second, x=648, height=104)
        self.assertEqual(sorted(set(self.codes("warn"))), ["G005", "G006"])
        self.move(second, height=120)
        self.assertEqual(self.codes("warn"), [])

    def test_page_of_another_size_warns_until_the_brief_names_it(self):
        self.edit_json(os.path.join(PAGE, "page.json"), lambda d: d.update({"width": 1920, "height": 1080}))
        self.move(CARD, x=32, y=32, width=920, height=120)
        self.move(BAR, x=32, y=176, width=1856, height=872)
        self.assertEqual(self.codes("warn"), ["G007"])       # margin 32 and gap 24 are the standard's set for 1920
        self.brief(size="1920 x 1080")
        self.assertEqual(self.codes("warn"), [])

    def test_rotated_visual_is_a_note_only(self):
        self.move(CARD, angle=30, x=-50)
        self.assertIn("G008", self.codes("note"))
        self.assertNot("G001")

    def test_the_before_copy_is_not_checked(self):
        shutil.copytree(self.path("Sample.Report"), self.path(os.path.join("_before", "Sample.Report")))
        self.move(os.path.join("_before", BAR), width=5000)
        self.assertEqual(self.codes(), ["I001"])
        self.assertEqual(len(cp.find_reports(self.root)), 1)


class FieldReferences(Case):
    def bind(self, kind, entity, prop):
        field = {"field": {kind: {"Expression": {"SourceRef": {"Entity": entity}}, "Property": prop}},
                 "queryRef": "%s.%s" % (entity, prop)}
        text = {"expr": {"Literal": {"Value": "'Made-up card for a test'"}}}
        self.edit_json(CARD, lambda d: (d["visual"].update({"query": {"queryState": {"Values": {"projections": [field]}}}}),
                                        d["visual"]["visualContainerObjects"].update(
                                            {"general": [{"properties": {"altText": text}}], "title": [{"properties": {"text": text}}]})))

    def test_field_the_model_has_passes(self):
        self.bind("Measure", "_Measures", "Total Sales")
        self.assertEqual(self.codes(False), [])

    def test_measure_named_with_its_old_table_fails(self):
        self.bind("Measure", "Sales", "Total Sales")
        self.assertEqual(self.codes(False), ["B001"])
        self.assertIn("Sales[Total Sales]", self.messages("B001")[0])

    def test_unknown_table_fails(self):
        self.bind("Column", "Orders", "Amount")
        self.assertIn("table 'Orders'", self.messages("B001")[0])

    def test_measure_made_in_the_report_passes(self):
        self.bind("Measure", "Sales", "Report Only")
        self.write(os.path.join("Sample.Report", "definition", "reportExtensions.json"),
                   json.dumps({"name": "extension", "entities": [{"name": "Sales", "measures": [{"name": "Report Only"}]}]}))
        self.assertNot("B001")

    def test_report_on_a_published_model_is_checked_against_the_saved_field_list(self):
        self.bind("Measure", "Elsewhere", "Anything")
        self.edit_json(os.path.join("Sample.Report", "definition.pbir"),
                       lambda d: d.update({"datasetReference": {"byConnection": {"connectionString": "semanticmodelid=x"}}}))
        self.assertNot("B001")                                    # no saved field list: nothing to check against
        self.assertEqual([f[4] for f in self.found() if f[0] == "B002"], ["note"])
        self.write(os.path.join("docs", "model-fields.md"), "| Table | Field | Kind |\n|---|---|---|\n| Elsewhere | Other | measure |\n")
        self.assertIn("Elsewhere[Anything]", self.messages("B001")[0])
        self.write(os.path.join("docs", "model-fields.md"), "| Table | Field | Kind |\n|---|---|---|\n| Elsewhere | Anything | measure |\n")
        self.assertNot("B001")
        self.assertNot("B002")

    def test_hidden_column_used_by_a_visual_warns(self):
        self.bind("Column", "Sales", "Amount")
        self.assertEqual(self.codes("warn"), ["M104"])


# ---------------------------------------------------------------- the two fix scripts

class SetModelProperties(Case):
    def run_set(self, *sets, dry=False):
        args = ["set_model_properties.py", self.root] + (["--dry-run"] if dry else [])
        for one in sets:
            args += ["--set", one]
        return quiet(smp.main, args)

    def test_dry_run_changes_nothing(self):
        before = self.read(SALES)
        code, out = self.run_set("Sales[Channel].displayFolder=Attributes", dry=True)
        self.assertEqual(code, 0)
        self.assertIn("would change  Sales[Channel]: displayFolder not set -> 'Attributes'", out)
        self.assertEqual(self.read(SALES), before)

    def test_only_the_one_line_changes(self):
        before = self.read(SALES).splitlines()
        self.assertEqual(self.run_set("Sales[Channel].displayFolder=Attributes")[0], 0)
        after = self.read(SALES).splitlines()
        self.assertEqual([line for line in after if line not in before], ["\t\tdisplayFolder: Attributes"])
        self.assertEqual(len(after), len(before) + 1)
        self.assertEqual(self.codes(), ["I001"])

    def test_existing_value_is_replaced_in_place(self):
        self.assertEqual(self.run_set("[Total Sales].formatString=#,0.00")[0], 0)
        self.assertIn("SUM ( Sales[Amount] ) // one-line DAX comment is allowed here\n\t\tformatString: #,0.00\n"
                      "\t\tdisplayFolder: Finance\\Base\n", self.read(MEASURES))

    def test_property_goes_after_a_multi_line_expression(self):
        self.replace(MEASURES, "\t\tformatString: 0.0%\n", "")
        self.assertEqual(self.run_set("[Return Rate].formatString=0.0%")[0], 0)
        self.assertIn("\t\t\t    COUNTROWS ( Sales )\n\t\t\t)\n\t\tformatString: 0.0%\n", self.read(MEASURES))
        self.assertEqual(self.codes(), ["I001"])

    def test_same_value_is_no_change(self):
        code, out = self.run_set("[Total Sales].displayFolder=Finance\\Base")
        self.assertEqual(code, 0)
        self.assertIn("no change", out)

    def test_hiding_a_column_and_a_table(self):
        self.assertEqual(self.run_set("Sales[Channel].isHidden=true", "Sales.isHidden=true")[0], 0)
        text = self.read(SALES)
        self.assertIn("table Sales\n\tisHidden\n", text)
        self.assertIn("\tcolumn Channel\n\t\tisHidden\n", text)

    def test_showing_again_and_other_values_are_refused(self):
        for bad in ("Sales[Amount].isHidden=false", "Sales[Amount].summarizeBy=sum", "Sales[Amount].name=Value",
                    "Sales[Amount].sourceColumn=X", "Sales[Missing].isHidden=true", "[Total Sales].summarizeBy=none",
                    "Sales[Channel].CalculatedReason=Not a calculated column", "[Total Sales].formatString="):
            before = self.read(SALES) + self.read(MEASURES)
            code, out = self.run_set(bad)
            self.assertEqual(code, 1, bad)
            self.assertIn("Nothing was written.", out)
            self.assertEqual(self.read(SALES) + self.read(MEASURES), before)

    def test_one_refusal_stops_every_change(self):
        before = self.read(SALES)
        code, _ = self.run_set("Sales[Channel].displayFolder=Attributes", "Sales[Nowhere].isHidden=true")
        self.assertEqual(code, 1)
        self.assertEqual(self.read(SALES), before)

    def test_summarisation_can_be_turned_off_when_asked(self):
        self.assertEqual(self.run_set("Sales[Amount].summarizeBy=none")[0], 0)
        self.assertIn("\t\tformatString: #,0.00\n\t\tsummarizeBy: none\n\t\tsourceColumn: Amount\n", self.read(SALES))

    def test_windows_line_endings_are_kept(self):
        with open(self.path(SALES), "rb") as fh:
            raw = fh.read().replace(b"\n", b"\r\n")
        with open(self.path(SALES), "wb") as fh:
            fh.write(raw)
        self.assertEqual(self.run_set("Sales[Channel].displayFolder=Attributes")[0], 0)
        with open(self.path(SALES), "rb") as fh:
            raw = fh.read()
        self.assertIn(b"\t\tdisplayFolder: Attributes\r\n", raw)
        self.assertEqual(raw.count(b"\n"), raw.count(b"\r\n"))
        self.assertFalse(raw.startswith(b"\xef\xbb\xbf"))

    def test_value_with_outer_spaces_is_quoted(self):
        self.assertEqual(self.run_set('Sales[Channel].displayFolder= Odd "name" ')[0], 0)
        self.assertIn('\t\tdisplayFolder: " Odd ""name"" "\n', self.read(SALES))

    def test_reason_on_a_calculated_table(self):
        self.write(os.path.join(TABLES, "Calendar.tmdl"),
                   "/// One row per day.\ntable Calendar\n\n\t/// The day.\n\tcolumn Date\n\t\tdataType: dateTime\n"
                   "\t\tformatString: Short Date\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Date]\n\n"
                   "\tpartition Calendar = calculated\n\t\tmode: import\n\t\tsource = CALENDAR(DATE(2026,1,1), DATE(2026,12,31))\n")
        self.assertEqual(self.codes(False), ["M105"])
        self.assertEqual(self.run_set("Calendar.CalculatedReason=The source has no calendar table.")[0], 0)
        self.assertTrue(self.read(os.path.join(TABLES, "Calendar.tmdl")).endswith(
            "DATE(2026,12,31))\n\n\tannotation CalculatedReason = The source has no calendar table.\n"))
        self.assertEqual(self.codes(False), [])
        self.assertEqual(self.run_set("Calendar.CalculatedReason=The source system has no calendar.")[0], 0)
        self.assertEqual(self.read(os.path.join(TABLES, "Calendar.tmdl")).count("CalculatedReason"), 1)

    def test_from_findings_hides_only_what_the_check_found(self):
        self.replace(SALES, "\t\tdataType: decimal\n\t\tisHidden\n", "\t\tdataType: decimal\n")
        self.replace(SALES, "\t\tsummarizeBy: sum\n", "\t\tsummarizeBy: none\n")
        code, out = quiet(smp.main, ["set_model_properties.py", self.root, "--from-findings", "M103", "--only", "Sales[Channel]"])
        self.assertEqual((code, "0 change(s)" in out), (0, True))
        code, out = quiet(smp.main, ["set_model_properties.py", self.root, "--from-findings", "M103"])
        self.assertIn("changed  Sales[Amount]: isHidden 'visible' -> 'true'", out)
        self.assertEqual(self.codes(), ["I001"])

    def test_from_findings_takes_no_other_code(self):
        self.assertEqual(quiet(smp.main, ["set_model_properties.py", self.root, "--from-findings", "M107"])[0], 2)
        self.assertEqual(quiet(smp.main, ["set_model_properties.py", self.root])[0], 2)


class SetPositions(Case):
    def test_move_writes_only_the_four_numbers(self):
        before = json.loads(self.read(CARD))
        code, out = quiet(sp.main, ["set_positions.py", self.root, "--move", "Overview/Overview_Card_TotalSales=24,24,304,120"])
        self.assertEqual(code, 0, out)
        after = json.loads(self.read(CARD))
        self.assertEqual(after["position"], dict(before["position"], width=304))
        before.pop("position")
        after.pop("position")
        self.assertEqual(after, before)
        self.assertIn("look at these pages: Overview.", out)

    def test_visual_can_be_named_by_label_and_page_by_tab_name(self):
        self.edit_json(os.path.join(PAGE, "page.json"), lambda d: d.update({"displayName": "Sales overview"}))
        code, out = quiet(sp.main, ["set_positions.py", self.root, "--move", "Sales overview/Overview_Bar_SalesByMonth=24,160,1232,528"])
        self.assertEqual(code, 0, out)
        self.assertEqual(json.loads(self.read(BAR))["position"]["height"], 528)

    def test_dry_run_changes_nothing(self):
        before = self.read(CARD)
        code, out = quiet(sp.main, ["set_positions.py", self.root, "--dry-run", "--move", "Overview/Overview_Card_TotalSales=24,24,304,120"])
        self.assertEqual(code, 0)
        self.assertIn("would change", out)
        self.assertEqual(self.read(CARD), before)

    def test_refusals_write_nothing_at_all(self):
        self.edit_json(BAR, lambda d: d.update({"parentGroupName": "Overview_Group_Header"}))
        before = self.read(CARD)
        for target in ("Overview/Overview_Group_Header=0,0,1280,24",          # a group
                       "Overview/4f0c9d2a7b1e8a6c3d5f=24,160,1232,528",       # inside a group
                       "Overview/Overview_Card_TotalSales=1000,24,608,120",   # would leave the page
                       "Overview/Overview_Card_TotalSales=24,24,0,120",       # no width
                       "Overview/Nothing=1,1,8,8"):                           # not found
            code, out = quiet(sp.main, ["set_positions.py", self.root, "--move",
                                        "Overview/Overview_Card_TotalSales=24,24,304,120", "--move", target])
            if target.startswith("Overview/Overview_Card_TotalSales"):
                code, out = quiet(sp.main, ["set_positions.py", self.root, "--move", target])
            self.assertEqual(code, 1, target)
            self.assertIn("Nothing was written.", out)
            self.assertEqual(self.read(CARD), before)

    def test_rotated_visual_is_refused(self):
        self.edit_json(CARD, lambda d: d["position"].update({"angle": 15}))
        code, out = quiet(sp.main, ["set_positions.py", self.root, "--move", "Overview/Overview_Card_TotalSales=24,24,304,120"])
        self.assertEqual(code, 1)
        self.assertIn("rotated", out)

    def test_snap_puts_numbers_on_the_grid_and_leaves_groups_and_mobile_alone(self):
        self.edit_json(CARD, lambda d: d["position"].update({"x": 26, "width": 605.5}))
        self.edit_json(GROUP, lambda d: d["position"].update({"height": 21}))
        mobile = os.path.join(os.path.dirname(CARD), "mobile.json")
        self.write(mobile, json.dumps({"$schema": "https://developer.microsoft.com/json-schemas/fabric/x", "position": {"x": 3, "y": 3, "width": 99, "height": 99}}))
        code, out = quiet(sp.main, ["set_positions.py", self.root, "--snap"])
        self.assertEqual(code, 0, out)
        self.assertEqual(json.loads(self.read(CARD))["position"]["x"], 24)
        self.assertEqual(json.loads(self.read(CARD))["position"]["width"], 608)
        self.assertEqual(json.loads(self.read(GROUP))["position"]["height"], 21)
        self.assertEqual(json.loads(self.read(mobile))["position"]["width"], 99)
        self.assertIn("left alone  Overview/Overview_Group_Header: it is a group", out)
        self.assertEqual(self.codes("warn"), [])

    def test_snap_skips_tooltip_pages(self):
        self.edit_json(os.path.join(PAGE, "page.json"), lambda d: d.update({"type": "Tooltip"}))
        self.edit_json(CARD, lambda d: d["position"].update({"x": 26}))
        code, out = quiet(sp.main, ["set_positions.py", self.root, "--snap"])
        self.assertIn("0 visual(s) changed", out)

    def test_other_numbers_in_the_file_stay_as_written(self):
        self.replace(CARD, '"z": 0', '"z": 1500.50')
        quiet(sp.main, ["set_positions.py", self.root, "--move", "Overview/Overview_Card_TotalSales=24,24,304,120"])
        self.assertIn('"z": 1500.50', self.read(CARD))

    def test_wrong_usage(self):
        for args in ([], ["--move", "Overview/X=1,2,3"], ["--move", "NoSlash=1,2,3,4"], ["--snap", "--move", "A/B=1,2,3,4"]):
            self.assertEqual(quiet(sp.main, ["set_positions.py", self.root] + args)[0], 2, args)


# ---------------------------------------------------------------- the flow

REVIEW_HEAD = "# Checklist review\n\n| Item | Status | Evidence |\n|---|---|---|\n"


def review_text(fails=(), not_applicable=()):
    rows = []
    for item in range(1, 80):
        status = "Fail" if item in fails else "Not applicable" if item in not_applicable else "Pass"
        rows.append("| %d | %s | docs/report-brief.md, section 6 |\n" % (item, status))
    return REVIEW_HEAD + "".join(rows)


class FlowCase(Case):
    """A made-up project inside a new Git repository."""

    def git(self, *args):
        done = subprocess.run(("git", "-C", self.root) + args, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.assertEqual(done.returncode, 0, done.stdout.decode("utf-8", "replace"))
        return done.stdout.decode("utf-8", "replace").strip()

    def setUp(self):
        super().setUp()
        self.write("Sample.pbip", json.dumps({"version": "1.0", "artifacts": [{"report": {"path": "Sample.Report"}}]}))
        self.write(".gitignore", "_before/\n__pycache__/\n")
        self.git("init", "-q", "-b", "work")
        self.git("config", "user.email", "tester@example.com")
        self.git("config", "user.name", "Tester")
        self.git("config", "commit.gpgsign", "false")
        self.commit("Start")

    def commit(self, message):
        self.git("add", "-A")
        self.git("commit", "-q", "-m", message)

    def step(self):
        return quiet(improve.next_step, self.root)[1]


@unittest.skipUnless(shutil.which("git"), "Git is not installed")
class Flow(FlowCase):

    def test_start_stops_when_something_is_not_committed(self):
        self.write("note.txt", "not committed\n")
        code, out = quiet(improve.start, self.root)
        self.assertEqual(code, 1)
        self.assertIn("not everything is committed", out)
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD"), "work")
        self.assertFalse(os.path.exists(self.path("_before")))

    def test_start_makes_a_branch_and_an_untouched_copy(self):
        head = self.git("rev-parse", "HEAD")
        code, out = quiet(improve.start, self.root)
        self.assertEqual(code, 0, out)
        branch = self.git("rev-parse", "--abbrev-ref", "HEAD")
        self.assertTrue(branch.startswith("improve/"))
        self.assertEqual(self.git("rev-parse", "work"), head)                 # the original branch did not move
        for name in ("Sample.pbip", os.path.join("Sample.Report", "definition.pbir"), MEASURES, CARD):
            with open(self.path(name), "rb") as one, open(self.path(os.path.join("_before", name)), "rb") as two:
                self.assertEqual(one.read(), two.read(), name)                # copied unchanged, names and all
        self.assertEqual(self.git("status", "--porcelain"), "")              # Git ignores the copy
        self.assertEqual(self.codes(), ["I001"])                             # and the checks skip it
        self.assertEqual(json.loads(self.read(os.path.join("_before", "Sample.Report", "definition.pbir")))
                         ["datasetReference"]["byPath"]["path"], "../Sample.SemanticModel")

    def test_start_is_refused_while_a_flow_is_running_or_left_its_files(self):
        quiet(improve.start, self.root)
        first = self.git("rev-parse", "--abbrev-ref", "HEAD")
        code, out = quiet(improve.start, self.root)                           # on the flow branch itself
        self.assertEqual(code, 1)
        self.assertIn("already a flow branch", out)
        self.git("checkout", "-q", "work")
        code, out = quiet(improve.start, self.root)                           # back on the old branch: _before/ is still there
        self.assertEqual(code, 1)
        self.assertIn("an earlier flow left _before", out)
        shutil.rmtree(self.path("_before"))
        self.write(os.path.join("docs", "fix-plan.md"), "old plan\n")
        self.commit("An old plan")
        code, out = quiet(improve.start, self.root)
        self.assertEqual(code, 1)
        self.assertIn("docs/fix-plan.md", out)
        self.assertEqual(self.git("rev-parse", "--abbrev-ref", "HEAD"), "work")
        self.assertEqual(self.git("branch", "--list", "improve/*").split(), [first])

    def test_start_is_refused_without_a_branch(self):
        self.git("checkout", "-q", "--detach")
        code, out = quiet(improve.start, self.root)
        self.assertEqual(code, 1)
        self.assertIn("no branch is checked out", out)

    def test_failed_copy_leaves_no_half_copy(self):
        saved = shutil.copytree

        def broken(source, target, **options):
            os.makedirs(target)
            raise shutil.Error("made-up failure")
        shutil.copytree = broken
        try:
            code, out = quiet(improve.start, self.root)
        finally:
            shutil.copytree = saved
        self.assertEqual(code, 0)
        self.assertIn("No second copy: copying failed", out)
        self.assertFalse(os.path.exists(self.path("_before")))

    def test_only_a_plain_yes_is_an_approval(self):
        quiet(improve.start, self.root)
        self.replace(CARD, '"width": 608', '"width": 610')
        self.commit("As found")
        self.write(os.path.join("docs", "checklist-review.md"), review_text(fails=(76,)))
        quiet(improve.snapshot, self.root)
        quiet(improve.plan, self.root)
        plan = os.path.join("docs", "fix-plan.md")
        text = self.read(plan).replace("<what will change>", "a").replace("<files>", "b").replace("<what could break>", "c")
        rows = [line for line in text.splitlines() if line.startswith("| F") and "| Layout |" in line]
        self.assertEqual(len(rows), 1)
        for answer in ("yes?", "yes/no", "yes or no", "Yes - not sure, ask Anna", "yes, but only after the backup", "n/a", "ok"):
            self.write(plan, text.replace(rows[0], rows[0][:-3] + " %s |" % answer))
            self.assertEqual(quiet(improve.check_plan, self.root)[0], 1, answer)
            self.assertIn("Step 25. Finish the fix plan", self.step(), answer)
        for answer in ("yes", "YES", "yes, 2026-11-11", "Yes 2026-11-11"):
            self.write(plan, text.replace(rows[0], rows[0][:-3] + " %s |" % answer))
            self.assertEqual(quiet(improve.check_plan, self.root)[0], 0, answer)
            self.assertIn("Apply the approved Layout rows only", self.step(), answer)

    def test_the_stop_holds_until_every_fix_row_has_an_answer(self):
        quiet(improve.start, self.root)
        self.replace(CARD, '"width": 608', '"width": 610')
        self.replace(SALES, "\t/// Sales channel of the order line: Web or Store.\n", "")
        self.commit("As found")
        self.write(os.path.join("docs", "checklist-review.md"), review_text(fails=(76,)))
        quiet(improve.snapshot, self.root)
        quiet(improve.plan, self.root)
        plan = os.path.join("docs", "fix-plan.md")
        text = self.read(plan).replace("<what will change>", "a").replace("<files>", "b").replace("<what could break>", "c")
        layout = [line for line in text.splitlines() if line.startswith("| F") and "| Layout |" in line][0]
        self.write(plan, text.replace(layout, layout[:-3] + " no |"))
        step = self.step()
        self.assertIn("Step 26. Stop.", step)                                 # one 'no' does not end the stop
        self.assertIn("1 row(s) still have no answer", step)

    def test_no_copy_when_git_would_not_ignore_it(self):
        self.write(".gitignore", "__pycache__/\n")
        self.commit("Do not ignore the copy")
        code, out = quiet(improve.start, self.root)
        self.assertEqual(code, 0)
        self.assertIn("No second copy: Git does not ignore _before/", out)
        self.assertFalse(os.path.exists(self.path("_before")))
        self.assertTrue(self.git("rev-parse", "--abbrev-ref", "HEAD").startswith("improve/"))

    def test_no_copy_when_a_path_would_be_too_long(self):
        saved = improve.PATH_LIMIT
        improve.PATH_LIMIT = 20
        try:
            code, out = quiet(improve.start, self.root)
        finally:
            improve.PATH_LIMIT = saved
        self.assertEqual(code, 0)
        self.assertIn("No second copy: a path in it would be", out)
        self.assertFalse(os.path.exists(self.path("_before")))

    def test_start_needs_a_project(self):
        shutil.rmtree(self.path("Sample.Report"))
        shutil.rmtree(self.path("Sample.SemanticModel"))
        os.remove(self.path("Sample.pbip"))
        self.commit("No project")
        self.assertEqual(quiet(improve.start, self.root)[0], 1)

    def test_the_whole_flow_step_by_step(self):
        self.replace(CARD, '"width": 608', '"width": 610')                    # something for the Layout kind
        self.replace(SALES, "\t/// Sales channel of the order line: Web or Store.\n", "")   # and for Mechanical
        self.commit("The report as it was found")
        self.assertIn("Step 23.", self.step())
        self.assertEqual(quiet(improve.start, self.root)[0], 0)
        self.assertIn("Step 24. Evaluate", self.step())

        self.assertEqual(quiet(improve.snapshot, self.root)[0], 1)            # no review yet
        self.write(os.path.join("docs", "checklist-review.md"), REVIEW_HEAD + "| 1 | Pass | x |\n")
        self.assertEqual(quiet(improve.snapshot, self.root)[0], 1)            # not a finished review
        self.write(os.path.join("docs", "checklist-review.md"), review_text(fails=(23, 49, 76), not_applicable=(79,)))
        self.assertIn("python scripts/improve.py snapshot", self.step())
        self.assertEqual(quiet(improve.snapshot, self.root)[0], 0)
        self.assertEqual(quiet(improve.snapshot, self.root)[0], 1)            # the 'before' is never replaced
        self.assertIn("Step 25. Write the fix plan", self.step())

        self.assertEqual(quiet(improve.plan, self.root)[0], 0)
        self.assertIn("Step 25. Finish the fix plan", self.step())
        plan = os.path.join("docs", "fix-plan.md")
        text = self.read(plan)
        self.assertIn("| Mechanical | D001 |", text)
        self.assertIn("| Layout | G003 |", text)
        self.assertIn("| Needs a person | Item 76 |", text)
        text = text.replace("| ? | Item 23 |", "| Mechanical | Item 23 |").replace("| ? | Item 49 |", "| Layout | Item 49 |")
        text = text.replace("<what will change>", "See the rows with a code").replace("<files>", "see those rows")
        self.write(plan, text.replace("<what could break>", "see those rows"))
        code, out = quiet(improve.check_plan, self.root)
        self.assertEqual(code, 0, out)
        self.assertIn("Step 26. Stop.", self.step())

        text = self.read(plan)
        approved = "\n".join(line[:-3] + " yes, 2026-11-11 |" if line.startswith("| F") and "| Needs a person |" not in line
                             else line for line in text.splitlines()) + "\n"
        self.write(plan, approved)
        self.assertIn("Apply the approved Mechanical rows only", self.step())
        self.replace(SALES, "\tcolumn Channel\n", "\t/// Sales channel of the order line: Web or Store.\n\tcolumn Channel\n")
        self.commit(improve.COMMITS["Mechanical"])
        self.assertIn("Apply the approved Layout rows only", self.step())
        self.assertEqual(quiet(sp.main, ["set_positions.py", self.root, "--snap"])[0], 0)
        self.commit(improve.COMMITS["Layout"])
        self.assertIn("Step 28. Evaluate again", self.step())

        self.write(os.path.join("docs", "checklist-review.md"), review_text(fails=(76,), not_applicable=(79,)))
        self.assertIn("python scripts/improve.py compare", self.step())
        code, out = quiet(improve.compare, self.root)
        self.assertEqual(code, 0)
        lines = [" ".join(line.split()) for line in out.splitlines()]
        self.assertIn("Before 75 3 1", lines)
        self.assertIn("After 77 1 1", lines)
        self.assertIn("Item 23: Fail -> Pass", lines)
        self.assertIn("Item 49: Fail -> Pass", lines)
        self.assertIn("Pages to look at in Power BI Desktop: Overview", lines)
        self.assertTrue(any(line.startswith("Needs a person: 1 row(s)") for line in lines))
        subjects = self.git("log", "--format=%s", "work..HEAD").splitlines()
        self.assertEqual(subjects[:2], [improve.COMMITS["Layout"], improve.COMMITS["Mechanical"]])   # one commit per group

    def test_only_approved_kinds_are_asked_for(self):
        quiet(improve.start, self.root)
        self.replace(CARD, '"width": 608', '"width": 610')
        self.commit("As found")
        self.write(os.path.join("docs", "checklist-review.md"), review_text(fails=(49,)))
        quiet(improve.snapshot, self.root)
        quiet(improve.plan, self.root)
        plan = os.path.join("docs", "fix-plan.md")
        text = self.read(plan).replace("| ? | Item 49 |", "| Layout | Item 49 |").replace("<what will change>", "a")
        text = text.replace("<files>", "b").replace("<what could break>", "c")
        self.write(plan, "\n".join(line[:-3] + " no, 2026-11-11 |" if line.startswith("| F") else line
                                   for line in text.splitlines()) + "\n")
        self.assertIn("python scripts/improve.py compare", self.step())       # nothing approved: nothing to apply

    def test_plan_table_problems_are_reported(self):
        self.write(os.path.join("docs", "fix-plan.md"),
                   "| Id | Kind | Item or code | Object | What will change | Files | What could break | Approved |\n|---|---|---|---|---|---|---|---|\n"
                   "| F1 | Cosmetic | M003 | [A] | Set the folder | a.tmdl | Nothing | maybe |\n"
                   "| F2 | Layout | G003 | x |  | b.json | Looks different |  |\n| F3 | Layout | G003 |\n")
        code, out = quiet(improve.check_plan, self.root)
        self.assertEqual(code, 1)
        for part in ("row F1: Kind must be one of", "row F1: Approved must be empty", "row F2: 'What will change' is empty",
                     "the row has 3 cells"):
            self.assertIn(part, out)

    def test_command_line(self):
        self.assertEqual(quiet(improve.main, ["improve.py"])[0], 2)
        self.assertEqual(quiet(improve.main, ["improve.py", "publish"])[0], 2)
        self.assertEqual(quiet(improve.main, ["improve.py", "next", self.root])[0], 0)
        self.assertEqual(quiet(improve.main, ["improve.py", "compare", self.root])[0], 1)


# ---------------------------------------------------------------- found by the adversarial review

AUTO_DATE = ("table LocalDateTable_0a1b\n\tisHidden\n\n\tcolumn Date\n\t\tdataType: dateTime\n\t\tisHidden\n"
             "\t\tsummarizeBy: none\n\t\tsourceColumn: [Date]\n\n"
             "\tcolumn Year = YEAR([Date])\n\t\tdataType: int64\n\t\tisHidden\n\t\tsummarizeBy: none\n\n"
             "\tcolumn MonthNo = MONTH([Date])\n\t\tdataType: int64\n\t\tisHidden\n\t\tsummarizeBy: none\n\n"
             "\tcolumn Month = FORMAT([Date], \"MMMM\")\n\t\tdataType: string\n\t\tisHidden\n\t\tsummarizeBy: none\n\n"
             "\tcolumn QuarterNo = INT(([MonthNo] + 2) / 3)\n\t\tdataType: int64\n\t\tisHidden\n\t\tsummarizeBy: none\n\n"
             "\tcolumn Quarter = \"Qtr \" & [QuarterNo]\n\t\tdataType: string\n\t\tisHidden\n\t\tsummarizeBy: none\n\n"
             "\tcolumn Day = DAY([Date])\n\t\tdataType: int64\n\t\tisHidden\n\t\tsummarizeBy: none\n\n"
             "\tpartition LocalDateTable_0a1b = calculated\n\t\tmode: import\n"
             "\t\tsource = Calendar(Date(2026,1,1), Date(2026,12,31))\n")


class ReviewedEdgeCases(Case):
    def test_auto_date_tables_are_left_out_of_the_model_standard(self):
        self.write(os.path.join(TABLES, "LocalDateTable_0a1b.tmdl"), AUTO_DATE)
        self.add_measure("\t/// Day of the order.\n\tcolumn 'Order Date'\n\t\tdataType: dateTime\n\t\tformatString: Short Date\n"
                         "\t\tsummarizeBy: none\n\t\tsourceColumn: OrderDate\n", SALES)
        self.write(RELATIONSHIPS, "relationship r1\n\tjoinOnDateBehavior: datePartOnly\n\tfromColumn: Sales.'Order Date'\n"
                                  "\ttoColumn: LocalDateTable_0a1b.Date\n")
        # no M105, M106, M010, M102, M110 or M201 for Power BI's own table; M401 says Auto date/time is on
        self.assertEqual(self.codes(), ["I001", "M401", "M403"])
        findings, _, _ = cp.run(self.root)
        self.assertEqual(findings.fixes, [])                       # and no proposal to hide the user's date column

    def test_odd_characters_inside_a_text_value_do_not_hide_later_objects(self):
        self.replace(MEASURES, '"http://example.com/help"', '"http://example.com/help \x0c\x85"')
        self.replace(MEASURES, "\t\tformatString: 0.0%\n", "")
        self.assertEqual(self.codes(False), ["M009"])
        self.replace(SALES, "/// One row per order line.", "/// One row per order line.")
        self.replace(SALES, "\t\tdataType: decimal\n\t\tisHidden\n", "\t\tdataType: decimal\n")
        self.assertEqual(sorted(self.codes(False)), ["M009", "M107"])

    def test_setter_keeps_every_other_byte(self):
        with open(self.path(MEASURES), "rb") as fh:
            raw = fh.read()
        odd = raw.replace(b'"http://example.com/help"', '"help \x0c\x85"'.encode("utf-8"))
        odd = odd.replace(b"\tmeasure 'Total Sales'", b"\r\n\tmeasure 'Total Sales'", 1).rstrip(b"\n")   # one CRLF; no final newline
        with open(self.path(MEASURES), "wb") as fh:
            fh.write(odd)
        code, out = quiet(smp.main, ["set_model_properties.py", self.root, "--set", "[Total Sales].formatString=#,0.00"])
        self.assertEqual(code, 0, out)
        with open(self.path(MEASURES), "rb") as fh:
            after = fh.read()
        self.assertEqual(after, odd.replace(b"formatString: #,0\n\t\tdisplayFolder: Finance", b"formatString: #,0.00\n\t\tdisplayFolder: Finance"))

    def test_new_last_line_of_a_file_without_final_newline(self):
        text = ("/// One row per day.\ntable Calendar\n\n\t/// The day.\n\tcolumn Date\n\t\tdataType: dateTime\n"
                "\t\tformatString: Short Date\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Date]\n\n"
                "\tpartition Calendar = calculated\n\t\tmode: import\n\t\tsource = CALENDAR(DATE(2026,1,1), DATE(2026,12,31))")
        self.write(os.path.join(TABLES, "Calendar.tmdl"), text)
        self.assertEqual(quiet(smp.main, ["set_model_properties.py", self.root, "--set", "Calendar.CalculatedReason=No calendar at the source."])[0], 0)
        self.assertEqual(self.read(os.path.join(TABLES, "Calendar.tmdl")),
                         text + "\n\n\tannotation CalculatedReason = No calendar at the source.")
        self.assertEqual(self.codes(False), [])

    def test_setter_special_cases(self):
        self.replace(SALES, "\tcolumn Channel\n\t\tdataType: string\n", "\tcolumn Channel\n\t\tisHidden: false\n\t\tdataType: string\n")
        self.assertEqual(quiet(smp.main, ["set_model_properties.py", self.root, "--set", "Sales[Channel].isHidden=true"])[0], 0)
        self.assertIn("\tcolumn Channel\n\t\tisHidden\n\t\tdataType: string\n", self.read(SALES))
        self.assertEqual(self.read(SALES).count("isHidden"), 3)

    def test_setter_follows_a_file_indented_with_spaces(self):
        self.write(SALES, self.read(SALES).replace("\t", "    "))
        self.assertEqual(quiet(smp.main, ["set_model_properties.py", self.root, "--set", "Sales[Channel].displayFolder=Attributes",
                                          "--set", "Sales.isHidden=true"])[0], 0)
        text = self.read(SALES)
        self.assertNotIn("\t", text)
        self.assertIn("    column Channel\n        displayFolder: Attributes\n", text)
        self.assertIn("table Sales\n    isHidden\n", text)

    def test_setter_refuses_what_it_cannot_do_safely(self):
        self.add_measure("\t/// Amount with a flat tax.\n\tcolumn 'Amount With Tax' = Sales[Amount] * 1.1\n"
                         "\t\tdataType: decimal\n\t\tformatString: #,0.00\n\t\tsummarizeBy: none\n\n"
                         "\t\tannotation CalculatedReason =\n\t\t\t\tfirst line\n\t\t\t\tsecond line\n", SALES)
        before = self.read(SALES)
        code, out = quiet(smp.main, ["set_model_properties.py", self.root, "--set", "Sales[Amount With Tax].CalculatedReason=New reason."])
        self.assertEqual(code, 1)
        self.assertIn("runs over several lines", out)
        self.assertEqual(self.read(SALES), before)
        shutil.copytree(self.path("Sample.SemanticModel"), self.path("Copy.SemanticModel"))
        code, out = quiet(smp.main, ["set_model_properties.py", self.root, "--set", "Sales.isHidden=true"])
        self.assertEqual(code, 1)
        self.assertIn("more than one model", out)
        shutil.rmtree(self.path("Copy.SemanticModel"))
        with open(self.path(os.path.join(TABLES, "Old.tmdl")), "wb") as fh:
            fh.write("table Caf\xe9\n".encode("cp1252"))
        code, out = quiet(smp.main, ["set_model_properties.py", self.root, "--set", "Sales.isHidden=true"])
        self.assertEqual(code, 1)
        self.assertIn("not UTF-8", out)
        self.assertEqual(self.read(SALES), before)

    def test_object_name_with_an_equals_sign_can_be_named(self):
        self.add_measure("\t/// Share of web orders.\n\tmeasure 'Share (Channel = Web)' = 1\n\t\tformatString: 0%\n"
                         "\t\tdisplayFolder: Customer\\Base\n")
        code, out = quiet(smp.main, ["set_model_properties.py", self.root, "--set", "[Share (Channel = Web)].displayFolder=Customer\\Ratios"])
        self.assertEqual(code, 0, out)
        self.assertIn("displayFolder: Customer\\Ratios", self.read(MEASURES))

    def test_the_untouched_copy_is_never_edited_even_when_named(self):
        shutil.copytree(self.path("Sample.Report"), self.path(os.path.join("_before", "Sample.Report")))
        shutil.copytree(self.path("Sample.SemanticModel"), self.path(os.path.join("_before", "Sample.SemanticModel")))
        copy = self.path("_before")
        self.edit_json(os.path.join("_before", CARD), lambda d: (d["visual"].pop("visualContainerObjects"), d["position"].update({"x": 26})))
        before = self.read(os.path.join("_before", CARD)) + self.read(os.path.join("_before", SALES))
        for target in (copy, os.path.join(copy, "Sample.Report"), os.path.join(copy, "Sample.SemanticModel")):
            self.assertEqual(quiet(svd.main, ["set_visual_defaults.py", target])[0], 2)
            self.assertEqual(quiet(sp.main, ["set_positions.py", target, "--snap"])[0], 2)
            self.assertEqual(quiet(smp.main, ["set_model_properties.py", target, "--set", "Sales.isHidden=true"])[0], 2)
            self.assertEqual(quiet(cp.main, ["check_project.py", target])[0], 2)
        self.assertEqual(self.read(os.path.join("_before", CARD)) + self.read(os.path.join("_before", SALES)), before)

    def test_huge_numbers_do_not_crash(self):
        for change in (lambda d: d["position"].update({"x": 10 ** 400}), lambda d: d["position"].update({"width": float("inf")})):
            self.setUp()
            data = json.loads(self.read(CARD))
            change(data)
            self.write(CARD, json.dumps(data).replace("Infinity", "1e400"))
            self.assertIn("J002", self.codes(False))
            self.assertEqual(quiet(sp.main, ["set_positions.py", self.root, "--snap"])[0], 0)
            self.tearDown()
        self.setUp()
        self.replace(os.path.join(PAGE, "page.json"), '"width": 1280', '"width": 1e400')
        self.assertEqual(self.codes("warn"), ["G007"])               # said, not skipped in silence
        self.assertEqual(quiet(sp.main, ["set_positions.py", self.root, "--snap"])[0], 0)
        code, out = quiet(sp.main, ["set_positions.py", self.root, "--move", "Overview/Overview_Card_TotalSales=24,24,304,120"])
        self.assertEqual(code, 1)
        self.assertIn("no width and height", out)

    def test_negative_size_and_page_without_size_are_reported(self):
        self.edit_json(CARD, lambda d: d["position"].update({"width": -5}))
        self.assertIn("J002", self.codes(False))
        self.edit_json(os.path.join(PAGE, "page.json"), lambda d: d.update({"width": "1280"}))
        self.assertIn("G007", self.codes("warn"))

    def test_page_of_unknown_size_asks_for_margin_and_gap(self):
        self.edit_json(os.path.join(PAGE, "page.json"), lambda d: d.update({"width": 1600, "height": 900}))
        self.brief(size="1600 x 900")
        self.assertEqual(self.codes("warn"), ["G004"])
        self.assertIn("write both in the brief", self.messages("G004")[0])

    def test_brief_numbers_with_thousands_separators_and_star_bullets(self):
        self.brief(size="1,920 x 1,080", margin="32", gap="24")
        self.write(BRIEF, self.read(BRIEF).replace("- Page size", "* Page size"))
        brief = cp.read_brief(self.root)
        self.assertEqual((brief["page_size"], brief["margin"], brief["gap"]), ((1920, 1080), 32, 24))
        self.brief(size="1280,720")
        self.assertEqual(cp.read_brief(self.root)["page_size"], (1280, 720))

    def test_exception_with_a_placeholder_reason_does_not_count(self):
        self.replace(SALES, "\t\tdataType: decimal\n\t\tisHidden\n", "\t\tdataType: decimal\n")
        for reason in ("TODO", "tbd", "n/a", "TODO(owner): ask finance"):
            self.brief(model="| M107 | Sales[Amount] | %s |" % reason)
            self.assertFails("M107")
        self.brief(model="| M107 | Sales[Amount] | Analysts total it in ad hoc tables |")
        self.assertNot("M107")

    def test_more_name_and_folder_breaches(self):
        self.replace(MEASURES, "measure 'Total Sales' =", "measure REVENUE =")
        self.assertEqual(self.codes(False), ["M007"])
        self.brief(own="REVENUE")
        self.assertEqual(self.codes(False), [])
        self.replace(MEASURES, "\t\tdisplayFolder: Finance\\Base\n", "\t\tdisplayFolder: Finance \\ Base\n")
        self.assertEqual(self.codes(False), ["M003"])
        self.assertIn("no space before or after", self.messages("M003")[0])

    def test_excel_candidates_leave_out_columns_with_a_variation(self):
        self.brief(excel="yes")
        self.assertIn("OrderId, Amount", self.messages("M301")[0])
        self.replace(SALES, "\t\tsourceColumn: OrderId\n", "\t\tsourceColumn: OrderId\n\n\t\tvariation Variation\n"
                     "\t\t\tisDefault\n\t\t\trelationship: r1\n\t\t\tdefaultHierarchy: Other.'A Hierarchy'\n")
        self.assertNotIn("OrderId", self.messages("M301")[0])


class ReviewedLayoutCases(Case):
    FIELDS = {"queryState": {"Values": {"projections": []}}}

    def stacked(self):
        """The card and the bar chart, both with fields, the chart moved onto the card."""
        self.edit_json(CARD, lambda d: d["visual"].update({"query": self.FIELDS}))
        self.edit_json(BAR, lambda d: (d["visual"].update({"query": self.FIELDS}), d["position"].update({"y": 100})))

    def bookmark(self, name, *hidden):
        containers = {visual: {"singleVisual": {"display": {"mode": "hidden"}}} for visual in hidden}
        self.write(os.path.join("Sample.Report", "definition", "bookmarks", name + ".bookmark.json"),
                   json.dumps({"name": name, "explorationState": {"sections": {"Overview": {"visualContainers": containers}}}}))

    def test_bookmark_that_hides_both_does_not_excuse_the_overlap(self):
        self.stacked()
        self.bookmark("HideBoth", "Overview_Card_TotalSales", "4f0c9d2a7b1e8a6c3d5f")
        self.assertFails("G002")
        self.bookmark("ShowCard", "4f0c9d2a7b1e8a6c3d5f")             # a bookmark that shows one without the other
        self.assertNot("G002")

    def test_member_of_a_group_that_is_not_there_counts_as_a_visual_of_the_page(self):
        self.edit_json(BAR, lambda d: (d.update({"parentGroupName": "nope"}), d["position"].update({"width": 5000})))
        self.assertFails("G001")

    def test_group_members_are_named_in_a_note(self):
        self.edit_json(BAR, lambda d: d.update({"parentGroupName": "Overview_Group_Header"}))
        self.assertIn("Overview_Bar_SalesByMonth", " ".join(self.messages("G008")))
        self.assertEqual(self.codes(False), [])

    def test_snap_keeps_touching_visuals_touching(self):
        self.edit_json(CARD, lambda d: (d["visual"].update({"query": self.FIELDS}), d["position"].update({"x": 30, "width": 109})))
        self.edit_json(BAR, lambda d: (d["visual"].update({"query": self.FIELDS}), d["position"].update({"x": 139, "y": 24, "width": 109, "height": 120})))
        self.assertNot("G002")
        self.assertEqual(quiet(sp.main, ["set_positions.py", self.root, "--snap"])[0], 0)
        card, bar = json.loads(self.read(CARD))["position"], json.loads(self.read(BAR))["position"]
        self.assertEqual(card["x"] + card["width"], bar["x"])
        self.assertNot("G002")
        self.assertNot("G003")

    def test_move_with_a_number_that_is_not_one_is_wrong_usage(self):
        before = self.read(CARD) + self.read(BAR)
        for bad in ("nan,24,608,120", "inf,24,608,120", "1e400,24,608,120"):
            code, _ = quiet(sp.main, ["set_positions.py", self.root, "--move", "Overview/Overview_Card_TotalSales=24,24,304,120",
                                      "--move", "Overview/4f0c9d2a7b1e8a6c3d5f=" + bad])
            self.assertEqual(code, 2)
        self.assertEqual(self.read(CARD) + self.read(BAR), before)

    def test_nothing_is_written_when_one_file_cannot_be_read_safely(self):
        self.replace(BAR, '"name": "4f0c9d2a7b1e8a6c3d5f",', '"name": "4f0c9d2a7b1e8a6c3d5f", "name": "4f0c9d2a7b1e8a6c3d5f",')
        self.edit_json(CARD, lambda d: d["position"].update({"x": 26}))
        before = self.read(CARD)
        code, out = quiet(sp.main, ["set_positions.py", self.root, "--move", "Overview/Overview_Card_TotalSales=24,24,304,120",
                                    "--move", "Overview/4f0c9d2a7b1e8a6c3d5f=24,160,1232,528"])
        self.assertEqual(code, 1, out)
        self.assertIn("cannot be read safely", out)
        self.assertEqual(self.read(CARD), before)

    def test_move_that_fits_two_visuals_is_refused(self):
        other = os.path.join("Sample.Report", "definition", "pages", "Second")
        shutil.copytree(self.path(PAGE), self.path(other))
        self.edit_json(os.path.join(other, "page.json"), lambda d: d.update({"name": "Second"}))     # same tab name, "Overview"
        before = self.read(CARD)
        code, out = quiet(sp.main, ["set_positions.py", self.root, "--move", "Overview/Overview_Card_TotalSales=24,24,304,120"])
        self.assertEqual(code, 1)
        self.assertIn("fits 2 visuals", out)
        self.assertEqual(self.read(CARD), before)
        code, out = quiet(sp.main, ["set_positions.py", self.root, "--move", "Second/Overview_Card_TotalSales=24,24,304,120"])
        self.assertEqual(code, 0, out)
        self.assertEqual(self.read(CARD), before)


class ReviewedFieldCases(Case):
    def query(self, node):
        self.edit_json(CARD, lambda d: d["visual"].update({"query": {"queryState": {"Values": {"projections": [node]}}}}))

    def test_hierarchy_level(self):
        level = {"field": {"HierarchyLevel": {"Expression": {"Hierarchy": {"Expression": {"SourceRef": {"Entity": "%s"}},
                                                                             "Hierarchy": "Calendar"}}, "Level": "Year"}}}
        self.query(json.loads(json.dumps(level) % "Nowhere"))
        self.assertIn("table 'Nowhere'", self.messages("B001")[0])
        self.query(json.loads(json.dumps(level) % "Sales"))
        self.assertIn("hierarchy 'Calendar' of table 'Sales'", self.messages("B001")[0])

    def test_alias_form_is_resolved(self):
        def filtered(entity, prop):
            return {"filter": {"From": [{"Name": "s", "Entity": entity, "Type": 0}],
                               "Where": [{"Condition": {"Column": {"Expression": {"SourceRef": {"Source": "s"}}, "Property": prop}}}]}}
        self.edit_json(CARD, lambda d: d.update({"filterConfig": {"filters": [filtered("Sales", "Channel")]}}))
        self.assertNot("B001")
        self.edit_json(CARD, lambda d: d.update({"filterConfig": {"filters": [filtered("Sales", "Region")]}}))
        self.assertIn("Sales[Region]", self.messages("B001")[0])
        self.edit_json(CARD, lambda d: d.update({"filterConfig": {"filters": [filtered("Gone", "Region")]}}))
        self.assertIn("table 'Gone'", self.messages("B001")[0])

    def test_report_that_points_to_a_missing_model_folder_fails(self):
        self.edit_json(os.path.join("Sample.Report", "definition.pbir"),
                       lambda d: d["datasetReference"]["byPath"].update({"path": "../Renamed.SemanticModel"}))
        self.assertIn("Renamed.SemanticModel", self.messages("B001")[0])


@unittest.skipUnless(shutil.which("git"), "Git is not installed")
class ReviewedFlowCases(FlowCase):
    def test_compare_refuses_a_review_that_is_not_finished(self):
        quiet(improve.start, self.root)
        self.write(os.path.join("docs", "checklist-review.md"), review_text(fails=(76,)))
        quiet(improve.snapshot, self.root)
        self.write(os.path.join("docs", "checklist-review.md"), review_text().replace("| 5 | Pass |", "| 5 | **Pass** |"))
        code, out = quiet(improve.compare, self.root)
        self.assertEqual(code, 1)
        self.assertIn("not a finished review", out)
        self.assertEqual(quiet(improve.plan, self.root)[0], 1)

    def test_pages_are_named_by_tab_when_the_project_sits_in_a_subfolder(self):
        inner = os.path.join(self.root, "report")
        os.mkdir(inner)
        for name in ("Sample.pbip", "Sample.Report", "Sample.SemanticModel"):
            shutil.move(self.path(name), os.path.join(inner, name))
        with open(os.path.join(inner, PAGE, "page.json"), encoding="utf-8") as fh:
            page = json.load(fh)
        page["displayName"] = "Sales overview"
        with open(os.path.join(inner, PAGE, "page.json"), "w", encoding="utf-8") as fh:
            json.dump(page, fh)
        self.commit("Project in a subfolder")
        self.assertEqual(quiet(improve.start, inner)[0], 0)
        self.assertTrue(os.path.isdir(os.path.join(inner, "_before", "Sample.Report")))
        self.assertEqual(self.git("status", "--porcelain"), "")
        with open(os.path.join(inner, CARD), encoding="utf-8") as fh:
            text = fh.read()
        with open(os.path.join(inner, CARD), "w", encoding="utf-8") as fh:
            fh.write(text.replace('"width": 608', '"width": 600'))
        self.commit(improve.COMMITS["Layout"])
        self.assertEqual(improve.changed_pages(inner), ["Sales overview"])


# ---------------------------------------------------------------- the template keeps its promises

class TemplateFiles(unittest.TestCase):
    def test_real_brief_has_every_label_the_checks_read(self):
        with open(os.path.join(REPO, "docs", "report-brief.md"), encoding="utf-8") as fh:
            text = fh.read()
        for label in list(cp.BRIEF_LABELS.values()) + [cp.MODEL_EXCEPTIONS, cp.LAYOUT_EXCEPTIONS]:
            self.assertIn(label, text)

    def test_empty_brief_gives_the_defaults_of_the_standards(self):
        brief = cp.read_brief(REPO)
        self.assertEqual((brief["page_size"], brief["margin"], brief["gap"], brief["grid"]), (None, None, None, 8))
        self.assertEqual(cp.PAGE_SIZE, (1280, 720))
        self.assertEqual(cp.page_numbers(brief, 1280), (24, 16))
        self.assertEqual(cp.page_numbers(brief, 1920), (32, 24))
        self.assertEqual(cp.page_numbers(brief, 1000), (None, None))
        self.assertEqual(brief["subjects"], list(cp.FOLDER_SUBJECTS))
        self.assertFalse(brief["excel"] or brief["copilot"])
        self.assertEqual(brief["model_exceptions"] | brief["layout_exceptions"], set())

    def test_template_check_fails_when_the_brief_loses_a_label(self):
        saved_root, saved_errors = ct.ROOT, list(ct.errors)
        tmp = tempfile.mkdtemp()
        try:
            ct.ROOT = tmp
            ct.errors[:] = []
            ct.check_brief()
            self.assertEqual([e[:4] for e in ct.errors], ["S008"])           # no brief at all
            os.makedirs(os.path.join(tmp, "docs"))
            with open(os.path.join(REPO, "docs", "report-brief.md"), encoding="utf-8") as fh:
                text = fh.read()
            with open(os.path.join(tmp, "docs", "report-brief.md"), "w", encoding="utf-8") as fh:
                fh.write(text)
            ct.errors[:] = []
            ct.check_brief()
            self.assertEqual(ct.errors, [])
            with open(os.path.join(tmp, "docs", "report-brief.md"), "w", encoding="utf-8") as fh:
                fh.write(text.replace("Grid step in pixels", "Grid").replace(cp.MODEL_EXCEPTIONS, "Model exceptions"))
            ct.errors[:] = []
            ct.check_brief()
            self.assertEqual(len(ct.errors), 2)
        finally:
            ct.ROOT = saved_root
            ct.errors[:] = saved_errors
            shutil.rmtree(tmp, ignore_errors=True)

    def all_codes(self):
        """{code: levels} for every finding the project check can give, read from the three check files."""
        import re
        found = {}
        for name, default in (("check_project.py", "fail"), ("model_rules.py", "fail"), ("report_rules.py", "warn")):
            with open(os.path.join(REPO, "scripts", name), encoding="utf-8") as fh:
                source = fh.read()
            for match in re.finditer(r'add\("([A-Z][0-9]{3})"', source):
                following = re.search(r'\badd\("[A-Z][0-9]{3}"', source[match.end():])
                call = source[match.end():match.end() + (following.start() if following else 900)][:900]
                level = ("note" if 'level="note"' in call or "info=True" in call else "warn" if 'level="warn"' in call
                         else "fail" if 'level="error"' in call else default)
                found.setdefault(match.group(1), set()).add(level)
        return found

    def test_every_code_is_listed_in_the_script_help_with_its_level(self):
        import re
        with open(os.path.join(REPO, "scripts", "check_project.py"), encoding="utf-8") as fh:
            source = fh.read()
        listed = dict(re.findall(r"^ {4}([A-Z][0-9]{3})  (\(warn\)|\(note\))?", source, re.M))
        codes = {c: levels for c, levels in self.all_codes().items() if c[0] not in "R"}
        self.assertEqual(sorted(set(codes) - set(listed)), [])
        for code in ("M402", "M502", "M901", "V001", "V006"):                # the new failures
            self.assertEqual((codes[code], listed[code]), ({"fail"}, ""), code)
        for code, levels in codes.items():
            if code[0] in "UVAP" or code[:2] in ("M4", "M5", "M6", "M7", "M8", "M9") or code in (
                    "M113", "M114", "M115", "M116", "M117", "M118", "M119"):
                if levels == {"warn"}:
                    self.assertEqual(listed[code], "(warn)", code)
                elif levels == {"note"}:
                    self.assertEqual(listed[code], "(note)", code)
                elif levels == {"fail"}:
                    self.assertEqual(listed[code], "", code)

    def test_every_error_and_warning_is_sorted_by_the_improve_flow(self):
        sorted_codes = set(improve.MECHANICAL) | set(improve.LAYOUT) | set(improve.PERSON)
        errors_and_warnings = {c for c, levels in self.all_codes().items()
                               if levels - {"note"} and c[0] in "MGBPVA"}
        self.assertEqual(sorted(errors_and_warnings - sorted_codes), [])
        for never in ("M001", "M005", "M006", "M007", "M107", "M108", "B001", "M118", "M119", "M502", "M802"):
            self.assertNotIn(never, improve.MECHANICAL)                       # renames, moves, types, summarisation, numbers

    def test_every_code_is_named_in_the_checklist_review_skill(self):
        import re
        with open(os.path.join(REPO, ".github", "skills", "pbi-checklist-review", "SKILL.md"), encoding="utf-8") as fh:
            text = fh.read()
        named = set(re.findall(r"\b([A-Z][0-9]{3})\b", text))
        for first, last in re.findall(r"\b([A-Z][0-9]{3})-([A-Z][0-9]{3})\b", text):
            named |= {"%s%03d" % (first[0], n) for n in range(int(first[1:]), int(last[1:]) + 1)}
        missing = sorted(c for c in self.all_codes() if c not in named and c[0] not in "RF" and c != "F001")
        self.assertEqual(missing, [])

    def test_suggestions_are_always_notes_and_never_start_the_lessons_loop(self):
        codes = self.all_codes()
        for code, levels in codes.items():
            if code.startswith("U"):
                self.assertEqual(levels, {"note"}, code)

if __name__ == "__main__":
    unittest.main()
