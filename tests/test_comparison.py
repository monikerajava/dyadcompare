import unittest

from src.dyadcompare.comparison import compare_text


class CompareTextTests(unittest.TestCase):
    def test_identical_files_are_aligned_as_equal(self):
        rows = compare_text(["alpha", "beta"], ["alpha", "beta"])

        self.assertEqual(
            [(row.left_line, row.left_text, row.right_line, row.right_text, row.kind) for row in rows],
            [
                (1, "alpha", 1, "alpha", "equal"),
                (2, "beta", 2, "beta", "equal"),
            ],
        )

    def test_inserted_line_has_no_original_counterpart(self):
        rows = compare_text(["alpha", "omega"], ["alpha", "new", "omega"])

        self.assertEqual(rows[1].kind, "insert")
        self.assertIsNone(rows[1].left_line)
        self.assertIsNone(rows[1].left_text)
        self.assertEqual((rows[1].right_line, rows[1].right_text), (2, "new"))

    def test_deleted_line_has_no_compared_counterpart(self):
        rows = compare_text(["alpha", "old", "omega"], ["alpha", "omega"])

        deleted = next(row for row in rows if row.kind == "delete")
        self.assertEqual((deleted.left_line, deleted.left_text), (2, "old"))
        self.assertIsNone(deleted.right_line)
        self.assertIsNone(deleted.right_text)

    def test_replaced_lines_are_paired_and_extra_lines_are_unpaired(self):
        rows = compare_text(["old one", "old two"], ["new one"])

        self.assertEqual(
            [(row.left_text, row.right_text, row.kind) for row in rows],
            [("old one", "new one", "replace"), ("old two", None, "replace")],
        )

    def test_two_empty_files_have_no_rows(self):
        self.assertEqual(compare_text([], []), [])

    def test_empty_file_against_content_is_an_insertion(self):
        rows = compare_text([], ["first", "second"])

        self.assertEqual([row.kind for row in rows], ["insert", "insert"])
        self.assertTrue(all(row.left_text is None for row in rows))

    def test_ignore_whitespace_keeps_original_text_and_line_numbers(self):
        rows = compare_text(["a b"], ["ab"], ignore_whitespace=True)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0].kind, "equal")
        self.assertEqual((rows[0].left_text, rows[0].right_text), ("a b", "ab"))
        self.assertEqual((rows[0].left_line, rows[0].right_line), (1, 1))

    def test_ignore_case_uses_casefolding(self):
        rows = compare_text(["Straße"], ["STRASSE"], ignore_case=True)

        self.assertEqual([row.kind for row in rows], ["equal"])

    def test_ignore_blank_lines_preserves_source_line_numbers(self):
        rows = compare_text(["first", "", "last"], ["first", "last"], ignore_blank_lines=True)

        self.assertEqual([row.kind for row in rows], ["equal", "equal"])
        self.assertEqual([(row.left_line, row.right_line) for row in rows], [(1, 1), (3, 2)])


if __name__ == "__main__":
    unittest.main()
