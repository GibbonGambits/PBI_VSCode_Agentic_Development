"""Tests of the model checks added in round 3 (scripts/model_rules.py).

Run from the repository root:
    python -m unittest discover -s tests -v

tests/fixtures/star is a made-up star schema that meets every rule. Each test copies it to a temporary
folder, breaks one thing, and expects the code of that rule; test_star_is_clean shows that the correct
model gives no finding at all.
"""
import os
import shutil
import sys
import tempfile
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "scripts"))

import check_project as cp            # noqa: E402

DEFINITION = os.path.join("Star.SemanticModel", "definition")
TABLES = os.path.join(DEFINITION, "tables")
DATE = os.path.join(TABLES, "Date.tmdl")
STORE = os.path.join(TABLES, "Store.tmdl")
SALES = os.path.join(TABLES, "Sales.tmdl")
MEASURES = os.path.join(TABLES, "_Measures.tmdl")
MODEL = os.path.join(DEFINITION, "model.tmdl")
DATABASE = os.path.join(DEFINITION, "database.tmdl")
RELATIONSHIPS = os.path.join(DEFINITION, "relationships.tmdl")
FUNCTIONS = os.path.join(DEFINITION, "functions.tmdl")
EXPRESSIONS = os.path.join(DEFINITION, "expressions.tmdl")
ROLE = os.path.join(DEFINITION, "roles", "Readers.tmdl")

MEASURE = ("\t/// Made-up measure for a test.\n\tmeasure '%s' = %s\n\t\tformatString: #,0.00\n"
           "\t\tdisplayFolder: Finance\\Base\n\n")
SHIP_KEY = ("\tcolumn 'Ship Date Key'\n\t\tdataType: int64\n\t\tisHidden\n\t\tsummarizeBy: none\n"
            "\t\tsourceColumn: Ship Date Key\n\n")
SHIP_RELATIONSHIP = ("\nrelationship SalesToShipDate\n\tisActive: false\n\tfromColumn: Sales.'Ship Date Key'\n"
                     "\ttoColumn: Date.'Date Key'\n")
QUERY = "\t\t\t\tlet\n\t\t\t\t    // Read the made-up source.\n\t\t\t\t    Source = %s\n\t\t\t\tin\n\t\t\t\t    Source\n"
TABLE = ("/// Made-up table for a test.\ntable %(name)s\n\n%(columns)s\tpartition %(name)s = m\n\t\tmode: import\n"
         "\t\tsource =\n" + QUERY % "#table(type table [Id = Int64.Type], {})")
KEY_COLUMN = "\tcolumn '%s'\n\t\tdataType: int64\n\t\tisHidden\n\t\tsummarizeBy: none\n\t\tsourceColumn: %s\n\n"


class StarCase(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.mkdtemp()
        self.root = os.path.join(self.tmp, "project")
        shutil.copytree(os.path.join(HERE, "fixtures", "star"), self.root)

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def read(self, rel):
        with open(os.path.join(self.root, rel), encoding="utf-8") as fh:
            return fh.read()

    def write(self, rel, text):
        path = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)

    def replace(self, rel, old, new):
        text = self.read(rel)
        self.assertIn(old, text, "test setup: text to replace not found in %s" % rel)
        self.write(rel, text.replace(old, new, 1))

    def measure(self, name, formula):
        self.replace(MEASURES, "\tcolumn Placeholder", MEASURE % (name, formula) + "\tcolumn Placeholder")

    def table(self, name, columns=""):
        self.write(os.path.join(TABLES, "%s.tmdl" % name), TABLE % {"name": name, "columns": columns})
        self.write(MODEL, self.read(MODEL) + "ref table %s\n" % name)

    def ship_date(self):
        """An inactive second relationship from Sales to Date."""
        self.replace(SALES, "\tcolumn Amount", SHIP_KEY + "\tcolumn Amount")
        self.write(RELATIONSHIPS, self.read(RELATIONSHIPS) + SHIP_RELATIONSHIP)

    def role(self, table, rule, extra=""):
        self.write(ROLE, "role Readers\n\tmodelPermission: read\n\n\ttablePermission %s = %s\n%s" % (table, rule, extra))

    def direct_query(self, table=SALES):
        self.replace(table, "\t\tmode: import", "\t\tmode: directQuery")

    def source(self, rel, expression):
        text = self.read(rel)
        start = text.index("\t\t\t\tlet")
        self.write(rel, text[:start] + QUERY % expression)

    def found(self):
        findings, _, _ = cp.run(self.root)
        return findings.items

    def codes(self, level=None):
        return sorted({f[0] for f in self.found() if level is None or f[4] == level})

    def assertFinds(self, code, level):
        """The code is reported, at the level the standard gives it."""
        levels = {f[4] for f in self.found() if f[0] == code}
        self.assertEqual(levels, {level}, "%s: expected level %r, found %r; all codes %s"
                         % (code, level, levels, self.codes()))

    def assertNot(self, code):
        self.assertNotIn(code, self.codes())


class CleanStar(StarCase):
    def test_star_is_clean(self):
        self.assertEqual(self.found(), [])


class Integrity(StarCase):
    def test_M901_relationship_to_a_missing_column_fails(self):
        self.replace(RELATIONSHIPS, "Store.'Store Key'", "Store.'Missing Key'")
        self.assertFinds("M901", False)

    def test_M902_hierarchy_level_on_a_missing_column_fails(self):
        self.replace(DATE, "\t\t\tcolumn: Year", "\t\t\tcolumn: Decade")
        self.assertFinds("M902", False)

    def test_M903_sort_by_a_missing_column_fails(self):
        self.replace(DATE, "sortByColumn: 'Month Number'", "sortByColumn: 'Month Order'")
        self.assertFinds("M903", False)

    def test_M904_data_column_without_source_column_fails(self):
        self.replace(STORE, "\t\tsourceColumn: City\n", "")
        self.assertFinds("M904", False)

    def test_M905_measure_with_empty_expression_fails(self):
        self.replace(MEASURES, "\tcolumn Placeholder", "\t/// Empty.\n\tmeasure 'Empty One' =\n\t\tformatString: 0\n"
                     "\t\tdisplayFolder: Finance\\Base\n\n\tcolumn Placeholder")
        self.assertFinds("M905", False)

    def test_M906_control_character_in_a_description_fails(self):
        self.replace(STORE, "/// Name of the store.", "/// Name of the\x07 store.")
        self.assertFinds("M906", False)

    def test_M907_mdx_off_on_a_sort_column_fails(self):
        self.replace(DATE, "\t\tsourceColumn: Month Number\n", "\t\tsourceColumn: Month Number\n\t\tisAvailableInMdx: false\n")
        self.assertFinds("M907", False)
        self.replace(DATE, "\t\tsourceColumn: Month Number\n\t\tisAvailableInMdx: false\n", "\t\tsourceColumn: Month Number\n")
        self.replace(SALES, "\t\tsourceColumn: Amount\n", "\t\tsourceColumn: Amount\n\t\tisAvailableInMdx: false\n")
        self.assertNot("M907")

    def test_M908_formula_naming_a_missing_column_fails(self):
        self.measure("Total Cost", "SUM ( Sales[Cost] )")
        self.assertFinds("M908", False)

    def test_M908_column_named_only_inside_text_or_a_comment_passes(self):
        self.measure("Total Note", 'IF ( [Total Sales] > 0, "Sales[Cost]" ) // Sales[Cost]')
        self.assertNot("M908")

    def test_M909_unknown_function_warns(self):
        self.measure("Total Odd", "SUMMIFY ( Sales[Amount] )")
        self.assertFinds("M909", "warn")


