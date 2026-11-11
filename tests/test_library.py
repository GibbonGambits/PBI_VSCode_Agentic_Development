"""Tests of the practice library: the structure of the skill, of every topic file and of the index.

Run from the repository root:
    python -m unittest discover -s tests -v

The library is the skill `pbi-practice-library`. These tests read its files; they change nothing.
"""
import os
import re
import sys
import unittest

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(REPO, "scripts"))

import check_template as ct           # noqa: E402

SKILL = os.path.join(REPO, ".github", "skills", "pbi-practice-library")
REFERENCES = os.path.join(SKILL, "references")
RECORD = os.path.join(REPO, "maintenance", "library-removed.md")
START_COUNT = 2318                    # notes before anything was removed
LINE_LIMIT = 400                      # no library file is longer than about this
WORD_LIMIT = 45                       # a note is one or two lines
SHELVES = ["## General practice", "## Special-case techniques and facts"]
NOTE = re.compile(r"^\*\*(T(\d\d)-[AW]\d{3}-\d+)\.\*\* (\S.*)$")
FACTS = re.compile(r"^- (Must|Should|Consider|Option|Fact)\. (Check\. )?(20[12]\d)\. "
                   r"(https://www\.sqlbi\.com/\S+/(?: ; https://www\.sqlbi\.com/\S+/)*)$")
TOPIC_FILE = re.compile(r"^t(\d\d)-[a-z0-9-]+-(\d+)\.md$")


def read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def topic_files():
    return sorted(name for name in os.listdir(REFERENCES) if name != "index.md")


def notes_of(name):
    """Every note of one topic file: (id, text, the lines under it, shelf)."""
    found = []
    shelf = None
    lines = read(os.path.join(REFERENCES, name)).split("\n")
    for number, line in enumerate(lines):
        if line in SHELVES:
            shelf = line
        m = NOTE.match(line)
        if m:
            under = []
            for nxt in lines[number + 1:]:
                if not nxt.startswith("- "):
                    break
                under.append(nxt)
            found.append((m.group(1), m.group(3), under, shelf))
    return found


class Skill(unittest.TestCase):
    def test_skill_file_meets_the_template_rules(self):
        text = read(os.path.join(SKILL, "SKILL.md"))
        fields = ct.front_matter(text)
        self.assertEqual(fields.get("name"), "pbi-practice-library")
        self.assertTrue(ct.SKILL_NAME.match(fields["name"]))
        self.assertTrue(0 < len(fields.get("description", "")) <= 1024)
        self.assertLessEqual(text.count("\n") + 1, ct.LINE_BUDGET["SKILL.md"])
        self.assertIn("\nChecklist items: none\n", text)

    def test_skill_says_how_the_library_is_used(self):
        text = read(os.path.join(SKILL, "SKILL.md"))
        for words in ("`references/index.md`", "Never read the whole library", "`pbi-lookup`",
                      "checklist", "information"):
            self.assertIn(words, text)

    def test_project_instructions_name_the_skill_once(self):
        text = read(os.path.join(REPO, ".github", "copilot-instructions.md"))
        self.assertEqual(text.count("`pbi-practice-library`"), 1)

    def test_no_file_but_markdown_in_the_library(self):
        for folder, _, files in os.walk(SKILL):
            for name in files:
                self.assertTrue(name.endswith(".md"), name)


