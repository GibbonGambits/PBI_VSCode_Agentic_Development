"""Tests of the one-pass formula scanner (scripts/formula_scanner.py) on hard formulas.

Run from the repository root:
    python -m unittest discover -s tests -v

Every formula here is made up. Each one holds something that fools a plain text search: a comment mark
inside a text value, a bracket inside a table name, a quote inside a name, and so on.
"""
import os
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "scripts"))

import formula_scanner as fs          # noqa: E402

DAX, M = fs.DAX, fs.M


def states(text, language):
    return [(state, text[start:end]) for state, start, end in fs.segments(text, language)]


def kinds(text, language, kind):
    return [token.value for token in fs.tokens(text, language, comments=True) if token.kind == kind]


def references(text):
    return [(table, name) for table, name, _ in fs.dax_references(fs.tokens(text, DAX))]


def call_names(text, language=DAX):
    return [call.name for call in fs.calls(fs.tokens(text, language))]


class SixStates(unittest.TestCase):
    def test_every_character_belongs_to_one_state(self):
        for language, text in ((DAX, "SUM ( 'A b'[c] ) -- x\n/* y */ & \"z\""), (M, 'let a = #"b c"[d] /* e */ in a // f')):
            pieces = fs.segments(text, language)
            self.assertEqual("".join(text[start:end] for _, start, end in pieces), text)
            self.assertTrue(all(state in fs.STATES for state, _, _ in pieces))

    def test_all_six_states_in_one_dax_formula(self):
        text = "CALCULATE ( [Total Sales], 'Sales Orders'[Region] = \"North\" ) // note\n/* block */"
        found = {state for state, _ in states(text, DAX)}
        self.assertEqual(found, set(fs.STATES))

    def test_all_six_states_in_one_power_query(self):
        text = 'let\n    // note\n    #"Kept Rows" = Table.SelectRows(Source, each [Region] = "North") /* block */\nin\n    #"Kept Rows"'
        found = {state for state, _ in states(text, M)}
        self.assertEqual(found, set(fs.STATES))


class HardDax(unittest.TestCase):
    """Hard formulas 1 to 12."""

    def test_01_comment_marks_inside_a_text_value(self):
        text = 'IF ( [Flag] = "a // b -- c /* d */", 1, 0 )'
        self.assertEqual(kinds(text, DAX, fs.TEXT), ["a // b -- c /* d */"])
        self.assertEqual(kinds(text, DAX, fs.LINE_COMMENT) + kinds(text, DAX, fs.BLOCK_COMMENT), [])

    def test_02_web_address_in_text_is_not_a_comment(self):
        text = '"https://example.com/a" & [Path] // real comment'
        self.assertEqual(kinds(text, DAX, fs.TEXT), ["https://example.com/a"])
        self.assertEqual(len(kinds(text, DAX, fs.LINE_COMMENT)), 1)

    def test_03_doubled_quote_inside_a_text_value(self):
        text = '"He said ""no"" [Not A Column]" & [Real]'
        self.assertEqual(kinds(text, DAX, fs.TEXT), ['He said "no" [Not A Column]'])
        self.assertEqual(references(text), [(None, "Real")])

    def test_04_bracket_inside_a_quoted_table_name(self):
        text = "SUM ( 'Sales [2024]'[Amount] )"
        self.assertEqual(references(text), [("Sales [2024]", "Amount")])

    def test_05_apostrophe_inside_a_table_name_and_a_column_name(self):
        text = "COUNTROWS ( 'Owner''s Orders' ) + SUM ( Orders[Customer's Total] )"
        self.assertEqual(kinds(text, DAX, fs.QUOTED_NAME), ["Owner's Orders"])
        self.assertEqual(references(text), [("Orders", "Customer's Total")])

    def test_06_closing_bracket_inside_a_column_name(self):
        text = "SUM ( Sales[Amount [net]]] ) / 2"
        self.assertEqual(references(text), [("Sales", "Amount [net]")])

    def test_07_division_sign_inside_names_text_and_comments_is_not_code(self):
        text = "[Km/h] + 'A/B'[C/D] + \"1/2\" /* 3/4 */ // 5/6\n+ DIVIDE ( 1, 2 )"
        code = fs.blank(text, DAX, keep=(fs.CODE,))
        self.assertNotIn("/", code)

    def test_08_double_minus_is_a_comment_in_dax(self):
        text = "5 -- 3 is not subtracted\n+ 1"
        self.assertEqual([t.value for t in fs.tokens(text, DAX)], ["5", "+", "1"])

    def test_09_keyword_before_a_bracket_is_not_a_table(self):
        text = "VAR Result = [Total Sales]\nRETURN [Total Sales] + Result"
        self.assertEqual(references(text), [(None, "Total Sales"), (None, "Total Sales")])

    def test_10_function_name_inside_a_comment_or_a_name_is_not_a_call(self):
        text = "// IFERROR ( 1 )\n[IFERROR ( x )] + 'IFERROR ( t )'[c] + \"IFERROR ( s )\" + SUM ( T[c] )"
        self.assertEqual(call_names(text), ["SUM"])

    def test_11_nested_calls_and_arguments(self):
        text = "CALCULATE ( SUM ( Sales[Amount] ), FILTER ( ALL ( Sales[Region] ), Sales[Region] = \"N,E\" ), Dates[Year] = 2024 )"
        stream = fs.tokens(text, DAX)
        outer = fs.calls(stream)[0]
        self.assertEqual(outer.name, "CALCULATE")
        self.assertEqual(len(outer.args), 3)
        self.assertEqual(call_names(text), ["CALCULATE", "SUM", "FILTER", "ALL"])

    def test_12_block_comment_over_several_lines_keeps_line_numbers(self):
        text = "/* one\ntwo\nthree */\nSUM ( Sales[Amount] )"
        stream = fs.tokens(text, DAX)
        self.assertEqual(stream[0].value, "SUM")
        self.assertEqual(stream[0].line, 4)

    def test_13_unfinished_text_runs_to_the_end_and_does_not_crash(self):
        text = 'IF ( [A] = "open text, [B] )'
        self.assertEqual(references(text), [(None, "A")])

    def test_14_same_formula_with_other_spacing_and_comments_compares_equal(self):
        first = fs.text_of(fs.tokens("sum(Sales[Amount])  // total", DAX))
        second = fs.text_of(fs.tokens("SUM (\n    sales[amount]\n)", DAX))
        self.assertEqual(first, second)
        third = fs.text_of(fs.tokens('SUM ( Sales[Amount] ) & "sum(Sales[Amount])"', DAX))
        self.assertNotEqual(first, third)