class Dates(StarCase):
    AUTO = ("table LocalDateTable_0a1b\n\tisHidden\n\tshowAsVariationsOnly\n\n\tcolumn Date\n\t\tdataType: dateTime\n"
            "\t\tisHidden\n\t\tsourceColumn: [Date]\n\n\tpartition LocalDateTable_0a1b = calculated\n\t\tmode: import\n"
            "\t\tsource = Calendar(Date(2024,1,1), Date(2024,12,31))\n")

    def test_M401_auto_date_time_tables_warn(self):
        self.write(os.path.join(TABLES, "LocalDateTable_0a1b.tmdl"), self.AUTO)
        self.assertFinds("M401", "warn")

    def test_M401_annotation_that_desktop_writes_warns(self):
        self.write(MODEL, self.read(MODEL) + "\nannotation __PBI_TimeIntelligenceEnabled = 1\n")
        self.assertFinds("M401", "warn")
        self.replace(MODEL, "__PBI_TimeIntelligenceEnabled = 1", "__PBI_TimeIntelligenceEnabled = 0")
        self.assertNot("M401")

    def test_M402_time_intelligence_without_a_date_table_fails(self):
        self.replace(DATE, "\tdataCategory: Time\n", "")
        self.assertFinds("M402", False)
        self.assertFinds("M404", "warn")

    def test_M403_date_columns_without_a_date_table_warn(self):
        self.replace(DATE, "\tdataCategory: Time\n", "")
        self.replace(MEASURES, "DATESYTD ( 'Date'[Date] )", "Store[City] = \"Utrecht\"")
        self.assertFinds("M403", "warn")
        self.assertNot("M402")


class Relationships(StarCase):
    def test_M405_both_directions_warns_and_the_brief_excuses_it(self):
        self.replace(RELATIONSHIPS, "relationship SalesToStore\n", "relationship SalesToStore\n\tcrossFilteringBehavior: bothDirections\n")
        self.assertFinds("M405", "warn")
        self.write(os.path.join("docs", "report-brief.md"), "## 9. Exceptions to the model standard\n\n| Code | Object | Reason |\n"
                   "|---|---|---|\n| M405 | Sales[Store Key] to Store[Store Key] | The store slicer must show only stores with sales |\n")
        self.assertNot("M405")

    def test_M406_M407_M408_many_to_many(self):
        self.replace(RELATIONSHIPS, "relationship SalesToStore\n", "relationship SalesToStore\n\ttoCardinality: many\n")
        self.assertFinds("M406", "warn")
        self.assertFinds("M408", "warn")
        self.assertNot("M407")
        self.replace(RELATIONSHIPS, "\ttoCardinality: many\n", "\ttoCardinality: many\n\tcrossFilteringBehavior: bothDirections\n")
        self.assertFinds("M407", "warn")

    def test_M409_one_to_one_warns(self):
        self.replace(RELATIONSHIPS, "relationship SalesToStore\n", "relationship SalesToStore\n\tfromCardinality: one\n")
        self.assertFinds("M409", "warn")

    def test_M410_inactive_relationship_nothing_uses_warns(self):
        self.ship_date()
        self.assertFinds("M410", "warn")
        self.measure("Shipped Sales", "CALCULATE ( [Total Sales], USERELATIONSHIP ( Sales[Ship Date Key], 'Date'[Date Key] ) )")
        self.assertNot("M410")

    def test_M411_table_without_a_relationship_warns(self):
        self.table("Notes")
        self.assertFinds("M411", "warn")

    def test_M412_snowflake_warns(self):
        self.table("Region", KEY_COLUMN % ("Region Key", "Region Key"))
        self.replace(os.path.join(TABLES, "Region.tmdl"), "\t\tisHidden\n", "\t\tisHidden\n\t\tisKey\n")
        self.replace(STORE, "\t/// Name of the store.", KEY_COLUMN % ("Region Key", "Region Key") + "\t/// Name of the store.")
        self.write(RELATIONSHIPS, self.read(RELATIONSHIPS) + "\nrelationship StoreToRegion\n\tfromColumn: Store.'Region Key'\n"
                   "\ttoColumn: Region.'Region Key'\n")
        self.assertFinds("M412", "warn")

    def test_M413_one_side_not_marked_as_key_warns(self):
        self.replace(STORE, "\t\tisHidden\n\t\tisKey\n", "\t\tisHidden\n")
        self.assertFinds("M413", "warn")

    def test_M414_roles_with_an_inactive_relationship_warn(self):
        self.ship_date()
        self.role("Store", 'Store[City] = "Utrecht"')
        self.assertFinds("M414", "warn")

    def test_M415_userelationship_towards_a_secured_table_fails(self):
        self.ship_date()
        self.role("Date", "'Date'[Year] = 2024")
        self.measure("Shipped Sales", "CALCULATE ( [Total Sales], USERELATIONSHIP ( Sales[Ship Date Key], 'Date'[Date Key] ) )")
        self.assertFinds("M415", False)

    def test_M417_a_column_for_each_month_warns(self):
        months = "January February March April May June July August September October November December".split()
        columns = "".join("\tcolumn %s\n\t\tdataType: decimal\n\t\tisHidden\n\t\tsummarizeBy: none\n\t\tsourceColumn: %s\n\n" % (m, m)
                          for m in months)
        self.replace(SALES, "\tcolumn Amount", columns + "\tcolumn Amount")
        self.assertFinds("M417", "warn")


