"""Native Copier overlay update lifecycle (v0.1 plan, Task 6).

Nothing is mocked. The module builds a temporary Git repository that holds the
overlay as a template source with two tagged revisions — `v0.1.0` and `v0.2.0` —
then creates one project per scenario with the pinned `uv`, Copier, mise and
OpenSpec executables, commits a clean baseline, and drives native `copier update`
between the two revisions:

* **A** an update never takes ownership of `main.py`, a project regression test,
  `pyproject.toml` or `uv.lock`;
* **B** a project-owned documentation page, and the project's own edit to an
  overlay-owned entry point, both survive;
* **C** an independent edit to the same region of an overlay-owned file produces
  a visible, resolvable conflict instead of a silent overwrite;
* **D** `.copier-answers.yml` advances, the source path stays the temporary
  template, and no unrelated file is rewritten.

Every operation stays inside pytest's temporary directories. No ai-devkit release
tag is created, moved or pushed, and an autouse fixture fails this module if the
devkit working tree changes.

Two things are deliberately *not* asserted: the exit status of a conflicting
update, and the exact number of conflict markers Copier writes. Copier 9.19.1
reports inline conflicts through the working tree and the Git index, and exit
statuses are the tool's business; the assertions below describe observable
results.
"""

from __future__ import annotations

import hashlib
import re
import shutil
import subprocess
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path

import pytest

# PyYAML arrives with the pinned Copier dependency, which reads
# `.copier-answers.yml` with it; no new dependency is introduced here.
import yaml

from testkit import (
    DEV_DEPENDENCIES,
    REPO_ROOT,
    UV_INIT_FLAGS,
    executable,
    git_status,
    run,
    run_ok,
)

# The two temporary template revisions the scenarios update between.
BASELINE_TAG = "v0.1.0"
UPDATE_TAG = "v0.2.0"

# The overlay inside the template source; `_subdirectory` in `copier.yml` limits
# rendering to this directory.
TEMPLATE_DIRECTORY = Path("templates") / "python-script-overlay" / "template"

# The controlled `v0.2.0` change. Appending to two overlay-owned files keeps the
# changed region predictable: one file is the conflict fixture, the other proves
# that a non-conflicting overlay change still lands during the same update.
TEMPLATE_AGENTS_SECTION = """
## Review notes

Record why a change was needed in the commit message.
"""
TEMPLATE_OWNERSHIP_SECTION = """
## Update notes

The overlay is applied with `copier update`; review the diff before committing it.
"""

# The project's independent edit to the same region of `AGENTS.md`.
PROJECT_AGENTS_SECTION = """
## Project rule

Every behavior change needs a CHANGELOG entry.
"""

# Scenario A: project-owned application behavior and its regression test. Both
# files are outside the template, so an update has nothing to render for them.
PROJECT_ENTRY_POINT = '''"""Project-owned entry point: greet the name given on the command line."""

from __future__ import annotations

import sys


def greeting(name: str) -> str:
    """Return the greeting for the given name."""
    return f"Hello, {name}!"


def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "project"
    print(greeting(name))


if __name__ == "__main__":
    main()
'''

PROJECT_REGRESSION_TEST = '''"""Regression test for this project's own greeting behavior."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_command_line_name_is_used() -> None:
    result = subprocess.run(
        [sys.executable, "main.py", "world"],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )

    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "Hello, world!"
'''

# Scenario B: a documentation page the project wrote, and the line that links it
# from the overlay-owned entry point that the project edited.
PROJECT_DOC_PAGE = """# Keep a changelog

This page belongs to the project. The overlay never rendered it, and the overlay
never links it, so an overlay update has nothing to say about it.

The project keeps one line per behavior change so a reviewer can see why the code
moved.
"""

PROJECT_INDEX_LINK = """
## Project pages

- [Keep a changelog](how-to/keep-a-changelog.md) — owned by this project.
"""

