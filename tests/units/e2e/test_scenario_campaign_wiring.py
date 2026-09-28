"""Contracts so the live scenario campaign actually drives 0.9 Generate.

Two failure modes showed up in the 0.9 campaign:

1. ``make scenario-campaign`` sourced ``.venv/bin/activate`` while
   ``VIRTUAL_ENV`` still pointed at another worktree, so pytest ran that
   worktree's interpreter (and its scenario files) against this app.
2. Scenario 1 still treated Generate as a one-shot OWL apply. The top
   button now starts Stage 1 detection; classes only land after Review →
   Complete. Polling ``/ontology/load`` right after the click times out
   with an empty class list even when detection succeeded.
"""

from pathlib import Path

import pytest

pytestmark = pytest.mark.unit

REPO_ROOT = Path(__file__).resolve().parents[3]
MAKEFILE = REPO_ROOT / "Makefile"
SCENARIO_01 = (
    REPO_ROOT / "tests/e2e/scenarios/test_scenario_01_generate_live.py"
)


def _read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _campaign_recipe() -> str:
    text = _read(MAKEFILE)
    start = text.index("scenario-campaign:")
    rest = text[start:]
    nxt = rest.find("\nformat:")
    return rest if nxt < 0 else rest[:nxt]


class TestCampaignUsesThisWorktreeInterpreter:
    def test_the_recipe_runs_pytest_through_uv_frozen(self):
        recipe = _campaign_recipe()
        assert "uv run --frozen pytest" in recipe

    def test_the_recipe_does_not_source_activate(self):
        """``source .venv/bin/activate`` keeps a foreign VIRTUAL_ENV python."""
        recipe = _campaign_recipe()
        assert "activate" not in recipe

    def test_the_recipe_clears_a_foreign_virtual_env(self):
        recipe = _campaign_recipe()
        assert "env -u VIRTUAL_ENV" in recipe


class TestScenario1DrivesTheStagedWizard:
    def test_it_detects_then_posts_complete(self):
        src = _read(SCENARIO_01)
        assert "wizardTopGenerateBtn" in src
        assert "/ontology/wizard/generate/draft" in src
        assert "/ontology/wizard/generate/complete" in src
        assert "gen_btn.click()" in src
        detect = src.index("gen_btn.click()")
        complete = src.index("/ontology/wizard/generate/complete", detect)
        load = src.index("/ontology/load", complete)
        assert detect < complete < load

    def test_it_polls_the_completion_task_not_the_review_button(self):
        src = _read(SCENARIO_01)
        assert "_poll_task(" in src
        assert "wizardReviewContinueBtn" not in src