class Columns(StarCase):
    def test_M113_month_name_without_sort_column_warns(self):
        self.replace(DATE, "\t\tsortByColumn: 'Month Number'\n", "")
        self.assertFinds("M113", "warn")

    def test_M114_place_without_data_category_warns(self):
        self.replace(STORE, "\t\tdataCategory: City\n", "")
        self.assertFinds("M114", "warn")

    def test_M115_column_repeated_in_the_related_table_warns(self):
        self.replace(SALES, "\tcolumn Amount", "\tcolumn City\n\t\tdataType: string\n\t\tisHidden\n\t\tsummarizeBy: none\n"
                     "\t\tsourceColumn: City\n\n\tcolumn Amount")
        self.assertFinds("M115", "warn")

    def test_M116_flag_column_as_a_number_warns(self):
        self.replace(STORE, "\t/// City the store is in.", "\t/// Whether the store is open.\n\tcolumn 'Is Open'\n\t\tdataType: int64\n"
                     "\t\tformatString: 0\n\t\tsummarizeBy: none\n\t\tsourceColumn: Is Open\n\n\t/// City the store is in.")
        self.assertFinds("M116", "warn")

    def test_M117_partition_named_differently_from_its_table_warns(self):
        self.replace(STORE, "\tpartition Store = m", "\tpartition Shops = m")
        self.assertFinds("M117", "warn")

    def test_M118_code_style_table_or_column_name_warns(self):
        self.replace(STORE, "column 'Store Name'", "column store_name")
        self.assertFinds("M118", "warn")

    def test_M118_hidden_key_keeps_its_source_name(self):
        self.replace(STORE, "column 'Store Key'", "column StoreKey")
        self.replace(RELATIONSHIPS, "Store.'Store Key'", "Store.StoreKey")
        self.assertNot("M118")

    def test_M119_column_named_like_a_hierarchy_warns(self):
        self.replace(DATE, "\thierarchy Calendar\n", "\thierarchy Year\n")
        self.assertFinds("M119", "warn")


class DaxStyle(StarCase):
    def style(self, formula):
        self.measure("Test Measure", formula)
        return " ".join(f[3] for f in self.found() if f[0] == "M520")

    def test_M520_is_a_warning_and_names_the_formula(self):
        self.measure("Test Measure", "SUM(Sales[Amount]) * 2")
        self.assertFinds("M520", "warn")
        self.assertIn("[Test Measure]", self.style("1"))

    def test_M520_each_rule(self):
        for formula, words in (("SUM(Sales[Amount]) * 2", "space between a function name"),
                               ("SUM ( Sales[Amount]) * 2", "space before ')'"),
                               ("[Total Sales]*2", "both sides of an operator"),
                               ("[Total Sales] ( Store[City] = \"Utrecht\" )", "CALCULATE in full"),
                               ("SUM ( Sales [Amount] ) * 2", "directly after its table"),
                               ("DIVIDE ( [Total Sales], 2 ) * 2", "each argument on its own line"),
                               ("COUNTROWS ( VALUES ( Store[City] ) ) * 2", "holds another function"),
                               ("COUNTROWS ( ADDCOLUMNS ( Store, \"Sales\", [Total Sales] ) )", "with @")):
            with self.subTest(formula=formula):
                self.setUp()
                self.assertIn(words, self.style(formula))

    def test_formula_in_the_style_passes(self):
        self.replace(MEASURES, "\tcolumn Placeholder", "\t/// Made-up measure for a test.\n\tmeasure 'Sales Share' =\n"
                     "\t\t\tVAR Total =\n\t\t\t    CALCULATE (\n\t\t\t        [Total Sales],\n\t\t\t        REMOVEFILTERS ( Store )\n"
                     "\t\t\t    )\n\t\t\tRETURN\n\t\t\t    DIVIDE (\n\t\t\t        [Total Sales] - 1,\n\t\t\t        Total\n\t\t\t    )\n"
                     "\t\tformatString: 0.0%\n\t\tdisplayFolder: Finance\\Ratios\n\n\tcolumn Placeholder")
        self.assertEqual(self.codes(), [])

    def test_M520_is_excused_by_a_row_in_the_brief(self):
        self.measure("Test Measure", "SUM(Sales[Amount]) * 2")
        self.write(os.path.join("docs", "report-brief.md"), "## 9. Exceptions to the model standard\n\n| Code | Object | Reason |\n"
                   "|---|---|---|\n| M520 | [Test Measure] | Pasted from the finance team, kept as they wrote it |\n")
        self.assertNot("M520")


class Dax(StarCase):
    def check(self, code, level, formula, good=None):
        self.measure("Test Measure", formula)
        self.assertFinds(code, level)
        if good is not None:
            self.replace(MEASURES, formula, good)
            self.assertNot(code)

    def test_M501_iferror(self):
        self.check("M501", "warn", "IFERROR ( [Total Sales] * 2, 0 )", "[Total Sales] * 2")

    def test_M502_division_sign_fails_and_a_fixed_divisor_passes(self):
        self.check("M502", False, "[Total Sales] / [Total Sales YTD]", "[Total Sales] / 1000")

    def test_M502_slash_inside_text_a_name_or_a_comment_is_not_a_division(self):
        self.measure("Test Measure", 'IF ( [Total Sales] > 0, "a/b" ) // one/two')
        self.assertNot("M502")

    def test_M503_count_of_a_column(self):
        self.check("M503", "warn", "COUNT ( Sales[Amount] )", "COUNTROWS ( Sales )")

    def test_M504_hasonevalue_with_values(self):
        self.check("M504", "warn", "IF ( HASONEVALUE ( Store[City] ), VALUES ( Store[City] ) )", "SELECTEDVALUE ( Store[City] )")

    def test_M505_filter_over_a_whole_table(self):
        self.check("M505", "warn", 'CALCULATE ( [Total Sales], FILTER ( Store, Store[City] = "Utrecht" ) )',
                   'CALCULATE ( [Total Sales], Store[City] = "Utrecht" )')

    def test_M505_filter_over_values_of_a_column_passes(self):
        self.measure("Test Measure", "CALCULATE ( [Total Sales], FILTER ( VALUES ( Store[City] ), [Total Sales] > 100 ) )")
        self.assertNot("M505")

    def test_M506_blank_turned_into_zero(self):
        self.check("M506", "warn", "IF ( ISBLANK ( [Total Sales] ), 0, [Total Sales] )", "[Total Sales] * 1")
        self.replace(MEASURES, "[Total Sales] * 1", "[Total Sales] + 0")
        self.assertFinds("M506", "warn")

    def test_M507_expression_written_twice(self):
        twice = ("CALCULATE ( [Total Sales], Store[City] = \"Utrecht\" ) - CALCULATE ( [Total Sales], Store[City] = \"Utrecht\" ) * 0.1")
        once = "VAR Local = CALCULATE ( [Total Sales], Store[City] = \"Utrecht\" ) RETURN Local - Local * 0.1"
        self.check("M507", "warn", twice, once)

    def test_M508_two_measures_with_one_formula(self):
        self.measure("Test Measure", "sum(Sales[Amount])   // same as Total Sales, other spacing")
        self.assertFinds("M508", "warn")

    def test_M509_measure_that_only_repeats_another(self):
        self.check("M509", "warn", "[Total Sales YTD]", "[Total Sales YTD] * 2")

    def test_M510_intersect(self):
        self.check("M510", "warn", "CALCULATE ( [Total Sales], INTERSECT ( VALUES ( Store[City] ), VALUES ( Store[City] ) ) )")

    def test_M511_one_minus_a_ratio(self):
        self.check("M511", "warn", "1 - DIVIDE ( [Total Sales], [Total Sales YTD] )",
                   "DIVIDE ( [Total Sales YTD] - [Total Sales], [Total Sales YTD] )")

    def test_M511_one_minus_a_division(self):
        self.measure("Test Measure", "1 - SUM ( Sales[Amount] ) / 1000")
        self.assertFinds("M511", "warn")

    def test_M010_also_reads_role_rules_and_calculation_items(self):
        self.role("Store", '[City] = "Utrecht"')
        self.assertFinds("M010", "warn")
        self.assertIn("role 'Readers', table 'Store'", " ".join(f[3] for f in self.found() if f[0] == "M010"))

    def test_M512_evaluateandlog(self):
        self.check("M512", "warn", "EVALUATEANDLOG ( [Total Sales] )")

    def test_M513_time_intelligence_in_a_directquery_model(self):
        self.assertNot("M513")
        self.direct_query()
        self.assertFinds("M513", "warn")

    def test_M514_earlier(self):
        self.replace(SALES, "\tpartition Sales = m", "\tcolumn 'Running Rank' = COUNTROWS ( FILTER ( Sales, Sales[Amount] > EARLIER ( Sales[Amount] ) ) )\n"
                     "\t\tdataType: int64\n\t\tisHidden\n\t\tsummarizeBy: none\n\n\t\tannotation CalculatedReason = Made up for a test.\n\n"
                     "\tpartition Sales = m")
        self.assertFinds("M514", "warn")

    def test_M516_window_function_without_orderby(self):
        self.check("M516", "warn", "RANK ( DENSE, ALLSELECTED ( Store[City] ) )",
                   "RANK ( DENSE, ALLSELECTED ( Store[City] ), ORDERBY ( [Total Sales], DESC ) )")

    def test_M517_values_compared_with_one_value(self):
        self.check("M517", "warn", 'IF ( VALUES ( Store[City] ) = "Utrecht", [Total Sales] )',
                   'IF ( SELECTEDVALUE ( Store[City] ) = "Utrecht", [Total Sales] )')