class HardPowerQuery(unittest.TestCase):
    """Hard formulas 15 to 24."""

    def test_15_double_minus_is_not_a_comment_in_power_query(self):
        text = "let a = 5 --3 in a"
        self.assertEqual(kinds(text, M, fs.LINE_COMMENT), [])
        self.assertIn("3", [t.value for t in fs.tokens(text, M)])

    def test_16_apostrophe_is_an_ordinary_character_in_power_query(self):
        text = "let a = \"it's\", b = Text.From(1) in b"
        self.assertEqual(kinds(text, M, fs.QUOTED_NAME), [])
        self.assertEqual(call_names(text, M), ["TEXT.FROM"])

    def test_17_quoted_step_name_with_comment_marks_and_quotes(self):
        text = 'let\n    #"Step // one ""x""" = 1\nin\n    #"Step // one ""x"""'
        self.assertEqual(kinds(text, M, fs.QUOTED_NAME), ['Step // one "x"', 'Step // one "x"'])
        self.assertEqual(kinds(text, M, fs.LINE_COMMENT), [])

    def test_18_record_stays_code_and_field_access_is_a_name(self):
        text = 'Source{[Schema = "dbo", Item = "Sales"]}[Data]'
        self.assertEqual(kinds(text, M, fs.BRACKET_NAME), ["Data"])
        self.assertEqual(kinds(text, M, fs.TEXT), ["dbo", "Sales"])

    def test_19_list_of_fields_and_quoted_field(self):
        text = 'Table.SelectColumns(Source, {"A"}) & Source[[Amount], [#"Net Amount"]]'
        self.assertEqual(kinds(text, M, fs.BRACKET_NAME), ["Amount", "Net Amount"])

    def test_20_steps_of_the_outer_let_only(self):
        text = ("let\n"
                "    // first\n"
                "    Source = let inner = 1, other = 2 in inner + other,\n"
                "    // second\n"
                "    Kept = Table.SelectRows(Source, each let x = [A] in x > 1),\n"
                "    Record = [a = 1, b = 2]\n"
                "in\n"
                "    Kept")
        steps, found = fs.m_steps(text)
        self.assertTrue(found)
        self.assertEqual([s["name"] for s in steps], ["Source", "Kept", "Record"])
        self.assertEqual([s["described"] for s in steps], [True, True, False])

    def test_21_comment_at_the_end_of_the_line_above_does_not_describe_a_step(self):
        text = "let\n    A = 1, // about A\n    B = 2\nin\n    B"
        steps, _ = fs.m_steps(text)
        self.assertEqual([(s["name"], s["described"]) for s in steps], [("A", False), ("B", False)])

    def test_22_block_comment_above_a_step_describes_it_and_a_blank_line_breaks_it(self):
        text = "let\n    /* about A\n       more */\n    A = 1,\n    // about B\n\n    B = 2\nin\n    B"
        steps, _ = fs.m_steps(text)
        self.assertEqual([(s["name"], s["described"]) for s in steps], [("A", True), ("B", False)])

    def test_23_word_let_inside_text_or_a_comment_is_not_a_let(self):
        text = '// let us begin\n"let it be"'
        self.assertEqual(fs.m_steps(text), ([], False))

    def test_24_equals_inside_brackets_is_not_a_step(self):
        text = ("let\n"
                "    // typed table\n"
                "    Source = #table(type table [Id = Int64.Type, Name = text], {{1, \"a = b\"}}),\n"
                "    // each row\n"
                "    Added = Table.AddColumn(Source, \"Flag\", each if [Id] = 1 then \"x\" else \"y\")\n"
                "in\n"
                "    Added")
        steps, _ = fs.m_steps(text)
        self.assertEqual([s["name"] for s in steps], ["Source", "Added"])
        self.assertTrue(all(s["described"] for s in steps))

    def test_25_step_on_the_let_line_is_marked(self):
        steps, _ = fs.m_steps("let A = 1,\n    // about B\n    B = 2\nin B")
        self.assertEqual([(s["name"], s["on_let_line"]) for s in steps], [("A", True), ("B", False)])


if __name__ == "__main__":
    unittest.main()
