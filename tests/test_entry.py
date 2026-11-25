"""Tests for the one-line resignation letter entry."""

import os
import subprocess
import sys
import tempfile
import unittest

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN_PY = os.path.join(REPO_ROOT, "main.py")

EXPECTED_LINE = (
    "I resign. After 47 retries, the payment gateway finally answered: "
    "'have you tried turning it off and on again?'"
)


class TestEntry(unittest.TestCase):
    def test_line_content_and_length(self):
        self.assertEqual(len(EXPECTED_LINE), 111)
        self.assertLessEqual(len(EXPECTED_LINE), 140)
        self.assertTrue(EXPECTED_LINE.strip())
        self.assertNotIn("\n", EXPECTED_LINE)

    def test_program_writes_valid_entry_txt(self):
        with tempfile.TemporaryDirectory() as tmp:
            out_path = os.path.join(tmp, "entry.txt")
            env = dict(os.environ, MAKEFUN_ENTRY_OUTPUT=out_path)
            proc = subprocess.run(
                [sys.executable, MAIN_PY],
                env=env,
                capture_output=True,
                text=True,
                timeout=30,
            )
            self.assertEqual(proc.returncode, 0, proc.stderr)
            with open(out_path, "r", encoding="utf-8") as fh:
                content = fh.read()
            lines = content.split("\n")
            self.assertEqual(lines[0], EXPECTED_LINE)
            self.assertEqual(lines[1], "")
            self.assertEqual(len(lines[0]), 111)
            self.assertGreaterEqual(len(lines[0]), 1)
            self.assertLessEqual(len(lines[0]), 140)
            mode = os.stat(out_path).st_mode & 0o777
            self.assertEqual(mode, 0o644)

    def test_main_py_is_stdlib_only(self):
        with open(MAIN_PY, "r", encoding="utf-8") as fh:
            source = fh.read()
        self.assertIn("import os", source)
        self.assertNotIn("import requests", source)
        self.assertNotIn("import socket", source)
        self.assertNotIn("urllib", source)


if __name__ == "__main__":
    unittest.main()