class Security(StarCase):
    def test_M601_text_functions_in_a_rule(self):
        self.role("Store", 'LEFT ( Store[City], 1 ) = "U"')
        self.assertFinds("M601", "warn")

    def test_plain_rule_on_a_dimension_passes(self):
        self.role("Store", 'Store[City] = "Utrecht"')
        self.assertEqual(self.codes(), [])

    def test_M602_rule_on_a_fact_table(self):
        self.role("Sales", "Sales[Amount] > 0")
        self.assertFinds("M602", "warn")

    def test_M603_username(self):
        self.role("Store", "Store[City] = USERNAME ()")
        self.assertFinds("M603", "warn")
        self.role("Store", "Store[City] = USERPRINCIPALNAME ()")
        self.assertNot("M603")

    def test_M604_rule_next_to_a_many_to_many_relationship(self):
        self.replace(RELATIONSHIPS, "relationship SalesToStore\n", "relationship SalesToStore\n\ttoCardinality: many\n")
        self.role("Store", 'Store[City] = "Utrecht"')
        self.assertFinds("M604", "warn")

    def test_M605_rule_that_ends_in_true(self):
        self.role("Store", 'IF ( USERPRINCIPALNAME () = "a@example.com", Store[City] = "Utrecht", TRUE () )')
        self.assertFinds("M605", "warn")

    def test_M606_object_level_security_on_a_field_a_visual_uses(self):
        self.write(ROLE, "role Readers\n\tmodelPermission: read\n\n\ttablePermission Store\n\n\t\tcolumnPermission City = none\n")
        self.assertNot("M606")
        visual = os.path.join("Star.Report", "definition", "pages", "Overview", "visuals", "Overview_Table_Stores", "visual.json")
        self.write(os.path.join("Star.Report", "definition.pbir"),
                   '{"version": "4.0", "datasetReference": {"byPath": {"path": "../Star.SemanticModel"}}}')
        self.write(os.path.join("Star.Report", "definition", "pages", "Overview", "page.json"), '{"name": "Overview"}')
        self.write(visual, '{"name": "Overview_Table_Stores", "visual": {"query": {"queryState": {"Values": {"projections": [{"field": '
                           '{"Column": {"Expression": {"SourceRef": {"Entity": "Store"}}, "Property": "City"}}, "queryRef": "Store.City"}]}}}}}')
        self.assertFinds("M606", "warn")


class ObjectSecurity(StarCase):
    def test_M607_row_rules_and_object_rules_in_different_roles_warn(self):
        self.role("Store", 'Store[City] = "Utrecht"')
        self.assertNot("M607")
        self.write(os.path.join(DEFINITION, "roles", "No Amounts.tmdl"),
                   "role 'No Amounts'\n\tmodelPermission: read\n\n\ttablePermission Sales\n\n\t\tcolumnPermission Amount = none\n")
        self.assertFinds("M607", "warn")

    def test_M608_hidden_table_in_the_middle_of_a_chain_fails(self):
        self.table("Region", KEY_COLUMN % ("Region Key", "Region Key"))
        self.replace(os.path.join(TABLES, "Region.tmdl"), "\t\tisHidden\n", "\t\tisHidden\n\t\tisKey\n")
        self.replace(STORE, "\t/// Name of the store.", KEY_COLUMN % ("Region Key", "Region Key") + "\t/// Name of the store.")
        self.write(RELATIONSHIPS, self.read(RELATIONSHIPS) + "\nrelationship StoreToRegion\n\tfromColumn: Store.'Region Key'\n"
                   "\ttoColumn: Region.'Region Key'\n")
        self.write(ROLE, "role Readers\n\tmodelPermission: read\n\n\ttablePermission Store\n\t\tmetadataPermission: none\n")
        self.assertFinds("M608", False)
        self.write(ROLE, "role Readers\n\tmodelPermission: read\n\n\ttablePermission Region\n\t\tmetadataPermission: none\n")
        self.assertNot("M608")


