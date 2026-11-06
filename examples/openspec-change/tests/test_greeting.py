"""Regression test for the `--name` argument.

Both scenarios of the `greeting` specification are covered: an explicit name, and
the default greeting that existing usage depends on.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _greeting(*args: str) -> str:
    """Run `main.py` and return its standard output."""
    result = subprocess.run(
        [sys.executable, "main.py", *args],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr
    return result.stdout


def test_explicit_name_is_greeted() -> None:
    assert _greeting("--name", "Ada") == "Hello from Ada!\n"


def test_default_greeting_is_unchanged() -> None:
    assert _greeting() == "Hello from script-project!\n"
