"""Tests of the report checks added in round 3 (scripts/report_rules.py) and of the schema check.

Run from the repository root:
    python -m unittest discover -s tests -v

Each test copies the made-up project tests/fixtures/good to a temporary folder, adds or breaks one thing,
and expects the code of that rule at the level the report standard gives it.
"""
import json
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "scripts"))

import check_project as cp            # noqa: E402
import json_schema                    # noqa: E402

DEFINITION = os.path.join("Sample.Report", "definition")
PAGES = os.path.join(DEFINITION, "pages")
PAGES_JSON = os.path.join(PAGES, "pages.json")
VISUAL_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/visualContainer/2.13.0/schema.json"
PAGE_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/page/2.1.0/schema.json"
BOOKMARK_SCHEMA = "https://developer.microsoft.com/json-schemas/fabric/item/report/definition/bookmark/2.1.0/schema.json"


def lit(text):
    return {"expr": {"Literal": {"Value": text}}}


OFF = [{"properties": {"show": lit("false")}}]


def field(table, name, kind="Measure"):
    return {"field": {kind: {"Expression": {"SourceRef": {"Entity": table}}, "Property": name}},
            "queryRef": "%s.%s" % (table, name)}


class ReportCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, "project")
        shutil.copytree(os.path.join(HERE, "fixtures", "good"), self.root)
        self.order = 10

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def write_json(self, rel, data):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(data, fh, indent=2)

    def read_json(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as fh:
            return json.load(fh)

    def page(self, name, **extra):
        data = {"$schema": PAGE_SCHEMA, "name": name, "displayName": name, "displayOption": "FitToPage",
                "height": 720, "width": 1280}
        data.update(extra)
        self.write_json(os.path.join(PAGES, name, "page.json"), data)
        listed = self.read_json(PAGES_JSON)
        if name not in listed["pageOrder"]:
            listed["pageOrder"].append(name)
            self.write_json(PAGES_JSON, listed)

    def visual(self, page, name, kind="card", fields=(), x=24, y=200, cards=None, objects=None, described=True, **top):
        """A visual with header icons and tooltips off, and (unless described is False) alt text and a title."""
        self.order += 1
        body = {"visualType": kind, "visualContainerObjects": {"visualHeader": OFF, "visualTooltip": OFF}}
        if fields:
            body["query"] = {"queryState": {"Values": {"projections": list(fields)}}}
            if described:
                body["visualContainerObjects"]["general"] = [{"properties": {"altText": lit("'Made-up visual for a test'")}}]
                body["visualContainerObjects"]["title"] = [{"properties": {"text": lit("'Made-up title'")}}]
        body["visualContainerObjects"].update(cards or {})
        if objects:
            body["objects"] = objects
        data = {"$schema": VISUAL_SCHEMA, "name": name,
                "position": {"x": x, "y": y, "z": self.order, "width": 160, "height": 56, "tabOrder": self.order},
                "visual": body}
        data.update(top)
        self.write_json(os.path.join(PAGES, page, "visuals", name, "visual.json"), data)
        return os.path.join(PAGES, page, "visuals", name, "visual.json")

    def button(self, page, name, kind, **targets):
        link = {"show": lit("true"), "type": lit("'%s'" % kind)}
        link.update({key: lit("'%s'" % value) for key, value in targets.items()})
        return self.visual(page, name, kind="actionButton", cards={"visualLink": [{"properties": link}]})

    def found(self):
        findings, _, _ = cp.run(self.root)
        return findings.items

    def codes(self, level=None):
        return sorted({f[0] for f in self.found() if level is None or f[4] == level})

    def assertFinds(self, code, level):
        levels = {f[4] for f in self.found() if f[0] == code}
        self.assertEqual(levels, {level}, "%s: expected level %r, found %r; all findings %s"
                         % (code, level, levels, [(f[0], f[3][:90]) for f in self.found()]))

    def assertNot(self, code):
        self.assertNotIn(code, self.codes(), [f[3] for f in self.found() if f[0] == code])


SALES = field("_Measures", "Total Sales")


class Pages(ReportCase):
    def test_good_report_gives_no_report_finding(self):
        self.assertEqual([c for c in self.codes() if c[0] in "VAU"], [])

    def test_V001_drillthrough_page_without_a_back_button_fails(self):
        self.page("Detail", type="Drillthrough")
        self.visual("Detail", "Detail_Card_Sales", fields=[SALES])
        self.assertFinds("V001", False)
        self.button("Detail", "Detail_Button_Back", "Back")
        self.assertNot("V001")

    def test_V002_to_V005_tooltip_page(self):
        self.page("Tip", type="Tooltip", width=1280, height=720)
        self.visual("Tip", "Tip_Card_Sales", fields=[SALES])
        self.visual("Tip", "Tip_Slicer_Product", kind="slicer", fields=[field("Sales", "Product", "Column")])
        for code in ("V002", "V003", "V004", "V005"):
            self.assertFinds(code, "warn")

    def test_small_hidden_tooltip_page_with_three_facts_passes(self):
        self.page("Tip", type="Tooltip", width=320, height=240, visibility="HiddenInViewMode")
        self.visual("Tip", "Tip_Card_Sales", fields=[SALES, field("_Measures", "Return Rate"), field("_Measures", "Order Count")])
        for code in ("V002", "V003", "V004", "V005"):
            self.assertNot(code)

    def test_V006_V007_page_density(self):
        self.page("Busy")
        for number in range(13):
            self.visual("Busy", "Busy_Card_N%d" % number, fields=[SALES], x=24 + number * 8)
        self.assertFinds("V007", "warn")
        self.assertNot("V006")
        for number in range(13, 17):
            self.visual("Busy", "Busy_Card_N%d" % number, fields=[SALES], x=24 + number * 8)
        self.assertFinds("V006", False)

    def test_V006_is_excused_by_a_row_in_the_brief(self):
        self.page("Busy")
        for number in range(17):
            self.visual("Busy", "Busy_Card_N%d" % number, fields=[SALES], x=24 + number * 8)
        os.makedirs(os.path.join(self.root, "docs"), exist_ok=True)
        with open(os.path.join(self.root, "docs", "report-brief.md"), "w", encoding="utf-8") as fh:
            fh.write("## 10. Exceptions to the layout standard\n\n| Code | Page | Visual | Reason |\n|---|---|---|---|\n"
                     "| V006 | Busy | - | A wall of small cards the control room asked for |\n")
        self.assertNot("V006")

    def test_V008_button_that_goes_nowhere_warns(self):
        self.button("Overview", "Overview_Button_Detail", "PageNavigation", navigationSection="Detail")
        self.assertFinds("V008", "warn")
        self.page("Detail")
        self.assertNot("V008")

    def test_V008_button_to_a_missing_bookmark_warns(self):
        self.button("Overview", "Overview_Button_Trend", "Bookmark", bookmark="ShowTrend")
        self.assertFinds("V008", "warn")
        self.write_json(os.path.join(DEFINITION, "bookmarks", "ShowTrend.bookmark.json"),
                        {"$schema": BOOKMARK_SCHEMA, "name": "ShowTrend", "displayName": "Show trend",
                         "explorationState": {"version": "1.3", "activeSection": "Overview", "sections": {}}})
        self.assertNot("V008")

    def test_V009_styling_on_one_visual_warns_and_a_theme_colour_passes(self):
        path = self.visual("Overview", "Overview_Card_Styled", fields=[SALES],
                           objects={"labels": [{"properties": {"fontSize": lit("14D"),
                                                               "color": {"solid": {"color": lit("'#FF0000'")}}}}]})
        self.assertFinds("V009", "warn")
        theme = {"solid": {"color": {"expr": {"ThemeDataColor": {"ColorId": 1, "Percent": 0}}}}}
        data = self.read_json(path)
        data["visual"]["objects"] = {"labels": [{"properties": {"color": theme}}]}
        self.write_json(path, data)
        self.assertNot("V009")

    def test_V010_bookmark_with_a_visual_that_is_gone_warns(self):
        self.write_json(os.path.join(DEFINITION, "bookmarks", "ShowTrend.bookmark.json"),
                        {"$schema": BOOKMARK_SCHEMA, "name": "ShowTrend", "displayName": "Show trend",
                         "explorationState": {"version": "1.3", "activeSection": "Overview", "sections": {
                             "Overview": {"visualContainers": {"Overview_Line_Gone": {"singleVisual": {"display": {"mode": "hidden"}}}}}}}})
        self.assertFinds("V010", "warn")

    def test_V011_page_list_that_disagrees_with_the_folders_warns(self):
        listed = self.read_json(PAGES_JSON)
        listed["pageOrder"].append("Ghost")
        self.write_json(PAGES_JSON, listed)
        self.assertFinds("V011", "warn")


class Accessibility(ReportCase):
    def test_A001_A003_visual_without_alt_text_or_title_warns(self):
        self.visual("Overview", "Overview_Card_Bare", fields=[SALES], described=False)
        self.assertFinds("A001", "warn")
        self.assertFinds("A003", "warn")

    def test_described_visual_passes_and_a_shape_needs_nothing(self):
        self.visual("Overview", "Overview_Card_Clear", fields=[SALES])
        self.visual("Overview", "Overview_Shape_Line", kind="shape")
        self.assertNot("A001")
        self.assertNot("A003")

    def test_A002_shared_tab_order_number_warns(self):
        first = self.visual("Overview", "Overview_Card_One", fields=[SALES])
        second = self.visual("Overview", "Overview_Card_Two", fields=[SALES], x=400)
        self.assertNot("A002")
        data = self.read_json(second)
        data["position"]["tabOrder"] = self.read_json(first)["position"]["tabOrder"]
        self.write_json(second, data)
        self.assertFinds("A002", "warn")


class Suggestions(ReportCase):
    def test_U101_same_slicer_on_two_pages_not_synced(self):
        product = field("Sales", "Product", "Column")
        self.page("Detail")
        self.visual("Overview", "Overview_Slicer_Product", kind="slicer", fields=[product])
        self.visual("Detail", "Detail_Slicer_Product", kind="slicer", fields=[product])
        self.assertFinds("U101", "note")

    def test_U102_three_page_buttons(self):
        for name in ("One", "Two", "Three"):
            self.page(name)
            self.button("Overview", "Overview_Button_%s" % name, "PageNavigation", navigationSection=name)
        self.assertFinds("U102", "note")

    def test_U103_stacked_visuals_switched_by_bookmarks(self):
        self.visual("Overview", "Overview_Line_Sales", kind="lineChart", fields=[SALES])
        self.visual("Overview", "Overview_Line_Returns", kind="lineChart", fields=[field("_Measures", "Return Rate")])
        self.write_json(os.path.join(DEFINITION, "bookmarks", "ShowSales.bookmark.json"),
                        {"$schema": BOOKMARK_SCHEMA, "name": "ShowSales", "displayName": "Show sales",
                         "explorationState": {"version": "1.3", "activeSection": "Overview", "sections": {
                             "Overview": {"visualContainers": {"Overview_Line_Returns": {"singleVisual": {"display": {"mode": "hidden"}}}}}}}})
        self.assertFinds("U103", "note")


class Schema(ReportCase):
    def test_J003_property_that_is_not_in_microsofts_schema_fails(self):
        path = os.path.join(PAGES, "Overview", "page.json")
        data = self.read_json(path)
        data["pageColour"] = "blue"
        self.write_json(path, data)
        self.assertFinds("J003", False)
        self.assertIn("pageColour", [f[3] for f in self.found() if f[0] == "J003"][0])

    def test_J003_wrong_type_and_missing_required_property_fail(self):
        path = os.path.join(PAGES, "Overview", "page.json")
        data = self.read_json(path)
        data["width"] = "wide"
        del data["displayOption"]
        self.write_json(path, data)
        self.assertFinds("J003", False)

    def test_J004_schema_version_that_is_not_shipped_is_a_note(self):
        path = os.path.join(PAGES, "Overview", "page.json")
        data = self.read_json(path)
        data["$schema"] = PAGE_SCHEMA.replace("2.1.0", "9.9.0")
        self.write_json(path, data)
        self.assertFinds("J004", "note")
        self.assertNot("J003")

    def test_every_shipped_schema_loads_and_names_its_own_address(self):
        versions = json_schema.shipped_versions()
        self.assertIn("fabric/item/report/definition/visualContainer", versions)
        for name, found in versions.items():
            for version in found:
                address = "%s%s/%s/schema.json" % (json_schema.ADDRESS_PREFIX, name, version)
                self.assertIsInstance(json_schema.load_schema(address), dict, address)

    def test_validator_reads_references_enums_and_one_of(self):
        schema = {"definitions": {"size": {"type": "integer"}},
                  "type": "object", "required": ["kind"], "additionalProperties": False,
                  "properties": {"kind": {"enum": ["a", "b"]}, "size": {"$ref": "#/definitions/size"},
                                 "either": {"oneOf": [{"type": "string"}, {"type": "number"}]}}}

        def problems(value):
            return json_schema.validate(value, schema, schema, "local")
        self.assertEqual(problems({"kind": "a", "size": 3, "either": "x"}), [])
        self.assertTrue(problems({"kind": "c"}))
        self.assertTrue(problems({"kind": "a", "size": "big"}))
        self.assertTrue(problems({"kind": "a", "other": 1}))
        self.assertTrue(problems({"size": 1}))
        self.assertTrue(problems({"kind": "a", "either": True}))


if __name__ == "__main__":
    unittest.main()