class Storage(StarCase):
    def test_M701_directquery_native_query_with_a_cte_fails(self):
        self.direct_query()
        self.source(SALES, 'Value.NativeQuery(Sql.Database("server", "db"), "WITH x AS (SELECT 1 AS a) SELECT a FROM x")')
        self.assertFinds("M701", False)
        self.source(SALES, 'Value.NativeQuery(Sql.Database("server", "db"), "SELECT a FROM x")')
        self.assertNot("M701")

    def test_M702_M703_directquery_steps_and_current_date(self):
        self.direct_query()
        self.source(SALES, 'Table.AddColumn(Sql.Database("server", "db"), "Today", each DateTime.LocalNow())')
        self.assertFinds("M702", "warn")
        self.assertFinds("M703", "warn")

    def test_M704_M705_calculated_column_in_a_directquery_table(self):
        self.direct_query()
        self.replace(SALES, "\tcolumn Amount", "\tcolumn 'Store Total' = CALCULATE ( SUM ( Sales[Amount] ) )\n\t\tdataType: decimal\n"
                     "\t\tisHidden\n\t\tsummarizeBy: none\n\n\t\tannotation CalculatedReason = Made up for a test.\n\n\tcolumn Amount")
        self.assertFinds("M705", False)
        self.replace(RELATIONSHIPS, "Sales.'Store Key'", "Sales.'Store Total'")
        self.assertFinds("M704", "warn")

    def test_M706_imported_dimension_of_a_directquery_fact(self):
        self.direct_query()
        self.assertFinds("M706", "warn")
        self.replace(STORE, "\t\tmode: import", "\t\tmode: dual")
        self.replace(DATE, "\t\tmode: import", "\t\tmode: dual")
        self.assertNot("M706")

    POLICY = ("\trefreshPolicy\n\t\tpolicyType: basic\n\t\trollingWindowGranularity: year\n\t\trollingWindowPeriods: 2\n"
              "\t\tincrementalGranularity: day\n\t\tincrementalPeriods: 10\n\t\tsourceExpression =\n"
              "\t\t\t\tlet\n\t\t\t\t    // Read the made-up source.\n\t\t\t\t    Source = %s\n\t\t\t\tin\n\t\t\t\t    Source\n\n")
    PARAMETERS = ("/// Start of the refresh window.\nexpression RangeStart = #datetime(2024, 1, 1, 0, 0, 0) meta [IsParameterQuery=true, "
                  "Type=\"DateTime\", IsParameterQueryRequired=true]\n\n/// End of the refresh window.\nexpression RangeEnd = "
                  "#datetime(2025, 1, 1, 0, 0, 0) meta [IsParameterQuery=true, Type=\"DateTime\", IsParameterQueryRequired=true]\n")

    def test_M707_refresh_policy_without_its_two_parameters_fails(self):
        self.replace(SALES, "\tcolumn 'Date Key'", self.POLICY % 'Sql.Database("server", "db")' + "\tcolumn 'Date Key'")
        self.assertFinds("M707", False)
        self.write(EXPRESSIONS, self.PARAMETERS)
        self.assertNot("M707")

    def test_M707_parameter_that_is_not_a_date_time_fails(self):
        self.write(EXPRESSIONS, self.PARAMETERS.replace('#datetime(2024, 1, 1, 0, 0, 0) meta [IsParameterQuery=true, Type="DateTime"',
                                                        '20240101 meta [IsParameterQuery=true, Type="Number"'))
        self.replace(SALES, "\tcolumn 'Date Key'", self.POLICY % 'Sql.Database("server", "db")' + "\tcolumn 'Date Key'")
        self.assertFinds("M707", False)

    def test_M709_both_ends_of_the_window_included_fails(self):
        self.write(EXPRESSIONS, self.PARAMETERS)
        both = 'Table.SelectRows(Sql.Database("server", "db"), each [OrderDate] >= RangeStart and [OrderDate] <= RangeEnd)'
        self.replace(SALES, "\tcolumn 'Date Key'", self.POLICY % both + "\tcolumn 'Date Key'")
        self.assertFinds("M709", False)
        self.replace(SALES, "[OrderDate] <= RangeEnd", "[OrderDate] < RangeEnd")
        self.assertNot("M709")

    def test_M708_refresh_policy_on_a_native_query_warns(self):
        self.write(EXPRESSIONS, self.PARAMETERS)
        self.replace(SALES, "\tcolumn 'Date Key'", self.POLICY % 'Value.NativeQuery(Sql.Database("server", "db"), "SELECT a FROM x")'
                     + "\tcolumn 'Date Key'")
        self.assertFinds("M708", "warn")