# Git identity for Copier's own scratch repositories, so the test does not depend
# on a host- or CI-wide `user.name`/`user.email`. Environment variables apply to
# one subprocess tree and write no configuration anywhere.
GIT_SCRATCH_ENV = {
    "GIT_AUTHOR_NAME": "ai-devkit integration test",
    "GIT_AUTHOR_EMAIL": "integration-test@example.invalid",
    "GIT_COMMITTER_NAME": "ai-devkit integration test",
    "GIT_COMMITTER_EMAIL": "integration-test@example.invalid",
}

# Copier 9.19.1 marks an inline conflict with these exact lines.
CONFLICT_START = "<<<<<<< before updating"
CONFLICT_END = ">>>>>>> after updating"

# The paths a `v0.1.0` -> `v0.2.0` update is expected to touch.
EXPECTED_UPDATE_PATHS = frozenset(
    {".copier-answers.yml", "AGENTS.md", "docs/explanation/ownership.md"}
)


@dataclass(frozen=True)
class UpdatableProject:
    """One copied baseline project, committed and ready to receive an update."""

    destination: Path
    template_repo: Path
    answers_before: dict[str, str]


def _git(repo: Path, *args: str) -> str:
    """Run one Git command in a fixture repository and return its stdout."""
    return run_ok((executable("git"), *args), cwd=repo).stdout


def _initialize_repository(repo: Path) -> None:
    """Start a fixture Git repository with a local identity and no mode churn.

    The identity is configured in this repository only, so neither the host nor
    a CI runner needs a global `user.name`/`user.email`. File modes are ignored
    because the acceptance platform's mount marks files executable, which would
    otherwise turn every rendered file into a mode change.
    """
    _git(repo, "init", "--quiet")
    _git(repo, "config", "core.fileMode", "false")
    _git(repo, "config", "user.name", "ai-devkit integration test")
    _git(repo, "config", "user.email", "integration-test@example.invalid")


def _commit(repo: Path, message: str) -> None:
    """Stage everything in a fixture repository and commit it."""
    _git(repo, "add", "--all")
    _git(repo, "commit", "--quiet", "-m", message)


def _append(path: Path, text: str) -> None:
    """Append to a file, keeping whatever the file already said."""
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def _answers(destination: Path) -> dict[str, str]:
    """Read `.copier-answers.yml`, Copier's own provenance record."""
    document = yaml.safe_load(
        (destination / ".copier-answers.yml").read_text(encoding="utf-8")
    )
    assert isinstance(document, dict), document
    return {str(key): str(value) for key, value in document.items()}


def _snapshot(root: Path) -> dict[str, str]:
    """Hash every Git-tracked file, so an update's exact footprint is provable."""
    listed = _git(root, "ls-files", "-z")
    snapshot: dict[str, str] = {}
    for relative in listed.split("\0"):
        if not relative:
            continue
        snapshot[relative] = hashlib.sha256((root / relative).read_bytes()).hexdigest()
    return snapshot


def _update_overlay(project: UpdatableProject) -> subprocess.CompletedProcess[str]:
    """Run native `copier update` to the second revision and capture its output.

    The exit status is returned rather than asserted: Copier 9.19.1 exits zero
    when it leaves inline conflicts behind, so the scenarios assert on the
    conflict evidence instead of on the status.
    """
    return run(
        (
            executable("mise"),
            "exec",
            "--",
            "uv",
            "run",
            "--locked",
            "copier",
            "update",
            "--vcs-ref",
            UPDATE_TAG,
            "--defaults",
            str(project.destination),
        ),
        cwd=REPO_ROOT,
        env=GIT_SCRATCH_ENV,
    )


def _update_state(project: UpdatableProject) -> str:
    """Ask native Copier what it thinks of the project's update state."""
    result = run_ok(
        (
            executable("mise"),
            "exec",
            "--",
            "uv",
            "run",
            "--locked",
            "copier",
            "check-update",
            str(project.destination),
        ),
        cwd=REPO_ROOT,
        env=GIT_SCRATCH_ENV,
    )
    return result.stdout


def _run_checks(project: UpdatableProject) -> None:
    """Run the project's own verification contract."""
    run_ok((executable("mise"), "run", "check"), cwd=project.destination)


