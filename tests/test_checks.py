"""Proves that each machine check fails on a broken example and passes on a correct one.

Run from the repository root:
    python -m unittest discover -s tests -v

The project under tests/fixtures/good is made-up test data for the scripts. It is not a report
to open in Power BI Desktop. Each test copies it to a temporary folder, breaks one thing, and
confirms that the matching check reports it.
"""
import contextlib
import io
import json
import os
import shutil
import sys
import tempfile
import unittest
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
GOOD = os.path.join(HERE, "fixtures", "good")
sys.path.insert(0, os.path.join(REPO, "scripts"))

import check_project as cp        # noqa: E402
import check_template as ct       # noqa: E402
import lessons                    # noqa: E402
import list_visuals               # noqa: E402
import set_visual_defaults        # noqa: E402

SALES = os.path.join("Sample.SemanticModel", "definition", "tables", "Sales.tmdl")
MEASURES = os.path.join("Sample.SemanticModel", "definition", "tables", "_Measures.tmdl")
EXPRESSIONS = os.path.join("Sample.SemanticModel", "definition", "expressions.tmdl")
PAGE = os.path.join("Sample.Report", "definition", "pages", "Overview")
CARD = os.path.join(PAGE, "visuals", "Overview_Card_TotalSales", "visual.json")
OLD = os.path.join(PAGE, "visuals", "4f0c9d2a7b1e8a6c3d5f", "visual.json")
REPORT = os.path.join("Sample.Report", "definition", "report.json")


def quiet(function, *args):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        code = function(*args)
    return code, out.getvalue()


class ProjectCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, "project")
        shutil.copytree(GOOD, self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def path(self, relative):
        return os.path.join(self.root, relative)

    def read(self, relative):
        with open(self.path(relative), encoding="utf-8") as fh:
            return fh.read()

    def write(self, relative, text):
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

    def codes(self):
        findings, _, _ = cp.run(self.root)
        return [f[0] for f in findings.errors()]

    def assertFails(self, code):
        self.assertIn(code, self.codes())

    def assertClean(self):
        self.assertEqual(self.codes(), [])

    def assertCleanFiles(self):
        """No error from the file checks. For tests that add an object only to try the file reader:
        the model standard and the layout standard (codes M, G and B) have their own tests in test_standards.py."""
        self.assertEqual([code for code in self.codes() if code[0] not in "MGB"], [])


class GoodProject(ProjectCase):
    def test_good_project_has_no_errors(self):
        self.assertClean()

    def test_placeholder_is_listed_but_is_not_an_error(self):
        findings, _, _ = cp.run(self.root)
        self.assertEqual([f[0] for f in findings.items], ["I001"])

    def test_command_line_exit_codes(self):
        code, out = quiet(cp.main, ["check_project.py", self.root])
        self.assertEqual(code, 0)
        self.assertNotIn("record one lesson", out)
        self.replace(SALES, "\t/// Sales channel of the order line: Web or Store.\n", "")
        code, out = quiet(cp.main, ["check_project.py", self.root])
        self.assertEqual(code, 1)
        self.assertIn("record one lesson for each code (D001)", out)       # the reminder that starts the improvement loop
        self.assertIn("scripts/lessons.py add --trigger check", out)
        empty = os.path.join(self.tmp, "empty")
        os.mkdir(empty)
        self.assertEqual(quiet(cp.main, ["check_project.py", empty])[0], 2)


class Descriptions(ProjectCase):
    def test_table_without_description_fails(self):
        self.replace(SALES, "/// One row per order line. Made-up sample rows used only by the template's tests.\n", "")
        self.assertFails("D001")

    def test_measure_without_description_fails(self):
        self.replace(MEASURES, "\t/// Total order amount in US dollars. Adds up the Amount column.\n", "")
        self.assertFails("D001")

    def test_column_without_description_fails(self):
        self.replace(SALES, "\t/// Sales channel of the order line: Web or Store.\n", "")
        self.assertFails("D001")

    def test_hidden_column_needs_no_description(self):
        self.assertIn("column OrderId\n\t\tdataType: int64\n\t\tisHidden", self.read(SALES))
        self.assertClean()

    def test_unhiding_an_undescribed_column_fails(self):
        self.replace(SALES, "\t\tisHidden\n", "")
        self.assertFails("D001")

    def test_hidden_table_needs_no_descriptions(self):
        text = self.read(SALES).replace("\t/// Sales channel of the order line: Web or Store.\n", "")
        self.write(SALES, text.replace("table Sales\n", "table Sales\n\tisHidden\n", 1))
        self.assertClean()

    def test_blank_line_between_description_and_object_fails(self):
        self.replace(SALES, "\t/// Sales channel of the order line: Web or Store.\n",
                     "\t/// Sales channel of the order line: Web or Store.\n\n")
        codes = self.codes()
        self.assertIn("D003", codes)
        self.assertIn("D001", codes)

    def test_shared_query_without_description_fails(self):
        self.replace(EXPRESSIONS, "/// Smallest order amount kept by the Sales query. Made-up value for the tests.\n", "")
        self.assertFails("D002")


class Comments(ProjectCase):
    def test_comment_line_outside_expression_fails(self):
        self.replace(SALES, "\tcolumn Amount\n", "\tcolumn Amount\n\t\t// amount of the order\n")
        self.assertFails("C001")

    def test_comment_after_a_property_fails(self):
        self.replace(SALES, "\t\tisHidden\n", "\t\tisHidden // not for report authors\n")
        self.assertFails("C001")

    def test_comment_at_top_of_file_fails(self):
        self.write(SALES, "// sales table\n" + self.read(SALES))
        self.assertFails("C001")

    def test_comments_inside_m_and_dax_are_allowed(self):
        text = self.read(SALES) + self.read(MEASURES)
        self.assertIn("// Count the returned lines", text)         # inside a multi-line DAX block
        self.assertIn("// one-line DAX comment", text)            # after a one-line DAX expression
        self.assertIn("// Build a small in-line table", text)     # inside a Power Query block
        self.assertIn('"http://example.com/help"', text)          # '//' inside a text value
        self.assertIn("https://example.com/made-up-data", text)   # '//' inside an annotation value
        self.assertClean()

    def test_comment_inside_backtick_block_is_allowed(self):
        self.replace(MEASURES, "\tmeasure 'Help Link' = \"http://example.com/help\"\n",
                     "\tmeasure 'Help Link' = ```\n\t\t\t// plain text link\n\t\t\t\"http://example.com/help\"\n\t\t\t```\n")
        self.assertClean()


class PowerQuerySteps(ProjectCase):
    def test_step_without_description_line_fails(self):
        self.replace(SALES, "\t\t\t\t    // Build a small in-line table so the sample needs no outside data source.\n", "")
        self.assertFails("P001")

    def test_block_comment_counts_as_a_step_description(self):
        self.assertIn("/* Keep only order lines", self.read(SALES))
        self.assertClean()

    def test_second_step_without_description_fails(self):
        self.replace(SALES, "\t\t\t\t    /* Keep only order lines at or above the MinimumAmount parameter. */\n", "")
        self.assertFails("P001")


class JsonAndSchema(ProjectCase):
    def test_broken_json_fails(self):
        self.write(CARD, self.read(CARD)[:-5])
        self.assertFails("J001")

    def test_byte_order_mark_fails(self):
        with open(self.path(CARD), "rb") as fh:
            raw = fh.read()
        with open(self.path(CARD), "wb") as fh:
            fh.write(b"\xef\xbb\xbf" + raw)
        self.assertFails("J001")

    def test_missing_schema_fails(self):
        self.edit_json(CARD, lambda d: d.pop("$schema"))
        self.assertFails("S001")

    def test_foreign_schema_address_fails(self):
        self.edit_json(os.path.join(PAGE, "page.json"), lambda d: d.update({"$schema": "https://example.com/page.json"}))
        self.assertFails("S001")


class Names(ProjectCase):
    def test_page_folder_with_space_fails(self):
        os.rename(self.path(PAGE), self.path(os.path.join("Sample.Report", "definition", "pages", "Over view")))
        self.assertFails("N001")

    def test_page_name_with_bad_character_fails(self):
        self.edit_json(os.path.join(PAGE, "page.json"), lambda d: d.update({"name": "Over.view"}))
        self.assertFails("N001")

    def test_visual_name_over_50_characters_fails(self):
        self.edit_json(CARD, lambda d: d.update({"name": "Overview_Card_" + "A" * 40}))
        self.assertFails("N002")

    def test_visual_folder_with_bad_character_fails(self):
        folder = os.path.dirname(self.path(CARD))
        os.rename(folder, folder + ".Visual")
        self.assertFails("N002")

    def test_existing_visual_without_label_fails(self):
        self.edit_json(OLD, lambda d: d.pop("annotations"))
        self.assertFails("N003")

    def test_existing_visual_with_label_passes(self):
        self.assertIn("VisualLabel", self.read(OLD))
        self.assertClean()

    def test_label_that_does_not_start_with_the_page_fails(self):
        self.edit_json(OLD, lambda d: d.update({"annotations": [{"name": "VisualLabel", "value": "Sales_Bar_ByMonth"}]}))
        self.assertFails("N003")

    def test_label_with_only_two_parts_fails(self):
        self.edit_json(OLD, lambda d: d.update({"annotations": [{"name": "VisualLabel", "value": "Overview_Bar"}]}))
        self.assertFails("N003")

    def test_label_may_use_the_tab_name_when_the_page_name_is_an_identifier(self):
        self.edit_json(os.path.join(PAGE, "page.json"),
                       lambda d: d.update({"name": "0f9e8d7c6b5a4f3e2d1c", "displayName": "Sales Detail"}))
        for path in (CARD, OLD, os.path.join(PAGE, "visuals", "Overview_Group_Header", "visual.json")):
            self.edit_json(path, lambda d: d.update(
                {"annotations": [{"name": "VisualLabel", "value": "SalesDetail_Chart_Example"}]}))
        self.assertNotIn("N003", self.codes())

    def test_named_visual_in_differently_named_folder_fails(self):
        folder = os.path.dirname(self.path(CARD))
        os.rename(folder, os.path.join(os.path.dirname(folder), "Overview_Card_Other"))
        self.assertFails("N004")

    def test_duplicate_visual_names_fail(self):
        self.edit_json(OLD, lambda d: d.update({"name": "Overview_Card_TotalSales"}))
        self.assertFails("N005")


class HeaderIconsAndTooltips(ProjectCase):
    def test_header_setting_missing_fails(self):
        self.edit_json(CARD, lambda d: d["visual"]["visualContainerObjects"].pop("visualHeader"))
        self.assertEqual(self.codes(), ["H001"])

    def test_tooltip_setting_missing_fails(self):
        self.edit_json(CARD, lambda d: d["visual"]["visualContainerObjects"].pop("visualTooltip"))
        self.assertEqual(self.codes(), ["H002"])

    def test_no_container_settings_at_all_fails_both(self):
        self.edit_json(CARD, lambda d: d["visual"].pop("visualContainerObjects"))
        self.assertEqual(sorted(self.codes()), ["H001", "H002"])

    def test_header_on_fails(self):
        def turn_on(d):
            d["visual"]["visualContainerObjects"]["visualHeader"][0]["properties"]["show"]["expr"]["Literal"]["Value"] = "true"
        self.edit_json(CARD, turn_on)
        self.assertEqual(self.codes(), ["H001"])

    def test_tooltip_on_fails(self):
        def turn_on(d):
            d["visual"]["visualContainerObjects"]["visualTooltip"][0]["properties"]["show"]["expr"]["Literal"]["Value"] = "true"
        self.edit_json(CARD, turn_on)
        self.assertEqual(self.codes(), ["H002"])

    def test_plain_false_instead_of_the_expression_form_fails(self):
        def plain(d):
            d["visual"]["visualContainerObjects"]["visualHeader"][0]["properties"]["show"] = False
        self.edit_json(CARD, plain)
        self.assertEqual(self.codes(), ["H001"])

    def test_documented_exception_passes(self):
        def excuse(d):
            d["visual"].pop("visualContainerObjects")
            d["annotations"] = [{"name": "HeaderTooltipException", "value": "both: drill buttons and hover detail needed on this chart"}]
        self.edit_json(CARD, excuse)
        self.assertClean()

    def test_exception_covers_only_what_it_names(self):
        def excuse(d):
            d["visual"].pop("visualContainerObjects")
            d["annotations"] = [{"name": "HeaderTooltipException", "value": "tooltip: hover detail asked for by the owner"}]
        self.edit_json(CARD, excuse)
        self.assertEqual(self.codes(), ["H001"])          # header icons are still required to be off

    def test_exception_that_does_not_say_what_stays_on_fails(self):
        def excuse(d):
            d["visual"].pop("visualContainerObjects")
            d["annotations"] = [{"name": "HeaderTooltipException", "value": "needed on this chart"}]
        self.edit_json(CARD, excuse)
        self.assertEqual(sorted(self.codes()), ["H001", "H001", "H002"])     # one more H001 for the annotation itself

    def test_badly_formed_exception_is_reported_even_when_settings_are_off(self):
        self.edit_json(CARD, lambda d: d.update({"annotations": [{"name": "HeaderTooltipException", "value": "Header - wanted"}]}))
        self.assertEqual(self.codes(), ["H001"])
        code, out = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        self.assertIn("note", out)

    def test_exception_without_a_reason_fails(self):
        def excuse(d):
            d["visual"].pop("visualContainerObjects")
            d["annotations"] = [{"name": "HeaderTooltipException", "value": "both:   "}]
        self.edit_json(CARD, excuse)
        self.assertEqual(sorted(self.codes()), ["H001", "H001", "H002"])

    def test_groups_are_not_checked(self):
        group = os.path.join(PAGE, "visuals", "Overview_Group_Header", "visual.json")
        self.assertNotIn("visualContainerObjects", self.read(group))
        self.assertClean()


class Theme(ProjectCase):
    def test_no_registered_theme_fails(self):
        self.edit_json(REPORT, lambda d: d["themeCollection"].pop("customTheme"))
        self.assertFails("T001")

    def test_registered_theme_file_missing_fails(self):
        os.remove(self.path(os.path.join("Sample.Report", "StaticResources", "RegisteredResources", "fixture-theme.json")))
        self.assertFails("T001")


class SetVisualDefaults(ProjectCase):
    def test_sets_both_off_and_leaves_exceptions_alone(self):
        self.edit_json(CARD, lambda d: d["visual"].pop("visualContainerObjects"))

        def excuse(d):
            d["visual"]["visualContainerObjects"]["visualHeader"][0]["properties"]["show"]["expr"]["Literal"]["Value"] = "true"
            d["annotations"].append({"name": "HeaderTooltipException", "value": "header: needs the drill buttons"})
        self.edit_json(OLD, excuse)
        before_exception = self.read(OLD)
        self.assertEqual(self.codes(), ["H001", "H002"])

        code, out = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root, "--dry-run"])
        self.assertEqual(code, 0)
        self.assertIn("would change", out)
        self.assertEqual(self.codes(), ["H001", "H002"])            # dry run changed nothing

        code, _ = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        self.assertEqual(code, 0)
        self.assertClean()
        self.assertEqual(self.read(OLD), before_exception)          # documented exception untouched
        card = json.loads(self.read(CARD))
        self.assertEqual(card["name"], "Overview_Card_TotalSales")  # nothing renamed
        self.assertEqual(card["visual"]["visualContainerObjects"]["visualHeader"][0]["properties"]["show"],
                         {"expr": {"Literal": {"Value": "false"}}})

    def test_turns_an_on_setting_off(self):
        def turn_on(d):
            d["visual"]["visualContainerObjects"]["visualTooltip"][0]["properties"]["show"]["expr"]["Literal"]["Value"] = "true"
        self.edit_json(CARD, turn_on)
        self.assertEqual(self.codes(), ["H002"])
        quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        self.assertClean()

    def test_adds_a_label_without_renaming(self):
        self.edit_json(OLD, lambda d: d.pop("annotations"))
        self.assertEqual(self.codes(), ["N003"])
        code, _ = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root,
                                                   "--label", "Overview/4f0c9d2a7b1e8a6c3d5f=Overview_Bar_SalesByMonth"])
        self.assertEqual(code, 0)
        self.assertClean()
        self.assertEqual(json.loads(self.read(OLD))["name"], "4f0c9d2a7b1e8a6c3d5f")

    def test_rejects_a_label_that_breaks_the_pattern(self):
        code, _ = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root,
                                                   "--label", "Overview/4f0c9d2a7b1e8a6c3d5f=bad label"])
        self.assertEqual(code, 1)

    def test_keeps_windows_line_endings(self):
        raw = self.read(CARD).replace("\n", "\r\n")
        with open(self.path(CARD), "wb") as fh:
            fh.write(raw.encode("utf-8"))
        self.edit_json  # (not used: keep the CRLF bytes written above)
        data = json.loads(raw)
        data["visual"].pop("visualContainerObjects")
        with open(self.path(CARD), "wb") as fh:
            fh.write(json.dumps(data, indent=2).replace("\n", "\r\n").encode("utf-8"))
        quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        with open(self.path(CARD), "rb") as fh:
            written = fh.read()
        self.assertIn(b"\r\n", written)
        self.assertNotIn(b"\xef\xbb\xbf", written)
        self.assertClean()


class ListVisuals(ProjectCase):
    def test_lists_label_type_and_position(self):
        code, out = quiet(list_visuals.main, ["list_visuals.py", self.root, "--page", "Overview"])
        self.assertEqual(code, 0)
        lines = [" ".join(line.split()) for line in out.splitlines()]
        self.assertIn("label type x y width height folder", lines)
        self.assertIn("Overview_Card_TotalSales cardVisual 24 24 608 120 Overview_Card_TotalSales", lines)
        self.assertIn("Overview_Bar_SalesByMonth barChart 24 160 1232 536 4f0c9d2a7b1e8a6c3d5f", lines)   # label from the annotation
        self.assertIn("Overview_Group_Header group 0 0 1280 20 Overview_Group_Header", lines)

    def test_page_can_be_chosen_by_tab_name_or_folder(self):
        self.edit_json(os.path.join(PAGE, "page.json"), lambda d: d.update({"displayName": "Sales overview"}))
        for wanted in ("Overview", "Sales overview"):
            self.assertEqual(quiet(list_visuals.main, ["list_visuals.py", self.root, "--page", wanted])[0], 0)

    def test_odd_values_do_not_crash(self):
        self.edit_json(os.path.join(PAGE, "page.json"), lambda d: d.update({"displayName": {}, "width": 10 ** 400}))
        self.edit_json(CARD, lambda d: d["position"].update({"x": 10 ** 400}))
        code, out = quiet(list_visuals.main, ["list_visuals.py", self.root])
        self.assertEqual(code, 0)
        quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root, "--dry-run"])

    def test_unknown_page_is_reported(self):
        code, _ = quiet(list_visuals.main, ["list_visuals.py", self.root, "--page", "Nowhere"])
        self.assertEqual(code, 2)