class Objects(StarCase):
    FUNCTION = "/// Adds tax to an amount.\nfunction AddTax = ( amount : NUMERIC, rate : NUMERIC ) => amount * ( 1 + rate )\n"

    def test_good_function_passes(self):
        self.write(FUNCTIONS, self.FUNCTION)
        self.assertEqual(self.codes(), [])

    def test_M801_function_below_level_1702_fails(self):
        self.write(FUNCTIONS, self.FUNCTION)
        self.replace(DATABASE, "compatibilityLevel: 1702", "compatibilityLevel: 1600")
        self.assertFinds("M801", False)

    def test_M802_function_named_like_a_built_in_fails(self):
        self.write(FUNCTIONS, self.FUNCTION.replace("AddTax", "DIVIDE"))
        self.assertFinds("M802", False)

    def test_M803_M804_function_without_description_or_types_warns(self):
        self.write(FUNCTIONS, "function AddTax = (amount, rate : NUMERIC) => amount * ( 1 + rate )\n")
        self.assertFinds("M803", "warn")
        self.assertFinds("M804", "warn")

    def test_M805_function_that_calls_itself_fails(self):
        self.write(FUNCTIONS, self.FUNCTION.replace("amount * ( 1 + rate )", "AddTax ( amount, rate )"))
        self.assertFinds("M805", False)

    GROUP = ("/// Switches a measure between periods.\ntable 'Time Calculation'\n\n\tcalculationGroup\n\t\tprecedence: %s\n\n%s"
             "\t/// The period to show.\n\tcolumn Period\n\t\tdataType: string\n\t\tsummarizeBy: none\n\t\tsourceColumn: Name\n"
             "\t\tsortByColumn: Ordinal\n\n\tcolumn Ordinal\n\t\tdataType: int64\n\t\tisHidden\n\t\tsummarizeBy: none\n"
             "\t\tsourceColumn: Ordinal\n")
    ITEMS = ("\t\t/// The measure as it is.\n\t\tcalculationItem Current = SELECTEDMEASURE ()\n\n"
             "\t\t/// From the start of the year.\n\t\tcalculationItem YTD =\n\t\t\t\tCALCULATE (\n"
             "\t\t\t\t    SELECTEDMEASURE (),\n\t\t\t\t    DATESYTD ( 'Date'[Date] )\n\t\t\t\t)\n\n")

    def group(self, name="Time Calculation", precedence="10", items=None):
        text = self.GROUP % (precedence, self.ITEMS if items is None else items)
        self.write(os.path.join(TABLES, "%s.tmdl" % name), text.replace("'Time Calculation'", "'%s'" % name))
        self.write(MODEL, self.read(MODEL) + "ref table '%s'\n" % name)

    def test_good_calculation_group_passes(self):
        self.group()
        self.assertEqual(self.codes(), [])

    def test_M811_calculation_group_without_items_warns(self):
        self.group(items="")
        self.assertFinds("M811", "warn")

    def test_M812_calculation_item_without_description_warns(self):
        self.group(items="\t\tcalculationItem Current = SELECTEDMEASURE ()\n\n")
        self.assertFinds("M812", "warn")

    def test_M813_two_calculation_groups_with_one_precedence_warn(self):
        self.group()
        self.group(name="Currency Calculation")
        self.assertFinds("M813", "warn")

    def test_M814_calculation_group_without_the_model_switch_warns(self):
        self.group()
        self.replace(MODEL, "\tdiscourageImplicitMeasures\n", "")
        self.assertFinds("M814", "warn")

    PARAMETER = ("/// Lets a reader pick the measure.\ntable 'Sales Metric'\n\n\t/// The measure to show.\n\tcolumn 'Sales Metric'\n"
                 "\t\tdataType: string\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Value1]\n\t\tsortByColumn: 'Sales Metric Order'\n\n"
                 "\t\trelatedColumnDetails\n\t\t\tgroupByColumn: 'Sales Metric Fields'\n\n\tcolumn 'Sales Metric Fields'\n"
                 "\t\tdataType: string\n\t\tisHidden\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Value2]\n"
                 "\t\tsortByColumn: 'Sales Metric Order'\n\n\t\textendedProperty ParameterMetadata = {\"version\":3,\"kind\":2}\n\n"
                 "\tcolumn 'Sales Metric Order'\n\t\tdataType: int64\n\t\tisHidden\n\t\tsummarizeBy: none\n\t\tsourceColumn: [Value3]\n\n"
                 "\tpartition 'Sales Metric' = calculated\n\t\tmode: import\n\t\tsource =\n\t\t\t\t{\n"
                 "\t\t\t\t    (\"Total Sales\", NAMEOF('_Measures'[Total Sales]), 0),\n"
                 "\t\t\t\t    (\"Total Sales YTD\", NAMEOF('_Measures'[Total Sales YTD]), 1)\n\t\t\t\t}\n\n"
                 "\tannotation CalculatedReason = A field parameter is a calculated table by design.\n")

    def parameter(self, text=None):
        self.write(os.path.join(TABLES, "Sales Metric.tmdl"), text or self.PARAMETER)
        self.write(MODEL, self.read(MODEL) + "ref table 'Sales Metric'\n")

    def test_good_field_parameter_passes(self):
        self.parameter()
        self.assertEqual(self.codes(), [])

    def test_M821_field_parameter_naming_a_missing_measure_fails(self):
        self.parameter(self.PARAMETER.replace("[Total Sales YTD])", "[Total Sales QTD])"))
        self.assertFinds("M821", False)

    def test_M822_field_parameter_not_wired_warns(self):
        self.parameter(self.PARAMETER.replace("\t\trelatedColumnDetails\n\t\t\tgroupByColumn: 'Sales Metric Fields'\n\n", ""))
        self.assertFinds("M822", "warn")

    def test_M841_preview_feature_without_the_developers_yes_warns(self):
        self.replace(DATE, "\tpartition Date = m", "\tcalendar 'Shop Calendar'\n\n\t\tcalendarColumnGroup = year\n"
                     "\t\t\tprimaryColumn: Year\n\n\tpartition Date = m")
        self.assertFinds("M841", "warn")
        self.write(os.path.join("docs", "report-brief.md"), "## 11. Preview features and optional tools the developer agreed to\n\n"
                   "| Feature or tool | Agreed by | Date | Notes |\n|---|---|---|---|\n"
                   "| calendar-based time intelligence | A. Developer | 2026-11-11 | fiscal weeks |\n")
        self.assertNot("M841")

    def test_M831_empty_perspective_warns(self):
        self.write(os.path.join(DEFINITION, "perspectives", "Sales Only.tmdl"), "perspective 'Sales Only'\n")
        self.assertFinds("M831", "warn")
        self.write(os.path.join(DEFINITION, "perspectives", "Sales Only.tmdl"), "perspective 'Sales Only'\n\n\tperspectiveTable Date\n\t\tincludeAll\n")
        self.assertNot("M831")


class PowerQuery(StarCase):
    def test_P002_native_query_joined_from_text_warns(self):
        self.source(SALES, 'Sql.Database("server", "db", [Query = "SELECT a FROM x WHERE y = " & Text.From(1)])')
        self.assertFinds("P002", "warn")

    def test_P003_query_that_feeds_two_tables_warns(self):
        self.write(EXPRESSIONS, "/// Staging query for a test.\nexpression Staging =\n\t\tlet\n\t\t    // Read the made-up source.\n"
                   "\t\t    Source = #table(type table [Id = Int64.Type], {})\n\t\tin\n\t\t    Source\n")
        self.source(SALES, "Staging")
        self.assertNot("P003")
        self.source(STORE, "Staging")
        self.assertFinds("P003", "warn")

    def test_P004_dataverse_without_its_options_warns(self):
        self.source(SALES, 'CommonDataService.Database("org.crm.dynamics.com")')
        self.assertFinds("P004", "warn")
        self.source(SALES, 'CommonDataService.Database("org.crm.dynamics.com", [CreateNavigationProperties = false])')
        self.assertNot("P004")

    def test_P005_local_file_warns(self):
        self.source(SALES, 'Csv.Document(File.Contents("C:\\Data\\sales.csv"))')
        self.assertFinds("P005", "warn")

    def test_P006_heavy_reshaping_warns(self):
        self.source(SALES, 'Table.Distinct(Table.Sort(Table.Group(Sql.Database("server", "db"), {"a"}, {}), {"a"}))')
        self.assertFinds("P006", "warn")


class Suggestions(StarCase):
    def test_U001_three_measures_of_one_pattern(self):
        for name in ("North", "South", "East"):
            self.measure("Sales %s" % name, 'CALCULATE ( [Total Sales], Store[City] = "%s", Store[Store Name] <> "x" )' % name)
        self.assertFinds("U001", "note")

    def test_U002_many_time_variants(self):
        for number in range(5):
            self.measure("Sales YTD %d" % number, "CALCULATE ( [Total Sales] * %d, DATESYTD ( 'Date'[Date] ) )" % (number + 2))
        self.assertFinds("U002", "note")

    def test_U003_switch_between_measures(self):
        self.measure("Chosen Sales", 'SWITCH ( SELECTEDVALUE ( Store[City] ), "a", [Total Sales], "b", [Total Sales YTD], [Total Sales] )')
        self.assertFinds("U003", "note")

    def test_U004_directquery_without_aggregations(self):
        self.direct_query()
        self.assertFinds("U004", "note")

    def test_U005_measure_that_returns_formatted_text(self):
        self.measure("Sales Text", 'FORMAT ( [Total Sales], "#,0" )')
        self.assertFinds("U005", "note")

    def test_U006_two_inactive_relationships_to_one_table(self):
        self.ship_date()
        self.replace(SALES, "\tcolumn Amount", SHIP_KEY.replace("Ship Date Key", "Due Date Key") + "\tcolumn Amount")
        self.write(RELATIONSHIPS, self.read(RELATIONSHIPS) + SHIP_RELATIONSHIP.replace("Ship", "Due"))
        self.assertFinds("U006", "note")

    def test_U007_drill_path_without_a_hierarchy(self):
        self.replace(STORE, "\t/// City the store is in.", "\t/// Country the store is in.\n\tcolumn Country\n\t\tdataType: string\n"
                     "\t\tdataCategory: Country\n\t\tsummarizeBy: none\n\t\tsourceColumn: Country\n\n\t/// City the store is in.")
        self.assertFinds("U007", "note")

    def test_suggestions_never_count_as_errors_or_warnings(self):
        self.direct_query()
        self.replace(STORE, "\t\tmode: import", "\t\tmode: dual")
        self.replace(DATE, "\t\tmode: import", "\t\tmode: dual")
        items = [f for f in self.found() if f[0].startswith("U")]
        self.assertTrue(items)
        self.assertTrue(all(f[4] == "note" for f in items))