def _failure_detail(result: subprocess.CompletedProcess[str]) -> str:
    return (
        f"copier update failed with exit code {result.returncode}\n"
        f"--- stdout ---\n{result.stdout}\n--- stderr ---\n{result.stderr}"
    )


@pytest.fixture(scope="module", autouse=True)
def devkit_working_tree() -> Iterator[str]:
    """Fail this module if a scenario changes a tracked devkit file.

    The reading is taken before the first test creates anything and compared
    after the last one has finished, so the guard does not depend on test order
    and covers files the assertions never name.
    """
    before = git_status()
    yield before
    assert git_status() == before, (
        "the update scenarios changed the devkit working tree"
    )


@pytest.fixture(scope="module")
def template_repo(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """A temporary template repository with two tagged overlay revisions."""
    repo = tmp_path_factory.mktemp("update template source") / "ai-devkit template"
    repo.mkdir()
    shutil.copy2(REPO_ROOT / "copier.yml", repo / "copier.yml")
    shutil.copytree(
        REPO_ROOT / "templates",
        repo / "templates",
        ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
    )
    _initialize_repository(repo)
    _commit(repo, "overlay as v0.1.0")
    _git(repo, "tag", BASELINE_TAG)

    # The controlled change between the two revisions: overlay-owned files only,
    # so the update has something to apply that project code cannot collide with.
    overlay = repo / TEMPLATE_DIRECTORY
    _append(overlay / "AGENTS.md", TEMPLATE_AGENTS_SECTION)
    _append(
        overlay / "docs" / "explanation" / "ownership.md", TEMPLATE_OWNERSHIP_SECTION
    )
    _commit(repo, "overlay as v0.2.0")
    _git(repo, "tag", UPDATE_TAG)

    assert _git(repo, "tag").split() == [BASELINE_TAG, UPDATE_TAG]
    return repo


@pytest.fixture(scope="module")
def baseline_project(
    tmp_path_factory: pytest.TempPathFactory, template_repo: Path
) -> Path:
    """One project created from `v0.1.0`, verified once, copied per scenario.

    Creating and locking the project is the expensive part of this module, so it
    happens once. The scenarios take copies and never share a working tree.
    """
    mise = executable("mise")
    destination = tmp_path_factory.mktemp("update lifecycle") / "script project"

    run_ok(
        (mise, "exec", "--", "uv", "init", *UV_INIT_FLAGS, str(destination)),
        cwd=REPO_ROOT,
    )
    run_ok(
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
            BASELINE_TAG,
            "--defaults",
            str(template_repo),
            str(destination),
        ),
        cwd=REPO_ROOT,
    )

    # The documented project-owned edit: `uv init` writes `def main():`, which
    # `mypy --strict` rejects, and Copier never patches application code.
    main_path = destination / "main.py"
    scaffold = main_path.read_text(encoding="utf-8")
    assert "def main():\n" in scaffold, scaffold
    main_path.write_text(
        scaffold.replace("def main():\n", "def main() -> None:\n", 1), encoding="utf-8"
    )

    run_ok(
        (mise, "exec", "--", "uv", "add", "--dev", *DEV_DEPENDENCIES), cwd=destination
    )
    run_ok((mise, "exec", "--", "uv", "lock"), cwd=destination)
    run_ok(
        (
            mise,
            "exec",
            "--",
            "openspec",
            "init",
            "--tools",
            "opencode,codex",
            "--profile",
            "core",
        ),
        cwd=destination,
    )
    run_ok((mise, "run", "check"), cwd=destination)
    return destination


@pytest.fixture
def updatable_project(
    tmp_path: Path, baseline_project: Path, template_repo: Path
) -> UpdatableProject:
    """A pristine copy of the baseline with a committed, clean Git baseline."""
    destination = tmp_path / "updatable project"
    ignored = (
        ".venv",
        "site",
        "__pycache__",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
    )
    shutil.copytree(
        baseline_project,
        destination,
        ignore=shutil.ignore_patterns(*ignored),
    )
    _initialize_repository(destination)
    _commit(destination, "project baseline")
    assert _git(destination, "status", "--porcelain") == ""

    # The copy has no virtual environment; rebuild it from the copy's own
    # `uv.lock` with the interpreter mise selects for that directory.
    run_ok(
        (executable("mise"), "exec", "--", "uv", "sync", "--locked"), cwd=destination
    )

    return UpdatableProject(
        destination=destination,
        template_repo=template_repo,
        answers_before=_answers(destination),
    )


