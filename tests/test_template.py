"""End-to-end integration test for the first-project workflow.

Nothing is mocked. The test runs the pinned `mise`, `uv`, `git` and Copier
executables and follows the documented recipe in
`docs/tutorials/first-python-project.md`:

1. native `uv init` creates an unpackaged application in a directory whose name
   contains spaces, outside this repository;
2. the Copier overlay is applied from a tagged template source;
3. the baseline development dependencies are installed with `uv add`;
4. the documented project-owned annotation is added to `main.py`;
5. the project's own lockfiles are generated with native commands;
6. the entry point, the smoke test and `mise run check` are executed;
7. file ownership, isolation and failure detection are asserted.

The workflow reads no agent configuration and no credential store: it uses only
`mise`, `uv`, `git`, Copier and the files it creates in a temporary directory.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tomllib
from collections.abc import Sequence
from dataclasses import dataclass
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

# Files the overlay must provide.
OVERLAY_FILES = (
    ".copier-answers.yml",
    ".gitignore",
    "AGENTS.md",
    "README.md",
    "docs/explanation/ownership.md",
    "docs/how-to/add-a-dependency.md",
    "docs/how-to/update-the-overlay.md",
    "docs/index.md",
    "docs/reference/commands.md",
    "docs/tutorials/run-the-script.md",
    "mise.toml",
    "mypy.ini",
    "pytest.ini",
    "ruff.toml",
    "tests/test_main.py",
    "zensical.toml",
)

# Files that uv and the project developer own; the overlay must never render them.
FORBIDDEN_TEMPLATE_FILES = ("main.py", "pyproject.toml", "uv.lock", ".python-version")

# A tag for the temporary template repository. No real ai-devkit release tag is
# created, moved or pushed by this test.
TEST_TAG = "v0.0.0"

GIT_IDENTITY = (
    "-c",
    "user.name=ai-devkit integration test",
    "-c",
    "user.email=integration-test@example.invalid",
)

# The one project-owned edit the native scaffold requires: the pinned uv defines
# `def main():` without a return annotation, which `mypy --strict` rejects.
SCAFFOLD_ENTRY_POINT = "def main():\n"
ANNOTATED_ENTRY_POINT = "def main() -> None:\n"


@dataclass(frozen=True)
class GeneratedProject:
    """Evidence collected while creating and verifying the project."""

    destination: Path
    template_repo: Path
    scaffold_main: str
    overlay_main: str
    scaffold_pyproject: str
    overlay_pyproject: str
    git_status_before: str


def _which(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        pytest.fail(
            f"`{name}` is required by this integration test; install the pinned "
            "toolchain with `mise install --locked`."
        )
    return path


def _run(
    args: Sequence[str], cwd: Path, *, timeout: int = 1800
) -> subprocess.CompletedProcess[str]:
    """Run one command without a shell and capture its output."""
    return subprocess.run(
        list(args),
        check=False,
        cwd=str(cwd),
        capture_output=True,
        text=True,
        timeout=timeout,
        env=dict(os.environ),
    )


def _run_ok(args: Sequence[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    result = _run(args, cwd)
    assert result.returncode == 0, (
        f"command failed with exit code {result.returncode}: {' '.join(args)}\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )
    return result


def _git_status() -> str:
    """Return `git status --porcelain` for this repository."""
    return _run_ok((_which("git"), "status", "--porcelain"), cwd=REPO_ROOT).stdout


@pytest.fixture(scope="module")
def generated_project(tmp_path_factory: pytest.TempPathFactory) -> GeneratedProject:
    """Create the project once with the real tools, then verify it per scenario."""
    mise = _which("mise")
    git = _which("git")

    base = tmp_path_factory.mktemp("first-python-project")

    # A temporary git repository holding the devkit's template source, tagged so
    # that Copier records a version. It stands in for a real ai-devkit release.
    template_repo = base / "ai-devkit template"
    template_repo.mkdir()
    shutil.copy2(REPO_ROOT / "copier.yml", template_repo / "copier.yml")
    shutil.copytree(
        REPO_ROOT / "templates",
        template_repo / "templates",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    _run_ok((git, "init", "--quiet"), cwd=template_repo)
    # Acceptance-platform files are not executable; record that in the fixture so
    # rendered files inherit the same mode instead of this host's mount defaults.
    _run_ok((git, "config", "core.fileMode", "false"), cwd=template_repo)
    _run_ok((git, "add", "--all"), cwd=template_repo)
    _run_ok(
        (git, *GIT_IDENTITY, "commit", "--quiet", "-m", "overlay fixture"),
        cwd=template_repo,
    )
    _run_ok((git, "tag", TEST_TAG), cwd=template_repo)

    git_status_before = _git_status()

    # 1. Native uv initialization. The destination contains a space and lives
    #    outside this repository.
    destination = base / "script project"
    _run_ok(
        (mise, "exec", "--", "uv", "init", *UV_INIT_FLAGS, str(destination)),
        cwd=REPO_ROOT,
    )
    scaffold_main = (destination / "main.py").read_text(encoding="utf-8")
    scaffold_pyproject = (destination / "pyproject.toml").read_text(encoding="utf-8")

    # 2. The Copier overlay, applied from the tagged template source.
    _run_ok(
        (
            mise,
            "exec",
            "--",
            "uv",
            "run",
            "--locked",
            "copier",
            "copy",
            "--vcs-ref",
            TEST_TAG,
            "--defaults",
            str(template_repo),
            str(destination),
        ),
        cwd=REPO_ROOT,
    )
    overlay_main = (destination / "main.py").read_text(encoding="utf-8")
    overlay_pyproject = (destination / "pyproject.toml").read_text(encoding="utf-8")

    # 3. Baseline development dependencies, installed by uv inside the project so
    #    that the project's own mise.toml selects the pinned Python and uv.
    _run_ok(
        (mise, "exec", "--", "uv", "add", "--dev", *DEV_DEPENDENCIES), cwd=destination
    )

    # 4. The documented project-owned edit. Copier never makes this edit.
    assert SCAFFOLD_ENTRY_POINT in overlay_main
    (destination / "main.py").write_text(
        overlay_main.replace(SCAFFOLD_ENTRY_POINT, ANNOTATED_ENTRY_POINT, 1),
        encoding="utf-8",
    )

    # 5. Native lockfile generation and verification.
    _run_ok((mise, "exec", "--", "uv", "lock"), cwd=destination)
    _run_ok((mise, "exec", "--", "uv", "lock", "--check"), cwd=destination)

    # 6. The entry point, the smoke test and the project's own verification.
    _run_ok(
        (mise, "exec", "--", "uv", "run", "--locked", "python", "main.py"),
        cwd=destination,
    )
    smoke = _run_ok(
        (mise, "exec", "--", "uv", "run", "--locked", "pytest"), cwd=destination
    )
    assert "1 passed" in smoke.stdout, smoke.stdout
    _run_ok((mise, "run", "check"), cwd=destination)

    return GeneratedProject(
        destination=destination,
        template_repo=template_repo,
        scaffold_main=scaffold_main,
        overlay_main=overlay_main,
        scaffold_pyproject=scaffold_pyproject,
        overlay_pyproject=overlay_pyproject,
        git_status_before=git_status_before,
    )


def test_generated_project_has_working_checks(
    generated_project: GeneratedProject,
) -> None:
    """Scenario A: the generated project runs, tests and verifies itself."""
    destination = generated_project.destination
    assert " " in destination.name, "the destination must exercise spaces in its path"

    for relative in OVERLAY_FILES:
        assert (destination / relative).is_file(), f"missing overlay file: {relative}"

    app = _run_ok(
        (_which("mise"), "exec", "--", "uv", "run", "--locked", "python", "main.py"),
        cwd=destination,
    )
    assert app.stdout.strip(), "the entry point produced no output"


def test_dependencies_are_exact_and_locked(generated_project: GeneratedProject) -> None:
    """Scenario A: the release's baseline versions are recorded by uv itself."""
    pyproject_path = generated_project.destination / "pyproject.toml"
    pyproject = tomllib.loads(pyproject_path.read_text(encoding="utf-8"))

    assert pyproject["project"]["name"] == "script-project"
    assert pyproject["project"]["dependencies"] == []
    assert set(pyproject["dependency-groups"]["dev"]) == set(DEV_DEPENDENCIES)
    # Unpackaged application: no build backend and no workspace membership.
    assert "build-system" not in pyproject
    assert "workspace" not in pyproject_path.read_text(encoding="utf-8")

    lockfile = (generated_project.destination / "uv.lock").read_text(encoding="utf-8")
    assert 'name = "script-project"' in lockfile
    for requirement in DEV_DEPENDENCIES:
        name, version = requirement.split("==")
        assert re.search(rf'name = "{name}"\nversion = "{version}"', lockfile), (
            f"uv.lock does not pin {name}=={version}"
        )


