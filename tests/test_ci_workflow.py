"""Static checks on the GitHub Actions workflow (v0.1 plan, Task 6).

Hosted runners are not started from here: only GitHub can execute the workflow,
and its result is reported separately from a local test run. What these tests do
is reject a workflow that would grant write access, run an unpinned action,
execute untrusted pull-request code with privileges, read a secret, or leave out
a documented verification command.

PyYAML is already installed through the pinned Copier and Zensical dependencies
(Copier reads `.copier-answers.yml` with it), so parsing the workflow introduces
no dependency. The `on:` key is YAML 1.1's `True`, which the helper below handles.
"""

from __future__ import annotations

import re
from typing import Any

import pytest
import yaml

from testkit import REPO_ROOT

WORKFLOW_PATH = REPO_ROOT / ".github" / "workflows" / "verify.yml"

# The actions the workflow may use, each pinned to the full commit SHA of the
# release tag recorded here.
PINNED_ACTIONS = {
    "actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1": "v7.0.1",
    "jdx/mise-action@f5be966e4a917d54244728e6a5fdcd1d93a35e6c": "v5.2.6",
}

# The verification commands the workflow must run, in the documented order.
REQUIRED_COMMANDS = (
    "mise install --locked",
    "mise exec -- uv sync --locked",
    "mise run versions",
    "mise run check",
    "mise run test-template",
)

# Owners whose actions are reviewed. Anything else is an unreviewed dependency.
ALLOWED_ACTION_OWNERS = {"actions", "jdx"}

FULL_SHA = re.compile(r"^[0-9a-f]{40}$")


@pytest.fixture(scope="module")
def workflow_text() -> str:
    return WORKFLOW_PATH.read_text(encoding="utf-8")


@pytest.fixture(scope="module")
def workflow(workflow_text: str) -> dict[str, Any]:
    document = yaml.safe_load(workflow_text)
    assert isinstance(document, dict), document
    return document


@pytest.fixture(scope="module")
def job(workflow: dict[str, Any]) -> dict[str, Any]:
    jobs = workflow["jobs"]
    assert len(jobs) == 1, f"one job is enough for this repository: {list(jobs)}"
    (only_job,) = jobs.values()
    return only_job


@pytest.fixture(scope="module")
def steps(job: dict[str, Any]) -> list[dict[str, Any]]:
    return job["steps"]


def _triggers(workflow: dict[str, Any]) -> dict[str, Any]:
    """Return the `on` block; YAML 1.1 parsers read that key as `True`."""
    for key in ("on", True):
        if key in workflow:
            value = workflow[key]
            assert isinstance(value, dict), value
            return value
    pytest.fail("the workflow declares no triggers")


def _commands(steps: list[dict[str, Any]]) -> str:
    """Join every `run:` script in the order the job executes them."""
    return "\n".join(step.get("run", "") for step in steps)


def test_workflow_triggers_on_main(workflow: dict[str, Any]) -> None:
    """Requirement: pushes to `main` and pull requests targeting `main`."""
    triggers = _triggers(workflow)

    assert set(triggers) == {"push", "pull_request"}, triggers
    assert triggers["push"]["branches"] == ["main"]
    assert triggers["pull_request"]["branches"] == ["main"]


def test_workflow_is_read_only(workflow: dict[str, Any], job: dict[str, Any]) -> None:
    """Requirement: no write permission anywhere, and none requested per job."""
    assert workflow["permissions"] == {"contents": "read"}
    # A job-level block would override the workflow default, so none may exist.
    assert "permissions" not in job, job.get("permissions")


def test_workflow_pins_every_action_to_a_full_sha(
    steps: list[dict[str, Any]],
) -> None:
    """Requirement: third-party actions are pinned to verified commit SHAs."""
    used = [step["uses"] for step in steps if "uses" in step]

    assert len(used) == len(set(used)), f"an action is used twice: {used}"
    assert set(used) == set(PINNED_ACTIONS), (
        "unexpected action reference; the reviewed pins are "
        f"{PINNED_ACTIONS}, the workflow uses {used}"
    )

    for reference in used:
        owner, _, pinned = reference.partition("/")
        _, _, revision = pinned.partition("@")
        assert owner in ALLOWED_ACTION_OWNERS, reference
        assert FULL_SHA.match(revision), (
            f"{reference} is not pinned to a full commit SHA; a tag or a short SHA "
            "can move"
        )


def test_workflow_runs_the_documented_verification_commands(
    steps: list[dict[str, Any]],
) -> None:
    """Requirement: the same command sequence a developer runs locally."""
    commands = _commands(steps)

    positions = [commands.find(command) for command in REQUIRED_COMMANDS]
    assert all(position >= 0 for position in positions), (
        f"missing command; executed:\n{commands}"
    )
    assert positions == sorted(positions), (
        f"the verification commands run out of order:\n{commands}"
    )


def test_workflow_runs_the_repository_tasks_not_a_copy_of_them(
    steps: list[dict[str, Any]],
) -> None:
    """Requirement: delegate to the mise tasks instead of duplicating test logic."""
    commands = _commands(steps)

    assert "mise run check" in commands
    assert "mise run test-template" in commands
    # The workflow must not call a checker directly: the task owns the command.
    for checker in ("pytest", "ruff", "mypy", "zensical", "openspec"):
        assert checker not in commands, f"the workflow runs {checker} itself"


def test_workflow_uses_an_explicit_runner_and_a_bounded_timeout(
    job: dict[str, Any],
) -> None:
    """Requirement: an explicit Ubuntu 24.04 runner and a reasonable timeout."""
    assert job["runs-on"] == "ubuntu-24.04"

    timeout = job.get("timeout-minutes")
    assert isinstance(timeout, int) and 0 < timeout <= 60, timeout


def test_workflow_exposes_no_credentials_and_runs_no_untrusted_code_with_access(
    workflow_text: str,
) -> None:
    """Requirement: no secrets, no model access, no privileged pull-request run."""
    forbidden = (
        "pull_request_target",
        "secrets.",
        "OPENAI_API_KEY",
        "DEEPSEEK",
        "ANTHROPIC_API_KEY",
        "write-all",
        "contents: write",
        "packages: write",
        "id-token: write",
    )
    for needle in forbidden:
        assert needle not in workflow_text, f"the workflow mentions {needle}"


def test_workflow_does_not_publish_or_tag(steps: list[dict[str, Any]]) -> None:
    """Requirement: verification only; no commit, push, tag or release step."""
    commands = _commands(steps)

    for forbidden in ("git commit", "git push", "git tag", "gh release", "docker"):
        assert forbidden not in commands, f"the workflow runs {forbidden}"


def test_workflow_confirms_verification_changed_no_tracked_file(
    steps: list[dict[str, Any]],
) -> None:
    """Requirement: a successful run leaves the tracked tree unchanged."""
    commands = _commands(steps)

    assert 'test -z "$(git status --porcelain)"' in commands, commands
    # The check must come after both verification tasks, or it certifies a state
    # that later steps can still change.
    assert commands.index("test -z") > commands.index("mise run test-template")
