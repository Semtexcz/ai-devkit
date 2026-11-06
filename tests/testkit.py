"""Shared helpers and release facts for the integration tests.

`test_template.py` (generation) and `test_update_lifecycle.py` (overlay updates)
drive the same native executables the same way, so the subprocess contract lives
here once. Nothing is mocked: every helper runs a real pinned executable and
reports its captured output when it fails.

The constants describe this release, not a helper: they are the documented
baseline that both test modules must agree on.
"""

from __future__ import annotations

import os
import shutil
import subprocess
from collections.abc import Mapping, Sequence
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]

# The documented uv initialization flags (see the tutorial and the v0.1 plan).
UV_INIT_FLAGS = (
    "--app",
    "--no-package",
    "--no-workspace",
    "--no-pin-python",
    "--no-readme",
    "--vcs",
    "none",
)

# The exact baseline development dependencies of this release.
DEV_DEPENDENCIES = (
    "mypy==2.4.1",
    "pytest==9.2.0",
    "ruff==0.17.3",
    "zensical==0.0.74",
)

# A Git identity for fixture repositories. Passed as `-c` flags, so it applies to
# one command and never reaches the host's global configuration.
GIT_IDENTITY = (
    "-c",
    "user.name=ai-devkit integration test",
    "-c",
    "user.email=integration-test@example.invalid",
)


def executable(name: str) -> str:
    """Return the absolute path of a required executable."""
    path = shutil.which(name)
    if path is None:
        pytest.fail(
            f"`{name}` is required by this integration test; install the pinned "
            "toolchain with `mise install --locked`."
        )
    return path


def run(
    args: Sequence[str],
    cwd: Path,
    *,
    env: Mapping[str, str] | None = None,
    timeout: int = 1800,
) -> subprocess.CompletedProcess[str]:
    """Run one command without a shell and capture its output.

    Standard input is closed, so a tool that decides to prompt fails instead of
    waiting forever in a test run.
    """
    return subprocess.run(
        list(args),
        check=False,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout,
        stdin=subprocess.DEVNULL,
        env={**os.environ, **(env or {})},
    )


def run_ok(
    args: Sequence[str], cwd: Path, *, env: Mapping[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    """Run one command and fail with its output unless it exits with zero."""
    result = run(args, cwd, env=env)
    assert result.returncode == 0, (
        f"command failed with exit code {result.returncode}: {' '.join(args)}\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
    return result


def git_status() -> str:
    """Return `git status --porcelain` for this repository."""
    return run_ok((executable("git"), "status", "--porcelain"), cwd=REPO_ROOT).stdout