def test_project_owned_application_survives_update(
    updatable_project: UpdatableProject,
) -> None:
    """Scenario A: an update never takes ownership of code or manifests."""
    destination = updatable_project.destination

    # 1-4. Project-specific behavior, its regression test, committed.
    (destination / "main.py").write_text(PROJECT_ENTRY_POINT, encoding="utf-8")
    (destination / "tests" / "test_regression.py").write_text(
        PROJECT_REGRESSION_TEST, encoding="utf-8"
    )
    _commit(destination, "project: own the entry point and its regression test")

    owned = ("main.py", "tests/test_regression.py", "pyproject.toml", "uv.lock")
    before = {relative: (destination / relative).read_bytes() for relative in owned}

    # 5. Native update to the second overlay revision.
    result = _update_overlay(updatable_project)
    assert result.returncode == 0, _failure_detail(result)

    # The overlay change did land, so the assertions below are not vacuous.
    assert TEMPLATE_AGENTS_SECTION in (destination / "AGENTS.md").read_text(
        encoding="utf-8"
    )
    assert TEMPLATE_OWNERSHIP_SECTION in (
        destination / "docs" / "explanation" / "ownership.md"
    ).read_text(encoding="utf-8")

    # 6-7. Application code, its test and both Python dependency manifests are
    # byte-identical: the template never rendered them.
    for relative, expected in before.items():
        assert (destination / relative).read_bytes() == expected, relative

    # 8. The project still passes its own checks with the updated overlay.
    _run_checks(updatable_project)


def test_project_owned_documentation_survives_update(
    updatable_project: UpdatableProject,
) -> None:
    """Scenario B: project documentation survives, and so does a local edit.

    The new page is project-owned: the overlay never rendered it. The entry point
    is overlay-owned but edited by the project, and the second revision does not
    change it, so both come through the update unchanged.
    """
    destination = updatable_project.destination
    page = destination / "docs" / "how-to" / "keep-a-changelog.md"
    entry_point = destination / "docs" / "index.md"

    page.write_text(PROJECT_DOC_PAGE, encoding="utf-8")
    _append(entry_point, PROJECT_INDEX_LINK)
    _commit(destination, "docs: add the project changelog page")

    page_before = page.read_bytes()
    entry_point_before = entry_point.read_bytes()

    result = _update_overlay(updatable_project)
    assert result.returncode == 0, _failure_detail(result)

    # The page and its content survived, including the entry point's link to it.
    assert page.read_bytes() == page_before
    assert entry_point.read_bytes() == entry_point_before
    assert "how-to/keep-a-changelog.md" in entry_point.read_text(encoding="utf-8")

    # The overlay change landed, and the documentation build still succeeds.
    assert TEMPLATE_AGENTS_SECTION in (destination / "AGENTS.md").read_text(
        encoding="utf-8"
    )
    run_ok((executable("mise"), "run", "docs"), cwd=destination)
    _run_checks(updatable_project)


