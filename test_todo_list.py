"""Regression test: loading a CSV with blank/malformed rows must skip them.

The module runs an interactive menu at import time, so this test drives a
copy of ``todo_list.py`` as a subprocess instead of importing it.
"""

import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent


class TestLoadCsvSkipsMalformedRows(unittest.TestCase):
    def _run_menu(self, workdir: Path, choices: str) -> str:
        proc = subprocess.run(
            [sys.executable, str(workdir / "todo_list.py")],
            input=choices,
            capture_output=True,
            text=True,
            cwd=workdir,
            timeout=60,
        )
        self.assertEqual(proc.returncode, 0)
        return proc.stdout

    def test_blank_line_does_not_abort_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            shutil.copy(REPO_ROOT / "todo_list.py", workdir / "todo_list.py")
            (workdir / "Historical data.csv").write_text(
                "Name,Description,Priority\n"
                "TaskA,DescA,High\n"
                "\n"
                "TaskB,DescB,Low\n",
                encoding="utf-8",
            )
            # 5 = load from CSV, then 3 = view list, then 6 = exit.
            output = self._run_menu(workdir, "5\n3\n6\n")

        self.assertNotIn("Error loading", output)
        self.assertIn("Skipped 1 malformed row(s).", output)
        # Both valid tasks load, including the one after the blank line.
        self.assertIn("TaskA", output)
        self.assertIn("TaskB", output)

    def test_short_row_does_not_abort_load(self):
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            shutil.copy(REPO_ROOT / "todo_list.py", workdir / "todo_list.py")
            (workdir / "Historical data.csv").write_text(
                "Name,Description,Priority\n"
                "OnlyName\n"
                "TaskC,DescC,Medium\n",
                encoding="utf-8",
            )
            output = self._run_menu(workdir, "5\n3\n6\n")

        self.assertNotIn("Error loading", output)
        self.assertIn("TaskC", output)


if __name__ == "__main__":
    unittest.main()