def test_overlay_owns_no_application_code_or_manifest(
    generated_project: GeneratedProject,
) -> None:
    """Scenario B: uv and the developer own main.py and pyproject.toml."""
    destination = generated_project.destination

    # Native scaffold shape, including the missing annotation that mypy rejects.
    assert generated_project.scaffold_main.startswith(SCAFFOLD_ENTRY_POINT)
    assert ANNOTATED_ENTRY_POINT not in generated_project.scaffold_main

    # Copier rendered neither file: both are byte-identical to the uv output.
    assert generated_project.overlay_main == generated_project.scaffold_main
    assert generated_project.overlay_pyproject == generated_project.scaffold_pyproject

    # The only change to main.py is the documented project-owned annotation.
    expected_main = generated_project.scaffold_main.replace(
        SCAFFOLD_ENTRY_POINT, ANNOTATED_ENTRY_POINT, 1
    )
    assert (destination / "main.py").read_text(encoding="utf-8") == expected_main

    # And no template file could ever render those paths.
    template_root = REPO_ROOT / "templates"
    for path in template_root.rglob("*"):
        assert path.name not in FORBIDDEN_TEMPLATE_FILES, f"overlay renders {path}"
    assert not (destination / ".python-version").exists()


def test_copier_provenance_is_recorded(generated_project: GeneratedProject) -> None:
    """Scenario B: provenance comes from native Copier answers."""
    answers_path = generated_project.destination / ".copier-answers.yml"
    assert answers_path.is_file()

    answers = {}
    for line in answers_path.read_text(encoding="utf-8").splitlines():
        if not line or line.startswith("#"):
            continue
        key, _, value = line.partition(": ")
        answers[key] = value

    assert answers["_src_path"] == str(generated_project.template_repo)
    assert answers["_commit"] == TEST_TAG
    assert answers["project_name"] == generated_project.destination.name