class ClosingTheCoverage(StarCase):
    """The checks added when the open rows of maintenance/coverage.md were closed."""

    BRIEF_COPILOT = "## 4. Standards to follow\n\n- Power BI Copilot check on (yes or no): yes\n"

    def test_M416_key_that_allows_blanks_is_a_note(self):
        self.replace(STORE, "\t\tisNullable: false\n", "")
        self.assertFinds("M416", "note")

    def test_M609_security_filter_in_both_directions_warns(self):
        self.replace(RELATIONSHIPS, "relationship SalesToStore\n", "relationship SalesToStore\n\tsecurityFilteringBehavior: bothDirections\n")
        self.assertFinds("M609", "warn")

    def test_M120_table_that_shows_more_than_thirty_columns_warns(self):
        columns = "".join("\t/// Made-up column %d.\n\tcolumn 'Trait %d'\n\t\tdataType: string\n\t\tsummarizeBy: none\n"
                          "\t\tsourceColumn: Trait %d\n\n" % (n, n, n) for n in range(31))
        self.replace(STORE, "\tpartition Store = m", columns + "\tpartition Store = m")
        self.assertFinds("M120", "warn")

    def test_M303_dimension_without_a_default_label_only_when_the_brief_asks(self):
        self.assertNot("M303")
        self.write(os.path.join("docs", "report-brief.md"), self.BRIEF_COPILOT)
        self.assertFinds("M303", "note")
        self.replace(STORE, "\tcolumn 'Store Name'\n\t\tdataType: string\n", "\tcolumn 'Store Name'\n\t\tdataType: string\n\t\tisDefaultLabel\n")
        self.assertNot("M303")

    def test_M518_divide_by_a_fixed_number_warns(self):
        self.measure("Sales in Thousands", "DIVIDE ( [Total Sales], 1000 )")
        self.assertFinds("M518", "warn")

    def test_M518_divide_by_a_measure_passes(self):
        self.measure("Sales Share", "DIVIDE ( [Total Sales], [Total Sales YTD] )")
        self.assertNot("M518")

    def test_M519_all_as_a_filter_argument_warns_and_removefilters_passes(self):
        self.measure("Sales All Stores", "CALCULATE ( [Total Sales], ALL ( Store ) )")
        self.assertFinds("M519", "warn")
        self.replace(MEASURES, "ALL ( Store )", "REMOVEFILTERS ( Store )")
        self.assertNot("M519")

    def test_M519_all_inside_filter_passes(self):
        self.measure("Sales Big Stores", "CALCULATE ( [Total Sales], FILTER ( ALL ( Store[City] ), Store[City] <> \"x\" ) )")
        self.assertNot("M519")

    def test_M521_calculate_directly_inside_calculate_warns(self):
        self.measure("Sales Utrecht", 'CALCULATE ( CALCULATE ( [Total Sales], Store[City] = "Utrecht" ), REMOVEFILTERS ( \'Date\' ) )')
        self.assertFinds("M521", "warn")

    def test_M522_summarize_that_adds_a_column_warns(self):
        self.measure("Best City Sales", 'MAXX ( SUMMARIZE ( Sales, Store[City], "@Sales", [Total Sales] ), [@Sales] )')
        self.assertFinds("M522", "warn")
        self.replace(MEASURES, 'SUMMARIZE ( Sales, Store[City], "@Sales", [Total Sales] )',
                     'ADDCOLUMNS ( SUMMARIZE ( Sales, Store[City] ), "@Sales", [Total Sales] )')
        self.assertNot("M522")

    def test_M523_summarizecolumns_with_a_filter_argument_in_a_measure_warns(self):
        self.measure("Cities With Sales", 'COUNTROWS ( SUMMARIZECOLUMNS ( Store[City], TREATAS ( { "Utrecht" }, Store[City] ) ) )')
        self.assertFinds("M523", "warn")
        self.replace(MEASURES, 'SUMMARIZECOLUMNS ( Store[City], TREATAS ( { "Utrecht" }, Store[City] ) )',
                     'CALCULATETABLE ( SUMMARIZECOLUMNS ( Store[City] ), TREATAS ( { "Utrecht" }, Store[City] ) )')
        self.assertNot("M523")

    FUNCTION = "/// Sales of one city.\nfunction CitySales = ( city : STRING ) => CALCULATE ( [Total Sales], %s = city )\n"

    def test_M010_reads_functions_too(self):
        self.write(FUNCTIONS, self.FUNCTION % "[City]")
        self.assertFinds("M010", "warn")
        self.write(FUNCTIONS, self.FUNCTION % "Store[City]")
        self.assertNot("M010")

    def test_M806_function_naming_an_object_a_role_hides_warns(self):
        self.write(FUNCTIONS, self.FUNCTION % "Store[City]")
        self.assertNot("M806")
        self.write(ROLE, "role Readers\n\tmodelPermission: read\n\n\ttablePermission Store\n\n\t\tcolumnPermission City = none\n")
        self.assertFinds("M806", "warn")

    def test_M807_function_and_parameter_names_outside_the_style_warn(self):
        self.write(FUNCTIONS, "/// Adds tax.\nfunction add_tax = ( Amount : NUMERIC ) => Amount * 1.21\n")
        self.assertFinds("M807", "warn")
        self.write(FUNCTIONS, "/// Adds tax.\nfunction Finance.AddTax = ( amount : NUMERIC ) => amount * 1.21\n")
        self.assertNot("M807")

    def test_M711_direct_lake_table_with_a_power_query_partition_warns(self):
        self.replace(SALES, "\t\tmode: import", "\t\tmode: directLake")
        self.assertFinds("M711", "warn")

    LEGACY = ("\tpartition Store = query\n\t\tmode: import\n\t\tdataSource: Warehouse\n\t\tquery = SELECT * FROM Store\n")
    SOURCE = "dataSource Warehouse\n\ttype: %s\n\tconnectionDetails = {\"protocol\":\"tds\"}\n"

    def legacy(self, kind):
        text = self.read(STORE)
        self.write(STORE, text[:text.index("\tpartition Store = m")] + self.LEGACY)
        self.write(os.path.join(DEFINITION, "dataSources.tmdl"), self.SOURCE % kind)

    def test_M833_query_partition_on_a_structured_data_source_fails(self):
        self.legacy("structured")
        self.assertFinds("M833", False)
        self.assertNot("M832")

    def test_M832_data_source_that_no_partition_uses_warns(self):
        self.write(os.path.join(DEFINITION, "dataSources.tmdl"), self.SOURCE % "structured")
        self.assertFinds("M832", "warn")
        self.assertNot("M833")

    CITY_TABLE = ("/// Made-up list of cities.\ntable City\n\n\t/// Name of the city.\n\tcolumn 'City Name'\n\t\tdataType: string\n"
                  "\t\tsummarizeBy: none\n\t\tsourceColumn: [%s]\n\n\tpartition City = calculated\n\t\tmode: import\n"
                  "\t\tsource = SELECTCOLUMNS ( Store, \"City Name\", Store[City] )\n\n"
                  "\tannotation CalculatedReason = A made-up calculated table for a test.\n")

    def test_M910_calculated_table_column_the_formula_does_not_produce_warns(self):
        self.write(os.path.join(TABLES, "City.tmdl"), self.CITY_TABLE % "City Label")
        self.write(MODEL, self.read(MODEL) + "ref table City\n")
        self.assertFinds("M910", "warn")
        self.write(os.path.join(TABLES, "City.tmdl"), self.CITY_TABLE % "City Name")
        self.assertNot("M910")

    def test_P007_loaded_table_that_only_feeds_another_query_warns(self):
        self.table("Staging")
        self.source(SALES, "Staging")
        self.assertFinds("P007", "warn")

    def test_P007_table_a_relationship_uses_passes(self):
        self.source(SALES, "Store")
        self.assertNot("P007")

    def test_U008_directquery_relationship_without_assumed_integrity_is_a_note(self):
        self.direct_query(SALES)
        self.direct_query(STORE)
        self.assertFinds("U008", "note")
        self.replace(RELATIONSHIPS, "relationship SalesToStore\n", "relationship SalesToStore\n\trelyOnReferentialIntegrity\n")
        self.assertNot("U008")


    SECTION_11 = ("## 11. Preview features and optional tools the developer agreed to\n\n"
                  "| Feature or tool | Agreed by | Date | Notes |\n|---|---|---|---|\n| %s | A. Developer | 2026-11-11 | made-up |\n")

    def test_M841_value_filter_behavior_needs_the_developers_yes(self):
        self.replace(MODEL, "\tdiscourageImplicitMeasures\n", "\tdiscourageImplicitMeasures\n\tvalueFilterBehavior: independent\n")
        self.assertFinds("M841", "warn")
        self.write(os.path.join("docs", "report-brief.md"), self.SECTION_11 % "value filter behavior")
        self.assertNot("M841")

    def test_M841_user_context_column_needs_the_developers_yes(self):
        self.replace(STORE, "\tpartition Store = m", "\t/// Store name for the reader.\n\tcolumn 'Store Name Local' = Store[Store Name]\n"
                     "\t\tdataType: string\n\t\tsummarizeBy: none\n\t\texpressionContext: userContext\n\n"
                     "\t\tannotation CalculatedReason = Made-up reason for a test.\n\n\tpartition Store = m")
        self.assertFinds("M841", "warn")
        self.write(os.path.join("docs", "report-brief.md"), self.SECTION_11 % "user-context calculated columns")
        self.assertNot("M841")

    def test_M841_calculated_table_over_direct_lake_needs_the_developers_yes(self):
        self.write(os.path.join(TABLES, "City.tmdl"), self.CITY_TABLE % "City Name")
        self.write(MODEL, self.read(MODEL) + "ref table City\n")
        self.assertNot("M841")
        text = self.read(STORE)
        self.write(STORE, text[:text.index("\tpartition Store = m")] + "\tpartition Store = entity\n\t\tmode: directLake\n"
                   "\t\tsource\n\t\t\tentityName: store\n\t\t\tschemaName: dbo\n\t\t\texpressionSource: Lake\n")
        self.assertFinds("M841", "warn")
        self.write(os.path.join("docs", "report-brief.md"), self.SECTION_11 % "calculated tables over Direct Lake")
        self.assertNot("M841")

    def test_D003_description_above_a_selection_expression_passes(self):
        self.write(os.path.join(TABLES, "Time Calculation.tmdl"),
                   "/// Switches a measure between periods.\ntable 'Time Calculation'\n\n\tcalculationGroup\n\t\tprecedence: 10\n\n"
                   "\t\t/// What a measure shows when no item is picked.\n\t\tnoSelectionExpression = SELECTEDMEASURE ()\n\n"
                   "\t\t/// The measure as it is.\n\t\tcalculationItem Current = SELECTEDMEASURE ()\n\n"
                   "\t/// The period to show.\n\tcolumn Period\n\t\tdataType: string\n\t\tsummarizeBy: none\n\t\tsourceColumn: Name\n")
        self.write(MODEL, self.read(MODEL) + "ref table 'Time Calculation'\n")
        self.assertNot("D003")


    def test_M524_userculture_in_a_calculated_column_warns_and_a_measure_passes(self):
        self.replace(STORE, "\tpartition Store = m", "\t/// Language at refresh time.\n\tcolumn 'Reader Language' = USERCULTURE ()\n"
                     "\t\tdataType: string\n\t\tsummarizeBy: none\n\n\t\tannotation CalculatedReason = Made-up reason for a test.\n\n"
                     "\tpartition Store = m")
        self.assertFinds("M524", "warn")

    LABEL = ('SWITCH (\n\t\t\t    USERCULTURE (),\n\t\t\t    "nl-NL",\n\t\t\t    "Verkoop"%s\n\t\t\t)')

    def label(self, default):
        text = ("\t/// Made-up label for a test.\n\tmeasure 'Sales Label' =\n\t\t\t" + self.LABEL % default
                + "\n\t\tdisplayFolder: Finance\\Base\n\n")
        self.replace(MEASURES, "\tcolumn Placeholder", text + "\tcolumn Placeholder")

    def test_M525_label_without_a_default_warns(self):
        self.write(os.path.join(DEFINITION, "cultures", "nl-NL.tmdl"), "cultureInfo nl-NL\n")
        self.label("")
        self.assertFinds("M525", "warn")
        self.assertNot("M524")

    def test_M525_label_naming_a_culture_without_a_file_warns(self):
        self.label(',\n\t\t\t    "Sales"')
        self.assertFinds("M525", "warn")
        self.write(os.path.join(DEFINITION, "cultures", "nl-NL.tmdl"), "cultureInfo nl-NL\n")
        self.assertNot("M525")


if __name__ == "__main__":
    unittest.main()
