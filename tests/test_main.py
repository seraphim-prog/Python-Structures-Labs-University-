import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from main import (
    STUDENTS, average_grade, count_words, task1, task2, task3, task4,
    tokenize, unique_with_list, unique_with_set,
)


class StructuresTests(unittest.TestCase):
    def test_frequency_normalization_and_apostrophes(self):
        self.assertEqual(count_words("PYTHON, Python! Об’єкт об'єкт обʼєкт."),
                         {"python": 2, "об'єкт": 3})

    def test_empty_input_and_missing_key(self):
        self.assertEqual(count_words("... 123 _"), {})
        self.assertEqual(count_words("").get("немає", 0), 0)

    def test_separators_and_unicode(self):
        self.assertEqual(tokenize("Їжак\nҐанок; дані-слова 123 Python_код"),
                         ["їжак", "ґанок", "дані", "слова", "python", "код"])

    def test_aggregate_uses_every_grade(self):
        self.assertAlmostEqual(average_grade(STUDENTS), 804 / 9)
        self.assertEqual(average_grade([("А", "Г", (100,)), ("Б", "Г", (40, 70))]), 70)

    def test_no_grades(self):
        for records in ([], [("А", "Г", ())]):
            with self.assertRaises(ValueError):
                average_grade(records)

    def test_unique_edge_cases_and_order(self):
        for values, expected in (([], []), ([7], [7]), ([3, 1, 3, 2, 1], [3, 1, 2])):
            self.assertEqual(unique_with_list(values), expected)
            self.assertEqual(unique_with_set(values), set(expected))

    def test_demo_output(self):
        stream = io.StringIO()
        with contextlib.redirect_stdout(stream):
            task1()
            task2()
            task4()
        output = stream.getvalue()
        self.assertIn("[12, 99, 44, 55, 3, 18, 10, 2, 30]", output)
        self.assertIn("89.33", output)
        self.assertIn("TypeError", output)
        self.assertIn("C є підмножиною A: True", output)
        self.assertIn("B є підмножиною A: False", output)

    def test_utf8_file_and_frequency_export(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "input.txt"
            source.write_text("Дані, дані! Захист.", encoding="utf-8-sig")
            with contextlib.redirect_stdout(io.StringIO()):
                task3(source, root / "output", 2)
            result = (root / "output" / "frequencies.tsv").read_text(encoding="utf-8")
            self.assertIn("дані\t2", result)
            self.assertIn("захист\t1", result)


if __name__ == "__main__":
    unittest.main()