class ReviewTable(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.file = os.path.join(self.tmp, "review.md")

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write(self, rows):
        with open(self.file, "w", encoding="utf-8") as fh:
            fh.write("| Item | Status | Evidence |\n|---|---|---|\n")
            for row in rows:
                fh.write("| %s | %s | %s |\n" % row)

    def codes(self):
        findings = cp.Findings()
        cp.check_review(self.file, findings)
        return [f[0] for f in findings.errors()]

    def good_rows(self):
        return [(n, "Pass", "seen in Sales.tmdl") for n in range(1, 80)]

    def test_complete_review_passes(self):
        rows = self.good_rows()
        rows[1] = (2, "Fail", "local file path in the Sales query")
        rows[38] = (39, "Not applicable", "Mark N/A when: no row filtering is required (brief, section 3)")
        self.write(rows)
        self.assertEqual(self.codes(), [])
        self.assertEqual(quiet(cp.main, ["check_project.py", "--review", self.file])[0], 0)

    def test_missing_item_fails(self):
        rows = self.good_rows()
        del rows[40]
        self.write(rows)
        self.assertEqual(self.codes(), ["R003"])
        self.assertEqual(quiet(cp.main, ["check_project.py", "--review", self.file])[0], 1)

    def test_other_status_word_fails(self):
        rows = self.good_rows()
        rows[4] = (5, "Partly", "some columns")
        self.write(rows)
        self.assertEqual(self.codes(), ["R004"])

    def test_empty_evidence_fails(self):
        rows = self.good_rows()
        rows[9] = (10, "Pass", "")
        self.write(rows)
        self.assertEqual(self.codes(), ["R005"])

    def test_item_listed_twice_fails(self):
        rows = self.good_rows() + [(7, "Fail", "again")]
        self.write(rows)
        self.assertIn("R002", self.codes())


def checklist_markdown(topics):
    parts = ["# Test checklist\n"]
    for n, topic in enumerate(topics, 1):
        parts.append("## Item %d\n\n- Area: Model\n- Category: Cat %d\n"
                     "- Microsoft documentation: [Microsoft Learn](https://example.com/%d)\n- Topic:\n\n~~~text\n%s\n~~~\n"
                     % (n, n, n, topic))
    return "\n".join(parts)


def write_xlsx(path, topics):
    """A minimal spreadsheet with the same layout as the owner's: one sheet, four columns, links in column D."""
    def cell(ref, text):
        text = text.replace("&", "&amp;").replace("<", "&lt;")
        return '<c r="%s" t="inlineStr"><is><t xml:space="preserve">%s</t></is></c>' % (ref, text)
    rows = ['<row r="1">%s</row>' % "".join(cell(c + "1", h) for c, h in zip("ABCD", ct.HEADER))]
    links, rels = [], []
    for n, topic in enumerate(topics, 1):
        r = n + 1
        rows.append('<row r="%d">%s</row>' % (r, cell("A%d" % r, "Model") + cell("B%d" % r, "Cat %d" % n)
                                              + cell("C%d" % r, topic) + cell("D%d" % r, "Microsoft Learn")))
        links.append('<hyperlink ref="D%d" r:id="rId%d"/>' % (r, n))
        rels.append('<Relationship Id="rId%d" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/hyperlink" '
                    'Target="https://example.com/%d" TargetMode="External"/>' % (n, n))
    main = "http://schemas.openxmlformats.org/spreadsheetml/2006/main"
    rel = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
    pkg = "http://schemas.openxmlformats.org/package/2006/relationships"
    with zipfile.ZipFile(path, "w") as z:
        z.writestr("xl/workbook.xml", '<workbook xmlns="%s" xmlns:r="%s"><sheets><sheet name="Checklist Review" sheetId="1" r:id="rId1"/></sheets></workbook>' % (main, rel))
        z.writestr("xl/_rels/workbook.xml.rels", '<Relationships xmlns="%s"><Relationship Id="rId1" Type="x" Target="worksheets/sheet1.xml"/></Relationships>' % pkg)
        z.writestr("xl/worksheets/sheet1.xml", '<worksheet xmlns="%s" xmlns:r="%s"><sheetData>%s</sheetData><hyperlinks>%s</hyperlinks></worksheet>' % (main, rel, "".join(rows), "".join(links)))
        z.writestr("xl/worksheets/_rels/sheet1.xml.rels", '<Relationships xmlns="%s">%s</Relationships>' % (pkg, "".join(rels)))


class TemplateCase(unittest.TestCase):
    """Runs check_template against a small made-up repository in a temporary folder."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.saved = (ct.ROOT, ct.CHECKLIST_MD_SHA256, ct.THEME_SHA256, ct.XLSX_SHA256)
        ct.ROOT = self.tmp
        ct.errors[:] = []
        ct.notes[:] = []
        self.topics = ["Assess item %d.\n• When applicable: always\n• Guidance: read it" % n for n in range(1, 80)]
        self.put("checklist/checklist.md", checklist_markdown(self.topics))
        self.put("theme/theme.json", '{\n  "name": "T"\n}\n')
        self.xlsx = os.path.join(self.tmp, "..", os.path.basename(self.tmp) + ".xlsx")
        write_xlsx(self.xlsx, self.topics)
        ct.CHECKLIST_MD_SHA256 = ct.sha256(os.path.join(self.tmp, "checklist", "checklist.md"))
        ct.THEME_SHA256 = ct.sha256(os.path.join(self.tmp, "theme", "theme.json"))
        ct.XLSX_SHA256 = ct.sha256(self.xlsx)

    def tearDown(self):
        ct.ROOT, ct.CHECKLIST_MD_SHA256, ct.THEME_SHA256, ct.XLSX_SHA256 = self.saved
        ct.errors[:] = []
        ct.notes[:] = []
        shutil.rmtree(self.tmp, ignore_errors=True)
        if os.path.exists(self.xlsx):
            os.remove(self.xlsx)

    def put(self, relative, text):
        path = os.path.join(self.tmp, relative)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    def codes(self, function, *args):
        ct.errors[:] = []
        function(*args)
        return [line.split()[0] for line in ct.errors]


class ChecklistAgainstSpreadsheet(TemplateCase):
    def test_identical_checklist_passes(self):
        self.assertEqual(self.codes(ct.check_checklist, self.xlsx), [])
        self.assertTrue(any("match the spreadsheet word for word" in n for n in ct.notes))

    def test_one_changed_word_fails(self):
        changed = list(self.topics)
        changed[22] = changed[22].replace("always", "sometimes")
        self.put("checklist/checklist.md", checklist_markdown(changed))
        codes = self.codes(ct.check_checklist, self.xlsx)
        self.assertIn("K008", codes)      # differs from the spreadsheet
        self.assertIn("K004", codes)      # and the file hash changed
        self.assertEqual(codes.count("K008"), 1)

    def test_dropped_item_fails(self):
        self.put("checklist/checklist.md", checklist_markdown(self.topics[:-1]))
        self.assertIn("K002", self.codes(ct.check_checklist, None))

    def test_reordered_items_fail(self):
        swapped = list(self.topics)
        swapped[0], swapped[1] = swapped[1], swapped[0]
        self.put("checklist/checklist.md", checklist_markdown(swapped))
        self.assertEqual(self.codes(ct.check_checklist, self.xlsx).count("K008"), 2)

    def test_changed_link_fails(self):
        text = checklist_markdown(self.topics).replace("https://example.com/5)", "https://example.com/five)")
        self.put("checklist/checklist.md", text)
        self.assertIn("K008", self.codes(ct.check_checklist, self.xlsx))

    def test_edit_is_caught_without_the_spreadsheet(self):
        self.put("checklist/checklist.md", checklist_markdown(self.topics).replace("Assess item 7.", "Check item 7."))
        self.assertEqual(self.codes(ct.check_checklist, None), ["K004"])


class RealChecklistFile(unittest.TestCase):
    def test_real_checklist_has_79_items_in_order(self):
        items = ct.parse_checklist_md(os.path.join(REPO, "checklist", "checklist.md"))
        self.assertEqual([i["n"] for i in items], list(range(1, 80)))
        self.assertTrue(all(i["labels"] == ct.HEADER for i in items))


class ThemeIntegrity(TemplateCase):
    def test_unchanged_theme_passes(self):
        self.assertEqual(self.codes(ct.check_theme), [])

    def test_changed_theme_fails(self):
        self.put("theme/theme.json", '{\n  "name": "T2"\n}\n')
        self.assertEqual(self.codes(ct.check_theme), ["T102"])

    def test_registered_copy_with_other_content_fails(self):
        shutil.copytree(os.path.join(GOOD, "Sample.Report"), os.path.join(self.tmp, "Starter.Report"))
        self.assertEqual(self.codes(ct.check_theme), ["T105"])

    def test_registered_copy_with_same_content_passes(self):
        shutil.copytree(os.path.join(GOOD, "Sample.Report"), os.path.join(self.tmp, "Starter.Report"))
        self.put("Starter.Report/StaticResources/RegisteredResources/fixture-theme.json", '{"name":"T"}')
        self.assertEqual(self.codes(ct.check_theme), [])
        self.assertTrue(any("same JSON values, different bytes" in n for n in ct.notes))


SKILL = "---\nname: %s\ndescription: Use this skill when testing.\n---\n# Test\n\nChecklist items: 1-78\n"


class GuidanceFiles(TemplateCase):
    def good(self):
        self.put(".github/copilot-instructions.md", "Rules.\n\nChecklist items: 79\n")
        self.put(".github/skills/demo-skill/SKILL.md", SKILL % "demo-skill")
        self.put(".github/skills/pbi-checklist-review/SKILL.md",
                 (SKILL % "pbi-checklist-review").replace("1-78", "1-79"))
        rows = "".join("| %d |  |  |\n" % n for n in range(1, 80))
        self.put(".github/skills/pbi-checklist-review/references/review-template.md", "| Item | Status | Evidence |\n|---|---|---|\n" + rows)

    def all_codes(self):
        return self.codes(ct.check_guidance) + self.codes(ct.check_links) + self.codes(ct.check_citations)

    def test_good_guidance_passes(self):
        self.good()
        self.assertEqual(self.all_codes(), [])

    def test_skill_name_must_match_folder(self):
        self.good()
        self.put(".github/skills/demo-skill/SKILL.md", SKILL % "Demo_Skill")
        self.assertIn("S003", self.all_codes())

    def test_missing_description_fails(self):
        self.good()
        self.put(".github/skills/demo-skill/SKILL.md", (SKILL % "demo-skill").replace("description: Use this skill when testing.\n", ""))
        self.assertIn("S004", self.all_codes())

    def test_model_field_fails(self):
        self.good()
        self.put(".github/skills/demo-skill/SKILL.md", (SKILL % "demo-skill").replace("---\n# Test", "model: any-model\n---\n# Test"))
        self.assertIn("S002", self.all_codes())

    def test_naming_an_ai_model_fails(self):
        self.good()
        self.put(".github/copilot-instructions.md", "Use %s for this.\n\nChecklist items: 79\n" % "-".join(["GPT", "4"]))
        self.assertIn("S006", self.all_codes())

    def test_calling_an_excluded_tool_fails(self):
        self.good()
        self.put(".github/copilot-instructions.md", "Run `%s validate` first.\n\nChecklist items: 79\n" % "".join(["pb", "ir"]))
        self.assertIn("S007", self.all_codes())

    def test_oversized_always_loaded_file_fails(self):
        self.good()
        self.put(".github/copilot-instructions.md", "line\n" * 60 + "Checklist items: 79\n")
        self.assertIn("S001", self.all_codes())

    def test_missing_path_fails(self):
        self.good()
        self.put(".github/copilot-instructions.md", "Run `scripts/not_there.py`.\n\nChecklist items: 79\n")
        self.assertIn("L002", self.all_codes())

    def test_broken_link_fails(self):
        self.good()
        self.put(".github/copilot-instructions.md", "See [the brief](../docs/missing.md).\n\nChecklist items: 79\n")
        self.assertIn("L001", self.all_codes())

    def test_file_without_checklist_items_fails(self):
        self.good()
        self.put(".github/skills/demo-skill/SKILL.md", (SKILL % "demo-skill").replace("Checklist items: 1-78\n", ""))
        codes = self.all_codes()
        self.assertIn("C002", codes)
        self.assertIn("C003", codes)      # items 1-78 are now applied nowhere

    def test_item_number_out_of_range_fails(self):
        self.good()
        self.put(".github/copilot-instructions.md", "Rules.\n\nChecklist items: 79, 80\n")
        self.assertIn("C001", self.all_codes())

    def test_review_template_missing_a_row_fails(self):
        self.good()
        rows = "".join("| %d |  |  |\n" % n for n in range(1, 79))
        self.put(".github/skills/pbi-checklist-review/references/review-template.md", rows)
        self.assertIn("C005", self.all_codes())

    def test_missing_path_inside_a_command_fails(self):
        self.good()
        self.put("docs/how.md", "Run this:\n\n```bash\npython scripts/not_there.py .\n```\n")
        self.assertIn("L002", self.all_codes())
        for command in ("python scripts/not_there.py .", "python ./scripts/not_there.py .",
                        "python scripts\\not_there.py .", "python not_there.py .",
                        "python -m unittest discover -s nowhere -v"):
            self.put("docs/how.md", "Run `%s` now.\n" % command)
            self.assertIn("L002", self.all_codes(), command)
        self.put("docs/how.md", "Run `python -m unittest discover -s docs -v` now.\n")
        self.assertEqual(self.all_codes(), [])

    def test_link_with_escaped_space_resolves(self):
        self.good()
        self.put("docs/my guide.md", "Guide.\n")
        self.put("docs/how.md", "See [the guide](my%20guide.md).\n")
        self.assertEqual(self.all_codes(), [])


class ThemeFileDamage(TemplateCase):
    def test_theme_that_is_not_json_is_reported_not_crashed(self):
        self.put("theme/theme.json", '{\n  "name": "T"\n]\n')
        self.assertEqual(self.codes(ct.check_theme), ["T102"])
        self.assertFalse(any("matches the owner" in n for n in ct.notes))

    def test_changed_theme_prints_no_matching_note(self):
        self.put("theme/theme.json", '{\n  "name": "T2"\n}\n')
        self.codes(ct.check_theme)
        self.assertFalse(any("matches the owner" in n for n in ct.notes))


class OlderFormats(ProjectCase):
    def test_report_without_definition_folder_fails(self):
        shutil.rmtree(self.path(os.path.join("Sample.Report", "definition")))
        self.write(os.path.join("Sample.Report", "report.json"), "{}")
        self.assertFails("F001")
        self.assertEqual(quiet(cp.main, ["check_project.py", self.root])[0], 1)

    def test_model_without_definition_folder_fails(self):
        shutil.rmtree(self.path(os.path.join("Sample.SemanticModel", "definition")))
        self.write(os.path.join("Sample.SemanticModel", "model.bim"), "{}")
        self.assertFails("F001")

    def test_page_folder_without_page_json_fails(self):
        os.remove(self.path(os.path.join(PAGE, "page.json")))
        self.assertFails("F002")


class TmdlEdgeCases(ProjectCase):
    def test_comment_holding_an_equals_sign_after_a_property_fails(self):
        self.replace(SALES, "\t\tsummarizeBy: sum\n", "\t\tsummarizeBy: sum // key = no sum\n")
        self.assertFails("C001")

    def test_comment_after_an_object_line_fails_and_object_is_still_checked(self):
        self.replace(SALES, "\tannotation SampleSource", "\tcolumn Region // region = sales area\n\t\tdataType: string\n\n\tannotation SampleSource")
        codes = self.codes()
        self.assertIn("C001", codes)
        self.assertIn("D001", codes)

    def test_comment_after_the_table_line_fails(self):
        self.replace(SALES, "table Sales\n", "table Sales // grain = order line\n")
        self.assertFails("C001")

    def test_comment_without_a_space_before_it_fails(self):
        self.replace(SALES, "\t\tdataType: decimal\n", "\t\tdataType: decimal//money\n")
        self.assertFails("C001")

    def test_quoted_name_with_equals_sign_keeps_its_expression_block(self):
        self.replace(SALES, "\tannotation SampleSource",
                     "\t/// Sales where the returned flag is set.\n"
                     "\tmeasure 'Sales (Returned = Yes)' =\n"
                     "\t\t\t// only returned lines\n"
                     "\t\t\tCALCULATE(SUM(Sales[Amount]), Sales[Returned] = TRUE())\n"
                     "\t\tformatString: #,0\n\n\tannotation SampleSource")
        self.assertCleanFiles()

    def test_name_and_source_column_holding_two_slashes_are_not_comments(self):
        self.replace(SALES, "\tannotation SampleSource",
                     "\t/// Latitude and longitude as text.\n\tcolumn 'Lat // Long'\n\t\tdataType: string\n"
                     "\t\tsourceColumn: Lat // Long\n\n\tannotation SampleSource")
        self.assertClean()

    def test_empty_description_line_does_not_count(self):
        self.replace(SALES, "\t/// Sales channel of the order line: Web or Store.\n", "\t///\n")
        self.assertFails("D001")
        self.write(SALES, self.read(SALES).replace("\t///\n", "\t///   \n"))
        self.assertFails("D001")

    def test_description_above_a_property_fails(self):
        self.replace(SALES, "\t\tdataType: decimal\n", "\t\t/// the type\n\t\tdataType: decimal\n")
        self.assertFails("D003")

    def test_unquoted_two_word_name_is_still_checked(self):
        self.replace(SALES, "\tannotation SampleSource", "\tmeasure Order Count = COUNTROWS(Sales)\n\n\tannotation SampleSource")
        self.assertFails("D001")

    def test_function_query_steps_are_checked(self):
        self.write(EXPRESSIONS, self.read(EXPRESSIONS)
                   + "\n/// Trims and upper-cases a text value.\nexpression fnClean =\n"
                     "\t\t(t as text) as text =>\n\t\tlet\n\t\t    Trimmed = Text.Trim(t),\n"
                     "\t\t    Upper = Text.Upper(Trimmed)\n\t\tin\n\t\t    Upper\n")
        self.assertEqual(self.codes(), ["P001", "P001"])

    def test_query_that_starts_with_a_block_comment_is_checked(self):
        self.write(EXPRESSIONS, self.read(EXPRESSIONS)
                   + "\n/// Staging rows.\nexpression Staging =\n\t\t/* staging query */\n\t\tlet\n"
                     "\t\t    Source = #table({\"A\"}, {{1}})\n\t\tin\n\t\t    Source\n")
        self.assertEqual(self.codes(), ["P001"])

    def test_blank_line_between_step_description_and_step_fails(self):
        self.replace(SALES, "needs no outside data source.\n", "needs no outside data source.\n\n")
        self.assertFails("P001")

    def test_file_indented_with_spaces_keeps_its_expression_block(self):
        self.write(EXPRESSIONS, "/// Staging rows.\nexpression Staging =\n"
                                "        let\n            // Build one row.\n            Source = #table({\"A\"}, {{1}})\n"
                                "        in\n            Source\n")
        self.assertClean()

    def test_realistic_desktop_style_files_pass(self):
        base = os.path.join("Sample.SemanticModel", "definition")
        self.write(os.path.join(base, "relationships.tmdl"),
                   "relationship 3f6a2b10-aaaa-bbbb-cccc-000000000001\n\tfromColumn: Sales.OrderId\n\ttoColumn: Orders.OrderId\n")
        self.write(os.path.join(base, "roles.tmdl"),
                   "role 'Region Readers'\n\tmodelPermission: read\n\n\ttablePermission Sales = Sales[Amount] > 0 // DAX filter\n")
        self.write(os.path.join(base, "cultures.tmdl"),
                   "cultureInfo en-US\n\n\tlinguisticMetadata =\n\t\t\t{\n\t\t\t  \"Version\": \"1.0.0\",\n"
                   "\t\t\t  \"Help\": \"http://example.com//x\"\n\t\t\t}\n\t\tcontentType: json\n")
        self.replace(SALES, "\tannotation SampleSource",
                     "\t/// Amount with tax. Calculated column.\n\tcolumn 'Amount With Tax' = Sales[Amount] * 1.1 // flat rate\n"
                     "\t\tdataType: decimal\n\t\tformatString: #,0.00\n\n"
                     "\t/// Dynamic format example.\n\tmeasure 'Sales Dynamic' = SUM(Sales[Amount])\n"
                     "\t\tformatStringDefinition =\n\t\t\t\t// pick a format by size\n\t\t\t\tIF([Total Sales] > 1000, \"#,0\", \"0.00\")\n\n"
                     "\tannotation PBI_Example = {\"url\": \"https://example.com//a\"}\n\n\tannotation SampleSource")
        self.assertCleanFiles()


class JsonEdgeCases(ProjectCase):
    def test_broken_definition_pbir_fails(self):
        path = os.path.join("Sample.Report", "definition.pbir")
        self.write(path, self.read(path)[:-6])
        self.assertFails("J001")

    def test_byte_order_mark_on_definition_pbism_fails(self):
        path = self.path(os.path.join("Sample.SemanticModel", "definition.pbism"))
        with open(path, "rb") as fh:
            raw = fh.read()
        with open(path, "wb") as fh:
            fh.write(b"\xef\xbb\xbf" + raw)
        self.assertFails("J001")

    def test_broken_bookmark_and_mobile_files_fail(self):
        os.mkdir(self.path(os.path.join("Sample.Report", "definition", "bookmarks")))
        self.write(os.path.join("Sample.Report", "definition", "bookmarks", "b1.bookmark.json"), "{ not json")
        self.assertEqual(self.codes(), ["J001"])
        self.write(os.path.join("Sample.Report", "definition", "bookmarks", "b1.bookmark.json"), "{}")
        self.write(os.path.join(os.path.dirname(CARD), "mobile.json"), "{ not json")
        self.assertEqual(self.codes(), ["J001"])

    def test_nan_is_not_json(self):
        self.replace(CARD, '"x": 24', '"x": NaN')
        self.assertFails("J001")

    def test_wrongly_shaped_files_are_reported_without_a_crash(self):
        cases = [
            (CARD, lambda d: d.update({"visual": "card"})),
            (CARD, lambda d: d["visual"]["visualContainerObjects"]["visualHeader"][0].update({"properties": "show=false"})),
            (CARD, lambda d: d.update({"annotations": 5})),
            (CARD, lambda d: (d.pop("visual"), None)[1]),
            (CARD, lambda d: d.update({"position": "24,24"})),
            (REPORT, lambda d: d["themeCollection"].update({"customTheme": "fixture-theme.json"})),
        ]
        for relative, change in cases:
            original = self.read(relative)
            self.edit_json(relative, change)
            code, out = quiet(cp.main, ["check_project.py", self.root])
            self.assertEqual(code, 1, out)
            self.assertNotIn("Traceback", out)
            quiet(list_visuals.main, ["list_visuals.py", self.root])
            self.write(relative, original)
        self.write(REPORT, "[]")
        self.assertFails("J002")

    def test_header_card_written_as_an_object_fails_with_a_clear_message(self):
        def as_object(d):
            d["visual"]["visualContainerObjects"]["visualHeader"] = {"properties": {"show": {"expr": {"Literal": {"Value": "false"}}}}}
        self.edit_json(CARD, as_object)
        findings, _, _ = cp.run(self.root)
        messages = [f[3] for f in findings.errors() if f[0] == "H001"]
        self.assertEqual(len(messages), 1)
        self.assertIn("not a list", messages[0])
        before = self.read(CARD)
        code, out = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        self.assertEqual(code, 1)
        self.assertIn("skipped", out)
        self.assertEqual(self.read(CARD), before)          # the odd file is left untouched

    def test_other_letter_case_is_not_accepted(self):
        def upper(d):
            d["visual"]["visualContainerObjects"]["visualHeader"][0]["properties"]["show"]["expr"]["Literal"]["Value"] = "False"
        self.edit_json(CARD, upper)
        self.assertEqual(self.codes(), ["H001"])

    def test_mobile_layout_with_header_on_fails_and_is_fixed(self):
        mobile = os.path.join(os.path.dirname(CARD), "mobile.json")
        self.write(mobile, json.dumps({"visualContainerObjects": {"visualHeader": [
            {"properties": {"show": {"expr": {"Literal": {"Value": "true"}}}}}]}}))
        self.assertEqual(self.codes(), ["H001"])
        quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        self.assertClean()

    def test_page_name_ending_in_a_line_break_fails(self):
        self.edit_json(os.path.join(PAGE, "page.json"), lambda d: d.update({"name": "Overview\n"}))
        self.assertFails("N001")

    def test_two_visuals_with_the_same_label_fail(self):
        self.edit_json(OLD, lambda d: d.update({"annotations": [{"name": "VisualLabel", "value": "Overview_Card_TotalSales"}]}))
        self.assertFails("N005")


class NumbersStayAsWritten(ProjectCase):
    def test_decimal_numbers_keep_their_exact_text(self):
        def odd(d):
            d["visual"].pop("visualContainerObjects")
        self.edit_json(CARD, odd)
        self.replace(CARD, '"x": 24', '"x": 427.63636363636363')
        self.replace(CARD, '"width": 608', '"width": 3E+2')
        quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        text = self.read(CARD)
        self.assertIn('"x": 427.63636363636363', text)
        self.assertIn('"width": 3E+2', text)
        self.assertClean()


class ReviewEdgeCases(ReviewTable):
    def test_wrong_encoding_is_reported_not_crashed(self):
        with open(self.file, "w", encoding="utf-16") as fh:
            fh.write("| 1 | Pass | x |\n")
        self.assertEqual(self.codes()[0], "R001")

    def test_odd_digit_does_not_crash(self):
        rows = self.good_rows()
        rows[8] = ("\u2468", "Pass", "seen")
        self.write(rows)
        self.assertEqual(self.codes(), ["R003"])

    def test_later_tables_are_not_review_rows(self):
        self.write(self.good_rows())
        with open(self.file, "a", encoding="utf-8") as fh:
            fh.write("\n## Gaps to close\n\n| Item | Status | What to do |\n|---|---|---|\n| 2 | Fail | add a description |\n")
        self.assertEqual(self.codes(), [])

    def test_placeholder_evidence_fails(self):
        for text in ("TODO", "?", "n/a", "\u200b", "..."):
            rows = self.good_rows()
            rows[3] = (4, "Pass", text)
            self.write(rows)
            self.assertEqual(self.codes(), ["R005"], text)


class MoreTmdlEdgeCases(ProjectCase):
    def test_comment_glued_to_an_object_name_fails(self):
        self.replace(SALES, "\tannotation SampleSource", "\tcolumn Extra// the key\n\t\tisHidden\n\n\tannotation SampleSource")
        self.assertFails("C001")
        self.write(SALES, self.read(SALES).replace("table Sales\n", "table Sales// main table\n", 1))
        self.assertFails("C001")

    def test_quoted_names_holding_slashes_are_not_comments_where_referenced(self):
        base = os.path.join("Sample.SemanticModel", "definition")
        self.write(os.path.join(base, "relationships.tmdl"),
                   "relationship r1\n\tfromColumn: 'Sales // archive'.'Order = Date'\n\ttoColumn: Sales.OrderId\n")
        self.write(os.path.join(base, "model.tmdl"), "model Model\n\tculture: en-US\n\nref table 'Sales // archive'\nref table Sales\n")
        self.assertEqual(self.codes(), ["M901"])     # no C001; the made-up table is not in the model, which M901 reports

    def test_expression_whose_first_line_is_indented_deeper_is_kept_whole(self):
        self.replace(SALES, "\tannotation SampleSource",
                     "\t/// Example with a deeper first line.\n\tmeasure Deeper =\n\t\t\t    VAR a = 1\n"
                     "\t\t\t// explain the result\n\t\t\tRETURN a\n\t\tformatString: 0\n\n\tannotation SampleSource")
        self.assertCleanFiles()

    def test_lines_after_an_empty_expression_are_still_checked(self):
        self.replace(SALES, "\tannotation SampleSource",
                     "\t/// Empty expression.\n\tmeasure Empty =\n\t\t// stray comment\n\t\tformatString: 0\n\n\tannotation SampleSource")
        self.assertFails("C001")

    def test_plain_values_after_an_equals_sign_are_checked(self):
        self.replace(SALES, "\t\tmode: import\n", "\t\tmode: import\n\t\tchangedProperty = Name // renamed by hand\n")
        self.assertFails("C001")
        self.write(SALES, self.read(SALES).replace("changedProperty = Name // renamed by hand", "changedProperty = Name")
                   .replace("\tpartition Sales = m\n", "\tpartition Sales = m // the query\n"))
        self.assertFails("C001")

    def test_description_above_objects_the_check_does_not_inspect_is_allowed(self):
        self.replace(SALES, "\tannotation SampleSource",
                     "\t/// What the group does.\n\tcalculationGroup\n\t\tprecedence: 1\n\n\tannotation SampleSource")
        self.assertClean()

    def test_translations_are_not_treated_as_model_objects(self):
        self.write(os.path.join("Sample.SemanticModel", "definition", "cultures", "de-DE.tmdl"),
                   "cultureInfo de-DE\n\ttranslations\n\t\tmodel Model\n\t\t\ttable Sales\n\t\t\t\tcaption: Umsatz // alt\n")
        self.assertClean()

    def write(self, relative, text):
        os.makedirs(os.path.dirname(self.path(relative)), exist_ok=True)
        super().write(relative, text)

    def query(self, body):
        self.write(EXPRESSIONS, "/// A query for the test.\nexpression Q =\n" + body)

    def test_steps_are_found_in_less_usual_layouts(self):
        layouts = [
            "\t\t(\n\t\t    x as number\n\t\t) as number =>\n\t\tlet\n\t\t    A = x + 1\n\t\tin\n\t\t    A\n",
            "\t\t(x as number) => let\n\t\t    A = x + 1\n\t\tin\n\t\t    A\n",
            "\t\tlet // start\n\t\t    A = 1\n\t\tin\n\t\t    A\n",
            "\t\tlet\n\t\t    // first\n\t\t    A = 1,\n\t\t     B = A + 1\n\t\tin\n\t\t    B\n",
            "\t\tlet\n\t\t    // first\n\t\t    A = 1,\n\t\t    Källa = A + 1\n\t\tin\n\t\t    Källa\n",
            "\t\tlet\n\t\t    //\n\t\t    A = 1\n\t\tin\n\t\t    A\n",
            "\t\tlet A = 1\n\t\tin\n\t\t    A\n",
        ]
        for body in layouts:
            self.query(body)
            self.assertEqual(self.codes(), ["P001"], body)

    def test_more_step_layouts(self):
        # an inner 'let' opened inside a bracket must not hide the outer steps that follow it
        self.query("\t\tlet\n\t\t    // Start.\n\t\t    Source = #table({\"A\"}, {{1}}),\n"
                   "\t\t    // Add a column.\n\t\t    Added = Table.AddColumn(Source, \"X\", each let\n"
                   "\t\t            a = [A]\n\t\t        in\n\t\t            a),\n"
                   "\t\t    After1 = Added,\n\t\t    After2 = After1\n\t\tin\n\t\t    After2\n")
        self.assertEqual(self.codes(), ["P001", "P001"])
        # steps written with a leading comma
        self.query("\t\tlet\n\t\t    // Start.\n\t\t    Source = 1\n\t\t    , Step2 = Source\n\t\tin\n\t\t    Step2\n")
        self.assertEqual(self.codes(), ["P001"])
        # a whole query on the declaration line
        self.write(EXPRESSIONS, "/// A query for the test.\nexpression Q = let Source = 1, Other = Source in Other\n")
        self.assertEqual(self.codes(), ["P001"])
        self.write(EXPRESSIONS, "/// A parameter.\nexpression P = 5 meta [IsParameterQuery=true, Type=\"Number\"]\n")
        self.assertClean()

    def test_tmdl_file_that_is_not_utf8_is_reported(self):
        text = self.read(SALES)
        for encoding in ("utf-16", "utf-16-le"):
            with open(self.path(SALES), "wb") as fh:
                fh.write(text.encode(encoding))
            self.assertEqual(self.codes(), ["J001"], encoding)

    def test_nested_let_and_bracketed_lines_are_not_steps(self):
        self.query("\t\tlet\n\t\t    // Build a record.\n\t\t    A = [\n\t\t        x = 1,\n\t\t        y = 2\n\t\t    ],\n"
                   "\t\t    // Work out a value with an inner let.\n\t\t    B =\n\t\t        let\n\t\t            inner = A[x]\n"
                   "\t\t        in\n\t\t            inner\n\t\tin\n\t\t    B\n")
        self.assertClean()


class MoreStructureCases(ProjectCase):
    def test_json_null_is_reported(self):
        self.write(CARD, "null")
        self.assertFails("J002")
        self.write(CARD, json.dumps({"x": 1}))
        self.write(os.path.join(PAGE, "page.json"), "null")
        self.assertFails("J002")

    def test_deeply_nested_json_is_reported_not_crashed(self):
        self.write(CARD, "[" * 100000 + "]" * 100000)
        code, out = quiet(cp.main, ["check_project.py", self.root])
        self.assertEqual(code, 1)
        self.assertNotIn("Traceback", out)
        self.assertEqual(quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])[0], 1)

    def test_visual_folder_without_visual_json_fails(self):
        os.remove(self.path(CARD))
        self.assertFails("F002")

    def test_model_without_tmdl_files_fails(self):
        shutil.rmtree(self.path(os.path.join("Sample.SemanticModel", "definition")))
        os.makedirs(self.path(os.path.join("Sample.SemanticModel", "definition")))
        self.assertFails("F003")

    def test_mobile_layout_with_plain_true_fails(self):
        self.write(os.path.join(os.path.dirname(CARD), "mobile.json"),
                   json.dumps({"visualContainerObjects": {"visualTooltip": [{"properties": {"show": True}}]}}))
        self.assertEqual(self.codes(), ["H002"])


class MoreFixerCases(ProjectCase):
    def test_file_is_never_left_half_written(self):
        self.edit_json(CARD, lambda d: d["visual"].pop("visualContainerObjects"))
        text = self.read(CARD).replace('"visualType": "cardVisual"', '"visualType": "cardVisual", "note": "half \\ud83d emoji"')
        self.write(CARD, text)
        code, out = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        self.assertEqual(code, 1)
        self.assertIn("skipped", out)
        self.assertEqual(self.read(CARD), text)             # untouched, not emptied

    def test_odd_shapes_are_skipped_with_a_message(self):
        cases = [lambda d: d.update({"visual": "card"}), lambda d: d.update({"visual": []}),
                 lambda d: (d.pop("visual"), None)[1], lambda d: d.update({"annotations": 5}),
                 lambda d: d.update({"annotations": {"name": "HeaderTooltipException", "value": "both: x"}})]
        for change in cases:
            original = self.read(CARD)
            self.edit_json(CARD, change)
            before = self.read(CARD)
            code, out = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
            self.assertEqual(code, 1, out)
            self.assertIn("skipped", out)
            self.assertEqual(self.read(CARD), before)
            self.write(CARD, original)

    def test_nan_and_repeated_keys_are_refused(self):
        for text in ('{"name": "a", "name": "b", "visual": {}}', '{"name": "a", "visual": {}, "position": {"x": NaN}}'):
            self.write(CARD, text)
            code, out = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
            self.assertEqual(code, 1)
            self.assertEqual(self.read(CARD), text)

    def test_exception_keeps_only_the_named_setting(self):
        def excuse(d):
            d["visual"].pop("visualContainerObjects")
            d["annotations"] = [{"name": "HeaderTooltipException", "value": "tooltip: hover detail asked for"}]
        self.edit_json(CARD, excuse)
        quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        self.assertClean()
        objects = json.loads(self.read(CARD))["visual"]["visualContainerObjects"]
        self.assertIn("visualHeader", objects)
        self.assertNotIn("visualTooltip", objects)

    def test_label_already_used_on_the_page_is_refused(self):
        code, out = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root,
                                                     "--label", "Overview/4f0c9d2a7b1e8a6c3d5f=Overview_Card_TotalSales"])
        self.assertEqual(code, 1)
        self.assertIn("already", out)
        self.assertClean()

    def test_second_run_changes_nothing(self):
        self.edit_json(CARD, lambda d: d["visual"].pop("visualContainerObjects"))
        quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        after_first = self.read(CARD)
        code, out = quiet(set_visual_defaults.main, ["set_visual_defaults.py", self.root])
        self.assertEqual((code, self.read(CARD)), (0, after_first))
        self.assertIn("0 visual file(s) changed", out)


class MoreReviewCases(ReviewTable):
    def test_item_number_outside_the_checklist_fails(self):
        self.write(self.good_rows() + [(80, "Pass", "extra")])
        self.assertEqual(self.codes(), ["R006"])

    def test_very_long_number_does_not_crash(self):
        self.write(self.good_rows() + [("9" * 5000, "Pass", "extra")])
        self.assertEqual(self.codes(), [])

    def test_table_must_have_the_review_header(self):
        with open(self.file, "w", encoding="utf-8") as fh:
            fh.write("| No | Owner | Action |\n|---|---|---|\n| 1 | A | b |\n")
        self.assertEqual(self.codes(), ["R001"])

    def test_a_table_before_or_after_the_review_is_ignored(self):
        with open(self.file, "w", encoding="utf-8") as fh:
            fh.write("| No | Owner | Action |\n|---|---|---|\n| 1 | A | b |\n\n")
            fh.write("| Item | Status | Evidence |\n|---|---|---|\n")
            for n in range(1, 80):
                fh.write("| %d | Pass | seen in the model files |\n" % n)
            fh.write("\n| No | Owner | Action |\n|---|---|---|\n| 1 | A | b |\n| 99 | B | c |\n")
        self.assertEqual(self.codes(), [])

    def test_more_placeholders_fail(self):
        for text in ("TODO(owner)", "todo: check", "**TODO**", "<evidence>", "??", "---", "_", "x", "&nbsp;", "`-`"):
            rows = self.good_rows()
            rows[3] = (4, "Pass", text)
            self.write(rows)
            self.assertEqual(self.codes(), ["R005"], text)

    def test_text_in_a_fourth_column_does_not_hide_empty_evidence(self):
        rows = self.good_rows()
        rows[6] = (7, "Pass", " | a note")
        self.write(rows)
        self.assertEqual(self.codes(), ["R005"])


class MoreTemplateCases(TemplateCase):
    def test_missing_checklist_file_fails(self):
        os.remove(os.path.join(self.tmp, "checklist", "checklist.md"))
        self.assertEqual(self.codes(ct.check_checklist, None), ["K001"])

    def test_changed_column_label_fails(self):
        self.put("checklist/checklist.md", checklist_markdown(self.topics).replace("- Area: Model\n", "- Domain: Model\n", 1))
        self.assertIn("K003", self.codes(ct.check_checklist, None))

    def test_unreadable_spreadsheet_fails(self):
        self.assertEqual(self.codes(ct.check_checklist, os.path.join(self.tmp, "missing.xlsx")), ["K005"])

    def test_spreadsheet_with_other_header_or_row_count_fails(self):
        header = list(ct.HEADER)
        ct.HEADER[0] = "Domain"
        try:
            other = os.path.join(self.tmp, "..", os.path.basename(self.tmp) + "-b.xlsx")
            write_xlsx(other, self.topics[:-1])
        finally:
            ct.HEADER[:] = header
        try:
            codes = self.codes(ct.check_checklist, other)
        finally:
            os.remove(other)
        self.assertIn("K006", codes)
        self.assertIn("K007", codes)

    def test_missing_theme_file_fails(self):
        os.remove(os.path.join(self.tmp, "theme", "theme.json"))
        self.assertEqual(self.codes(ct.check_theme), ["T101"])

    def test_report_without_registered_theme_fails(self):
        shutil.copytree(os.path.join(GOOD, "Sample.Report"), os.path.join(self.tmp, "Starter.Report"))
        report = os.path.join(self.tmp, "Starter.Report", "definition", "report.json")
        with open(report) as fh:
            data = json.load(fh)
        del data["themeCollection"]["customTheme"]
        with open(report, "w") as fh:
            json.dump(data, fh)
        self.assertEqual(self.codes(ct.check_theme), ["T103"])

    def test_registered_theme_file_missing_fails(self):
        shutil.copytree(os.path.join(GOOD, "Sample.Report"), os.path.join(self.tmp, "Starter.Report"))
        os.remove(os.path.join(self.tmp, "Starter.Report", "StaticResources", "RegisteredResources", "fixture-theme.json"))
        self.assertEqual(self.codes(ct.check_theme), ["T104"])

    def test_skill_folder_without_skill_file_fails(self):
        os.makedirs(os.path.join(self.tmp, ".github", "skills", "empty-skill"))
        self.assertIn("S005", self.codes(ct.check_guidance))

    def test_markdown_file_that_is_not_utf8_is_reported_not_crashed(self):
        path = os.path.join(self.tmp, "docs", "notes.md")
        os.makedirs(os.path.dirname(path))
        with open(path, "wb") as fh:
            fh.write("Caf\u00e9 notes".encode("latin-1"))
        self.assertEqual(self.codes(ct.check_links), ["L003"])

    def test_item_both_review_only_and_applied_fails(self):
        self.put(".github/copilot-instructions.md", "Rules.\n\nChecklist items: 1-79\n")
        self.put(".github/skills/pbi-checklist-review/SKILL.md",
                 (SKILL % "pbi-checklist-review").replace("Checklist items: 1-78\n", "Checklist items: 1-79\nReview-only items: 5\n"))
        rows = "".join("| %d |  |  |\n" % n for n in range(1, 80))
        self.put(".github/skills/pbi-checklist-review/references/review-template.md", rows)
        self.assertEqual(self.codes(ct.check_citations), ["C004"])


LESSONS_HEAD = ("# Lessons\n\nRows are added by the script.\n\n"
                "| No | Date | Trigger | Key | Mistake | Correction | Fix went to | Approved in |\n"
                "|---|---|---|---|---|---|---|---|\n")
GOOD_ROW = "| %d | 2026-11-11 | developer | %s | Did this | Should do that | %s | %s |\n"


class LessonsCase(unittest.TestCase):
    """Runs scripts/lessons.py against a small made-up repository in a temporary folder."""

    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.saved = lessons.ROOT
        lessons.ROOT = self.tmp
        self.file = os.path.join(self.tmp, "docs", "lessons.md")
        for folder in ("docs", "scripts", "tests", "checklist", "theme", os.path.join(".github", "instructions")):
            os.makedirs(os.path.join(self.tmp, folder))
        for name in ("scripts/check_project.py", "tests/test_checks.py", ".github/instructions/tmdl.instructions.md",
                     "checklist/checklist.md", "theme/theme.json", "README.md", "docs/report-brief.md"):
            with open(os.path.join(self.tmp, name), "w", encoding="utf-8") as fh:
                fh.write("x\n")
        self.reset()

    def tearDown(self):
        lessons.ROOT = self.saved
        shutil.rmtree(self.tmp, ignore_errors=True)

    def reset(self, extra=""):
        with open(self.file, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(LESSONS_HEAD + extra)

    def text(self):
        with open(self.file, encoding="utf-8", newline="") as fh:
            return fh.read()

    def rows(self):
        rows, problems = lessons.read_rows(self.text())
        self.assertEqual(problems, [])
        return [row for _, row in rows]

    def add(self, key="measure-in-wrong-table", trigger="developer", fix="report", approved="-",
            mistake="Put the measure in the Calendar table", correction="Measures belong in the Sales table"):
        return lessons.add(self.file, trigger, key, mistake, correction, fix, approved, today="2026-11-11")

    def codes(self):
        return [line.split()[0] for line in lessons.check_file(self.file)]

    def run_main(self, *args):
        return quiet(lessons.main, ["lessons.py"] + list(args))


class LessonsFile(LessonsCase):
    def test_empty_file_passes(self):
        self.assertEqual(self.codes(), [])

    def test_one_lesson_is_recorded_and_passes(self):
        self.assertEqual(self.add(), (1, 0))
        row = self.rows()[0]
        self.assertEqual(row["Mistake"], "Put the measure in the Calendar table")
        self.assertEqual(row["Fix went to"], "report")
        self.assertEqual(self.codes(), [])

    def test_a_warning_or_a_note_of_the_check_does_not_start_the_loop(self):
        for key in ("M520", "A001", "U001"):                # two warnings and a suggestion
            with self.assertRaises(ValueError, msg=key):
                self.add(key=key, trigger="check")
        self.assertEqual(self.rows(), [])
        self.assertEqual(self.add(key="M502", trigger="check"), (1, 0))      # a failed check is recorded
        self.assertEqual(self.add(key="M520", trigger="developer"), (2, 0))  # the developer may still point one out

    def test_lessons_are_numbered_in_order_and_earlier_rows_are_untouched(self):
        self.add()
        before = self.text()
        self.add(key="D001", trigger="check")
        self.add(key="wrong-page")
        self.assertEqual([row["No"] for row in self.rows()], ["1", "2", "3"])
        self.assertTrue(self.text().startswith(before))
        self.assertEqual(self.codes(), [])

    def test_text_with_a_bar_or_line_break_stays_in_its_cell(self):
        self.add(mistake="Used A | B as\na name", correction="Use A or B")
        self.assertEqual(self.rows()[0]["Mistake"], "Used A | B as a name")
        self.assertEqual(self.codes(), [])

    def test_windows_line_endings_are_kept(self):
        with open(self.file, "wb") as fh:
            fh.write((LESSONS_HEAD + GOOD_ROW % (1, "a-key", "report", "-")).replace("\n", "\r\n").encode("utf-8"))
        before = self.text()
        self.add(key="b-key")
        after = self.text()
        self.assertTrue(after.startswith(before))
        self.assertTrue(after.endswith("\r\n"))
        self.assertNotIn("\n", after.replace("\r\n", ""))
        self.assertEqual(self.codes(), [])

    def test_text_that_cannot_be_saved_leaves_the_file_as_it_was(self):
        self.add()
        before = self.text()
        with self.assertRaises(ValueError):
            self.add(key="b-key", mistake="caf\udce9 in the page title")
        self.assertEqual(self.text(), before)
        self.assertFalse(os.path.exists(self.file + ".tmp"))

    def test_a_row_that_is_not_valid_is_never_written(self):
        bad = [dict(mistake=" "), dict(correction="-"), dict(trigger="copilot"), dict(key="Bad Key"),
               dict(fix="theme/theme.json", approved="pull request 2"),
               dict(fix="checklist/checklist.md", approved="pull request 2"),
               dict(fix="scripts/check_projct.py", approved="pull request 2"),      # a typing slip
               dict(fix="scripts/check_project.py"),                                # no pull request
               dict(fix="scripts/", approved="pull request 2"),                     # a folder, not a file
               dict(fix="declined:"), dict(fix="Report"), dict(fix="")]
        before = self.text()
        for values in bad:
            with self.assertRaises(ValueError, msg=str(values)):
                self.add(**values)
            self.assertEqual(self.text(), before, str(values))

    def test_repeated_mistake_fails_until_built_into_the_template(self):
        self.assertEqual(self.add(), (1, 0))
        self.assertEqual(self.codes(), [])
        self.assertEqual(self.add(), (2, 2))
        self.assertEqual(self.codes(), ["X003"])
        self.assertEqual(self.add(fix="scripts/check_project.py, tests/test_checks.py", approved="pull request 12"), (3, 0))
        self.assertEqual(self.codes(), [])

    def test_mistake_that_returns_after_a_template_fix_is_raised_again(self):
        self.add()
        self.add()
        self.add(fix=".github/instructions/tmdl.instructions.md", approved="#7")
        self.add()
        self.assertEqual(self.codes(), [])
        self.assertEqual(self.add(), (5, 2))
        self.assertEqual(self.codes(), ["X003"])

    def test_repeated_mistake_passes_when_the_developer_declines(self):
        self.add()
        self.add()
        self.assertEqual(self.codes(), ["X003"])
        self.add(fix="declined: one-off, specific to this model")
        self.assertEqual(self.codes(), [])

    def test_repeat_message_fits_the_kind_of_key(self):
        self.add(key="D001", trigger="check")
        self.add(key="D001", trigger="check")
        self.assertIn("a check already catches it", lessons.check_file(self.file)[0])
        self.reset()
        self.add()
        self.add()
        self.assertIn("a script check if a script can catch it", lessons.check_file(self.file)[0])

    def test_different_mistakes_are_not_repeats(self):
        self.add(key="a-first")
        self.add(key="a-second")
        self.assertEqual(self.codes(), [])

    def test_checklist_and_theme_are_never_a_fix_location(self):
        for target in ("checklist/checklist.md", "theme/theme.json", "./theme/theme.json", "`checklist/checklist.md`",
                       "theme\\theme.json", "Theme/Theme.json", "docs/../theme/theme.json", "/abs/theme/theme.json",
                       "scripts/check_project.py, theme/theme.json", "checklist"):
            self.reset(GOOD_ROW % (1, "a-key", target, "pull request 3"))
            self.assertEqual(self.codes(), ["X002"], target)

    def test_fix_location_must_be_a_template_file(self):
        for target in ("Sales.SemanticModel/definition/tables/Sales.tmdl", "../elsewhere.md", "docs/report-brief.md",
                       "somewhere", "declined:", "Report", "scripts/x.py,,README.md"):
            self.reset(GOOD_ROW % (1, "a-key", target, "pull request 3"))
            self.assertEqual(self.codes(), ["X002"], target)
        for target in ("scripts/check_project.py", ".github/instructions/tmdl.instructions.md", "README.md",
                       "scripts/check_project.py, tests/test_checks.py", "scripts/renamed_later.py"):
            self.reset(GOOD_ROW % (1, "a-key", target, "pull request 3"))
            self.assertEqual(self.codes(), [], target)

    def test_template_change_needs_a_pull_request_number_or_address(self):
        for approved in ("-", "", "none", "n/a", "TBD", "pending", "PR", "0"):
            self.reset(GOOD_ROW % (1, "a-key", "scripts/check_project.py", approved))
            self.assertEqual(self.codes(), ["X004"], approved)
        for approved in ("pull request 12", "#7", "https://example.com/owner/repo/pull/3"):
            self.reset(GOOD_ROW % (1, "a-key", "scripts/check_project.py", approved))
            self.assertEqual(self.codes(), [], approved)

    def test_badly_formed_rows_fail(self):
        good = GOOD_ROW % (1, "a-key", "report", "-")
        self.reset(good)
        self.assertEqual(self.codes(), [])
        broken = [good.replace("2026-11-11", "11/11/2026"), good.replace("2026-11-11", "2026-13-45"),
                  good.replace("developer", "copilot"), good.replace("a-key", "A Key"), good.replace("Did this", " "),
                  good.replace("Should do that", "-"), good.replace("| 1 |", "| 7 |"), good.replace(" | - |", " |")]
        for row in broken:
            self.reset(row)
            self.assertEqual(self.codes(), ["X001"], row)

    def test_missing_table_fails(self):
        with open(self.file, "w", encoding="utf-8") as fh:
            fh.write("# Lessons\n\nNothing here.\n")
        self.assertEqual(self.codes(), ["X001"])
        with self.assertRaises(ValueError):
            self.add()

    def test_rows_outside_the_table_are_not_ignored(self):
        self.reset(GOOD_ROW % (1, "a-key", "report", "-") + "\n" + GOOD_ROW % (2, "a-key", "theme/theme.json", "-"))
        self.assertEqual(self.codes(), ["X001"])
        with self.assertRaises(ValueError):
            self.add()

    def test_removing_an_earlier_lesson_is_noticed(self):
        self.add()
        self.add(key="wrong-page")
        kept = [line for line in self.text().splitlines(keepends=True) if not line.startswith("| 1 |")]
        with open(self.file, "w", encoding="utf-8", newline="") as fh:
            fh.write("".join(kept))
        self.assertEqual(self.codes(), ["X001"])

    def test_command_line(self):
        self.assertEqual(self.run_main("check")[0], 0)
        code, out = self.run_main("add", "--trigger", "check", "--key", "H001", "--mistake", "Left header icons on",
                                  "--correction", "Header icons off on every visual")
        self.assertEqual(code, 0)
        self.assertIn("Added lesson 1", out)
        code, out = self.run_main("add", "--trigger", "check", "--key", "H001", "--mistake", "Left header icons on again",
                                  "--correction", "Header icons off on every visual")
        self.assertEqual(code, 1)                       # the mistake has come back: action is needed
        self.assertIn("X003", out)
        self.assertIn("Ask the developer first", out)
        self.assertEqual(self.run_main("check")[0], 1)
        before = self.text()
        for args in (("add", "--trigger", "nobody", "--key", "x", "--mistake", "m", "--correction", "c"),
                     ("add", "--key", "x"),
                     ("add", "--trigger", "check", "--key", "Bad Key", "--mistake", "m", "--correction", "c"),
                     ("add", "--trigger", "check", "--key", "x", "--mistake", "m", "--correction", "c", "--fix", "theme/theme.json"),
                     ("add", "--trigger", "check", "--key", "x", "--mistake", "m", "--correction", "c", "--other", "y"),
                     ()):
            self.assertEqual(self.run_main(*args)[0], 2, args)
            self.assertEqual(self.text(), before)
        os.remove(self.file)
        self.assertEqual(self.run_main("check")[0], 1)
        self.assertEqual(self.run_main("add", "--trigger", "check", "--key", "x", "--mistake", "m", "--correction", "c")[0], 1)


class LessonsInTemplateCheck(TemplateCase):
    def test_missing_lessons_file_fails_the_template_check(self):
        saved = lessons.ROOT
        try:
            self.assertEqual(self.codes(ct.check_lessons), ["X001"])
            self.put("docs/lessons.md", LESSONS_HEAD)
            self.assertEqual(self.codes(ct.check_lessons), [])
            self.put("docs/lessons.md", LESSONS_HEAD
                     + "| 1 | 2026-11-11 | check | D001 | No description | Describe it | theme/theme.json | pull request 2 |\n")
            self.assertEqual(self.codes(ct.check_lessons), ["X002"])
        finally:
            lessons.ROOT = saved

    def test_file_that_applies_no_checklist_item_may_say_none(self):
        self.put(".github/copilot-instructions.md", "Rules.\n\nChecklist items: 79\n")
        self.put(".github/skills/demo-skill/SKILL.md", SKILL % "demo-skill")
        self.put(".github/skills/pbi-checklist-review/SKILL.md", (SKILL % "pbi-checklist-review").replace("1-78", "1-79"))
        self.put(".github/skills/no-items/SKILL.md", (SKILL % "no-items").replace("Checklist items: 1-78", "Checklist items: none"))
        rows = "".join("| %d |  |  |\n" % n for n in range(1, 80))
        self.put(".github/skills/pbi-checklist-review/references/review-template.md", rows)
        self.assertEqual(self.codes(ct.check_citations), [])


if __name__ == "__main__":
    unittest.main()