def test_shared_rule_conflict_is_visible_and_resolvable(
    updatable_project: UpdatableProject,
) -> None:
    """Scenario C: the same region edited on both sides stays visible.

    Copier's own three-way merge cannot choose a side here, so it must say so:
    inline markers in the file and unmerged index stages in Git. Silently
    discarding either side, or forcing the template version through, would make
    this test fail.
    """
    destination = updatable_project.destination
    agents = destination / "AGENTS.md"
    agents.write_text(
        agents.read_text(encoding="utf-8") + PROJECT_AGENTS_SECTION, encoding="utf-8"
    )
    _commit(destination, "project: add a local engineering rule")

    result = _update_overlay(updatable_project)

    conflicted = agents.read_text(encoding="utf-8")
    assert CONFLICT_START in conflicted, (
        f"Copier did not report the conflict\n{_failure_detail(result)}\n"
        f"--- AGENTS.md ---\n{conflicted}"
    )
    assert CONFLICT_END in conflicted, conflicted

    # Neither side's change was discarded.
    assert "Every behavior change needs a CHANGELOG entry." in conflicted
    assert "Record why a change was needed in the commit message." in conflicted

    # The conflict is exposed through Git's native mechanism too, which is what
    # makes it a reviewable state rather than a plain file edit.
    unmerged = _git(destination, "ls-files", "--unmerged")
    assert "AGENTS.md" in unmerged, unmerged
    assert "UU AGENTS.md" in _git(destination, "status", "--porcelain")

    # The rest of the update still applied, and provenance advanced, so the
    # conflict did not abort the run halfway.
    assert TEMPLATE_OWNERSHIP_SECTION in (
        destination / "docs" / "explanation" / "ownership.md"
    ).read_text(encoding="utf-8")
    assert _answers(destination)["_commit"] == UPDATE_TAG

    # Copier removes its own `.rej` witnesses after the inline merge.
    assert not list(destination.rglob("*.rej"))

    # Resolve by hand: keep both intents and drop the markers.
    resolved = re.sub(
        rf"{re.escape(CONFLICT_START)}\n(?P<ours>.*?)=======\n"
        rf"(?P<theirs>.*?){re.escape(CONFLICT_END)}\n",
        lambda match: match.group("ours") + match.group("theirs"),
        conflicted,
        flags=re.DOTALL,
    )
    assert CONFLICT_START not in resolved
    # Both intents are in the resolution, not just the surviving half.
    assert "Every behavior change needs a CHANGELOG entry." in resolved
    assert "Record why a change was needed in the commit message." in resolved
    agents.write_text(resolved, encoding="utf-8")
    _git(destination, "add", "AGENTS.md")
    assert _git(destination, "ls-files", "--unmerged") == ""

    # The resolved project passes its checks and commits as one reviewable change.
    _run_checks(updatable_project)
    _commit(destination, "chore: apply the v0.2.0 overlay update")
    assert _git(destination, "status", "--porcelain") == ""


def test_provenance_advances_without_rewriting_other_files(
    updatable_project: UpdatableProject,
) -> None:
    """Scenario D: `.copier-answers.yml` advances and nothing else moves."""
    destination = updatable_project.destination

    assert updatable_project.answers_before["_commit"] == BASELINE_TAG
    assert updatable_project.answers_before["_src_path"] == str(
        updatable_project.template_repo
    )

    before = _snapshot(destination)
    result = _update_overlay(updatable_project)
    assert result.returncode == 0, _failure_detail(result)
    after = _snapshot(destination)

    # No file was added or removed, and exactly the expected files changed.
    assert set(after) == set(before)
    changed = {path for path, digest in after.items() if before[path] != digest}
    assert changed == set(EXPECTED_UPDATE_PATHS), changed

    # Git sees the same set: the update rewrote nothing else.
    assert {
        line[3:] for line in _git(destination, "status", "--porcelain").splitlines()
    } == set(EXPECTED_UPDATE_PATHS)

    # The provenance record names the revision and the source that produced it,
    # and the answers the project gave are unchanged.
    answers = _answers(destination)
    assert answers["_commit"] == UPDATE_TAG
    assert answers["_src_path"] == str(updatable_project.template_repo)
    assert answers["project_name"] == updatable_project.answers_before["project_name"]
    assert (
        answers["project_description"]
        == updatable_project.answers_before["project_description"]
    )

    # Native Copier agrees that the project is at that revision.
    assert "Project is up-to-date!" in _update_state(updatable_project)


def test_update_lifecycle_leaves_the_devkit_untouched(
    updatable_project: UpdatableProject,
) -> None:
    """Scenario D: every scenario works outside the devkit checkout.

    The module's autouse `devkit_working_tree` fixture fails the run if a
    scenario changes the devkit's own working tree; this asserts the weaker,
    explicit property that the projects live outside it.
    """
    assert not updatable_project.destination.is_relative_to(REPO_ROOT)