class TopicFiles(unittest.TestCase):
    def test_file_names_follow_the_pattern_and_parts_are_numbered_from_one(self):
        parts = {}
        for name in topic_files():
            m = TOPIC_FILE.match(name)
            self.assertTrue(m, name)
            parts.setdefault(name.rsplit("-", 1)[0], []).append(int(m.group(2)))
        self.assertEqual(len(set(key[:3] for key in parts)), len(parts), "one file name stem for each topic")
        for stem, numbers in parts.items():
            self.assertEqual(sorted(numbers), list(range(1, len(numbers) + 1)), stem)

    def test_no_file_is_longer_than_the_limit(self):
        for name in topic_files() + ["index.md"]:
            lines = read(os.path.join(REFERENCES, name)).count("\n")
            self.assertLessEqual(lines, LINE_LIMIT, name)

    def test_every_file_explains_the_check_mark_at_the_top_and_has_two_shelves(self):
        for name in topic_files():
            lines = read(os.path.join(REFERENCES, name)).split("\n")
            self.assertTrue(lines[0].startswith("# "), name)
            top = "\n".join(lines[:8])
            self.assertIn("**Check**", top, name)
            self.assertIn("`pbi-lookup`", top, name)
            self.assertEqual([line for line in lines if line.startswith("## ")], SHELVES, name)

    def test_every_note_has_its_facts_on_short_lines(self):
        count = 0
        for name in topic_files():
            for note, text, under, shelf in notes_of(name):
                count += 1
                where = "%s %s" % (name, note)
                self.assertIsNotNone(shelf, where)
                self.assertLessEqual(len(text.split()), WORD_LIMIT, where)
                self.assertTrue(len(under) in (2, 3), where)
                self.assertTrue(FACTS.match(under[0]), where)
                self.assertTrue(under[1].startswith("- When: ") and len(under[1]) > 10, where)
                if len(under) == 3:
                    self.assertTrue(under[2].startswith("- Version: ") and len(under[2]) > 13, where)
        self.assertGreater(count, 0)

    def test_a_fact_stands_on_the_second_shelf(self):
        for name in topic_files():
            for note, _, under, shelf in notes_of(name):
                if under and under[0].startswith("- Fact."):
                    self.assertEqual(shelf, SHELVES[1], "%s %s" % (name, note))

    def test_note_ids_are_unique_and_sit_in_their_topic(self):
        seen = {}
        for name in topic_files():
            for note, _, _, _ in notes_of(name):
                self.assertNotIn(note, seen, "%s is in %s and %s" % (note, seen.get(note), name))
                seen[note] = name
                self.assertEqual(note[1:3], name[1:3], "%s in %s" % (note, name))

    def test_every_line_that_looks_like_a_note_is_one(self):
        for name in topic_files():
            for line in read(os.path.join(REFERENCES, name)).split("\n"):
                if line.startswith("**T"):
                    self.assertTrue(NOTE.match(line), "%s: %s" % (name, line[:40]))

    def test_no_code_block_and_no_image_in_the_library(self):
        for name in topic_files() + ["index.md"]:
            text = read(os.path.join(REFERENCES, name))
            self.assertNotIn("```", text, name)
            self.assertNotIn("![", text, name)


class Index(unittest.TestCase):
    def test_index_lists_every_topic_file_once_and_nothing_else(self):
        text = read(os.path.join(REFERENCES, "index.md"))
        listed = re.findall(r"^### `([^`]+)` \((\d+) notes\)$", text, re.M)
        self.assertEqual(sorted(name for name, _ in listed), topic_files())
        for name, count in listed:
            self.assertEqual(int(count), len(notes_of(name)), name)

    def test_every_entry_says_what_the_file_covers_and_mentions(self):
        text = read(os.path.join(REFERENCES, "index.md"))
        for block in text.split("\n### ")[1:]:
            name = block.split("`")[1]
            for label in ("- Covers: ", "- DAX functions: ", "- Features: "):
                self.assertIn("\n" + label, block, name)

    def test_functions_named_in_the_index_are_in_the_function_index(self):
        known = set(re.findall(r"^- ([A-Z][A-Z0-9.]*):", read(os.path.join(
            REPO, ".github", "skills", "pbi-semantic-model", "references", "dax-functions.md")), re.M))
        text = read(os.path.join(REFERENCES, "index.md"))
        for line in re.findall(r"^- DAX functions: (.*)\.$", text, re.M):
            if line == "none named":
                continue
            for name in line.split(", "):
                self.assertIn(name, known)


class Record(unittest.TestCase):
    """maintenance/library-removed.md: one row for each note that was removed, by ID only."""

    def rows(self):
        return re.findall(r"^\| (T\d\d-[AW]\d{3}-\d+) \| ([1-5]) \| (.+) \|$", read(RECORD), re.M)

    def test_kept_and_removed_add_up_to_the_start(self):
        kept = set(note for name in topic_files() for note, _, _, _ in notes_of(name))
        removed = [row[0] for row in self.rows()]
        self.assertEqual(len(removed), len(set(removed)))
        self.assertFalse(kept & set(removed))
        self.assertEqual(len(kept) + len(removed), START_COUNT)

    def test_every_covering_file_exists(self):
        for note, group, where in self.rows():
            if group == "1":
                continue
            m = re.match(r"^`([^`]+)`", where)
            self.assertTrue(m, note)
            self.assertTrue(os.path.isfile(os.path.join(REPO, m.group(1))), "%s: %s" % (note, m.group(1)))


if __name__ == "__main__":
    unittest.main()