def test_project_is_independent_of_the_devkit(
    generated_project: GeneratedProject,
) -> None:
    """Scenario C: the project owns its environment and lockfiles."""
    destination = generated_project.destination
    assert not destination.is_relative_to(REPO_ROOT)
    assert not (destination / ".python-version").exists()

    prefix = _run_ok(
        (
            _which("mise"),
            "exec",
            "--",
            "uv",
            "run",
            "--locked",
            "python",
            "-c",
            "import sys; print(sys.prefix)",
        ),
        cwd=destination,
    ).stdout.strip()
    assert Path(prefix) == destination / ".venv", prefix

    assert (destination / "uv.lock").read_bytes() != (
        REPO_ROOT / "uv.lock"
    ).read_bytes()

    # No agent configuration or credential file in the generated project.
    for name in (".env", ".opencode", ".codex", ".claude", "CLAUDE.md"):
        assert not (destination / name).exists(), f"unexpected path: {name}"

    ignore_lines = [
        line.strip()
        for line in (destination / ".gitignore")
        .read_text(encoding="utf-8")
        .splitlines()
        if line.strip() and not line.startswith("#")
    ]
    # Generated output and local state are ignored; project-owned files are not.
    for ignored in (
        ".venv/",
        "site/",
        ".pytest_cache/",
        ".ruff_cache/",
        ".mypy_cache/",
    ):
        assert ignored in ignore_lines, f"{ignored} must be ignored"
    for kept in ("uv.lock", "mise.lock", ".copier-answers.yml", "AGENTS.md", "docs/"):
        assert kept not in ignore_lines, f"{kept} must not be ignored"


def test_devkit_repository_is_untouched(generated_project: GeneratedProject) -> None:
    """Scenario C: verification creates nothing in the devkit working tree."""
    assert _git_status() == generated_project.git_status_before


def test_check_rejects_broken_verification(generated_project: GeneratedProject) -> None:
    """Scenario D: a broken test or quality check makes `mise run check` fail."""
    mise = _which("mise")
    destination = generated_project.destination
    test_path = destination / "tests" / "test_main.py"
    main_path = destination / "main.py"
    original_test = test_path.read_text(encoding="utf-8")
    original_main = main_path.read_text(encoding="utf-8")

    try:
        # A failing test must be detected by the pytest check.
        test_path.write_text(
            original_test
            + "\n\ndef test_deliberate_failure() -> None:\n"
            + '    assert "expected" == "actual"\n',
            encoding="utf-8",
        )
        broken_test = _run((mise, "run", "check"), cwd=destination)
        assert broken_test.returncode != 0, "a failing test must fail mise run check"
        output = broken_test.stdout + broken_test.stderr
        assert "test_deliberate_failure" in output, output

        # A lint violation must be detected by the Ruff check.
        test_path.write_text(original_test, encoding="utf-8")
        main_path.write_text(original_main + "\nimport os\n", encoding="utf-8")
        broken_lint = _run((mise, "run", "check"), cwd=destination)
        assert broken_lint.returncode != 0, "a lint violation must fail mise run check"
        lint_output = broken_lint.stdout + broken_lint.stderr
        assert "ruff" in lint_output.lower(), lint_output
    finally:
        test_path.write_text(original_test, encoding="utf-8")
        main_path.write_text(original_main, encoding="utf-8")

    restored = _run_ok((mise, "run", "check"), cwd=destination)
    assert "ERROR" not in restored.stdout
